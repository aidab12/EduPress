from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from apps.edu.api.company import AboutUsSerializer
from apps.edu.api.courses import CourseCategorySerializer, CourseSerializer
from apps.edu.models import CourseCategory, AboutCompany, Course


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


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreateView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer