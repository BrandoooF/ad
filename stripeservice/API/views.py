from rest_framework import viewsets, status
from accounts.models import User
from ..models import StripeConnectedUser
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
            "amount": payout_amount,  # amount in CENTS e.g 200 = $2.00 /// This is how we create our charge, NEED FEE CALCULATIONS
            "destination": destination,
        }
    )

    return Response({'response': charge_request})
