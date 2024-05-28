from django.contrib import admin

from user_authentication.models import UserAccount


# Register your models here.
class UserAdminList(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name", "role"]


admin.site.register(UserAccount, UserAdminList)
