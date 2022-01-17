# Generated by Django 4.0.1 on 2022-01-17 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(unique=True)),
                ('class_type', models.CharField(choices=[('Gi Class (Beginners)', 'GI'), ('NoGi Class (Beginners)', 'NOGI'), ('Gi Class (Mixed Levels)', 'GIMIX'), ('NoGi Class (Mixed Levels)', 'NOGIMIX'), ('Open Mat', 'OPEN'), ('Sparring Class', 'SPARRING'), ('Wrestling', 'WRESTLING')], max_length=50)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkins.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_in', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checkins.lesson')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'lesson')},
            },
        ),
    ]