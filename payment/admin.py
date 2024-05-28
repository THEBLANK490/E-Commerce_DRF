from django.contrib import admin

from payment.models import KhaltiInfo


# Register your models here.
class KhaltiInfoAdmin(admin.ModelAdmin):
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
