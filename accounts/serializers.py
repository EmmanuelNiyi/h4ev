from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        # extra_kwargs = {'password': {'write_only': True}}


# class UserReadSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["last_name"]


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "is_staff", "user_permissions"]
