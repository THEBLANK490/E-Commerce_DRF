from django.urls import path

from admin_api.views import AccountRole, GetStatistics, UserListAdmin

app_name = "user_admin"
urlpatterns = [
    path("update-role/", AccountRole.as_view()),
    path("user-stats/", GetStatistics.as_view()),
    path("user-list/", UserListAdmin.as_view()),
]
