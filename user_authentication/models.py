from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from user_authentication.managers import CustomUserManager

# Create your models here.
class Gender(models.TextChoices):
    M = "MALE"
    F = "FEMALE"
    O = "OTHERS"
    
class Role(models.TextChoices):
    A = "ADMIN"
    C = "CUSTOMER"
    S = "STAFF"

class UserAccount(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    photo = models.FileField(upload_to='uploads/',blank=True,null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    role = models.CharField(max_length=10,choices = Role.choices, default = "CUSTOMER")
    
    def __str__(self):
        return self.email
    

