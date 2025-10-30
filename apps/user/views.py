from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.api.serializers import (ChangePasswordSerializer,
                                  LoginSerializer, SignUpSerializer)

from apps.user.api.serializers import VerifySmsCodeSerializer, SendSmsCodeSerializer
from apps.user.tasks import custom_send_mail
from apps.user.utils import check_sms_code, random_code


@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Аутентификация/Авторизация']
    )
)
class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        email = serializer.data['email']
        code = random_code()
        custom_send_mail(email, code)

        return Response(
            serializer.to_representation(user),
            status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    post=extend_schema(
        summary='Отправка кода',
        tags=['Аутентификация/Авторизация']
    )
)
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        email = serializer.data['email']
        custom_send_mail(email, code)
        return Response({"message": "send sms code"})


@extend_schema_view(
    post=extend_schema(
        summary='Подтверждение почты',
        tags=['Аутентификация/Авторизация']
    )
)
class VerifyCodeAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(
            email=serializer.validated_data['email'],
            code=serializer.validated_data['code']
        )

        if not is_valid_code:
            return Response(
                {"message": "Invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.activate_user()

        return Response(serializer.get_data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary='Сброс пароля',
        tags=['Аутентификация/Авторизация'],
        request=ChangePasswordSerializer,
    )
)
class ChangePasswordView(APIView):
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid()
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
