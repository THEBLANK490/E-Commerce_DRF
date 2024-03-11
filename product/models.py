from django.db import models
from user_authentication.models import UserAccount
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True,max_length=50)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250, default='', blank=True, null=True)    
    product_image = models.ImageField(upload_to='uploads/products/')
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    user = models.ForeignKey(UserAccount,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.description