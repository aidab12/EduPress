from django.urls import path

from users.views import (SingupAPIView)
from rest_framework.authtoken.views import (obtain_auth_token,)


app_name = 'users'

urlpatterns = [
    path('singup/', SingupAPIView.as_view(), name='singup_api_view'),
    path('login/', obtain_auth_token, name='login_api_view'),
]