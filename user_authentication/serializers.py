from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from core.validators import (
    address_validator,
    password_validator,
    phone_number_unique_validator,
    phone_number_validator,
)
from user_authentication.models import Gender, UserAccount


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=255,
        required=True,
        validators=[UniqueValidator(queryset=UserAccount.objects.all())],
    )
    password = serializers.CharField(
        max_length=128, write_only=True, required=True, validators=[password_validator]
    )
    password2 = serializers.CharField(max_length=128, write_only=True, required=True)
    photo = serializers.ImageField(required=False, allow_empty_file=True, use_url=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(
        max_length=15,
        validators=[phone_number_validator, phone_number_unique_validator],
    )
    gender = serializers.ChoiceField(choices=Gender.choices)
    address = serializers.CharField(max_length=255, validators=[address_validator])

    class Meta:
        model = UserAccount
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "gender",
            "password",
            "address",
            "photo",
        ]

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error": "Password Fields don't match"})
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> UserAccount:
        fields = {
            "email": validated_data["email"],
            "first_name": validated_data["first_name"],
            "last_name": validated_data["last_name"],
            "phone_number": validated_data["phone_number"],
            "gender": validated_data["gender"],
            "password": validated_data["password"],
            "address": validated_data["address"],
        }
        user = UserAccount.objects.create_user(**fields)
        photo = validated_data.get("photo")
        if photo:
            user.photo = photo
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data: dict) -> dict:
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self) -> RefreshToken:
        Refresh_token = self.validated_data["refresh"]
        refresh_token = RefreshToken(Refresh_token)
        refresh_token.blacklist()
        return refresh_token


class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    photo = serializers.FileField(required=False)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(
        max_length=150,
        validators=[phone_number_validator, phone_number_unique_validator],
    )
    address = serializers.CharField(max_length=255)

    def update(self, instance: UserAccount, validated_data: dict) -> UserAccount:
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.address = validated_data.get("address", instance.address)
        if instance.photo:
            instance.photo = validated_data.get("photo", instance.photo)
        instance.save()
        return instance


class Password_Changer_Serializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128, write_only=True, required=True, validators=[password_validator]
    )
    password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error": "Password Fields don't match"})
        return data

    def update(self, instance: UserAccount, validated_data: dict) -> UserAccount:
        instance.password = make_password(
            validated_data.get("password", instance.password)
        )
        instance.save()
        return instance
