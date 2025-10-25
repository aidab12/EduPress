import djoser
from django.urls import include, path, re_path

from user.views import ChangePasswordView, LoginAPIView, SignUpAPIView

app_name = 'user'
urlpatterns = [
    # path('singup/', SignUpAPIView.as_view(), name='signup_api_view'),
    # path('login/', LoginAPIView.as_view(), name='login_api_view'),
    # path('change-passwd/', ChangePasswordView.as_view(), name='change_passwd_api_view'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
