from django.urls import path
from django.conf import settings

from .views import cancel_check_in, check_in, confirm_cancel_view

app_name = "checkins"

urlpatterns = [
    path('', check_in, name="checkin_view"),
    path('confirm/<lesson>', confirm_cancel_view, name="confirm_cancel_view"),
    path('cancel/', cancel_check_in, name="checkin_cancel_view"),
]
