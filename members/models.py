from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    stripe_customer_id = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Receiver to create customer in Stripe and assing their StripeID to the CustomUser object


@receiver(post_save, sender=CustomUser)
def create_stripe_id(sender, instance, **kwargs):

    name = str("{0} {1}").format(instance.first_name, instance.last_name)

    if instance.stripe_customer_id == None:

        stripe_customer = stripe.Customer.create(
            name=name,
            email=instance.email
        )

        instance.stripe_customer_id = stripe_customer["id"]

        post_save.disconnect(create_stripe_id, sender=CustomUser)
        instance.save()
        post_save.connect(create_stripe_id, sender=CustomUser)

# Membership features


class MembershipFeature(models.Model):
    feature = models.CharField(max_length=180)

    def __str__(self):
        return self.feature

# Membership Class


class Membership(models.Model):
    name = models.CharField(max_length=100)  # Monthly / Quarterly / Annual
    slug = models.SlugField()
    features = models.ManyToManyField(MembershipFeature)
    stripe_price_id = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    frequency = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Subscription Class


class Subscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, related_name='memberships')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == "active" or self.status == "inactive"

# Schedule Class

# Technique of the Week Class
