from django.db import models
from django.utils import timezone

from .managers import CustomModelManager


class AbstractTimeStamp(models.Model):
    """Abstract time stamp model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomModelManager()

    def get_created_time(self):
        td = timezone.now() - self.created_at
        days, hours, minutes, seconds = (
            td.days,
            td.seconds // 3600,
            td.seconds % 3600 // 60,
            td.seconds % 60,
        )
        if not days:
            if not hours:
                if not minutes:
                    return f"{seconds} seconds ago"
                return f"{minutes} minutes ago"
            return f"{hours} hours ago"
        return f"{days} days ago"

    class Meta:
        abstract = True
