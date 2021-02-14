from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin definition"""

    list_display = (
        "writer",
        "community",
        "content",
        "get_thumbnail",
    )

    def get_thumbnail(self, instance):
        if instance.photo:
            return mark_safe(
                f"<img src={instance.photo.url} style='width:40px; height:40px;'/> "
            )
        else:
            return None

    get_thumbnail.short_description = "thumbnail"
