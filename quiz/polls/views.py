from django.views.generic import ListView, FormView
from quiz.polls.forms import QuizForm

from quiz.polls.models import Quiz


class QuizListView(ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz_list.html'


class QuizFormView(FormView):
    form_class = QuizForm
    template_name = 'quiz.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(QuizFormView, self).get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = self.kwargs.get('pk', None)
        return kwargs
