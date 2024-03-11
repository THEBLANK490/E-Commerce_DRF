from django.urls import path
from cart.views import CartView,Checkout

app_name = "cart"
urlpatterns = [
    path('cart-view/',CartView.as_view()),
    path('checkout-view/',Checkout.as_view())
]