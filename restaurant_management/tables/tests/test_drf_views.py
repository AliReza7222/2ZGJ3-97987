from decimal import Decimal

from rest_framework import status

from restaurant_management.tables.enums import ReservationStatusEnum
from restaurant_management.tables.models import Reservation, Table


class TestTableRetrieving:
    """
    Tests for retrieving table information from the API.

    This class includes the following tests:
    1. Retrieving a list of all tables.
    2. Retrieving a specific table by its ID.
    """

    def test_get_all_tables(self, create_table, client_api):
        """
        Test retrieving a list of all tables.
        """
        [create_table() for _ in range(3)]
        response = client_api.get("/api/tables/")
        count_table = Table.objects.count()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == count_table

    def test_get_table_by_id(self, create_table, client_api):
        """
        Test retrieving a specific table by its ID.
        """
        table = create_table(seats=4)

        response = client_api.get(f"/api/tables/{table.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == table.id
        assert response.data["seats"] == table.seats


class TestReservation:
    """
    Tests for reservation related API endpoints.
    """

    def test_access_for_anonymous_user_retrieving(self, client_api, create_reservation):
        """
        Test that anonymous users cannot retrieve reservations.
        """
        [create_reservation() for _ in range(2)]

        response = client_api.get("/api/book/")
        error = response.data["detail"]

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error.code == "not_authenticated"

    def test_access_for_authenticated_user(self, client_api, user, create_reservation):
        """
        Test that authenticated users can retrieve only their own reservations.
        """
        [create_reservation(reservation_by=user) for _ in range(2)]
        create_reservation()

        client_api.force_authenticate(user=user)
        response = client_api.get("/api/book/")
        count_reservation_user = Reservation.objects.filter(reservation_by=user).count()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == count_reservation_user

    def test_access_for_user_to_other_user_reservations(
        self,
        client_api,
        user,
        create_reservation,
    ):
        """
        Test that users cannot access other users' reservations.
        """
        reservation = create_reservation()

        client_api.force_authenticate(user=user)
        response = client_api.get(f"/api/book/{reservation.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_access_for_anonymous_user_cancel_reservation(
        self,
        client_api,
        create_reservation,
    ):
        """
        Test that anonymous users cannot cancel a reservation.
        """
        reservation = create_reservation()

        response = client_api.get(f"/api/book/{reservation.id}/cancel/")
        error = response.data["detail"]

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error.code == "not_authenticated"

    def test_cancel_active_reservation(self, client_api, user, create_reservation):
        """
        Test that an authenticated user can cancel their own active reservation.
        """
        reservation = create_reservation(
            reservation_by=user,
            status=ReservationStatusEnum.ACTIVE.name,
        )

        client_api.force_authenticate(user=user)
        response = client_api.put(f"/api/book/{reservation.id}/cancel/")

        reservation.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert reservation.status == ReservationStatusEnum.CANCEL.name

    def test_create_reservation_for_authenticated_user(
        self,
        client_api,
        user,
        create_table,
    ):
        """
        Test reservation creation for authenticated users.
        """
        create_table(seats=10)
        create_table(seats=4)
        table3 = create_table(seats=6)

        client_api.force_authenticate(user=user)

        data = {
            "start_time": "12:00:00",
            "end_time": "14:00:00",
            "seats_reserved": 5,
        }

        response = client_api.post("/api/book/create/", data)

        assert response.status_code == status.HTTP_201_CREATED

        reservation = Reservation.objects.first()
        assert reservation.table.id == table3.id  # type: ignore
        assert reservation.total_cost == Decimal((reservation.table.seats - 1) * 100)  # type: ignore
        assert reservation.status == ReservationStatusEnum.ACTIVE.name  # type: ignore

    def test_create_reservation_for_anonymous_user(self, client_api):
        """
        Test that anonymous users cannot create reservations.
        """
        data = {
            "start_time": "12:00:00",
            "end_time": "14:00:00",
            "seats_reserved": 3,
        }
        response = client_api.post("/api/book/create/", data)
        error = response.data["detail"]

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error.code == "not_authenticated"

    def test_start_time_after_end_time(self, client_api, user, create_table):
        """
        Test validation when start time is after end time.
        """
        create_table()
        client_api.force_authenticate(user=user)

        data = {
            "start_time": "14:00:00",
            "end_time": "12:00:00",
            "seats_reserved": 4,
        }

        response = client_api.post("/api/book/create/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
