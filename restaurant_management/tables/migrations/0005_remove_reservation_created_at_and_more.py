# Generated by Django 5.0.10 on 2025-02-06 12:23

import django.core.validators
import restaurant_management.tables.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_alter_reservation_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='table',
            name='is_available',
        ),
        migrations.AddField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(default='12:10:10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(default='12:10:10'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='table',
            name='seats',
            field=models.PositiveIntegerField(help_text='The number of seats at the table (must be between 4 and 10).', validators=[django.core.validators.MinValueValidator(4), django.core.validators.MaxValueValidator(10), restaurant_management.tables.validators.even_number_validator], verbose_name='Number of seats'),
        ),
    ]
