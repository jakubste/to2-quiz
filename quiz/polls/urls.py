from django.conf.urls import url

from quiz.polls.views import QuizListView, QuizFormView

urlpatterns = [
    url(r'^lista/$', QuizListView.as_view(), name='quiz_list'),
    url(r'^rozwiazuj/(?P<pk>[0-9]+)/$', QuizFormView.as_view(), name='quiz'),
]
