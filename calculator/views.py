from django.shortcuts import render

from .calculations import (
    calculate_iqr_details,
    calculate_population_standard_deviation_details,
)
from .forms import NumberListForm
from .json_history import save_calculation_record


def home(request):
    return render(request, "calculator/home.html")


def _calculator_page(request, operation, page_title, description):
    if request.method == "POST":
        form = NumberListForm(request.POST, operation=operation)
        if form.is_valid():
            numbers = form.cleaned_data["numbers"]
            numbers_text = ", ".join(str(number) for number in numbers)

            try:
                if operation == "standard_deviation":
                    record = calculate_population_standard_deviation_details(numbers)
                else:
                    record = calculate_iqr_details(numbers)
            except ValueError as exc:
                form.add_error("numbers", str(exc))
                return render(
                    request,
                    "calculator/calculator.html",
                    {
                        "form": form,
                        "page_title": page_title,
                        "description": description,
                    },
                )

            history_error = None
            try:
                save_calculation_record(record)
            except (OSError, ValueError) as exc:
                history_error = (
                    "The calculation succeeded, but its history could not be saved: "
                    f"{exc}"
                )

            result = record["result"]
            context = {
                "page_title": page_title,
                "numbers_text": numbers_text,
                "sorted_numbers_text": (
                    ", ".join(str(number) for number in record["sorted_values"])
                    if operation == "iqr"
                    else None
                ),
                "output_label": (
                    "Population Standard Deviation"
                    if operation == "standard_deviation"
                    else None
                ),
                "output_value": (
                    f'{result["population_standard_deviation"]:.4f}'
                    if operation == "standard_deviation"
                    else None
                ),
                "q1": str(result["q1"]) if operation == "iqr" else None,
                "q3": str(result["q3"]) if operation == "iqr" else None,
                "iqr": str(result["iqr"]) if operation == "iqr" else None,
                "history_error": history_error,
                "operation": operation,
            }
            return render(request, "calculator/result.html", context)
    else:
        form = NumberListForm(operation=operation)

    return render(
        request,
        "calculator/calculator.html",
        {
            "form": form,
            "page_title": page_title,
            "description": description,
        },
    )


def standard_deviation_view(request):
    return _calculator_page(
        request,
        operation="standard_deviation",
        page_title="Standard Deviation Calculator",
        description=(
            "Enter several numbers separated by commas. The app uses the population "
            "standard deviation formula."
        ),
    )


def iqr_view(request):
    return _calculator_page(
        request,
        operation="iqr",
        page_title="Interquartile Range Calculator",
        description=(
            "Enter several numbers separated by commas. This calculator uses the Tukey "
            "median-split method to find Q1, Q3, and the IQR."
        ),
    )
