from rest_framework.serializers import ModelSerializer
from apps.edu.models import CourseCategory, Course


class CourseCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'slug']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

