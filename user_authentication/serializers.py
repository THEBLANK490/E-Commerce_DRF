from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
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
    """
    Serializer for user registration.

    Attributes:
        email (EmailField): The email address of the user.
        password (CharField): The password for the user account.
        password2 (CharField): Confirmation of the password.
        photo (ImageField): The profile photo of the user (optional).
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        phone_number (CharField): The phone number of the user.
        gender (ChoiceField): The gender of the user.
        address (CharField): The address of the user.

    Methods:
        validate: Validates the data, ensuring password fields match.
        create: Creates a new user account with the validated data.
    """

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
        """
        Validates the data, ensuring password fields match.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If password fields don't match.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error": "Password Fields don't match"})
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> UserAccount:
        """
        Creates a new user account with the validated data.

        Args:
            validated_data (dict): The validated data for user creation.

        Returns:
            UserAccount: The newly created user account.
        """
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
    """
    Serializer for user login.

    Attributes:
        email (EmailField): The email address of the user (required).
        password (CharField): The password for the user account (required).

    Methods:
        validate: Validates the email and password, authenticating the user.
    """

    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data: dict) -> dict:
        """
        Validates the email and password, authenticating the user.

        Args:
            data (dict): The data containing email and password.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If authentication fails.
        """
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
    """
    Serializer for user logout.

    Attributes:
        refresh (CharField): The refresh token used for logout.

    Methods:
        save: Blacklists the provided refresh token.
    """

    refresh = serializers.CharField()

    def save(self) -> RefreshToken:
        """
        Blacklists the provided refresh token.

        Returns:
            RefreshToken: The blacklisted refresh token.
        """
        Refresh_token = self.validated_data["refresh"]
        refresh_token = RefreshToken(Refresh_token)
        refresh_token.blacklist()
        return refresh_token


class ProfileSerializer(serializers.Serializer):
    """
    Serializer for user profile.

    Attributes:
        email (EmailField): The email address of the user.
        photo (FileField): The profile photo of the user (optional).
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        phone_number (CharField): The phone number of the user.
        address (CharField): The address of the user.

    Methods:
        update: Updates the user profile with the validated data.
    """

    email = serializers.EmailField(max_length=255, read_only=True)
    photo = serializers.FileField(required=False)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(
        max_length=150,
        validators=[phone_number_validator, phone_number_unique_validator],
    )
    address = serializers.CharField(max_length=255)

    def update(self, instance: UserAccount, validated_data: dict) -> UserAccount:
        """
        Updates the user profile with the validated data.

        Args:
            instance (UserAccount): The user account instance to be updated.
            validated_data (dict): The validated data for user profile update.

        Returns:
            UserAccount: The updated user account.
        """
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
    """
    Serializer for changing user password.

    Attributes:
        password (CharField): The new password for the user account.
        password2 (CharField): Confirmation of the new password.

    Methods:
        validate: Validates that the new password fields match.
        update: Updates the user account password with the new password.
    """

    password = serializers.CharField(
        max_length=128, write_only=True, required=True, validators=[password_validator]
    )
    password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data: dict) -> dict:
        """
        Validates that the new password fields match.

        Args:
            data (dict): The data containing new password fields.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If password fields don't match.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"error": "Password Fields don't match"})
        return data

    def update(self, instance: UserAccount, validated_data: dict) -> UserAccount:
        """
        Updates the user account password with the new password.

        Args:
            instance (UserAccount): The user account instance to be updated.
            validated_data (dict): The validated data containing the new password.

        Returns:
            UserAccount: The updated user account.
        """
        instance.password = make_password(
            validated_data.get("password", instance.password)
        )
        instance.save()
        return instance
