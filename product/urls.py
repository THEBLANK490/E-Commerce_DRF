from django.urls import path

from product.views import (
    Category_all_view,
    CategoryFilter,
    CategoryView,
    Product_all_view,
    ProductFilter,
    ProductListPaginationView,
    ProductSearchView,
    ProductView,
    ReviewView,
)

app_name = "product"
urlpatterns = [
    path("category-crud-view/", CategoryView.as_view()),
    path("category-all-view", Category_all_view.as_view()),
    path("product-view/", ProductView.as_view()),
    path("product-all-view", Product_all_view.as_view()),
    path("product-filter/", CategoryFilter.as_view()),
    path("product-review/", ReviewView.as_view()),
    path("product-list-filter/", ProductFilter.as_view()),
    path("product-search/", ProductSearchView.as_view()),
    path("pagination-result/", ProductListPaginationView.as_view()),
]
