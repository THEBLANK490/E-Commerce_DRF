import datetime

from django.db import models

from product.models import Product
from user_authentication.models import UserAccount


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)

    def __str__(self) -> str:
        return str(self.user.email)


class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items_cart"
    )
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="cart_items_user"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items_product"
    )
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"Item {self.product.name} in cart for {self.user.first_name}"
