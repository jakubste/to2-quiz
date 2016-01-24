from datetime import datetime
from datetime import timedelta
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import smart_text
from quiz.polls.factories import QuizFactory, SolutionFactory
from quiz.utils.unittestcase import TestCase


class QuizListViewTest(TestCase):
    url = reverse_lazy('polls:quiz_list')

    def test_quiz_list_show_quizes(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['quizes']), 0)
        QuizFactory(pub_date=datetime.now()+timedelta(days=1))
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['quizes']), 0)
        quiz = QuizFactory()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['quizes']), 1)
        self.assertIn(quiz.name, smart_text(response))


class SolutionListViewTest(TestCase):
    url = reverse_lazy('polls:solution_list')

    def test_solution_list_show_own_solutions(self):
        self.user = self.login()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 0)
        SolutionFactory()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 0)
        solution = SolutionFactory(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 1)
        self.assertIn(str(solution.result), smart_text(response))

    def test_solution_list_show_all_if_is_staff(self):
        self.user = self.login(is_staff=True)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 0)
        solution1 = SolutionFactory()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 1)
        solution2 = SolutionFactory(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['solutions']), 2)
        self.assertIn(str(solution1.result), smart_text(response))
        self.assertIn(str(solution2.result), smart_text(response))

