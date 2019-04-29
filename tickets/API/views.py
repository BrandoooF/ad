from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .serializers import TicketSerializer, TicketOptionSerializer
from ..models import Ticket, TicketOption


class TicketViewSet(viewsets.ModelViewSet):
    user_info = serializers.SerializerMethodField()

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_user_info(self):
        return self.get_user_info()


class TicketOptionViewSet(viewsets.ModelViewSet):
    serializer_class = TicketOptionSerializer
    queryset = TicketOption.objects.all()

    def create(self, request, *args, **kwargs):
        from events.models import Event
        name = request.data['name']
        url = 'www.fanattix.com'
        price = request.data['price']
        event_occurrence_id = request.data['event']
        number_total = request.data['number_total']

        event = Event.objects.get(id=event_occurrence_id)

        ticket_option = TicketOption.objects.create(
            name=name,
            url=url,
            price=price,
            event=event,
            number_total=number_total
        )
        ticket_option.save()

        serializer = TicketOptionSerializer(ticket_option)

        return Response(serializer.data)


