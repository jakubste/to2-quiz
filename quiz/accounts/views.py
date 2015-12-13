from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from quiz.accounts.forms import LoginForm


class LoginView(FormView, LoginRequiredMixin):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'polls:quiz_list'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


def logout_view(request):
    logout(request)
    return redirect('polls:quiz_list')
