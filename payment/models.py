from django.db import models

from user_authentication.models import UserAccount


# Create your models here.
class KhaltiInfo(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user")
    pixd = models.CharField(max_length=250)
    transaction_id = models.CharField(max_length=250)
    total_amount = models.IntegerField()
    mobile = models.CharField(max_length=50)
    status = models.CharField(max_length=250)
    user_email = models.EmailField()
    data = models.DateTimeField(auto_now_add=True)
    purchase_order_id = models.CharField(max_length=100)
    purchase_order_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.pixd
