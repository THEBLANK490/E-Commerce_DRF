from rest_framework import serializers

from cart.models import Cart, CartItems
from product.models import Product


class CartSerializer(serializers.Serializer):
    def create(self, validated_data: dict) -> Cart:
        cart_instance = Cart.objects.create(**validated_data)
        return cart_instance


class CartItemSerializer(serializers.Serializer):
    product = serializers.CharField(source="cart_items_product.name")
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItems
        fields = ["id", "cart", "user", "product", "price", "quantity", "total_price"]
        read_only_fields = ["cart", "price", "total_price", "user"]

    def validate_product(self, value: str) -> str:
        if Product.objects.filter(name=value).exists():
            return value
        raise serializers.ValidationError("Provide a valid product name")

    def create(self, validated_data: dict) -> CartItems:
        request = self.context["request"]
        product = Product.objects.filter(
            name=validated_data.get("cart_items_product")["name"]
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
        product_name = validated_data.get("cart_items_product")["name"]
        product = Product.objects.filter(name=product_name).first()
        instance.product = product
        instance.quantity = validated_data.get("quantity")
        instance.save()
        return instance


class CheckoutSerializer(serializers.Serializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    user = serializers.CharField(source="user.email")
    product = serializers.CharField(source="product.name")
    price = serializers.FloatField(default=0)
    quantity = serializers.IntegerField(default=1)
    total_price = serializers.FloatField(default=0)
