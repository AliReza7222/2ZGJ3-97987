from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from restaurant_management.tables.api.views import (
    ReservationRetrievingViewset,
    TableRetrievingViewset,
)
from restaurant_management.users.api.views import UserRetrievingViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserRetrievingViewSet, basename="user")
router.register("tables", TableRetrievingViewset, basename="table")
router.register("book", ReservationRetrievingViewset, basename="book")


app_name = "api"
urlpatterns = router.urls
