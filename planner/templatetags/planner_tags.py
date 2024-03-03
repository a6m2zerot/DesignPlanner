from django import template
from planner.models import Subtask

register = template.Library()

@register.simple_tag() # Регистрация своего собственного шаблона в Library и его использование в go_to_project.html
def tags(filter):
    return Subtask.objects.filter(tasks_id=filter, subtask_status='active')