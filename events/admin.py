from django.contrib import admin
from .models import Event, EventOccurrence, Category, Type

# Register your models here.

admin.site.register(Event)
admin.site.register(EventOccurrence)
admin.site.register(Category)
admin.site.register(Type)
