from django.db import models
from user_authentication.models import UserAccount

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
    
class KhaltiInfo(models.Model):
    """
        pidx=ga6Zprq7XLRd5FXvRUmiRQ
        transaction_id=KigPyKyaqdXQwXLzUdBdeC
        tidx=KigPyKyaqdXQwXLzUdBdeC
        amount=1300
        total_amount=1300
        mobile=98XXXXX001
        status=Completed
        purchase_order_id=test123
        purchase_order_name=test123
    """
    pixd = models.CharField(max_length = 250)
    transaction_id= models.CharField(max_length = 250)
    tidx= models.CharField(max_length = 250)
    amount= models.IntegerField()
    total_amount=models.IntegerField()
    mobile=models.CharField(max_length = 50)
    status=models.CharField(max_length = 250)
    purchase_order_id=models.CharField(max_length = 250)
    purchase_order_name=models.CharField(max_length = 250)
    
    def __str__(self):
        return self.pixd