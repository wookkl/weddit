from django.db import models
from django.contrib.auth import get_user_model

from communities.models import Community


class Post(models.Model):
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
