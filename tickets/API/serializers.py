from rest_framework import serializers
from ..models import Ticket, TicketOption


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketOption
        fields = '__all__'
