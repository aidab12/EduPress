from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from root.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('api/v1/', include('main.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api-token-auth/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),

path('account/', include('main.urls')),
path('users/', include('users.urls', namespace='users')),
path("i18n/", include("django.conf.urls.i18n")),

) + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)
