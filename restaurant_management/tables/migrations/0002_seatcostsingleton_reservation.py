# Generated by Django 5.0.10 on 2025-02-06 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatCostSingleton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'SeatCost',
                'verbose_name_plural': 'SeatCost',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_reserved', models.PositiveIntegerField(default=4)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reservation_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reservations', to=settings.AUTH_USER_MODEL, verbose_name='Reservation By')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_reservations', to='tables.table', verbose_name='Table')),
            ],
        ),
    ]
