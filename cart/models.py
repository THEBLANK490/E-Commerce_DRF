from django.db import models
from user_authentication.models import UserAccount
from product.models import Product
import datetime

# Create your models here. 
class Cart(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.total_price)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(default = 0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Item {self.product.name} in cart for {self.user.first_name}"
    

