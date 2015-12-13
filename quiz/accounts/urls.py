from django.conf.urls import url

from quiz.accounts.views import LoginView, logout_view, RegisterView

urlpatterns = [
    # using default django auth views with custom templates
    url(r'^zaloguj/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^zarejestruj/$', RegisterView.as_view(), name='register'),
]
