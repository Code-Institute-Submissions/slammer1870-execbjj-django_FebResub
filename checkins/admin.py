from django.contrib import admin

from .models import Schedule, Lesson, Attendee

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Lesson)
admin.site.register(Attendee)