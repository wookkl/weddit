from django.db import models
from django.contrib.auth import get_user_model

from core.models import AbstractTimeStamp
from communities.models import Community


class Subscription(AbstractTimeStamp):
    """Subscription model definition"""

    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscriptions"
    )

    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="subscriptions"
    )

    def __str__(self):
        return f"{self.subscriber}-{self.community}"

    class Meta:
        unique_together = ["subscriber", "community"]
