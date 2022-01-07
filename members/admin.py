from django.contrib import admin
from. models import CustomUser, Membership, MembershipFeature, Subscription

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Membership)
admin.site.register(MembershipFeature)
admin.site.register(Subscription)
