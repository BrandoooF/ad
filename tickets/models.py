from django.db import models
from events.models import EventOccurrence, Event
from accounts.models import User

# Create your models here.


class TicketOption(models.Model):
    name = models.CharField(max_length=60, default='Unnamed Ticket')
    url = models.URLField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    number_total = models.IntegerField()

    def get_number_purchased(self):
        return Ticket.objects.get(event_occurrence=self.id).count()

    def get_number_left(self):
        return self.number_total - self.get_number_left()

    def get_event(self):
        return self.event


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    ticket_option = models.ForeignKey(TicketOption, on_delete=models.CASCADE, blank=True, null=True)
    # event_occurrence = models.ForeignKey(EventOccurrence, on_delete=models.CASCADE, blank=True, null=True)

    '''def get_event_occurrence(self):
        return self.event_occurrence'''

    def get_ticket_option(self):
        return self.ticket_option

    def get_user(self):
        return self.user

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


