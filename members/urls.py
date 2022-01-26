from django.urls import path
from django.conf import settings

from .views import MembershipSelectView, create_customer_portal, newsletter, success_view, check_in, newsletter, contact, crypto_payment, coinbase_webhook

app_name = "members"

urlpatterns = [
    path('', MembershipSelectView.as_view(), name="membership_page"),
    path('success/', success_view, name="success_page"),
    path('check-in/', check_in, name="check_in"),
    path('newsletter/', newsletter, name="newsletter"),
    path('contact/', contact, name="contact"),
    path('create-customer-portal/', create_customer_portal, name="customer_portal"),
    path('crypto-payment/', crypto_payment, name="crypto_payment"),
    path('coinbase-webhook/', coinbase_webhook, name="coinbase_webhook")
]
