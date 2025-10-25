from django.urls import path

from apps.edu.api.views import (AboutUsListView, CourseCategoryDetailView,
                                CourseCategoryListView, CourseCreateView,
                                CourseDetailView, CourseListView)

app_name = 'edu'

urlpatterns = [
    path('about-us/', AboutUsListView.as_view(), name='aboutus_list'),
    path('category/', CourseCategoryListView.as_view(), name='category_list'),
    path('category/<str:pk>/', CourseCategoryDetailView.as_view(), name='category_detail'),

    path('course/', CourseListView.as_view(), name='course_list'),
    path('course/<str:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/', CourseCreateView.as_view(), name='course_create'),
]
