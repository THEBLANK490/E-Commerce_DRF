from rest_framework import serializers

from product.models import Category


def name_validator(name: str) -> None:
    """
    Validates if a category name already exists.

    Args:
        name (str): The category name to validate.

    Raises:
        serializers.ValidationError: If the category name already exists.
    """
    if Category.objects.filter(name=name).exists():
        raise serializers.ValidationError({"error": "Category already exists"})
