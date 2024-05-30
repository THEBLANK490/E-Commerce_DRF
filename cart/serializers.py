from rest_framework import serializers

from cart.models import Cart, CartItems
from product.models import Product


class CartSerializer(serializers.Serializer):
    """
    Serializer for cart.

    Methods:
        create: Creates a new Cart instance with the validated data.
    """

    def create(self, validated_data: dict) -> Cart:
        """
        Creates a new Cart instance with the validated data.

        Args:
            validated_data (dict): The validated data for Cart creation.

        Returns:
            Cart: The newly created Cart instance.
        """
        cart_instance = Cart.objects.create(**validated_data)
        return cart_instance


class CartItemSerializer(serializers.Serializer):
    """
    Serializer for cart item.

    Attributes:
        product (CharField): The name of the product associated with the cart item.
        quantity (IntegerField): The quantity of the product in the cart item.

    Methods:
        validate_product: Validates the product name provided.
        create: Creates a new CartItems instance with the validated data.
        update: Updates an existing CartItems instance with the validated data.
    """

    # product = serializers.CharField(source="cart_items_product.name")
    product = serializers.CharField(source="product.name")
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItems
        fields = ["id", "cart", "user", "product", "price", "quantity", "total_price"]
        read_only_fields = ["cart", "price", "total_price", "user"]

    def validate_product(self, value: str) -> str:
        """
        Validates the product name provided.

        Args:
            value (str): The product name to validate.

        Returns:
            str: The validated product name.

        Raises:
            serializers.ValidationError: If the provided product name is not valid.
        """
        if Product.objects.filter(name=value).exists():
            return value
        raise serializers.ValidationError("Provide a valid product name")

    def create(self, validated_data: dict) -> CartItems:
        """
        Creates a new CartItems instance with the validated data.

        Args:
            validated_data (dict): The validated data for CartItems creation.

        Returns:
            CartItems: The newly created CartItems instance.
        """
        request = self.context["request"]
        product = Product.objects.filter(
            name=validated_data.get("product")["name"]
        ).first()
        cart = Cart.objects.filter(user=request.user).first()
        fields = {
            "cart": cart,
            "user": request.user,
            "product": product,
            "price": product.price,
            "quantity": validated_data.get("quantity"),
            "total_price": product.price * validated_data.get("quantity"),
        }
        cart_item = CartItems.objects.create(**fields)
        cart_item.save()
        return cart_item

    def update(self, instance: CartItems, validated_data: dict) -> CartItems:
        """
        Updates an existing CartItems instance with the validated data.

        Args:
            instance (CartItems): The CartItems instance to be updated.
            validated_data (dict): The validated data for CartItems update.

        Returns:
            CartItems: The updated CartItems instance.
        """
        product_name = validated_data.get("product")["name"]
        product = Product.objects.filter(name=product_name).first()
        instance.product = product
        instance.quantity = validated_data.get("quantity")
        instance.save()
        return instance


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer for checkout.

    Attributes:
        cart (PrimaryKeyRelatedField): The primary key related field for cart.
        user (CharField): The email of the user.
        product (CharField): The name of the product.
        price (FloatField): The price.
        quantity (IntegerField): The quantity.
        total_price (FloatField): The total price.
    """

    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    user = serializers.CharField(source="user.email")
    product = serializers.CharField(source="product.name")
    price = serializers.FloatField(default=0)
    quantity = serializers.IntegerField(default=1)
    total_price = serializers.FloatField(default=0)
