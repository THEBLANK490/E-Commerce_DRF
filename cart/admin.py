from django.contrib import admin

from cart.models import Cart, CartItems


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "date"]
    search_fields = ["user"]


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "user", "product", "price", "quantity", "total_price"]
    search_fields = ["user"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)
