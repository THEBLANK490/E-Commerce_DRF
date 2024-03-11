from rest_framework import serializers
from product.models import Category

def name_validator(name):
    if Category.objects.filter(name=name).exists():
        raise serializers.ValidationError({"error":"Category already exists"})