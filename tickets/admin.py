from django.contrib import admin
from .models import Ticket, TicketOption

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketOption)
