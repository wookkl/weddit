from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from communities.models import Community
from core.models import AbstractTimeStamp


class Post(AbstractTimeStamp):
    """Post model definition"""

    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    photo = models.ImageField(null=True, upload_to="photos/posts/", blank=True)
    hits = models.IntegerField(default=0)

    def get_photo_url(self):
        return self.photo.url

    def get_comment_count(self):
        return self._get_count(self.comments.count())

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.writer}'s post"

    def get_hits_count(self):
        return self._get_count(self.hits)

    def get_vote_score(self):
        votes = self.votes.all()
        up_votes = down_votes = 0
        for vote in votes:
            if vote.like:
                up_votes += 1
            else:
                down_votes += 1
        score = up_votes - down_votes
        return self._get_count(score)

    class Meta:
        default_related_name = "posts"
