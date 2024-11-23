from django.apps import AppConfig


class RequestdataappConfig(AppConfig):
    """
    Configuration class for the 'requestdataapp' Django application.

    This class defines the configuration for the Django app named 'requestdataapp'.
    It sets the default primary key field type to 'BigAutoField' for models in this app.

    Attributes:
        default_auto_field: The default type of primary key to use for models in this app.
        name: The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "requestdataapp"
