# coding=utf-8
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView
from django.views.generic.detail import DetailView

from quiz.polls.forms import QuizForm
from quiz.polls.models import Quiz, Solution, Question


class QuizListView(ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz_list.html'


class SolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'solutions_list.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SolutionListView, self).dispatch(request, *args, **kwargs)


class SolutionDetailView(LoginRequiredMixin, DetailView):
    model = Solution
    context_object_name = 'solution'
    template_name = 'solution_detail.html'


def serialize_answers(quiz, form):
    answers = {}
    correct, incorrect = 0, 0
    for question in quiz.questions.all():
        answered = form['question' + str(question.pk)].value()

        answers[question.pk] = {}
        answers[question.pk]['question'] = Question.objects.get(pk=question.pk).text
        answers[question.pk]['choices'] = {}

        for answer in question.choices.all():
            answers[question.pk]['choices'][answer.pk] = {}
            answers[question.pk]['choices'][answer.pk]['answer'] = answer.text
            answers[question.pk]['choices'][answer.pk]['is_correct'] = answer.correct
            answers[question.pk]['choices'][answer.pk]['selected'] = False
            if unicode(answer.pk) in answered:
                answers[question.pk]['choices'][answer.pk]['selected'] = True

        correct_answers = question.choices.filter(correct=True)
        correct_answers = [unicode(ans.pk) for ans in correct_answers]
        if answered == correct_answers:
            correct += 1
        else:
            incorrect += 1
    question_number = correct + incorrect
    percent = (correct / float(question_number)) * 100

    return answers, percent


class QuizFormView(LoginRequiredMixin, FormView):
    form_class = QuizForm
    template_name = 'quiz.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizFormView, self).get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = self.kwargs.get('pk', None)
        return kwargs

    def form_valid(self, form):
        quiz_pk = self.kwargs.get('pk', None)
        quiz = Quiz.objects.get(pk=quiz_pk)

        answers, percent = serialize_answers(quiz, form)

        messages.info(self.request, u'Twój wynik to: {}%'.format(int(percent)))
        Solution.objects.create(quiz=quiz, user=self.request.user, result=percent, answers=answers)
        return redirect(reverse('polls:quiz_list'))
