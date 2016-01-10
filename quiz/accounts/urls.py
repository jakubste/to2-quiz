from django.conf.urls import url

from quiz.accounts.views import LoginView, logout_view, RegisterView, MarkAsEgzaminer, Home

urlpatterns = [

    url(r'^$', Home.as_view(), name='login'),
    url(r'^zaloguj/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^zarejestruj/$', RegisterView.as_view(), name='register'),
    url(r'^mianuj-egzaminatorem/(?P<pk>[0-9]+)/$', MarkAsEgzaminer.as_view(), name='mark_as_egzaminer'),
]
