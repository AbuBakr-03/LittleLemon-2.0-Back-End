# LittleLemonApp/serializers.py
from rest_framework import serializers
from .models import Category, Menu, Booking
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuSerialzer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "title",
            "logo",
            "description",
            "price",
            "inventory",
            "category",
            "category_id",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = "admin" if self.user.is_superuser else "user"
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Get the refresh token and extract user info
        refresh = RefreshToken(attrs["refresh"])
        user_id = refresh.payload.get("user_id")

        if user_id:
            from django.contrib.auth import get_user_model

            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                data["role"] = "admin" if user.is_superuser else "user"
                print(
                    f"Custom refresh serializer: User {user.username}, Role: {data['role']}"
                )
            except User.DoesNotExist:
                data["role"] = "user"
        else:
            data["role"] = "user"

        return data
