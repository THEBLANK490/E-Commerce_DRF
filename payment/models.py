from django.db import models

from user_authentication.models import UserAccount


# Create your models here.
class KhaltiInfo(models.Model):
    """
    Model representing Khalti payment information.

    Attributes:
        user (UserAccount): The user associated with the payment (ForeignKey relationship).
        pixd (str): The PIXD associated with the transaction.
        transaction_id (str): The unique transaction ID.
        total_amount (int): The total amount of the transaction.
        mobile (str): The mobile number associated with the transaction.
        status (str): The status of the transaction.
        user_email (str): The email address of the user.
        data (DateTimeField): The date and time when the transaction data was created.
        purchase_order_id (str): The ID of the purchase order.
        purchase_order_name (str): The name of the purchase order.

    Methods:
        __str__: Returns a string representation of the PIXD associated with the transaction.
    """

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
