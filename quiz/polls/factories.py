from django.contrib.auth.models import User

import factory
from factory import fuzzy
from quiz.accounts.factories import UserFactory
from quiz.polls.models import Quiz, Choice, Solution
from quiz.polls.models import Question


class QuizFactory(factory.DjangoModelFactory):
    class Meta:
        model = Quiz

    name = fuzzy.FuzzyText(prefix='quiz-')


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    quiz = factory.SubFactory(QuizFactory)
    text = fuzzy.FuzzyText(prefix='question-')


class ChoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    text = fuzzy.FuzzyText(prefix='choice-')
    correct = fuzzy.FuzzyChoice(choices=(True, False))


class SolutionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Solution

    quiz = factory.SubFactory(QuizFactory)
    user = factory.SubFactory(UserFactory)
    result = fuzzy.FuzzyFloat(0, 100)
