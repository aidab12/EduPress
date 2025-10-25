from django.urls import path

from edu.api.views import (AboutUsListView, CourseCategoryDetailView,
                           CourseCategoryListView, CourseDetailView, CourseListCreateAPIView)

app_name = 'edu'

urlpatterns = [
    path('about-us/', AboutUsListView.as_view(), name='aboutus_list'),
    path('category/', CourseCategoryListView.as_view(), name='category_list'),
    path('category/<str:pk>/', CourseCategoryDetailView.as_view(), name='category_detail'),

    path('courses/', CourseListCreateAPIView.as_view(), name='course_list'),
    path('courses/<str:pk>/', CourseDetailView.as_view(), name='course_detail'),
]
