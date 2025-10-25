from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView

from edu.api.company import AboutUsSerializer
from edu.api.courses import CourseCategorySerializer, CourseSerializer
from edu.models import AboutCompany, Course, CourseCategory


class CourseCategoryListView(ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class CourseCategoryDetailView(RetrieveAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class AboutUsListView(RetrieveAPIView):
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutCompany.objects.filter(email__isnull=False).first()


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

