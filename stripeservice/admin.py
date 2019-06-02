from django.contrib import admin
from .models import StripeConnectedUser, StripeToken

# Register your models here.
admin.site.register(StripeConnectedUser)
admin.site.register(StripeToken)
