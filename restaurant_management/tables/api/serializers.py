from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from restaurant_management.tables.enums import ReservationStatusEnum
from restaurant_management.tables.models import Reservation, SeatCostSingleton, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class ReservationRetrievingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = (
            "id",
            "reservation_by",
            "table",
            "total_cost",
            "seats_reserved",
            "start_time",
            "end_time",
            "status",
        )


class ReservationCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("reservation_by", "table", "total_cost", "status")

    def validate(self, data):
        start_time, end_time = data.get("start_time"), data.get("end_time")
        seats_reserved = data.get("seats_reserved")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"start_time": _("The start time cannot be later than the end time.")},
            )

        cheapest_table = Reservation.objects.find_cheapest_table(
            seats_reserved=seats_reserved,
            start_time=start_time,
            end_time=end_time,
        )

        if not cheapest_table:
            raise serializers.ValidationError(
                {
                    "seats_reserved": _(
                        "We do not have an available table for the selected "
                        "time and seat count.",
                    ),
                },
            )

        self.cheapest_table = cheapest_table
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        seat_cost = SeatCostSingleton.objects.get_seat_cost()

        reservation = Reservation.objects.create(
            reservation_by=user,
            table=self.cheapest_table,
            total_cost=(self.cheapest_table.seats - 1) * seat_cost,
            status=ReservationStatusEnum.ACTIVE.name,
            **validated_data,
        )
        return reservation  # noqa: RET504
