from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.generics import (CreateAPIView)
from rest_framework.permissions import (AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import SignUpSerializer, LoginSerializer


class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = AllowAny,


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
