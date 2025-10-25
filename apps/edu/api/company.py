from rest_framework.serializers import ModelSerializer

from edu.models import AboutCompany


class AboutUsSerializer(ModelSerializer):
    class Meta:
        model = AboutCompany
        fields = (
            'title',
            'text',
            'email',
            'phone1',
            'address',
            'location',
        )