from django.forms import ValidationError
from django.utils.translation import gettext as _


def get_error_fields_already_exists(*fields):
    """Return FIELDS + already exists"""

    list_field = [*fields]
    string_fields = ", ".join(list_field)
    plural = "s" if len(list_field) > 1 else ""
    return ValidationError(_(f"{string_fields} already exist{plural}".capitalize()))


def get_error_fields_not_match(*fields):
    """Return FIELDS + do not"""

    list_field = [*fields]
    string_fields = ", ".join(list_field)
    plural = "es" if len(list_field) > 1 else ""
    return ValidationError(_(f"{string_fields} do{plural} not match".capitalize()))
