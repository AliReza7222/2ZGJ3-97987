from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from restaurant_management.tables.api.serializers import (
    ReservationCancelSerializer,
    ReservationCreatingSerializer,
    ReservationRetrievingSerializer,
    TableSerializer,
)
from restaurant_management.tables.enums import ReservationStatusEnum
from restaurant_management.tables.models import Reservation, Table


class TableRetrievingViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ("seats",)
    search_fields = ("seats",)


class ReservationRetrievingViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationRetrievingSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ("reservation_by__email", "table__id")
    ordering_fields = ("start_time", "seats_reserved")

    def get_queryset(self):
        """
        Override the get_queryset method to ensure that users can
        only see their own reservations.

        Admins or superusers can see all reservations.
        """
        queryset = Reservation.objects.select_related("reservation_by", "table")

        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(reservation_by=self.request.user)  # type: ignore


class ReservationCancelAPIView(UpdateAPIView):
    serializer_class = ReservationCancelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Restrict to only reservations that are ACTIVE and belong to the
        authenticated user.
        """
        return Reservation.objects.select_related("reservation_by", "table").filter(  # type: ignore
            reservation_by=self.request.user,
            status=ReservationStatusEnum.ACTIVE.name,
        )

    def perform_update(self, serializer):
        reservation = serializer.instance
        reservation.status = ReservationStatusEnum.CANCEL.name
        reservation.save(update_fields=["status"])


class ReservationCreateAPIView(CreateAPIView):
    serializer_class = ReservationCreatingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.select_related("table", "reservation_by")
