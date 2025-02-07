from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework.test import APIClient

from restaurant_management.tables.tests.factories import (
    ReservationFactory,
    TableFactory,
)
from restaurant_management.users.tests.factories import UserFactory

if TYPE_CHECKING:
    from collections.abc import Callable

    from restaurant_management.tables.models import Reservation, Table
    from restaurant_management.users.models import User as UserType


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> UserType:
    return UserFactory()


@pytest.fixture
def create_table(db) -> Callable:
    def _create_table(**kwargs) -> Table:
        return TableFactory(**kwargs)

    return _create_table


@pytest.fixture
def create_reservation(db) -> Callable:
    def _create_reservation(**kwargs) -> Reservation:
        return ReservationFactory(**kwargs)

    return _create_reservation


@pytest.fixture
def client_api(db) -> APIClient:
    return APIClient()
