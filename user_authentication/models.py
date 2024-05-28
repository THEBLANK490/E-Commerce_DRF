from django.contrib.auth.models import AbstractUser
from django.db import models

from core.managers import CustomUserManager


# Create your models here.
class Gender(models.TextChoices):
    """
    Choices for gender.

    Attributes:
        M (str): Male gender.
        F (str): Female gender.
        O (str): Other gender.
    """

    M = "MALE"
    F = "FEMALE"
    O = "OTHERS"


class Role(models.TextChoices):
    """
    Choices for user roles.

    Attributes:
        A (str): Administrator role.
        C (str): Customer role.
        S (str): Staff role.
    """

    A = "ADMIN"
    C = "CUSTOMER"
    S = "STAFF"


class UserAccount(AbstractUser):
    """
    Model representing a user account.

    Attributes:
        email (str): The email address of the user (unique).
        photo (ImageField): The profile photo of the user (optional).
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The phone number of the user (unique).
        address (str): The address of the user.
        gender (str): The gender of the user (choices from Gender).
        role (str): The role of the user (choices from Role, default is 'CUSTOMER').

    Managers:
        objects: Custom manager for UserAccount model.

    Fields:
        REQUIRED_FIELDS: Fields required for creating a user.
        USERNAME_FIELD: Field used for authentication (email).

    Methods:
        __str__: Returns a string representation of the user's email.
    """

    username = None
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to="uploads/user/", blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    role = models.CharField(max_length=10, choices=Role.choices, default="CUSTOMER")

    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email
