from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, ModelSerializer


class SendSmsCodeSerializer(Serializer):
    pass

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'