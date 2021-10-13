from django.urls import path
from django.conf import settings

from .views import MembershipSelectView, create_customer_portal, newsletter, success_view, check_in, newsletter, contact

app_name="members"

urlpatterns = [
    path('', MembershipSelectView.as_view(), name="membership_page"),
    path('success/', success_view, name="success_page"),
    path('check-in/', check_in, name="check_in"),
    path('newsletter/', newsletter, name="newsletter"),
    path('contact/', contact, name="contact"),
    path('create-customer-portal/', create_customer_portal, name="customer_portal")
]