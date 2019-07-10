from django.shortcuts import render
from .models import Ticket


# Create your views here.


def get_ticket(request, ticket_id):
    # ticketId = request.GET.get('ticket_id', '432')
    ticket = Ticket.objects.get(id=ticket_id)
    event = ticket.get_event_detail()
    return render(request, 'tickets/ticket_qr_code.html',
                  context={
                      'ticketId': ticket_id,
                      'ticket': ticket,
                      'event': event
                  })

