# Generated by Django 4.0.1 on 2022-01-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_techniqueoftheweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniqueoftheweek',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
