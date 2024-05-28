import re

from rest_framework import serializers

from product.models import Category
from user_authentication.models import UserAccount


def phone_number_validator(phone):
    pattern = r"^9[0-9]{9}$"
    match = re.match(pattern, phone)
    if match is None:
        raise serializers.ValidationError({"phone": "Enter a valid phone number"})


def phone_number_unique_validator(phone):
    qs = UserAccount.objects.filter(phone_number=phone)
    if qs:
        raise serializers.ValidationError({"phone": "Phone number must be unique"})


def password_validator(data):
    if len(data) < 5:
        raise serializers.ValidationError({"password": "Password length less than 5"})


def address_validator(data):
    if len(data) < 5:
        raise serializers.ValidationError({"address": "Address length less than 5"})


def category_name_validator(name):
    if Category.objects.filter(name=name).exists():
        raise serializers.ValidationError({"error": "Category already exists"})


def email_is_user_instance_validator(email):
    qs = UserAccount.objects.filter(email=email)
    if not qs:
        raise serializers.ValidationError({"email": "Email must be of registered user"})
