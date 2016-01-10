from django.conf.urls import url

from quiz.polls.views import QuizListView, QuizFormView, SolutionListView, SolutionDetailView

urlpatterns = [
    url(r'^$', QuizListView.as_view(), name='quiz_list'),
    url(r'^rozwiazuj/(?P<pk>[0-9]+)/$', QuizFormView.as_view(), name='quiz'),
    url(r'^wyniki/$', SolutionListView.as_view(), name='solution_list'),
    url(r'^wyniki/(?P<pk>[0-9]+)$', SolutionDetailView.as_view(), name='solution_detail'),

]
