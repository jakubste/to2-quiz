# coding=utf-8
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView

from quiz.polls.forms import QuizForm
from quiz.polls.models import Quiz, Solution


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
        correct = 0
        incorrect = 0
        for question in quiz.questions.all():
            answered = form['question' + str(question.pk)].value()
            correct_answers = question.choices.filter(correct=True)
            correct_answers = [unicode(ans.pk) for ans in correct_answers]
            if answered == correct_answers:
                correct += 1
            else:
                incorrect += 1
        question_number = correct + incorrect
        percent = (correct / float(question_number)) * 100
        messages.info(self.request, u'Twój wynik to: {}%'.format(int(percent)))
        Solution.objects.create(quiz=quiz, user=self.request.user, result=percent)
        return redirect(reverse('polls:quiz_list'))
