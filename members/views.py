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

import stripe
import json
import hashlib

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .forms import RegisterForm, NewsletterForm, ContactForm

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def index_page(request):
    #messages.success(request, "Hey")

    newsletter_form = NewsletterForm()
    contact_form = ContactForm()

    context = {
        "newsletter_form": newsletter_form,
        "contact_form": contact_form
    }
    return render(request, "index.html", context)

#Newsletter signup view
def newsletter(request):
    if request.method == 'POST': #Checks that form posts valid data
        
        form = NewsletterForm(request.POST) 

        if form.is_valid():

            name = form.cleaned_data.get('name')

            first, *last = name.split()

            subscriber_hash = hashlib.md5(form.cleaned_data.get('email').encode('utf-8')).hexdigest() #Gets subscriber hash

            try:
                client = MailchimpMarketing.Client() #Configures Mailchimp client
                client.set_config({
                "api_key": settings.MAILCHIMP_API_KEY,
                "server": settings.MAILCHIMP_SERVER
            })

                #Adds poster to newsletter
                client.lists.add_list_member(settings.MAILCHIMP_LIST_ID, {"merge_fields":{"FNAME": first, "LNAME": " ".join(last)} ,"email_address": form.cleaned_data.get('email'), "status": "subscribed", "tags":["beginners course"]})

                messages.success(request, "Thank you for subscribing")
                return redirect('index_page')
            except ApiClientError as error:
                print(error.text)
                res = json.loads(error.text)
                #Custom condition for users that are already subscribed
                if res['title'] == "Member Exists":
                    client.lists.update_list_member_tags(settings.MAILCHIMP_LIST_ID, subscriber_hash, {"tags":[{"name": "beginners course", "status": "active"}]})
                    messages.warning(request, "You are already subscribed!")
                    return redirect('index_page')
                messages.error(request, "An error occured")  
                return redirect('index_page')
    messages.error(request, "That didn't work")
    return redirect('index_page')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)        

        #Check form post data is valid
        if form.is_valid():

            #SendGrid configuration
            message = Mail(
                from_email='sam@execbjj.com',
                to_emails='sam@execbjj.com',
                subject='New form submission from {}'.format(form.cleaned_data.get('name')),
                plain_text_content=form.cleaned_data.get('message'))
            message.reply_to=form.cleaned_data.get('email'), form.cleaned_data.get('name')
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY) #Initialises Sendgrid Client
                response = sg.send(message)
                messages.success(request, "Thank you for your message, we will respond shortly")
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
            return redirect('dashboard_page')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_page(request):

    subscription = Subscription.objects.filter(user=request.user)

    if subscription.exists():
        membership = subscription.first().membership
    else:
        membership = None

    context = {
        "membership": membership
    }
    return render(request, "dashboard.html", context)

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

    #Handles POST request from the memberships page
    def post(self, request, *args, **kwargs):

        customer_id = request.user.stripe_customer_id

        #Gets the membership type from hidden input in form
        membership = Membership.objects.get(name=request.POST.get('membership'))
        
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
                
                mode='subscription',
                #Redirects to referer url
                success_url=request.build_absolute_uri() +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri()
            )
            return redirect(checkout_session.url, code=303)
        
        except Exception as e:
            print(e)
            return e

@login_required
def success_view(request):

    #Gets sessionID from URL parameters
    session_id = request.GET.get("session_id")

    #Gets line item from checkout session
    line_item = stripe.checkout.Session.list_line_items(session_id, limit=1)

    #Retrieves checkout session object
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    
    #Creates new subscription with request user, priceID from line item (only works with one line item), subscriptionID from checkout session and sets status to active
    subscription, created = Subscription.objects.get_or_create(user=request.user, membership=Membership.objects.get(stripe_price_id=line_item.data[0].price.id), stripe_subscription_id=checkout_session['subscription'], status="active")
    subscription.save()

    messages.success(request, "Thank for you subscribing!")

    return redirect('dashboard_page')

def check_in(request):

    if request.method == "POST":

        subscription = Subscription.objects.filter(user=request.user)

        if subscription.exists():
        
            messages.info(request, "Check ins will open soon, keep an eye on your email inbox!")
            return redirect('dashboard_page')

        else:
            messages.error(request, "You must have an active membership to check in to class")
            return redirect('dashboard_page')
    return redirect('dashboard_page')


@csrf_exempt
def webhook(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    #webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body

    # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
    )
        data = event['data']
    except Exception as e:
        return e
        
    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    event_type = event['type']
    data_object = data['object']

    if event_type == 'invoice.payment_succeededTEST':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing

        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]

        stripe_sub = stripe.Subscription.retrieve(webhook_object["subscription"])
        stripe_price_id = stripe_sub["plan"]["id"]

        membership = Membership.objects.get(stripe_price_id=stripe_price_id)

        user = CustomUser.objects.get(stripe_customer_id=stripe_customer_id)
        user.subscription.status = stripe_sub["status"]
        user.subscription.stripe_subscription_id = webhook_object["subscription"]
        user.subscription.membership = membership
        user.subscription.save()

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
        customer = request.user.stripe_customer_id,
        return_url = "http://execbjj.com/dashboard",
    )
    return redirect(session.url)

def account_page(request):
    return True