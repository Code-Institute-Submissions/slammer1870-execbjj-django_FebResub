# Generated by Django 4.0.1 on 2022-01-17 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkins', '0003_alter_lesson_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['time']},
        ),
    ]
