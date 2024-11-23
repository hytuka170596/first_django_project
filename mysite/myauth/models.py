"""
Module containing the model classes Profile
"""

from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    TextField,
    BooleanField,
    DateTimeField,
    CharField,
    ImageField,
    EmailField,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def avatar_for_user_directory_path(instance: "User", filename: str) -> str:
    """
    Generate a file path for storing user avatars.

    Args:
        instance (User): The user instance for whom the avatar is being uploaded.
        filename (str): The name of the uploaded file.

    Returns:
        str: The file path where the avatar will be stored.
    """
    return "accounts/{user_pk}/avatar/{filename}".format(
        user_pk=instance.pk, filename=filename
    )


class Profile(models.Model):
    """
    A model representing a user's profile in the application.

    This model extends the default User model with additional fields
    such as bio, agreement acceptance, creation timestamp, and avatar.
    It establishes a one-to-one relationship with the User model.

    Attributes:
        user (OneToOneField): The associated User instance.
        bio (TextField): A short biography of the user.
        agreement_accepted (BooleanField): Indicates if the user has accepted terms.
        created_at (DateTimeField): Timestamp of when the profile was created.
        avatar (ImageField): The user's avatar image.
        sex (CharField): The user's sex.
        username (CharField): The user's unique username.
        email (EmailField): The user's unique email address.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
    """

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["-created_at"]

    user: User = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio: TextField = models.TextField(max_length=500, blank=True)
    agreement_accepted: BooleanField = models.BooleanField(default=False)
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    avatar: ImageField = models.ImageField(
        null=True,
        blank=True,
        upload_to=avatar_for_user_directory_path,
    )
    sex = models.CharField(null=True, blank=True, max_length=10)
    username: CharField = models.CharField(
        null=True, blank=True, max_length=255, unique=True
    )
    email: EmailField = models.EmailField(
        null=True,
        blank=True,
        max_length=255,
        unique=True,
    )
    first_name: CharField = models.CharField(null=True, blank=True, max_length=255)
    last_name: CharField = models.CharField(null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs) -> None:
        """
        Override the save method to set the username from the associated User.

        If the username field is not set, it will be populated with
        the username from the related User instance before saving.

        Args:
            *args: Positional arguments to pass to the parent save method.
            **kwargs: Keyword arguments to pass to the parent save method.
        """
        if not self.username:
            self.username: str = self.user.username
        if not self.email:
            self.email: str = self.user.email
        if not self.first_name:
            self.first_name: str = self.user.first_name
        if not self.last_name:
            self.last_name: str = self.user.last_name
        if not self.sex:
            self.sex: str = self.user.sex
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return a string representation of the Profile instance.
        """
        return f"{self.user.username} Profile"

    def __repr__(self) -> str:
        """
        Return a string representation of the Profile instance.
        """
        return f"{self.user.pk} | {self.user.username} Profile"
