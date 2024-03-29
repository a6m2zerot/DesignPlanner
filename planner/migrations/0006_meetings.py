# Generated by Django 4.2.2 on 2023-09-30 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_alter_multipleimages_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_name', models.CharField(max_length=30)),
                ('meeting_time_start', models.DateTimeField(blank=True, null=True)),
                ('meeting_time_finish', models.DateTimeField(blank=True, null=True)),
                ('meeting_notes', models.CharField(blank=True, max_length=300, null=True)),
                ('meeting_status', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.project')),
            ],
        ),
    ]
