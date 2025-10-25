from rest_framework.serializers import ModelSerializer

from edu.models import Course, CourseCategory


class CourseCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

