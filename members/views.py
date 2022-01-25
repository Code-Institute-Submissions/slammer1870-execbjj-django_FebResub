import email
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import base_user, login, authenticate
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from members.models import CustomUser, Membership, Subscription
from checkins.models import Schedule
from video.models import TechniqueOfTheWeek

from datetime import datetime, timedelta

import stripe
import json
import hashlib
import requests

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .forms import RegisterForm, NewsletterForm, ContactForm

from coinbase_commerce.client import Client

from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook

import logging

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def index_page(request):
    # messages.success(request, "Hey")

    newsletter_form = NewsletterForm()
    contact_form = ContactForm()

    context = {
        "newsletter_form": newsletter_form,
        "contact_form": contact_form
    }
    return render(request, "index.html", context)

# Newsletter signup view


def newsletter(request):
    if request.method == 'POST':  # Checks that form posts valid data

        form = NewsletterForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data.get('name')

            first, *last = name.split()

            subscriber_hash = hashlib.md5(form.cleaned_data.get(
                'email').encode('utf-8')).hexdigest()  # Gets subscriber hash

            try:
                client = MailchimpMarketing.Client()  # Configures Mailchimp client
                client.set_config({
                    "api_key": settings.MAILCHIMP_API_KEY,
                    "server": settings.MAILCHIMP_SERVER
                })

                # Adds poster to newsletter
                client.lists.add_list_member(settings.MAILCHIMP_LIST_ID, {"merge_fields": {"FNAME": first, "LNAME": " ".join(
                    last)}, "email_address": form.cleaned_data.get('email'), "status": "subscribed", "tags": ["beginners course"]})

                messages.success(request, "Thank you for subscribing")
                return redirect('index_page')
            except ApiClientError as error:
                print(error.text)
                res = json.loads(error.text)
                # Custom condition for users that are already subscribed
                if res['title'] == "Member Exists":
                    client.lists.update_list_member_tags(settings.MAILCHIMP_LIST_ID, subscriber_hash, {
                                                         "tags": [{"name": "beginners course", "status": "active"}]})
                    messages.warning(request, "You are already subscribed!")
                    return redirect('index_page')
                messages.error(request, "An error occured")
                return redirect('index_page')
    messages.error(request, "That didn't work")
    return redirect('index_page')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Check form post data is valid
        if form.is_valid():

            # SendGrid configuration
            message = Mail(
                from_email='sam@execbjj.com',
                to_emails='sam@execbjj.com',
                subject='New form submission from {}'.format(
                    form.cleaned_data.get('name')),
                plain_text_content=form.cleaned_data.get('message'))
            message.reply_to = form.cleaned_data.get(
                'email'), form.cleaned_data.get('name')
            try:
                # Initialises Sendgrid Client
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                messages.success(
                    request, "Thank you for your message, we will respond shortly")
                return redirect('index_page')
            except Exception as e:
                messages.error(request, "Oops something went wrong")
                return redirect('index_page')
        messages.error(request, "Oops something went wrong")
        return redirect('index_page')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard_redirect')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_page(request, date):

    year, month, day = date.split('-')

    try:
        date_object = datetime(year=int(year), month=int(month), day=int(day))
        if date_object < datetime.today() - timedelta(days=1):
            return redirect('dashboard_redirect')
    except ValueError:
        messages.error(request, "The date that you have entered is invalid")
        return redirect('dashboard_redirect')

    subscription = Subscription.objects.filter(user=request.user)

    day = Schedule.objects.filter(date=date)

    if day.exists():
        schedule = day.first()
    else:
        schedule = None

    if subscription.exists():
        membership = subscription.first().membership
    else:
        membership = None

    today = datetime.strptime(date, "%Y-%m-%d")

    tomorrow_date = today + timedelta(days=1)

    tomorrow = datetime.strftime(tomorrow_date, "%Y-%m-%d")

    if today >= datetime.today():
        yesterday_date = today - timedelta(days=1)
        yesterday = datetime.strftime(yesterday_date, "%Y-%m-%d")
    else:
        yesterday = None

    last_week = today + timedelta(days=-7)

    technique_of_the_week = TechniqueOfTheWeek.objects.filter(
        date__range=[last_week, today])

    if technique_of_the_week.exists():
        technique_of_the_week = technique_of_the_week.first()
        techniques = technique_of_the_week.video.all()
    else:
        techniques = None

    context = {
        "membership": membership,
        "today": today,
        "yesterday": yesterday,
        "tomorrow": tomorrow,
        "schedule": schedule,
        "techniques": techniques,
    }
    return render(request, "dashboard.html", context)


@login_required
def dashboard_redirect(request):
    return redirect('dashboard_page', datetime.strftime(datetime.today(), "%Y-%m-%d"))


def membership_page(request):
    return render(request, "memberships.html")


def get_user_membership(request):
    user_membership_qs = Subscription.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'members/membership_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['memberships'] = Membership.objects.filter(active=True)

        if current_membership:
            context['current_membership'] = current_membership
        return context

    # Handles POST request from the memberships page
    def post(self, request, *args, **kwargs):

        customer_id = request.user.stripe_customer_id

        # Gets the membership type from hidden input in form
        membership = Membership.objects.get(
            name=request.POST.get('membership'))

        if membership.slug == "beginners-course":
            mode = "payment"
        else:
            mode = "subscription"

        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': membership.stripe_price_id,
                        'quantity': 1,
                    },
                ],

                mode=mode,
                allow_promotion_codes=True,
                # Redirects to referer url
                success_url=request.build_absolute_uri() +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri()
            )
            return redirect(checkout_session.url, code=303)

        except Exception as e:
            print(e)
            return e


