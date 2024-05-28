import re

from rest_framework import serializers

from product.models import Category
from user_authentication.models import UserAccount


def phone_number_validator(phone):
    """
    Validator function to check if the phone number is in valid format.

    Args:
        phone (str): The phone number to be validated.

    Raises:
        serializers.ValidationError: If the phone number is invalid.
    """
    pattern = r"^9[0-9]{9}$"
    match = re.match(pattern, phone)
    if match is None:
        raise serializers.ValidationError({"phone": "Enter a valid phone number"})


def phone_number_unique_validator(phone):
    """
    Validator function to check if the phone number is unique.

    Args:
        phone (str): The phone number to be validated.

    Raises:
        serializers.ValidationError: If the phone number is not unique.
    """
    qs = UserAccount.objects.filter(phone_number=phone)
    if qs:
        raise serializers.ValidationError({"phone": "Phone number must be unique"})


def password_validator(data):
    """
    Validator function to check if the password length is greater than 5.

    Args:
        data (str): The password to be validated.

    Raises:
        serializers.ValidationError: If the password length is less than 5.
    """
    if len(data) < 5:
        raise serializers.ValidationError({"password": "Password length less than 5"})


def address_validator(data):
    """
    Validator function to check if the address length is greater than 5.

    Args:
        data (str): The address to be validated.

    Raises:
        serializers.ValidationError: If the address length is less than 5.
    """
    if len(data) < 5:
        raise serializers.ValidationError({"address": "Address length less than 5"})


def category_name_validator(name):
    """
    Validator function to check if the category name already exists.

    Args:
        name (str): The name of the category to be validated.

    Raises:
        serializers.ValidationError: If the category name already exists.
    """
    if Category.objects.filter(name=name).exists():
        raise serializers.ValidationError({"error": "Category already exists"})


def email_is_user_instance_validator(email):
    """
    Validator function to check if the email belongs to a registered user.

    Args:
        email (str): The email address to be validated.

    Raises:
        serializers.ValidationError: If the email does not belong to a registered user.
    """
    qs = UserAccount.objects.filter(email=email)
    if not qs:
        raise serializers.ValidationError({"email": "Email must be of registered user"})
