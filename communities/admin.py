from django.contrib import admin

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    prepopulated_fields = {"slug": ("name",)}  # new
