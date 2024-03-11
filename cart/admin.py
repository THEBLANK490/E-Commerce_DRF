from django.contrib import admin
from cart.models import Cart,CartItems

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','status','total_price','date']
    search_fields = ['user']


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['cart','user','product','price','quantity']
    search_fields = ['user']

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems,CartItemsAdmin)