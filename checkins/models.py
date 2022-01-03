from django.db import models
from django.conf import settings

# Create your models here.
class Schedule(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)

CLASS_CHOICES = (("Gi Class (Beginners)", "GI"), ("NoGi Class (Beginners)","NOGI"), ("Gi Class (Mixed Levels)", "GIMIX"), ("NoGi Class (Mixed Levels)","NOGIMIX"), ("Open Mat","OPEN"), ("Sparring Class","SPARRING"), ("Wrestling","WRESTLING"))

class Lesson(models.Model):
    time = models.DateTimeField(unique=True)
    class_type = models.CharField(choices=CLASS_CHOICES, max_length=50)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    @property
    def remaining(self):
        #NB Class size is hard coded to 20
        amount = 20 - len(self.attendee_set.all())
        return amount

    class Meta:
        ordering = ['time']

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
    