def beginners_course(request):

    products = {
        'beginners-course': {
            'name': 'Intro to Brazilian Jiu Jitsu - 6 Week Course',
            'price': 14900,
        },
    }

    if request.method == "POST":

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'product_data': {
                                'name': 'Intro to Brazilian Jiu Jitsu - 6 Week Course',
                            },
                            'unit_amount': 19900,
                            'currency': 'eur',
                        },
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                # Redirects to referer url
                success_url=request.build_absolute_uri() +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri()
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            return e

    return render(request, "beginners_course.html")


def beginners_success(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)

    context = {
        "customer": customer
    }

    return render(request, "success.html", context)


@login_required
def success_view(request):

    # Gets sessionID from URL parameters
    session_id = request.GET.get("session_id")

    # Gets line item from checkout session
    line_item = stripe.checkout.Session.list_line_items(session_id, limit=1)

    # Retrieves checkout session object
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    if checkout_session['subscription']:
        sub_id = checkout_session['subscription']
    else:
        sub_id = ""

    # Creates new subscription with request user, priceID from line item (only works with one line item), subscriptionID from checkout session and sets status to active
    subscription, created = Subscription.objects.update_or_create(user=request.user, defaults={'membership': Membership.objects.get(
        stripe_price_id=line_item.data[0].price.id), 'stripe_subscription_id': sub_id, 'status': "active"})
    subscription.save()

    messages.success(request, "Thank for you subscribing!")

    return redirect('dashboard_redirect')


def check_in(request):

    if request.method == "POST":

        subscription = Subscription.objects.filter(user=request.user)

        if subscription.exists():

            messages.info(
                request, "Check ins will open soon, keep an eye on your email inbox!")
            return redirect('dashboard_page')

        else:
            messages.error(
                request, "You must have an active membership to check in to class")
            return redirect('dashboard_page')
    return redirect('dashboard_page')


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@csrf_exempt
def webhook(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event_type = None

    try:
        event_type = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        data = event_type['data']
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    event_type = event_type['type']
    data_object = data['object']

    if event_type == 'customer.subscription.updated':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing

        webhook_object = data["object"]

        stripe_customer_id = webhook_object["customer"]

        stripe_sub = stripe.Subscription.retrieve(webhook_object["id"])
        stripe_price_id = stripe_sub["plan"]["id"]

        membership = Membership.objects.get(stripe_price_id=stripe_price_id)

        user = CustomUser.objects.get(stripe_customer_id=stripe_customer_id)

        subscription = Subscription.objects.get(user=user)
        subscription.status = stripe_sub["status"]
        subscription.stripe_subscription_id = webhook_object["id"]
        subscription.membership = membership
        subscription.save()

    if event_type == 'customer.subscription.deleted':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing

        webhook_object = data["object"]

        stripe_customer_id = webhook_object["customer"]

        user = CustomUser.objects.get(stripe_customer_id=stripe_customer_id)

        subscription = Subscription.objects.get(user=user)
        subscription.delete()

    return HttpResponse(status=200)


@login_required
def create_customer_portal(request):

    session = stripe.billing_portal.Session.create(
        customer=request.user.stripe_customer_id,
        return_url=request.META['HTTP_REFERER'],
    )
    return redirect(session.url)


def flyer(request):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.284',
        'X-Forwarded-For': '127.0.0.1',
        'Content-Type': 'application/json',
    }

    data = '{"name":"flyerview","url":"http://execbjj.com","domain":"execbjj.com","width":1666}'

    response = requests.post(
        'https://plausible.io/api/event', headers=headers, data=data)

    return redirect("index_page")


def crypto_payment(request):
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = settings.DOMAIN_URL
    product = {
        'name': 'Coffee',
        'description': 'A really good local coffee.',
        'local_price': {
            'amount': '0.01',
            'currency': 'EUR'
        },
        'pricing_type': 'fixed_price',
        'redirect_url': domain_url + 'dashboard/',
        'cancel_url': domain_url + 'memberships/',
        'metadata': {
            'customer_id': request.user.id if request.user.is_authenticated else None,
            'customer_username': request.user.email if request.user.is_authenticated else None,
        },
    }
    charge = client.charge.create(**product)

    return redirect(charge['hosted_url'])


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(
            request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:confirmed':
            logger.info('Payment confirmed.')
            customer_id = event['data']['metadata']['customer_id']  # new
            # new
            customer_username = event['data']['metadata']['customer_username']

            membership = Membership.objects.get(
                slug='annual')

            user = CustomUser.objects.get(
                email=customer_username)

            subscription = Subscription.objects.get_or_create(user=user)
            subscription.status = 'active'
            subscription.stripe_subscription_id = "coinbase"
            subscription.membership = membership
            subscription.save()
            messages.success(request, "Thank for you subscribing!")

            return redirect('dashboard_redirect')
            # TODO: run some custom code here
            # you can also use 'customer_id' or 'customer_username'
            # to fetch an actual Django user

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)
