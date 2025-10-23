from django.urls import path, include

from apps.user.views import SignUpAPIView, LoginAPIView, ChangePasswordView

app_name = 'user'
urlpatterns = [
    path('singup/', SignUpAPIView.as_view(), name='signup_api_view'),
    path('login/', LoginAPIView.as_view(), name='login_api_view'),
    path('change-passwd/', ChangePasswordView.as_view(), name='change_passwd_api_view'),
]
