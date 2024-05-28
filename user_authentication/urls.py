from django.urls import path

from user_authentication.views import (
    Login,
    Logout,
    Password_Changer,
    Register,
    ViewProfile,
)

app_name = "user_auth"
urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("user-profile/<int:id>", ViewProfile.as_view()),
    path("password-changer/<int:id>", Password_Changer.as_view()),
]
