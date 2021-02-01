from time import timezone

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)


class User(AbstractBaseUser, PermissionsMixin):
    """User model definition"""

    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]
    objects = UserManager()
