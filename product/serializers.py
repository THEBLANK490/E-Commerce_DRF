from rest_framework import serializers

from product.models import Category, Product, Review
from user_authentication.serializers import UserAccount


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def validate(self, attrs: dict) -> dict:
        if (
            Category.objects.filter(name=attrs.get("name")).exists()
            and self.context.get("request").method == "POST"
        ):
            raise serializers.ValidationError({"error": "Category already exists"})
        return attrs

    def create(self, validated_data: dict) -> Category:
        return Category.objects.create(name=validated_data["name"])

    def update(self, instance: Category, validated_data: dict) -> Category:
        instance.name = validated_data.get("name")
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # category = serializers.CharField(source ="category.name" )
    category_name = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=250)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=250, default="")
    product_image = serializers.ImageField()
    is_available = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "price",
            "description",
            "product_image",
            "is_available",
        ]

    def get_category_name(self, obj: Product) -> str:
        return obj.category.name if obj.category else None

    def create(self, validated_data: dict) -> Product:
        fields = {
            "category": validated_data["category"],
            "name": validated_data["name"],
            "price": validated_data["price"],
            "description": validated_data["description"],
            "product_image": validated_data["product_image"],
            "is_available": validated_data["is_available"],
        }
        return Product.objects.create(**fields)

    def update(self, instance: Product, validated_data: dict) -> Product:
        instance.category = validated_data.get("category", instance.category)
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        instance.product_image = validated_data.get(
            "product_image", instance.product_image
        )
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.save()
        return instance


class ReviewSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(read_only=True)
    description = serializers.CharField(default="description")
    user_id = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    user_name = serializers.SerializerMethodField()

    def get_product_name(self, obj: Review) -> str:
        return obj.product.name if obj.product else None

    def get_user_name(self, obj: Review) -> str:
        return obj.user.first_name if obj.user else None

    def create(self, validated_data: dict) -> Review:
        fields = {
            "product": validated_data["product_id"],
            "description": validated_data["description"],
            "user": validated_data["user_id"],
        }
        return Review.objects.create(**fields)
