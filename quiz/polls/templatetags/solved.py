from django import template

from quiz.polls.models import Solution

register = template.Library()


@register.assignment_tag(takes_context=True)
def solved(context, quiz):
    if context['user'].is_authenticated() and Solution.objects.filter(quiz=quiz, user=context['user']).exists():
        return Solution.objects.filter(quiz=quiz, user=context['user'])[0].result
    else:
        return False
