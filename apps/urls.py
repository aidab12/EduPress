from django.urls import include, path

urlpatterns = [
    path('', include('edu.api.urls', namespace='courses'), name='courses'),
    path('', include('user.urls', namespace='users'), name='users'),
]
