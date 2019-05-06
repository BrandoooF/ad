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

    def update(self, request, *args, **kwargs):
        if request.data['image']:   # If an image string in base64 is present convert it to an image
            img_data = convert_and_save_image(request.data['image'], request.data['name'])
            request.data['image'] = img_data

        # event = Event.objects.get(id=request.query_params['id'])

        return super().update(request)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            '''occurrence = {
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
            return Response(occ_serializer.errors)'''
            return Response(serializer.data)

        return Response(serializer.errors)

'''
@api_view(['GET',])
def get_my_events(request, id, *args, **kwargs):
    events = Event.objects.filter(id=id)
    serializer = EventSerializer(events, many=True)
    return serializer.data
    '''


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





