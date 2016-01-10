from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_variables
from django.views.generic import FormView, View, TemplateView

from quiz.accounts.forms import LoginForm, RegistrationForm


class Home(TemplateView):
    template_name = 'home.html'


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
    success_url = 'polls:quiz_list'

    @sensitive_variables('password')
    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


class MarkAsEgzaminer(View):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, *arg, **kwargs):
        user_pk = kwargs.pop('pk')
        user = User.objects.get(pk=user_pk)
        egzam_group = Group.objects.get_or_create(name='Egzaminatorzy')[0]
        if user.groups.filter(pk=egzam_group.pk):
            user.groups.remove(egzam_group)
            if not user.is_superuser:
                user.is_staff = False
            user.save()
        else:
            user.groups.add(egzam_group)
            user.is_staff = True
            user.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
