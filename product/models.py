from django.db import models
from user_authentication.models import UserAccount
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length = 250)
    price = models.CharField(max_length=250)
    description = models.CharField(max_length=250, default='', blank=True, null=True)    
    product_image = models.FileField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Order(models.Model):
    user_id = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
