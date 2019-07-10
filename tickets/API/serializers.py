from rest_framework import serializers
from ..models import Ticket, TicketOption, CheckIn
from events.models import Event


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketDetailSerializer(serializers.ModelSerializer):
    event_detail = serializers.SerializerMethodField()

    def get_event_detail(self, obj):
        from events.API.serializers import EventSerializer
        print(obj.id)
        event = obj.get_event_detail()
        serializer = EventSerializer(event)
        return serializer.data

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketOptionSerializer(serializers.ModelSerializer):
    tickets_sold = serializers.SerializerMethodField()
    dollar_amount_sold = serializers.SerializerMethodField()

    def get_tickets_sold(self, obj):
        return obj.get_number_tickets_sold()

    def get_dollar_amount_sold(self, obj):
        return obj.get_dollar_amount_sold()

    class Meta:
        model = TicketOption
        fields = '__all__'


class TicketOptionDetailSerializer(serializers.ModelSerializer):
    event_detail = serializers.SerializerMethodField()
    tickets_sold = serializers.SerializerMethodField()

    def get_event_detail(self, obj):
        from events.API.serializers import EventSerializer
        event = obj.get_event_detail()
        serializer = EventSerializer(event)
        return serializer.data

    def get_tickets_sold(self, obj):
        return obj.get_number_tickets_sold()

    def get_dollar_amount_sold(self, obj):
        return obj.get_dollar_amount_sold()

    class Meta:
        model = TicketOption
        fields = '__all__'


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'

