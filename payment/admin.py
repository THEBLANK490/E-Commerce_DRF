from django.contrib import admin

from payment.models import KhaltiInfo


# Register your models here.
class KhaltiInfoAdmin(admin.ModelAdmin):
    """
    Admin model configuration for KhaltiInfo.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = [
        "id",
        "user",
        "pixd",
        "transaction_id",
        "total_amount",
        "mobile",
        "status",
        "user_email",
        "data",
        "purchase_order_id",
        "purchase_order_name",
    ]
    search_fields = ["user"]


admin.site.register(KhaltiInfo, KhaltiInfoAdmin)
