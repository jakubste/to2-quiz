from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.debug import sensitive_variables
from django.views.generic import FormView

from quiz.accounts.forms import LoginForm, RegistrationForm


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


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = 'quiz:quiz_list'

    @sensitive_variables('password')
    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)
