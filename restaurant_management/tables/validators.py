from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def even_number_validator(value):
    if value % 2 != 0:
        raise ValidationError(_("The value must be an even number."))
    return value
