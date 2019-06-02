from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Event, EventOccurrence, Category, Type
from tickets.models import Ticket
from accounts.models import User
from django.db.models import FloatField, F
from service import functions

from service.functions import send_email_to_patrons

from datetime import datetime

from .serializers import EventOccurrenceSerializer, EventSerializer, CategorySerializer, TypeSerializer
from tickets.API.serializers import TicketSerializer
from service.functions import convert_and_save_image


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TypeViewSet(viewsets.ModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        if hasattr(request.data, 'image'):
            if request.data['image'] is not None:  # If an image string in base64 is present convert it to an image
                img_data = convert_and_save_image(request.data['image'], request.data['name'])
                request.data['image'] = img_data
                print(img_data)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            return Response({'event': serializer.data, 'message': 'Event Successfully Saved'})

        return Response({'errors': serializer.errors})

    def update(self, request, *args, **kwargs):
        print(request.data['image'])
        if request.data['image'] is not None:   # If an image string in base64 is present convert it to an image
            img_data = convert_and_save_image(request.data['image'], request.data['name'])
            request.data['image'] = img_data

        return super().update(request)


class EventOccurrenceViewSet(viewsets.ModelViewSet):
    serializer_class = EventOccurrenceSerializer
    queryset = EventOccurrence.objects.all()


@api_view(['POST', ])
def purchase_ticket(request, user_id, event_occurrence_id):
    ticket = Ticket.objects.create(
        user=user_id,
        event_occurrence=event_occurrence_id
    )

    serializer = TicketSerializer(ticket, many=True)
    return serializer.data


@api_view(['GET', ])
def get_my_events(request, user_id):
    # user_id = user_id
    user = User.objects.get(id=user_id)
    events = user.get_my_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def get_tickets(request, user_id):
    tickets = Ticket.objects.filter(user=user_id)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)


# ####### Search

@api_view(['GET', ])
def search_events_by_name(request):
    event_name = request.query_params.get('name')
    print(event_name)
    events = Event.objects.filter(name__icontains=event_name)
    print(events)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def get_free_events(request):
    from tickets.models import TicketOption
    event_ids = TicketOption.objects.filter(price__lte=0).values_list('event', flat=True)
    events = Event.objects.filter(id__in=event_ids)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
def search_events_by_CLD(request):  # CLD = Category, Location, Date
    category_id = request.data['category']
    # category = Category.objects.filter(id=category_id)
    search_lat = request.data['lat']
    search_lng = request.data['lng']
    date = request.data['date']
    print(request.data['date'])

    # Filter Category
    if request.data['category'] is not '':
        events_category = Event.objects.filter(category_obj_id=category_id)
    else:
        events_category = Event.objects.all()

    # Filter Date
    if request.data['date'] is not '':
        event_ids = EventOccurrence.objects.filter(start__lte=date).values_list('event_id', flat=True)
        print(event_ids)
        events_date = events_category.filter(id__in=event_ids)
    else:
        events_date = events_category

    # OKAY check distance from long and order by that, then check distance from lat and order by that
    # This will return events in order from distance of search
    events = events_date.annotate(dist_lng=search_lng - F('lng')).order_by('-dist_lng')\
        .annotate(dist_lat=search_lat - F('lat')).order_by('-dist_lat')

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
def send_email_to_patrons(request):
    event_id = request.data['event_id']
    message = request.data['message']
    subject = request.data['subject']
    sender_id = request.data['sender_id']
    sender = User.objects.get(id=sender_id)
    sender_email = sender.email
    print(request.data)
    tickets_user_ids = Ticket.objects.filter(ticket_option__event=event_id).values_list('id', flat=True)
    print(tickets_user_ids)
    users_emails = User.objects.filter(id__in=tickets_user_ids).values_list('email', flat=True)
    print(users_emails)

    functions.send_email_to_patrons(subject, message, sender_email, users_emails)

    return Response({'message': 'Hello Bruh'})




