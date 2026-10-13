import math

from django import forms


class NumberListForm(forms.Form):
    numbers = forms.CharField(
        label="Numbers",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: 10, 20, 30, 40",
                "class": "input-field",
            }
        ),
    )

    def __init__(self, *args, operation: str | None = None, **kwargs):
        self.operation = operation or "standard_deviation"
        super().__init__(*args, **kwargs)

    def clean_numbers(self):
        raw_value = self.cleaned_data["numbers"]
        if raw_value is None or not raw_value.strip():
            raise forms.ValidationError("Please enter numbers before submitting.")

        values: list[float] = []
        for item in raw_value.split(","):
            value = item.strip()
            if value == "":
                raise forms.ValidationError(
                    "Missing value between commas. Please enter all numbers clearly."
                )

            try:
                number = float(value)
            except ValueError as exc:
                raise forms.ValidationError(f"'{value}' is not a valid number.") from exc

            if not math.isfinite(number):
                raise forms.ValidationError("Numbers cannot be NaN or infinity.")

            values.append(number)

        minimum_values = 2 if self.operation == "standard_deviation" else 4
        if len(values) < minimum_values:
            if self.operation == "standard_deviation":
                raise forms.ValidationError(
                    "Standard deviation requires at least 2 numbers."
                )
            raise forms.ValidationError("IQR requires at least 4 numbers.")

        return values
