from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin definition"""

    list_display = (
        "post",
        "writer",
        "truncated_comment",
    )

    def truncated_comment(self, instance):
        if len(instance.comment) > 40:
            return f"{instance[:40]}..."
        return instance.comment

    truncated_comment.short_description = "comment"
