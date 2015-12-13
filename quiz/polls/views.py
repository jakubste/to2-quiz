from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.views.generic import ListView, FormView

from quiz.polls.forms import QuizForm
from quiz.polls.models import Quiz


class QuizListView(ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz_list.html'


class QuizFormView(LoginRequiredMixin, FormView):
    form_class = QuizForm
    template_name = 'quiz.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizFormView, self).get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = self.kwargs.get('pk', None)
        return kwargs

    # TODO: form says choices are invalid - need to fix it
    def form_valid(self, form):
        print form.fields['question1'].choices
        return redirect(reverse('polls:quiz_list'))

    def form_invalid(self, form):
        print form.fields['question1'].choices
        print form
        return redirect(reverse('polls:quiz_list'))
