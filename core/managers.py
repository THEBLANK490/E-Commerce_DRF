from django.contrib.auth.base_user import BaseUserManager

# from django.core.management.base import BaseCommand, CommandError


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email: str, password: str, **extra_fields):
        """
        Create and save a user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to save with the user.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the email is not provided.
        """

        if not email:
            raise ValueError("The Email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields to save with the superuser.

        Returns:
            User: The created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
