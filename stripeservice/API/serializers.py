from rest_framework import serializers
from ..models import StripeSavedPaymentMethod, StripeConnectedUser


class StripeConnectedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConnectedUser
        fields = '__all__'


class StripeSavedPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeSavedPaymentMethod
        fields = '__all__'
