from datetime import UTC, datetime, timedelta

import factory
from factory.django import DjangoModelFactory

from restaurant_management.tables.models import Reservation, Table
from restaurant_management.users.tests.factories import UserFactory


class TableFactory(DjangoModelFactory):
    class Meta:
        model = Table

    seats = factory.Faker("random_int", min=1, max=10)


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    reservation_by = factory.SubFactory(UserFactory)
    table = factory.SubFactory(TableFactory)
    total_cost = factory.LazyAttribute(
        lambda obj: (obj.table.seats - 1) * 100,
    )
    start_time = factory.Faker("time", pattern="%H:%M:%S")
    end_time = factory.LazyAttribute(
        lambda obj: (
            datetime.strptime(obj.start_time, "%H:%M:%S").replace(tzinfo=UTC)
            + timedelta(hours=1)
        ).time(),
    )
