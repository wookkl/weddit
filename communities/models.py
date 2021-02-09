from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify

from core.validators import alphanumeric_validator


class Community(models.Model):
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

    class Meta:
        verbose_name_plural = "communities"
