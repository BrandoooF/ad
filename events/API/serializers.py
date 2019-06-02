from rest_framework import serializers
from ..models import EventOccurrence, Event, Category, Type
from tickets.models import TicketOption
from tickets.API.serializers import TicketOptionSerializer


class CategorySerializer(serializers.ModelSerializer):
    # event_detail = serializers.SerializerMethodField()

    '''
    def get_event_detail(self, obj):
        events = obj.get_event_detail()
        serializer = EventSerializer(event)
        return serializer.data'''

    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    # event_detail = serializers.SerializerMethodField()

    '''
    def get_event_detail(self, obj):
        events = obj.get_event_detail()
        serializer = EventSerializer(event)
        return serializer.data'''

    class Meta:
        model = Type
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    ticket_options = serializers.SerializerMethodField()
    occurrences = serializers.SerializerMethodField()
    category_detail = serializers.SerializerMethodField()
    type_detail = serializers.SerializerMethodField()
    total_tickets_sold = serializers.SerializerMethodField()

    def get_ticket_options(self, obj):
        ticket_options = TicketOption.objects.filter(event=obj)
        serializer = TicketOptionSerializer(ticket_options, many=True)
        return serializer.data

    def get_occurrences(self, obj):
        occurrences = obj.get_occurrences()
        serializer = EventOccurrenceSerializer(occurrences, many=True)
        return serializer.data

    def get_category_detail(self, obj):
        category = obj.get_category()
        serializer = CategorySerializer(category)
        return serializer.data

    def get_type_detail(self, obj):
        type_obj = obj.get_type()
        serializer = TypeSerializer(type_obj)
        return serializer.data

    def get_total_tickets_sold(self, obj):
        return obj.get_total_tickets_sold()

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
