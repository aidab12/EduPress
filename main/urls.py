from django.urls import path
from . import views
from main.views import SendCodeAPIView, LoginAPIView

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code_email'),
    path('auth/verify-code', LoginAPIView.as_view(), name='verify_code'),
    path('login/', views.user_login, name='login'),
]
