from django.db import models
from django.conf import settings

# Create your models here.
class Schedule(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)

CLASS_CHOICES = (("Gi Class", "GI"), ("NoGi Class","NOGI"))

class Lesson(models.Model):
    time = models.DateTimeField(unique=True)
    class_type = models.CharField(choices=CLASS_CHOICES, max_length=12)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time)
    

class Attendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson',)

    def __str__(self):
        return str(self.user.first_name)
    

