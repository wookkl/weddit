from django.db import models
from django.utils import timezone

from .managers import CustomModelManager


class AbstractTimeStamp(models.Model):
    """Abstract time stamp model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomModelManager()

    class Meta:
        abstract = True
