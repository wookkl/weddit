from django.db import models
from django.contrib.auth import get_user_model

from communities.models import Community


class Subscription(models.Model):
    """Subscription model definition"""

    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscriptions"
    )

    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        unique_together = ["subscriber", "community"]
