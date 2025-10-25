import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer


class SendSmsCodeSerializer(Serializer):
    pass

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SendMailCodeSerializer(Serializer):
    email = CharField(default='abda@du.com')

    def validate_email(self, value):
        # Проверяем валидность email формата
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError('Enter a valid email address')

        local_part = value.split('@')[0]
        if len(local_part) < 3:
            raise ValidationError('Email local part must be at least 3 characters')

        return value

    def validate(self, attrs):
        email = attrs['email']
        user, created = User.objects.get_or_create(email=email)
        user.set_unusable_password()

        return super().validate(attrs)



class VerifyMailCodeSerializer(Serializer):
    email = CharField(default='abda@du.com')
    code = IntegerField(default=100000)