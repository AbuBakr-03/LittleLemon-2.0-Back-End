# LittleLemon/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from LittleLemonApp.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    logout_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("LittleLemonApp.urls")),
    path("auth/", include("djoser.urls")),
    # Custom JWT endpoints with HttpOnly cookie support
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt_create"),
    path("auth/jwt/refresh/", CustomTokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("auth/logout/", logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
