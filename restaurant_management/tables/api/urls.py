from django.urls import path

from .views import ReservationCancelAPIView, ReservationCreateAPIView

app_name = "api_tables"

urlpatterns = [
    path("<int:pk>/cancel/", ReservationCancelAPIView.as_view(), name="book-cancel"),
    path("create/", ReservationCreateAPIView.as_view(), name="book-create"),
]
