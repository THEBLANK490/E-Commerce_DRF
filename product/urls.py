from django.urls import path
from product.views import (CategoryView,ProductView,CategoryFilter,ReviewView,ProductFilter,
                           ProductSearchView,ProductListPaginationView)

app_name = "product"
urlpatterns = [
    path('category-view/',CategoryView.as_view()),
    path('category-view/<int:id>',CategoryView.as_view()),
    path('product-view/',ProductView.as_view()),
    path('product-view/<int:id>',ProductView.as_view()),
    path('product-filter/',CategoryFilter.as_view()),
    path('product-review/',ReviewView.as_view()),
    path('productlist-filter/',ProductFilter.as_view()),
    path('product-search/',ProductSearchView.as_view()),
    path('pagination-result/',ProductListPaginationView.as_view()),
    # path('verify-esewa/',VerifyEsewa.as_view())
]   