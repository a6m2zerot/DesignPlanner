from django.forms import ModelForm
from .models import Task, Subtask, Meetings, Project
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'deadline']
        labels = {
            'task': 'Введите новое название задачи',
            'deadline': 'Выберите новый дедлайн',
        }
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        initial = {
            'deadline': 'deadline', 
        }


class SubtaskForm(ModelForm):
    class Meta:
        model = Subtask
        fields = ['subtask']
        labels = {
            'subtask': 'Введите новое название подзадачи',
        }


class MeetingsForm(ModelForm):
    class Meta:
        model = Meetings
        fields = ['meeting_name', 'meeting_time_start', 'meeting_time_finish', 'meeting_notes' ]
        labels = {
            'meeting_name': 'Введите новое название встречи',
            'meeting_time_start': 'Выберите новое время начала',
            'meeting_time_finish': 'Выберите новое время окончания',
            'meeting_notes': 'Заметки'
        }
        widgets = {
            'meeting_time_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'meeting_time_finish': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        initial = {
            'meeting_time_start': 'meeting_time_start',
            'meeting_time_finish': 'meeting_time_finish'
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']