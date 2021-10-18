from django.db import models
from django.conf import settings

# Create your models here.
class Attendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)

CLASS_CHOICES = (("GI", "Gi Class"), ("NOGI","NoGi Class"))

class Lesson(models.Model):
    time = models.DateTimeField()
    class_type = models.CharField(choices=CLASS_CHOICES, max_length=12)
    attendees = models.ManyToManyField(Attendee)

class Schedule(models.Model):
    date = models.DateField()
    lessons = models.ManyToManyField(Lesson)

