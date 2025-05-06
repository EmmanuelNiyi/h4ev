import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()
logger = logging.getLogger("accounts")


def create_user_account(serializer):
    """Handles the core logic of user creation"""
    validated_data = serializer.validated_data

    password = validated_data.get("password")
    validated_data["password"] = make_password(password)  # Hash the password

    try:
        user = User.objects.create(**validated_data)

        return user
    except Exception as e:
        raise ValidationError(e)
