from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.


class User(AbstractUser):
    profile_img = models.ImageField(blank=True, null=True)
    receives_emails = models.BooleanField(default=True)
    receives_emails_from_organizers = models.BooleanField(default=True)

    def get_my_events(self):
        from events.models import Event
        return Event.objects.filter(creator=self)

    def get_tickets(self):
        from tickets.models import Ticket
        tickets = Ticket.objects.filter(user=self.id)
        return tickets

    def connect_stripe_account(self, stripe_user_id, stripe_access_token, stripe_publishable_key, refresh_token, scope):
        from stripeservice.models import StripeConnectedUser

        connect = StripeConnectedUser.objects.create(
            user=self,
            stripe_user_id=stripe_user_id,
            stripe_access_token=stripe_access_token,
            stripe_publishable_key=stripe_publishable_key,
            refresh_token=refresh_token,
            scope=scope
        )
        connect.save()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        print('created token')


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
