from django.db import models
from core.models import AbstractTimeStamp


class Vote(AbstractTimeStamp):
    """Vote model definition"""

    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    voter = models.ForeignKey("users.User", on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

    class Meta:
        default_related_name = "votes"
