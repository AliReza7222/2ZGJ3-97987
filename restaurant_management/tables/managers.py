from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models

from restaurant_management.tables import models as model_tables

from .enums import ReservationStatusEnum

if TYPE_CHECKING:
    from datetime import time
    from decimal import Decimal

    from .models import Table, TableCountSingleton


class SeatCostManager(models.Manager):
    def get_seat_cost(self) -> Decimal:
        """
        This method retrieves the seat cost from the database. If no instance exists,
        it creates one with the default cost from settings.
        """
        obj, _ = self.model.objects.get_or_create(  # type: ignore
            pk=1,
            defaults={"cost": settings.SEAT_COST},
        )
        return obj.cost


class TableCountManager(models.Manager):
    def get_obj(self) -> TableCountSingleton:
        """
        Retrieves the TableCountSingleton object. If it doesn't exist, it creates one
        with the initial count from the settings.
        """
        obj, _ = self.model.objects.get_or_create(  # type: ignore
            pk=1,
            defaults={"count": settings.TABLE_COUNT},
        )
        return obj

    def get_table_count(self) -> int:
        """
        Gets the current table count.
        """
        obj = self.get_obj()
        return obj.count

    def incr(self) -> None:
        """
        Increments the table count by 1. Saves the updated count in the database.
        """
        obj = self.get_obj()
        obj.count += 1
        obj.save()

    def decr(self) -> None:
        """
        Decrements the table count by 1 if the count is greater than 0.
        Saves the updated count in the database.
        """
        obj = self.get_obj()
        if obj.count > 0:
            obj.count -= 1
            obj.save()


class ReservationManager(models.Manager):
    def find_cheapest_table(
        self,
        seats_reserved: int,
        start_time: time,
        end_time: time,
    ) -> Table:
        """
        This is a method to find the best or cheapest table for the user.

        *Tip: This is not good in the real world, the user should choose the
              table themselves, not us choosing it for them, but we implement
              this method according to the project's requirements.
        """
        cheapest_tables = (
            model_tables.Table.objects.filter(
                seats__gte=seats_reserved,
            )
            .exclude(
                table_reservations__status=ReservationStatusEnum.ACTIVE.name,
                table_reservations__start_time__lt=end_time,
                table_reservations__end_time__gt=start_time,
            )
            .order_by("seats")
        )

        return cheapest_tables.first()  # type: ignore
