from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify

from core.validators import alphanumeric_validator
from core.models import AbstractTimeStamp


class Community(AbstractTimeStamp):
    """Community model definition"""

    name = models.CharField(
        max_length=30,
        unique=True,
        validators=[alphanumeric_validator],
    )
    slug = models.SlugField(null=False, unique=True)
    creater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="communities",
    )
    description = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(null=True, upload_to="avatar/communities/")
    photo = models.ImageField(null=True, upload_to="photos/communities/")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        alphanumeric_validator(self.name)
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("communities:detail", kwargs={"slug": self.slug})

    def get_avatar_url(self):
        return self.avatar.url

    def get_subscriber_count(self):
        count = self.subscriptions.count()
        count = 12000
        if count >= 1000000:
            return f"{count / 1000000:.2f}".rstrip("0").rstrip(".") + "m"
        elif count >= 1000:
            return f"{count / 1000:.2f}".rstrip("0").rstrip(".") + "k"
        return f"{count}"

    class Meta:
        verbose_name_plural = "communities"
