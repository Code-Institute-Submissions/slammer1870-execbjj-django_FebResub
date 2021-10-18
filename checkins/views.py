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


from members.models import CustomUser, Membership, Subscription
from checkins.models import Attendee, Lesson

# Create your views here.

@login_required
def check_in(request):

    if request.method == "POST":

        subscription = Subscription.objects.filter(user=request.user)

        if subscription.exists():
            #create new attendee instance with request.User
            attendee = Attendee.objects.create(user=request.user)
            #get lesson from form POST request
            lesson = Lesson.objects.get(time=request.POST.get('lesson'))
            #add attendee to lesson
            lesson.attendees.add(attendee)
        
            messages.info(request, "Thank you for checkin in!")
            return redirect('dashboard_page')

        else:
            messages.error(request, "You must have an active membership to check in to class")
            return redirect('dashboard_page')
    return redirect('dashboard_page')