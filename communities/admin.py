from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "get_thumbnail",
    )
    prepopulated_fields = {"slug": ("name",)}

    def get_thumbnail(self, instance):
        if instance.avatar:
            return mark_safe(
                f"<img src={instance.avatar.url} style='width:40px; height:40px;'/> "
            )
        else:
            return None

    get_thumbnail.short_description = "thumbnail"
