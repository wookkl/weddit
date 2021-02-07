from django.core.validators import RegexValidator
from django.utils.translation import gettext as _


alphanumeric_validator = RegexValidator(
    regex=r"^[0-9a-zA-Z]*$", message=_("Only alphanumeric characters are allowed")
)
