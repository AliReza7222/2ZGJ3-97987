from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Reservation, SeatCostSingleton, Table, TableCountSingleton


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("seats",)

    def clean(self):
        cleaned_data = super().clean()

        if TableCountSingleton.objects.get_table_count() <= 0 and not self.instance.pk:
            raise forms.ValidationError(
                _(
                    "You cannot add more tables. The maximum allowed number of \
                        tables has been reached.",
                ),
            )

        return cleaned_data


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            "reservation_by",
            "seats_reserved",
            "start_time",
            "end_time",
            "status",
        )

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            raise forms.ValidationError(_("Please enter the correct data."))

        if cleaned_data.get("start_time") > cleaned_data.get("end_time"):  # type: ignore
            raise forms.ValidationError(
                _("The start time cannot be later than the end time."),
            )

        cheapest_table = Reservation.objects.find_cheapest_table(
            seats_reserved=cleaned_data.get("seats_reserved"),  # type: ignore
            start_time=cleaned_data.get("start_time"),  # type: ignore
            end_time=cleaned_data.get("end_time"),  # type: ignore
        )

        if not cheapest_table:
            raise forms.ValidationError(
                _(
                    "We do not have an empty table with this number of seats \
                        for the time you selected.",
                ),
            )

        self.cheapest_table = cheapest_table

        return cleaned_data

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)
        instance.table = self.cheapest_table
        seat_cost = SeatCostSingleton.objects.get_seat_cost()
        instance.total_cost = (self.cheapest_table.seats - 1) * seat_cost
        if commit:
            instance.save()
        return instance
