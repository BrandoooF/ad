from django.db import models
from events.models import EventOccurrence, Event
from accounts.models import User

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Sum, Count

# Create your models here.


class TicketOption(models.Model):
    name = models.CharField(max_length=60, default='Unnamed Ticket')
    description = models.CharField(max_length=120, blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    number_total = models.IntegerField()

    def get_number_purchased(self):
        return Ticket.objects.get(event_occurrence=self.id).count()

    def get_event_detail(self):
        event = Event.objects.get(id=self.event.id)
        return event

    def get_number_left(self):
        return self.number_total - self.get_number_left()

    def post_ticket_purchase(self):
        self.number_total -= 1  # runs after each purchase
        return self.number_total

    def get_event(self):
        return self.event

    def assign_ticket(self, user_id, quantity):
        user = User.objects.get(id=user_id)
        quantity = quantity
        # ticket_option = TicketOption.objects.get(id=ticket_option_id)

        for x in range(quantity):
            ticket = Ticket.objects.create(
                user=user,
                ticket_option=self
            )

            print(x)

        subject = 'Your Tickets from Fanattix'
        html_message = render_to_string('mail/ticket.html', {'event': self.event, 'ticket_option': self})
        plain_message = strip_tags(html_message)
        from_email = 'brandon.f.fallings@gmail.com'
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)  # send the email

        return ticket

    def get_number_tickets_sold(self):
        ticket_count = Ticket.objects.filter(ticket_option=self).count()
        return ticket_count

    def get_dollar_amount_sold(self):
        dollar_amount_sold = Ticket.objects.filter(ticket_option=self).count() * self.price
        return dollar_amount_sold


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    ticket_option = models.ForeignKey(TicketOption, on_delete=models.CASCADE, blank=True, null=True)
    checked_in = models.BooleanField(default=False)
    # event_occurrence = models.ForeignKey(EventOccurrence, on_delete=models.CASCADE, blank=True, null=True)

    def check_in(self):
        try:
            checkin, created = CheckIn.objects.get_or_create(ticket=self)
            if created:
                created.save()
                self.checked_in = True
                response_dict = {'checkin': created, 'accepted': True}
                return response_dict
            if checkin:
                self.checked_in = True
                response_dict = {'checkin': checkin, 'accepted': False}
                return response_dict
        except:
            response_dict = {'checkin': 'Ticket Not Found', 'accepted': False}
            return response_dict

    def get_ticket_option(self):
        return self.ticket_option

    def get_event_detail(self):
        event = Event.objects.get(id=self.ticket_option.event.id)
        return event

    def get_user(self):
        return self.user

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class CheckIn(models.Model):
    date = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s", self.ticket.ticket_option.name, self.date



