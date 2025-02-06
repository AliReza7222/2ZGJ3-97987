from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Table
from .models import TableCountSingleton


@receiver(post_save, sender=Table)
def decrease_table_count(sender, instance, created, **kwargs):
    if created:
        TableCountSingleton.objects.decr()


@receiver(post_delete, sender=Table)
def increase_table_count(sender, instance, **kwargs):
    TableCountSingleton.objects.incr()
