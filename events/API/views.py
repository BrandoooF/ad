from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Event, EventOccurrence
from tickets.models import Ticket
from accounts.models import User

from datetime import datetime

from .serializers import EventOccurrenceSerializer, EventSerializer
from tickets.API.serializers import TicketSerializer
from service.functions import convert_and_save_image


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data['image'])
        if request.data['image']:   # If an image string in base64 is present convert it to an image
            img_data = convert_and_save_image(request.data['image'], request.data['name'])
            request.data['image'] = img_data

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            occurrence = {
                'creator': obj.creator.id,
                'event': obj.id,
                'start': datetime(2019, 12, 25),
                'end': datetime(2019, 12, 25)
            }

            occ_serializer = EventOccurrenceSerializer(data=occurrence)
            if occ_serializer.is_valid():
                occ_serializer.save()
                return Response({'event': serializer.data, 'occurrence': occ_serializer.data,
                                 'message': 'Event Successfully Created'})
            return Response(occ_serializer.errors)

        return Response(serializer.errors)


@api_view(['GET',])
def get_my_events(request, id, *args, **kwargs):
    events = Event.objects.filter(id=id)
    serializer = EventSerializer(events, many=True)
    return serializer.data


class EventOccurrenceViewSet(viewsets.ModelViewSet):
    serializer_class = EventOccurrenceSerializer
    queryset = EventOccurrence.objects.all()


@api_view(['POST', ])
def purchase_ticket(request, user_id, event_id):
    ticket = Ticket.objects.create(
        user=user_id,
        event_occurrence=event_id
    )

    serializer = TicketSerializer(ticket, many=True)
    return serializer.data


@api_view(['GET', ])
def get_events_created(request, user_id):
    # user_id = user_id
    user = User.objects.get(id=user_id)
    events = user.get_events_created()
    serializer = EventOccurrenceSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def get_tickets(request, user_id):
    tickets = Ticket.objects.filter(user=user_id)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)





