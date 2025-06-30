from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("LittleLemonApp.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", TokenBlacklistView.as_view(), name="jwt_blacklist"),
]
