from django.urls import path

from product.views import (
    Category_get_post_view,
    CategoryIndividualView,
    Product_get_view,
    Product_post_view,
    ProductIndividualView,
    ProductFilter,
    ProductListPaginationView,
    ProductSearchView,
    ReviewView,
    CategoryFilter,
)

app_name = "product"
urlpatterns = [
    path("category-individual-view/<int:id>", CategoryIndividualView.as_view()),
    path("category-view/", Category_get_post_view.as_view()),
    path("product-individual-view/<int:id>", ProductIndividualView.as_view()),
    path("product-get-view/", Product_get_view.as_view()),
    path("product-post-view/", Product_post_view.as_view()),
    path("product-filter/", CategoryFilter.as_view()),
    path("product-review/", ReviewView.as_view()),
    path("product-list-filter/", ProductFilter.as_view()),
    path("product-search/", ProductSearchView.as_view()),
    path("pagination-result/", ProductListPaginationView.as_view()),
]
