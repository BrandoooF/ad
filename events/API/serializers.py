from rest_framework import serializers
from ..models import EventOccurrence, Event
from tickets.models import TicketOption
from tickets.API.serializers import TicketOptionSerializer


class EventSerializer(serializers.ModelSerializer):
    ticket_options = serializers.SerializerMethodField()
    occurrences = serializers.SerializerMethodField()

    def get_ticket_options(self, obj):
        ticket_options = TicketOption.objects.filter(event=obj)
        serializer = TicketOptionSerializer(ticket_options, many=True)
        return serializer.data

    def get_occurrences(self, obj):
        occurrences = obj.get_occurrences()
        serializer = EventOccurrenceSerializer(occurrences, many=True)
        return serializer.data

    class Meta:
        model = Event
        fields = '__all__'


class EventOccurrenceSerializer(serializers.ModelSerializer):
    # event_detail = serializers.SerializerMethodField()

    def get_event_detail(self, obj):
        event = obj.get_event_detail()
        serializer = EventSerializer(event)
        return serializer.data

    class Meta:
        model = EventOccurrence
        fields = '__all__'
