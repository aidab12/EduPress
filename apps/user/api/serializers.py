import re
from typing import Any

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, EmailField
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework_simplejwt.tokens import Token, RefreshToken
from user.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(default='abda@example.com')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с такой почтой уже зарегестрирован.")

        if " " in email:
            raise serializers.ValidationError("Email не должен содержать пробелов.")

        return email

    # def validate_password(self, password):
    #     validate_password(password)
    #     return password

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        return {
            "user": {
                "id": instance.id,
                "email": instance.email,
                "username": instance.username,
            },
            "message": "Registration successful."
        }


class SendSmsCodeSerializer(Serializer):
    email = EmailField(default='abda@example.com')

    def validate(self, email):

        return email


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'email',


class VerifySmsCodeSerializer(Serializer):
    email = EmailField()
    code = IntegerField(default=1000)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials",
        "invalid_code": "Invalid verification code"
    }

    def validate(self, attrs: dict[str, Any]):
        try:
            self.user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise ValidationError(self.default_error_messages['no_active_account'])

        return attrs

    def activate_user(self):
        """Активирует пользователя после успешной верификации"""
        if not self.user.is_active:
            self.user.is_active = True
            self.user.save(update_fields=['is_active'])

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': "Account activated successfully",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label="Email", write_only=True)
    password = serializers.CharField(label="Password", write_only=True)
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password',)

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop('old_password')
        user.check_password(old_password)
        return super().validate(attrs)
