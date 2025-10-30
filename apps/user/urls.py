import djoser
from django.urls import include, path, re_path

from user.views import ChangePasswordView, LoginAPIView, SignUpAPIView

from apps.user.views import VerifyCodeAPIView, SendCodeAPIView

app_name = 'user'

urlpatterns = [
    path('singup/', SignUpAPIView.as_view(), name='signup_api_view'),
    path('send-code/', SendCodeAPIView.as_view(), name='send_code_api_view'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify_api_view'),
    path('login/', LoginAPIView.as_view(), name='login_api_view'),
    # path('change-passwd/', ChangePasswordView.as_view(), name='change_passwd_api_view'),
    # re_path(r'^auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.jwt')),
]
