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

    def get_comment_count(self):
        return self._get_count(self.comments.count())

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})
