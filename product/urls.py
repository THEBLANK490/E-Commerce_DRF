from django.urls import path
from product.views import CategoryView,ProductView,ProductFilter,ReviewView

app_name = "product"
urlpatterns = [
    path('category-view/',CategoryView.as_view()),
    path('category-view/<int:id>',CategoryView.as_view()),
    path('product-view/',ProductView.as_view()),
    path('product-view/<int:id>',ProductView.as_view()),
    path('product-filter/',ProductFilter.as_view()),
    path('product-review/',ReviewView.as_view()),
]