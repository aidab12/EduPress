from edu.api.company import AboutUsSerializer
from edu.api.courses import CourseCategorySerializer, CourseSerializer
from edu.models import AboutCompany, Course, CourseCategory
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class AboutUsListView(RetrieveAPIView):
    serializer_class = AboutUsSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (AllowAny,)

    def get_object(self):
        return AboutCompany.objects.filter(email__isnull=False).first()


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (AllowAny,)



class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = IsAuthenticatedOrReadOnly,


