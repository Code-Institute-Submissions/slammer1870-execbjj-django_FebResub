# Generated by Django 4.0.1 on 2022-01-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkins', '0002_alter_lesson_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='class_type',
            field=models.CharField(choices=[('Gi Class', 'GI'), ('NoGi Class', 'NOGI'), ('Open Mat', 'OPEN')], max_length=12),
        ),
    ]
