"""App's setting's module."""
from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Shop's app settings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"
    verbose_name = "OPIO-DEPORTE"
