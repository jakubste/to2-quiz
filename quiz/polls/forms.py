from django.forms import Form, CheckboxSelectMultiple
from django.forms.fields import MultipleChoiceField
from django.shortcuts import get_object_or_404

from quiz.polls.models import Quiz


class QuizForm(Form):
    def __init__(self, *args, **kwargs):
        quiz_id = kwargs.pop('quiz', None)
        self.quiz = get_object_or_404(Quiz, pk=quiz_id)
        super(QuizForm, self).__init__(*args, **kwargs)

        for question in self.quiz.questions.all():
            self.fields['question' + str(question.pk)] = MultipleChoiceField(
                choices=[(choice.pk, choice.text) for choice in question.choices.all()],
                required=True,
                label=question.text,
                help_text=u'Zaznacz wszystkie poprawne odpowiedzi',
                widget=CheckboxSelectMultiple(),
            )
