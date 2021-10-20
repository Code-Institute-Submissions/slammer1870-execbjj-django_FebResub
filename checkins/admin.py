from django.contrib import admin
from django.db import models

from .models import Schedule, Lesson, Attendee

# Register your models here.


class LessonInline(admin.TabularInline):
    model = Lesson

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [
        LessonInline,
    ]
    model = Schedule

class AttendeeInline(admin.TabularInline):
    model = Attendee

class LessonAdmin(admin.ModelAdmin):
    inlines = [
        AttendeeInline,
    ]
    model = Lesson

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Attendee)