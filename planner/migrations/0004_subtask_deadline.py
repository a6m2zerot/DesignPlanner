# Generated by Django 4.2.2 on 2023-08-29 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_rename_subtasks_subtask_tasks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
