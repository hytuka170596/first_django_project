"""
Configuration file for the application Shopapp.
"""

from django.apps import AppConfig


class ShopappConfig(AppConfig):
    """Configuration for the shopapp application."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "shopapp"
