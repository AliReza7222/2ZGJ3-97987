from contextlib import suppress

from django.apps import AppConfig


class TablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restaurant_management.tables"

    def ready(self):
        with suppress(ImportError):
            import restaurant_management.tables.signals  # noqa: F401
