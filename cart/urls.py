from django.urls import path

from cart.views import (
    CartItemView,
    CartView,
    Checkout,
    CartDeleteView,
    CartItemsUpdateDeleteView,
)

app_name = "cart"
urlpatterns = [
    path("cart-view/", CartView.as_view()),
    path("cart-delete-view/<int:id>/", CartDeleteView.as_view()),
    path("cart-items/", CartItemView.as_view()),
    path("cart-items/<int:id>/", CartItemsUpdateDeleteView.as_view()),
    path("checkout-view/", Checkout.as_view()),
]
