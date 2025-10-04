from django.shortcuts import render

from rest_framework.generics import (CreateAPIView)
from rest_framework.permissions import (AllowAny)

from users.serializers import SingupSerializer

class SingupAPIView(CreateAPIView):
    serializer_class = SingupSerializer
    permission_classes = AllowAny,


