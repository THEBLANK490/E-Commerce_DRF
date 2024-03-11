from django.contrib import admin
from product.models import Category,Product,Review

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','category','name','price','description','product_image','created']
    search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product','date_created','description','user']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Review,ReviewAdmin)
