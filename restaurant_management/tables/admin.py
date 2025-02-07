from django.contrib import admin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import path

from .enums import ReservationStatusEnum
from .forms import ReservationForm, TableForm
from .models import Reservation, SeatCostSingleton, Table, TableCountSingleton


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    form = TableForm


@admin.register(TableCountSingleton)
class TableCountSingletonAdmin(admin.ModelAdmin):
    pass


@admin.register(SeatCostSingleton)
class SeatCostSingletonAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ("reservation_by", "table", "start_time", "end_time", "status")
    autocomplete_fields = ("reservation_by",)
    list_per_page = 10
    fieldsets = (
        ("General", {"fields": ("reservation_by", "seats_reserved")}),
        ("Reservation Time", {"fields": ("start_time", "end_time")}),
        ("Reservation Status", {"fields": ("status",)}),
        ("Reservation Table", {"fields": ("table", "total_cost")}),
    )
    readonly_fields = ("table", "total_cost")

    def has_change_permission(self, request, obj=None):
        return False

    @transaction.atomic
    def cancel_reservation_view(self, request, reservation_id):
        """
        Cancels the reservation with the given ID and updates its status.
        """
        reservation = self.get_object(request, reservation_id)
        reservation.status = ReservationStatusEnum.CANCEL.name  # type: ignore
        self.message_user(
            request,
            f"Reservation {reservation.id} for {reservation.reservation_by} "  # type: ignore
            "has been successfully canceled.",
            level="success",
        )
        reservation.save()  # type: ignore
        return HttpResponseRedirect(request.headers.get("referer"))

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "cancel-reservation/<int:reservation_id>/",
                self.admin_site.admin_view(self.cancel_reservation_view),
                name="tables_reservation_cancelled_reservation",
            ),
        ]

        return custom_urls + urls

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({"active_status": ReservationStatusEnum.ACTIVE.name})
        return super().change_view(request, object_id, form_url, extra_context)
