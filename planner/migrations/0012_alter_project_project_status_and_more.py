# Generated by Django 4.2.2 on 2023-11-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0011_alter_project_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('active', 'active'), ('completed', 'completed')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='subtask_status',
            field=models.CharField(choices=[('active', 'active'), ('completed', 'completed')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('active', 'active'), ('completed', 'completed')], default='active', max_length=10),
        ),
    ]
