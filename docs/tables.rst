.. _tables:

Tables
======================================================================
You can find the tables app documentation here.

This app is designed for **managing restaurant tables**.

To control the number of tables, we use the **TableCountSingleton** model,
which allows you to set its value either through the **admin panel** or by configuring it in the **settings**.

This model follows a **Singleton design pattern**, ensuring that we can
define an appropriate number of tables for the restaurant while easily managing them.


To manage and set the cost for each seat, we also used the **Singleton design pattern**
and implemented a model called **SeatCostSingleton**.

You can configure its value either through the **admin panel** or in the **settings**.


**Tip**: The values for the number of tables and the cost per seat have default values in settings.


We have the **Table** model which takes only one field for the number of seats.

Since we only use tables with an even number of seats, we use a validator called
**even_number_validator** to ensure that the number of seats is even.

We have the **Reservation** model, which collects the **start time**, **end time**, and
the **number of seats** the user requires. Based on this information, we automatically
select a table with an even number of seats that is as close as possible to the user's request.


In the **Reservation** model, we have a custom manager called **``ReservationManager``**
which contains a method named **``find_cheapest_table``**. This method helps us find the best
available table with an even number of seats. This is done using the following query:

.. code-block:: bash

    cheapest_tables = (
        model_tables.Table.objects.filter(
            seats__gte=seats_reserved,
        )
        .exclude(
            Q(table_reservations__status=ReservationStatusEnum.ACTIVE.name)
            & Q(table_reservations__start_time__lt=end_time)
            & Q(table_reservations__end_time__gt=start_time),
        )
        .order_by("seats")
        .distinct()
    )

**Tip**: This is not good in the real world, the user should choose the
          table themselves, not us choosing it for them, but we implement
          this method according to the project's requirements.

We also use **Celery**, **Celery Beat**, and **Flower** to automatically update all active reservations to **CANCEL** status at **00:00** every day.
This ensures that no issues arise for table reservations on the following day.


To manage the site and perform important tasks, you should use the **admin panel**.
Additionally, we have created APIs that allow users to:

- View available tables.
- View their own reservations.
- Make new reservations.
- Cancel a reservation they have made previously.


Models
----------------------------------------------------------------------
.. automodule:: restaurant_management.tables.models
   :members:
   :noindex:


Forms
----------------------------------------------------------------------
.. automodule:: restaurant_management.tables.forms
   :members:
   :noindex:


Admins
----------------------------------------------------------------------
.. automodule:: restaurant_management.tables.admin
   :members:
   :noindex:


Serializers
----------------------------------------------------------------------
.. automodule:: restaurant_management.tables.api.serializers
   :members:
   :noindex:


Views
----------------------------------------------------------------------
.. automodule:: restaurant_management.tables.api.views
    :members:
    :noindex:
