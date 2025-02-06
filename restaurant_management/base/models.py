from django.db import models
from django.db import transaction


class SingletonBaseModel(models.Model):
    class Meta:
        abstract = True

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
