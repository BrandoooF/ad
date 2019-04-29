from django.contrib import admin
from .models import Event, EventOccurrence

# Register your models here.

admin.site.register(Event)
admin.site.register(EventOccurrence)
