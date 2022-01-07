from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import base_user, login, authenticate
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.db.models import Q

from members.models import CustomUser, Membership, Subscription
from checkins.models import Attendee, Lesson, Schedule

from datetime import datetime, timedelta
from django.utils import timezone


@login_required
def check_in(request):

    if request.method == "POST":

        subscription = Subscription.objects.filter(user=request.user)

        if subscription.exists():

            # get lesson from form POST request
            lesson = Lesson.objects.get(time=request.POST.get('lesson'))

            # check if user has an active booking
            bookings = Attendee.objects.filter(
                user=request.user, lesson__time__gte=timezone.localtime())

            # if bookings.exists():
            #    messages.warning(request, "You already have an active booking, you can only check into one class at a time!")
            #    return redirect('dashboard_page', lesson.schedule.date)

            # create new attendee instance with request.User
            attendee = Attendee(user=request.user)

            # add attendee to lesson
            attendee.lesson = lesson
            attendee.save()

            messages.success(request, "Thank you for checking in!")
            return redirect('dashboard_page', lesson.schedule.date)

        else:
            messages.error(
                request, "You must have an active membership to check in to class")
            return redirect('dashboard_redirect')
    return redirect('dashboard_redirect')


@login_required
def confirm_cancel_view(request, lesson):

    lesson = get_object_or_404(Lesson, time=lesson)

    return render(request, "checkins/confirm_cancel.html", {"lesson": lesson})


@login_required
def cancel_check_in(request):
    if request.method == "POST":
        lesson = Lesson.objects.get(time=request.POST.get('lesson'))

        attendee = Attendee.objects.get(lesson=lesson, user=request.user)
        attendee.delete()

        messages.warning(
            request, "You have successfully cancelled your appointment")
        return redirect('dashboard_page', lesson.schedule.date)
