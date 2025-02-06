from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def even_number_validator(value):
    """
    Validates that the given value is an even number.

    This validator was written because tables with an odd number of seats
    are not used, so it would be better to check right away that the number
    of seats is even.
    """
    if value % 2 != 0:
        raise ValidationError(_("The value must be an even number."))
    return value
