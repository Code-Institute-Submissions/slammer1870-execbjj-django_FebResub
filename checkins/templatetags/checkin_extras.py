from django import template
from django.utils import timezone

from checkins.models import Attendee

register = template.Library()

# Create your views here.

@register.filter
def checked_in(user, lesson):
    attendee = Attendee.objects.filter(user=user, lesson=lesson)
    if attendee.exists():
        return True
    else:
        return False

@register.filter
def already_happened(lesson):
    if lesson.time <= timezone.now():
        return True
    else:
        return False