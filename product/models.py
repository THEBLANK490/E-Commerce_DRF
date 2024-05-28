from django.db import models

from user_authentication.models import UserAccount


# Create your models here.
class Category(models.Model):
    """
    Model representing a category.

    Attributes:
        name (str): The name of the category (unique).

    Methods:
        __str__: Returns a string representation of the category name.
    """

    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        category (Category): The category to which the product belongs.
        name (str): The name of the product.
        price (Decimal): The price of the product.
        description (str): The description of the product (optional).
        product_image (ImageField): The image of the product.
        created (DateTimeField): The date and time when the product was created.
        modified_at (DateTimeField): The date and time when the product was last modified.
        is_available (bool): Indicates if the product is currently available.

    Methods:
        __str__: Returns a string representation of the product name.
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    product_image = models.ImageField(upload_to="uploads/products/")
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """
    Model representing a review for a product.

    Attributes:
        product (Product): The product being reviewed (ForeignKey relationship).
        date_created (DateTimeField): The date and time when the review was created.
        description (str): The description or content of the review.
        user (UserAccount): The user who created the review (ForeignKey relationship).

    Methods:
        __str__: Returns a string representation of the review description.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.description
