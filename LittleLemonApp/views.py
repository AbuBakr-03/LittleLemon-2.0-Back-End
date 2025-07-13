# LittleLemonApp/views.py - Debug Version
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Menu, Booking, Category
from .serializers import (
    MenuSerialzer,
    BookingSerializer,
    CategorySerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


# Your existing views...
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerialzer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class SingleMenuView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerialzer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["date"]


class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


# Debug Authentication Views
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            token = response.data
            # Create response with only access token (no refresh token in response body)
            response_data = {"access": token["access"], "role": token["role"]}
            # Set refresh token in HttpOnly cookie
            new_response = Response(response_data, status=status.HTTP_200_OK)
            cookie_max_age = int(
                settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
            )
            new_response.set_cookie(
                "refresh_token",
                token["refresh"],
                max_age=cookie_max_age,
                httponly=True,
                secure=not settings.DEBUG,  # Use secure cookies in production
                samesite="Lax",
            )
            return new_response
        else:
            print(f"LOGIN: Failed with status {response.status_code}: {response.data}")
        return response


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    def post(self, request, *args, **kwargs):
        # Get refresh token from HttpOnly cookie
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookies"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Add refresh token to request data
        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            token_data = response.data
            # If rotation is enabled, we get a new refresh token
            if "refresh" in token_data:
                # Update the refresh token cookie
                response.set_cookie(
                    "refresh_token",
                    token_data["refresh"],
                    max_age=settings.SIMPLE_JWT[
                        "REFRESH_TOKEN_LIFETIME"
                    ].total_seconds(),
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite="Lax",
                )
                # Remove refresh token from response body
                del token_data["refresh"]
        else:
            print(
                f"REFRESH: Failed with status {response.status_code}: {response.data}"
            )

        return response


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    """Clear the refresh token cookie"""
    response = Response(
        {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
    )
    response.delete_cookie("refresh_token")
    return response
