from django.contrib import admin

from user_authentication.models import UserAccount


# Register your models here.
class UserAdminList(admin.ModelAdmin):
    """
    Admin configuration for UserAccount model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
        search_fields (list): The fields to enable searching in the admin list view.
    """

    list_display = ["id", "email", "first_name", "last_name", "role"]


admin.site.register(UserAccount, UserAdminList)
