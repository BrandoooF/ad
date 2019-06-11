from rest_framework import viewsets, status
from accounts.models import User
from ..models import StripeConnectedUser, StripeSavedPaymentMethod
from .serializers import StripeSavedPaymentMethodSerializer, StripeConnectedUserSerializer
from tickets.API.views import purchase_ticket
from tickets.models import TicketOption
from tickets.API.serializers import TicketSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_CLIENT_SECRET


@api_view(['POST'])
def get_connect_user_info(request):
    user_id = request.data['user_id']
    code = request.data['code']
    grant_type = 'authorization_code'
    post_fields = {
        'client_secret': settings.STRIPE_CLIENT_SECRET,
        'code': code,
        'grant_type': grant_type
    }
    post_fields = urlencode(post_fields).encode()

    url = settings.STRIPE_TOKEN_ENDPOINT

    url_request = Request(url, data=post_fields)
    res = json.loads(urlopen(url_request).read().decode())
    print(res)

    # Create StripeConnectedAccount and save to User
    user = User.objects.get(id=user_id)
    user.connect_stripe_account(
        stripe_user_id=res['stripe_user_id'],
        stripe_access_token=res['access_token'],
        stripe_publishable_key=res['stripe_publishable_key'],
        refresh_token=res['refresh_token'],
        scope=res['scope']
    )

    return Response({'response': 'You Are Now Connected With Stripe!', 'status': status.HTTP_200_OK})


@api_view(['POST'],)
def charge(request):
    amount_raw = request.data['amount']
    amount = int(float(amount_raw) * 100)
    creator_id = request.data['creatorId']
    source_token = request.data['source_token']

    connected_account = StripeConnectedUser.objects.get(user_id=creator_id)
    destination = connected_account.stripe_user_id

    fee = int(float(settings.STRIPE_PERCENTAGE_FEE) * amount) + int(settings.STRIPE_FIXED_FEE)
    payout_amount = amount - fee

    charge_request = stripe.Charge.create(
        amount=amount,  # amount in CENTS e.g 1000 = $10.00
        currency="usd",
        source=source_token,
        transfer_data={
            # amount in CENTS e.g 200 = $2.00 /// This is how we create our charge, NEED FEE CALCULATIONS
            "amount": payout_amount,
            "destination": destination,
        }
    )

    # Then give user their ticket
    # This function comes from tickets.API.views import purchase_ticket
    ticket_option = TicketOption.objects.get(id=request.data['ticket_option_id'])
    assigned_ticket = ticket_option.assign_ticket(user_id=request.data['user_id'], quantity=request.data['quantity'])
    serializer = TicketSerializer(assigned_ticket)
    return Response({'response': charge_request, 'ticket': serializer.data})


@api_view(['POST'],)
def save_card(request):
    token = request.data['source_token']
    user_id = request.data['user_id']
    user = User.objects.get(id=user_id)
    user_email = user.email

    # current_payment_method = StripeSavedPaymentMethod.objects.get(user_id=user_id)

    customer = stripe.Customer.create(
        source=token,
        email=user_email
    )

    StripeSavedPaymentMethod.objects.create(
        user=user,
        token=token,
        last4=customer['sources']['data'][0]['last4']  # get last4 from response
    )

    return Response({'response': customer})


class StripeConnectedUserViewSet(viewsets.ModelViewSet):
    serializer_class = StripeConnectedUserSerializer
    queryset = StripeConnectedUser.objects.all()


@api_view(['GET'])
def get_connected_user(request, user_id):
    # user_id = request.query_params.get('user_id')
    connected_user = StripeConnectedUser.objects.filter(user_id=user_id)
    serializer = StripeConnectedUserSerializer(connected_user, many=True)
    return Response({'connected_account': serializer.data})


class StripeSavedPaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = StripeSavedPaymentMethodSerializer
    queryset = StripeSavedPaymentMethod.objects.all()


@api_view(['GET'])
def get_payment_methods(request, user_id):
    # user_id = request.query_params.get('user_id')
    payment_methods = StripeSavedPaymentMethod.objects.filter(user_id=user_id)
    serializer = StripeSavedPaymentMethodSerializer(payment_methods, many=True)
    return Response({'payment_methods': serializer.data})

