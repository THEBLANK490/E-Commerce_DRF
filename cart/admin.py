from django.contrib import admin

from cart.models import Cart, CartItems


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for Cart model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = ["id", "user", "status", "date"]
    search_fields = ["user"]


class CartItemsAdmin(admin.ModelAdmin):
    """
    Admin configuration for CartItems model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = ["id", "cart", "user", "product", "price", "quantity", "total_price"]
    search_fields = ["user"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
