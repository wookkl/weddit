from django.db import models
from django.conf import settings

from core.validators import alphanumeric_validator


class Community(models.Model):
    """Community model definition"""

    name = models.CharField(
        max_length=30,
        unique=True,
        validators=[alphanumeric_validator],
    )
    creater = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    description = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(null=True, upload_to="avatar/communities/")
    photo = models.ImageField(null=True, upload_to="photos/communities/")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        alphanumeric_validator(self.name)
        super().save(*args, **kwargs)
