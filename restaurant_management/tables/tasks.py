from celery import shared_task

from .enums import ReservationStatusEnum
from .models import Reservation


@shared_task
def cancel_old_reservations():
    Reservation.objects.filter(status=ReservationStatusEnum.ACTIVE.name).update(
        status=ReservationStatusEnum.CANCEL.name,
    )
