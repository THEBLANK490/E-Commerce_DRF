from rest_framework import serializers
from cart.models import Cart,CartItems
from user_authentication.models import UserAccount
from product.models import Product
import datetime


class CartSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    status = serializers.BooleanField(default=False)
    total_price = serializers.FloatField(default=0)
    date = serializers.DateField(default = datetime.date.today)
    

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.FloatField(default = 0)
    quantity = serializers.IntegerField(default=1)
    