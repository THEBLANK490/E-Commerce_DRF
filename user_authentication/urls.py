from django.urls import path
from user_authentication.views import Register,Login,Logout,ViewProfile

app_name = "user_auth"
urlpatterns = [
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),
    path('user-profile/',ViewProfile.as_view()),
    path('user-profile/<int:id>',ViewProfile.as_view()),
]