from rest_framework import serializers

from product.models import Category


def name_validator(name: str) -> None:
    if Category.objects.filter(name=name).exists():
        raise serializers.ValidationError({"error": "Category already exists"})
