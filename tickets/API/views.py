from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .serializers import TicketSerializer, TicketDetailSerializer, TicketOptionSerializer, TicketOptionDetailSerializer
from ..models import Ticket, TicketOption
from rest_framework.decorators import api_view


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_user_info(self):
        return self.get_user_info()


class TicketDetailViewSet(viewsets.ModelViewSet):
    serializer_class = TicketDetailSerializer
    queryset = Ticket.objects.all()


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


class TicketOptionDetailViewSet(viewsets.ModelViewSet):
    serializer_class = TicketOptionDetailSerializer
    queryset = TicketOption.objects.all()


@api_view(['POST', ])
def purchase_ticket(request):
    from accounts.models import User
    user = User.objects.get(id=request.data['user_id'])
    quantity = request.data['quantity']
    ticket_option = TicketOption.objects.get(id=request.data['ticket_option_id'])

    for x in range(quantity):
        ticket = Ticket.objects.create(
            user=user,
            ticket_option=ticket_option
        )
        print(x)

    return ticket


@api_view(['GET', ])
def get_purchased_tickets(request, user_id):
    from accounts.models import User
    user = User.objects.get(id=user_id)
    tickets = Ticket.objects.filter(user=user)

    serializer = TicketDetailSerializer(tickets, many=True)
    return Response(serializer.data)


