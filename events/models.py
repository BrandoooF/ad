from django.db import models
from ckeditor.fields import RichTextField

from eventtools.models import BaseEvent, BaseOccurrence
from accounts.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def get_events_in_category(self):
        return Event.objects.filter(category=self)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)

    def get_events_of_type(self):
        return Event.objects.filter(type=self)

    def __str__(self):
        return self.name


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
        ('Other', 'Other',)
    )

    CATEGORY_CHOICES = (
        ('Auto/Boat/Air', 'Auto/Boat/Air'),
        ('Business/Professional', 'Business/Professional'),
        ('Charity/Cause', 'Charity/Cause'),
        ('Community/Culture', 'Community/Culture'),
        ('Education', 'Education'),
        ('Fashion/Makeup/Beauty', 'Fashion/Makeup/Beauty'),
        ('Film/Media', 'Film/Media'),
        ('Food/Drink', 'Food/Drink'),
        ('Politics/Government', 'Politics/Government'),
        ('Health/Wellness', 'Health/Wellness'),
        ('Hobbies', 'Hobbies'),
        ('Home/Gardening/Lifestyle', 'Home/Gardening/Lifestyle'),
        ('School', 'School'),
        ('Science/Technology/Engineering/Math', 'Science/Technology/Engineering/Math'),
        ('Seasonal/Holiday', 'Seasonal/Holiday'),
        ('Sports/Fitness', 'Sports/Fitness'),
        ('Outdoor/Travel', 'Outdoor/Travel'),
        ('Other', 'Other')
    )

    name = models.CharField(max_length=70)
    description = RichTextField()
    # type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Other')
    type_obj = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    # category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Other')
    category_obj = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    location = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    organizers = models.CharField(max_length=70, blank=True, null=True)
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

    def get_category(self):
        # cat = Category.objects.get(id=self.category_obj.id)
        return self.category_obj

    def get_type(self):
        # type_obj = Type.objects.get(id=self.type_obj.id)
        return self.type_obj

    @staticmethod
    def filter_from_distance(miles, lat, lng):
        degrees = (miles / 69)
        max_lat = lat + degrees
        min_lat = lat - degrees

        max_lng = lng + ((90 - lat)*degrees)
        min_lng = lng - ((90 - lat)*degrees)

        near_by = Event.objects.filter(lat__lte=max_lat, lat__gte=min_lat, lng__lte=max_lng, lng__gte=min_lng)

        return near_by

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




