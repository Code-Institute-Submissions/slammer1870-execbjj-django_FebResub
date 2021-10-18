from django.urls import path
from django.conf import settings

from .views import check_in

app_name="checkins"

urlpatterns = [
    path('', check_in, name="checkin_view"),
]