# Generated by Django 4.2.2 on 2023-12-14 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0015_remove_task_change_task_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='completed_status_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='completed_status_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_status_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]