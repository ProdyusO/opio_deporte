"""Administration's model module."""
from django.contrib import admin
from .models import CartProduct, Category, Customer, Product  # pylint: disable=E0402


class ProductCartAdmin(admin.ModelAdmin):
    """Item's controller."""

    list_display = (
        "customer",
        "product",
        "price",
        "quantity",
        "total",
        "in_order",
        "done",
        "created",
    )


class CustomerAdmin(admin.ModelAdmin):
    """Customer's controller."""

    list_display = (
        "name",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "comment",
        "created",
    )


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CartProduct, ProductCartAdmin)
