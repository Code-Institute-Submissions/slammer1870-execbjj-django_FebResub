from django.contrib import admin

from .models import Video, Section, Difficulty, TechniqueOfTheWeek

# Register your models here.
admin.site.register(Video)
admin.site.register(Section)
admin.site.register(Difficulty)
admin.site.register(TechniqueOfTheWeek)