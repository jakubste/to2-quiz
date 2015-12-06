from django.views.generic import ListView, FormView
from quiz.polls.forms import QuizForm

from quiz.polls.models import Quiz

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


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

#tak wiem ze slabo zrobione i w zlym miejscu
@login_required
def logged_in(request):
    return render_to_response('logged_in.html',
        context_instance=RequestContext(request)
    )