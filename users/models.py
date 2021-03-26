from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from .managers import CustomUserManager

from core.validators import alphanumeric_validator


class User(AbstractBaseUser, PermissionsMixin):
    """User model definition"""

    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            alphanumeric_validator,
        ],
    )
    avatar = models.ImageField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    can_create_community = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def get_absolute_url(self):
        return reverse("user:detail", kwargs={"nickname": self.nickname})

    def save(self, *args, **kwargs):
        alphanumeric_validator(self.nickname)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nickname)