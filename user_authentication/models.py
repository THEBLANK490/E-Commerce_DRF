from django.db import models
from django.contrib.auth.models import AbstractUser
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
    photo = models.ImageField(upload_to='uploads/user/',blank=True,null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length = 150)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    role = models.CharField(max_length=10,choices = Role.choices, default = "CUSTOMER")
    
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.email
    

