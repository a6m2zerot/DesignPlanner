# Generated by Django 4.2.2 on 2023-06-27 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('logo', imagekit.models.fields.ProcessedImageField(blank=True, default='', null=True, upload_to='logo/')),
                ('status', models.CharField(default='Активно', max_length=10)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='MultipleImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='images/')),
                ('img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.project')),
            ],
        ),
    ]
