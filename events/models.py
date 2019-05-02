from django.db import models
from ckeditor.fields import RichTextField

from eventtools.models import BaseEvent, BaseOccurrence
from accounts.models import User

# Create your models here.


class Event(BaseEvent):
    TYPE_CHOICES = (
        ('appearance', 'Appearance'),
        ('attraction', 'Attraction'),
        ('class/training', 'Class/Training'),
        ('concert/performance', 'Concert/Performance'),
        ('Trip/Retreat', 'Trip/Retreat'),
        ('attraction', 'Attraction'),
        ('Dinner/Gala', 'Dinner/Gala'),
        ('Game/Competition', 'Game/Competition'),
        ('Networking', 'Networking'),
        ('Tradeshow/Expo', 'Tradeshow/Expo'),
        ('Tournament', 'Tournament'),
        ('Seminar', 'Seminar'),
        ('Race Event', 'Race Event'),
        ('other', 'Other',)
    )

    CATEGORY_CHOICES = (
        ('auto/boat/air', 'Auto/Boat/Air'),
        ('business/professional', 'Business/Professional'),
        ('charity/cause', 'Charity/Cause'),
        ('community/Culture', 'Community/Culture'),
        ('other', 'Other')
    )

    name = models.CharField(max_length=70)
    description = RichTextField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='other')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    location = models.TextField()
    venue = models.TextField()
    image = models.ImageField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def create_occurrence(self, creator_id, event_id, start, end, repeat):
        creator = User.objects.get(id=creator_id)
        event = Event.objects.get(id=event_id)
        occurrence = EventOccurrence.objects.create(
            creator=creator,
            event=event,
            start=start,
            end=end,
        )
        occurrence.save()

    def get_occurrences(self):
        return EventOccurrence.objects.filter(event=self.id)

    def __str__(self):
        return self.name


class EventOccurrence(BaseOccurrence):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def get_event_detail(self):
        return self.event

    # This Method may not be needed
    '''def create_ticket_options(self, url, event_occurrence_id, price, number_total):
        from tickets.models import TicketOption
        ticket_option = TicketOption.objects.create(
            url=url,
            event_occurrence=event_occurrence_id,
            price=price,
            number_total=number_total
        )
        ticket_option.save()'''

    def __str__(self):
        return self.event.name


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.event.name
