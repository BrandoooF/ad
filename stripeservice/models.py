from django.db import models

# Create your models here.


class StripeConnectedUser(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, blank=True, null=True)
    stripe_user_id = models.CharField(max_length=90)
    stripe_access_token = models.CharField(max_length=90)
    stripe_publishable_key = models.CharField(max_length=90)
    refresh_token = models.CharField(max_length=90)
    scope = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username


class StripeToken(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, blank=True, null=True)
    customer_id = models.CharField(max_length=90)

    def __str__(self):
        return self.user.email
