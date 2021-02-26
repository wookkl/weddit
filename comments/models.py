from django.db import models
from django.core.validators import ValidationError

from core.models import AbstractTimeStamp


class Comment(AbstractTimeStamp):
    """Comment model definition"""

    post = models.ForeignKey(
        "posts.Post", related_name="comments", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    comment = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        if not self.comment:
            raise ValidationError("Blank is not allowed")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.writer}'s comment: {self.comment[:10]}..."
