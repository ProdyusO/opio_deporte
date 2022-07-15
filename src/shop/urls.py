"""Url's module."""
# pylint: disable=E0402
from django.urls import path
from .views import (
    index,
    category_detail_view,
    product_detail_view,
    cart_product_view,
    cart_view,
    change_quantity,
    delete_cart_product,
)

urlpatterns = [
    path("", index, name="index"),
    path("cart/", cart_view, name="cart"),
    path("category/<int:category_id>/", category_detail_view, name="category_detail"),
    path("product/<int:pk>/", product_detail_view, name="product_detail"),
    path("add_to_cart/<int:pk>/", cart_product_view, name="add_to_cart"),
    path("quantity/<int:pk>/", change_quantity, name="quantity"),
    path("delete/<int:pk>/", delete_cart_product, name="delete"),
]
