from django.contrib import admin

from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Vote admin definition"""

    list_display = (
        "__str__",
        "voter",
        "post",
        "like",
    )
