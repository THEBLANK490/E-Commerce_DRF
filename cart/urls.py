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
    path("cart-get-post/", CartView.as_view()),
    path("cart-delete/<int:id>/", CartDeleteView.as_view()),
    path("cart-items-get-post/", CartItemView.as_view()),
    path("cart-items-patch-delete/<int:id>/", CartItemsUpdateDeleteView.as_view()),
    path("checkout/", Checkout.as_view()),
]
