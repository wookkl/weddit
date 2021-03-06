from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):

    ordering = ("id",)
    list_display = (
        "email",
        "nickname",
        "is_staff",
        "is_superuser",
        "can_create_community",
    )
    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        (
            _("Personal Info"),
            {
                "fields": (
                    "avatar",
                    "nickname",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "can_create_community",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = (
        "id",
        "password",
    )
