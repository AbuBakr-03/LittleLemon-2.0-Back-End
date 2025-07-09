from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from django.conf.urls.static import static
from LittleLemonApp.views import CustomTokenObtainPairView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("LittleLemonApp.urls")),
    path("auth/", include("djoser.urls")),
    # DON'T include djoser JWT urls since we're overriding them
    # path("auth/", include("djoser.urls.jwt")),
    # Custom JWT endpoints
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt_create"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="jwt_blacklist"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
