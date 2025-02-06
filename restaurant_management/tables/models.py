from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from restaurant_management.base.models import SingletonBaseModel

from .enums import ReservationStatusEnum
from .managers import SeatCostManager
from .managers import TableCountManager
from .validators import even_number_validator

User = get_user_model()


class SeatCostSingleton(SingletonBaseModel):
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Cost per seat"),
    )

    objects = SeatCostManager()

    class Meta:
        verbose_name = "SeatCost"
        verbose_name_plural = "SeatCost"

    def __str__(self):
        return "SeatCost Object"


class TableCountSingleton(SingletonBaseModel):
    count = models.PositiveIntegerField(
        verbose_name=_("Table Count"),
        help_text=_("Enter the number of your restaurant tables."),
    )

    objects = TableCountManager()

    class Meta:
        verbose_name = "TableCount"
        verbose_name_plural = "TableCount"

    def __str__(self):
        return "TableCount Object"


class Table(models.Model):
    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(10), even_number_validator],
        verbose_name=_("Number of seats"),
        help_text=_("The number of seats at the table (must be between 4 and 10)."),
    )

    def __str__(self):
        return f"table with {self.seats} seats"


class Reservation(models.Model):
    reservation_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_reservations",
        verbose_name=_("Reservation By"),
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="table_reservations",
        verbose_name=_("Table"),
    )
    seats_reserved = models.PositiveIntegerField(default=4)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    # We simply assume that all reservations are for a day.
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=50,
        choices=ReservationStatusEnum.choices(),
        default=ReservationStatusEnum.ACTIVE,
        verbose_name=_("Reservation status"),
    )

    def __str__(self):
        return f"{self.reservation_by}-{self.status}"
