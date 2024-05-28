from django.contrib import admin

from product.models import Category, Product, Review


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = [
        "id",
        "category",
        "name",
        "price",
        "description",
        "product_image",
        "created",
        "modified_at",
        "is_available",
    ]
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = ["id", "name"]
    search_fields = ["name"]


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = ["product", "date_created", "description", "user"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
