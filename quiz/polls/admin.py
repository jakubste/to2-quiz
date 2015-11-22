from django.contrib.admin import site
from django.contrib.admin.options import StackedInline, TabularInline
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from quiz.polls.models import Choice, Question, Quiz


class ChoiceInline(SuperInlineModelAdmin, TabularInline):
    model = Choice
    extra = 3


class QuestionInline(SuperInlineModelAdmin, StackedInline):
    model = Question
    extra = 3
    inlines = [ChoiceInline]


class QuizAdmin(SuperModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]


site.register(Quiz, QuizAdmin)

site.register(Question)
