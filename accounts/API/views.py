from rest_framework import viewsets
from .serializers import UserSerializer, UserShortSerializer, UserProfileSerializer
from ..models import User, UserProfile

from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):

        #username = request.data['username']

        content = {
            'username': request.data['username'],
            'password': request.data['password'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'groups': {},
        }

        serializer = UserSerializer(data=content)

        if serializer.is_valid():
            user = User.objects.create_user(
                username=content['username'],
                password=content['password'],
                first_name=content['first_name'],
                last_name=content['last_name'],
                email=request.data['email'],
            )
            user.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)

        else:
            return Response(serializer.error_messages)


class UserShortViewSet(viewsets.ModelViewSet):
    serializer_class = UserShortSerializer
    queryset = User.objects.all()


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
