from rest_framework import serializers

from core.validators import category_name_validator
from product.models import Category, Product, Review
from user_authentication.serializers import UserAccount


class CategorySerializer(serializers.Serializer):
    """
    Serializer for category.

    Attributes:
        name (CharField): The name of the category.

    Methods:
        validate: Validates the uniqueness of the category name during creation.
        create: Creates a new category with the validated data.
        update: Updates an existing category with the validated data.
    """

    name = serializers.CharField(max_length=50, validators=[category_name_validator])

    def validate(self, attrs: dict) -> dict:
        """
        Validates the uniqueness of the category name during creation.

        Args:
            attrs (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If category already exists during creation.
        """
        if (
            Category.objects.filter(name=attrs.get("name")).exists()
            and self.context.get("request").method == "POST"
        ):
            raise serializers.ValidationError({"error": "Category already exists"})
        return attrs

    def create(self, validated_data: dict) -> Category:
        """
        Creates a new category with the validated data.

        Args:
            validated_data (dict): The validated data for category creation.

        Returns:
            Category: The newly created category.
        """
        return Category.objects.create(name=validated_data["name"])

    def update(self, instance: Category, validated_data: dict) -> Category:
        """
        Updates an existing category with the validated data.

        Args:
            instance (Category): The category instance to be updated.
            validated_data (dict): The validated data for category update.

        Returns:
            Category: The updated category.
        """
        instance.name = validated_data.get("name")
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    """
    Serializer for product.

    Attributes:
        category (PrimaryKeyRelatedField): The primary key related field for category.
        category_name (SerializerMethodField): A method field to get category name.
        name (CharField): The name of the product.
        price (DecimalField): The price of the product.
        description (CharField): The description of the product.
        product_image (ImageField): The image of the product.
        is_available (BooleanField): Indicates if the product is available.

    Methods:
        get_category_name: Retrieves the name of the category associated with the product.
        create: Creates a new product with the validated data.
        update: Updates an existing product with the validated data.
    """

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
        """
        Retrieves the name of the category associated with the product.

        Args:
            obj (Product): The product instance.

        Returns:
            str: The name of the category associated with the product.
        """
        return obj.category.name if obj.category else None

    def create(self, validated_data: dict) -> Product:
        """
        Creates a new product with the validated data.

        Args:
            validated_data (dict): The validated data for product creation.

        Returns:
            Product: The newly created product.
        """
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
        """
        Updates an existing product with the validated data.

        Args:
            instance (Product): The product instance to be updated.
            validated_data (dict): The validated data for product update.

        Returns:
            Product: The updated product.
        """
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
    """
    Serializer for review.

    Attributes:
        product_id (PrimaryKeyRelatedField): The primary key related field for product.
        product_name (SerializerMethodField): A method field to get product name.
        date_created (DateTimeField): The date and time when the review was created.
        description (CharField): The description of the review.
        user_id (PrimaryKeyRelatedField): The primary key related field for user.
        user_name (SerializerMethodField): A method field to get user name.

    Methods:
        get_product_name: Retrieves the name of the product associated with the review.
        get_user_name: Retrieves the name of the user associated with the review.
        create: Creates a new review with the validated data.
    """

    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(read_only=True)
    description = serializers.CharField(default="description")
    user_id = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    user_name = serializers.SerializerMethodField()

    def get_product_name(self, obj: Review) -> str:
        """
        Retrieves the name of the product associated with the review.

        Args:
            obj (Review): The review instance.

        Returns:
            str: The name of the product associated with the review.
        """
        return obj.product.name if obj.product else None

    def get_user_name(self, obj: Review) -> str:
        """
        Retrieves the name of the user associated with the review.

        Args:
            obj (Review): The review instance.

        Returns:
            str: The name of the user associated with the review.
        """
        return obj.user.first_name if obj.user else None

    def create(self, validated_data: dict) -> Review:
        """
        Creates a new review with the validated data.

        Args:
            validated_data (dict): The validated data for review creation.

        Returns:
            Review: The newly created review.
        """
        fields = {
            "product": validated_data["product_id"],
            "description": validated_data["description"],
            "user": validated_data["user_id"],
        }
        return Review.objects.create(**fields)
