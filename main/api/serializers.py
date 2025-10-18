from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer, ModelSerializer


class SendSmsCodeSerializer(Serializer):
    pass

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SendMailCodeSerializer(Serializer):
    phone = CharField(default='971884040')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'phone'


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='971884040')
    code = IntegerField(default=100000)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        self.user = authenticate(phone=attrs['phone'], request=self.context['request'])

        if self.user is None:
            raise ValidationError(self.default_error_messages['no_active_account'])

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': "OK",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)