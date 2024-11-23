from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission


class Command(BaseCommand):
    """
        Command to assign the 'profile_manager' group and specific permissions
    to a user in the Django application.

    This command ensures that a user is added to the 'profile_manager' group
    and is granted the 'view_profile' and 'view_logentry' permissions.
    """
    def handle(self, user: User, *args, **options) -> None:
        """
         Handles the command execution.

        Retrieves the user by primary key, creates or gets the 'profile_manager'
        group, and assigns the necessary permissions to the user.
        Args:
            user (User): The user instance to be updated.
            *args: Additional positional arguments.
            **options: Additional keyword arguments.

        Returns: None

        """
        user: User = User.objects.get(pk=user.pk)
        group, created = Group.get_or_create(
            name="profile_manager",
        )
        permission_profile: Permission = Permission.objects.get(codename="view_profile")
        permission_logentry: Permission = Permission.objects.get(codename="view_logentry")

        group.permissions.add(permission_profile)
        user.groups.add(group)
        user.user_permissions.add(permission_logentry)
