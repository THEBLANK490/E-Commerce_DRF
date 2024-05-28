import datetime

from django.db import models

from product.models import Product
from user_authentication.models import UserAccount


# Create your models here.
class Cart(models.Model):
    """
    Model representing a user's shopping cart.

    Attributes:
        user (UserAccount): The user to whom the cart belongs (One-to-One relationship).
        status (bool): The status of the cart, indicating if it's active or not.
        date (DateField): The date when the cart was created.

    Methods:
        __str__: Returns a string representation of the cart, showing the user's email.
    """

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)

    def __str__(self) -> str:
        return str(self.user.email)


class CartItems(models.Model):
    """
    Model representing items added to a user's shopping cart.

    Attributes:
        cart (Cart): The cart to which the item belongs.
        user (UserAccount): The user who added the item to the cart.
        product (Product): The product added to the cart.
        price (float): The price of the product.
        quantity (int): The quantity of the product added to the cart.
        total_price (float): The total price of all units of the product in the cart.

    Methods:
        __str__: Returns a string representation of the cart item.
    """

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
