from django.contrib import admin
from .models import StripeConnectedUser, StripeToken, StripeSavedPaymentMethod

# Register your models here.
admin.site.register(StripeConnectedUser)
admin.site.register(StripeToken)
admin.site.register(StripeSavedPaymentMethod)
