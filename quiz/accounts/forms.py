# coding=utf-8
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label=u'Nazwa użytkownika')
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, label=u'Hasło')
