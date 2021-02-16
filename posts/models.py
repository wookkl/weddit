import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from communities.models import Community
from core.models import AbstractTimeStamp


class Post(AbstractTimeStamp):
    """Post model definition"""

    writer = models.ForeignKey(
        get_user_model(), related_name="posts", on_delete=models.CASCADE
    )
    community = models.ForeignKey(
        Community, related_name="posts", on_delete=models.CASCADE
    )
    content = models.TextField(blank=True)
    photo = models.ImageField(null=True, upload_to="photos/posts/")

    def get_photo_url(self):
        return self.photo.url

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

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
