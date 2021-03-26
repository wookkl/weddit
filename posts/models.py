from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from communities.models import Community
from core.models import AbstractTimeStamp


class Post(AbstractTimeStamp):
    """Post model definition"""

    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    photo = models.ImageField(null=True, upload_to="photos/posts/")

    def get_photo_url(self):
        return self.photo.url

    def get_comment_count(self):
        return self._get_count(self.comments.count())

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.writer}'s post"

    class Meta:
        default_related_name = "posts"
