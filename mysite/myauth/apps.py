"""
Module that configures the authentication and authorization using Django.

"""

from django.apps import AppConfig


class MyauthConfig(AppConfig):
    """
    Configuration class for the 'myauth' application.

    This class is used to configure the 'myauth' app, which may include
    settings related to authentication, user management, and permissions.

    Attributes:
        default_auto_field (str): The default type of auto-generated primary keys
                                   for models in this app.
        name (str): The name of the application, which is 'myauth'.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "myauth"
