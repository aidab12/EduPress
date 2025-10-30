import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer


