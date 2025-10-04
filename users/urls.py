from django.urls import path

from users.views import SignUpAPIView, LoginAPIView

app_name = 'users'

urlpatterns = [
    path('singup/', SignUpAPIView.as_view(), name='signup_api_view'),
    path('login/', LoginAPIView.as_view(), name='login_api_view'),
]
