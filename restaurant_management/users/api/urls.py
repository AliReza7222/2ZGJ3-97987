from django.urls import path

from .views import UserCreateAPIView

app_name = "api_users"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="user-register"),
]
