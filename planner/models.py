from django.db import models
from django.contrib.auth.models import User
# Ниже импорт пакета для изменения размера картинки, также нужно:
#  1. pip install django-imagekit  в терминале
#  2. добавить 'imagekit' в INSTALLED APPS в settings.py
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone


#Восстановление пароля
class PasswordToRecover(models.Model):
    password_to_send = models.CharField(max_length=6, blank=True, null=True) # Сюда прилетает результат функции password_generator(), который в user.views.py (временный пароль для восст-ия пользовательского)
    time_of_gen_password = models.DateTimeField(blank=True, null=True) # Время, в которое сгенерировался временный пароль
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')


class Project(models.Model):
    status = [
        ('active', 'active'),
        ('completed', 'completed'),
    ]
    project_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    logo = ProcessedImageField(upload_to='logo/', default="", blank=True, null=True,
                                           processors=[ResizeToFill(200, 200)],
                                           format='JPEG',
                                           options={'quality': 100})

    project_status = models.CharField(max_length=10, default='active', choices=status)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

    def __str__(self): return self.project_name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class MultipleImages(models.Model):
    images = models.ImageField(upload_to='images/', blank=True)
    img = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    status = [
        ('active', 'active'),
        ('completed', 'completed'),
    ]
    task = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    deadline =models.DateTimeField(auto_now=False,blank=True, null=True)
    task_status = models.CharField(max_length=10, default='active', choices=status)
    completed_status_date = models.DateTimeField(blank=True, null=True)


class Subtask(models.Model):
    status = [
        ('active', 'active'),
        ('completed', 'completed'),
    ]
    subtask = models.CharField(max_length=30)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask_status = models.CharField(max_length=10, default='active', choices=status)
    completed_status_date = models.DateTimeField(blank=True, null=True)


class Meetings(models.Model):
    status = [
        ('active', 'active'),
        ('completed', 'completed'),
    ]
    meeting_name = models.CharField(max_length=30)
    meeting_time_start = models.DateTimeField(auto_now=False,blank=True, null=True)
    meeting_time_finish = models.DateTimeField(auto_now=False,blank=True, null=True)
    meeting_notes = models.CharField(max_length=300, blank=True, null=True)
    meeting_status = models.CharField(max_length=10, default='active', choices=status)
    completed_status_date = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)





