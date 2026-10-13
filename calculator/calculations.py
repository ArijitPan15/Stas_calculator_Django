import math
from datetime import datetime
from statistics import median
from typing import Sequence


def parse_number_list(raw_input: str) -> list[float]:
    """Convert a comma-separated string into a list of valid finite floats."""
    if raw_input is None or not raw_input.strip():
        raise ValueError("Please enter at least one number.")

    numbers: list[float] = []
    for item in raw_input.split(","):
        value = item.strip()
        if value == "":
            raise ValueError("Missing value between commas. Please enter all numbers.")

        try:
            number = float(value)
        except ValueError as exc:
            raise ValueError(f"'{value}' is not a valid number.") from exc

        if not math.isfinite(number):
            raise ValueError("Numbers cannot be NaN or infinity.")

        numbers.append(number)

    return numbers


def calculate_population_standard_deviation(values: Sequence[float]) -> float:
    """Return the population standard deviation for a list of numbers."""
    return calculate_population_standard_deviation_details(values)["result"][
        "population_standard_deviation"
    ]


def calculate_population_standard_deviation_details(
    values: Sequence[float],
) -> dict:
    """Calculate population standard deviation and return a complete history record."""
    if len(values) < 2:
        raise ValueError("Standard deviation requires at least 2 numbers.")

    try:
        mean_value = math.fsum(value / len(values) for value in values)
        deviations = [value - mean_value for value in values]
        squared_deviations = [deviation**2 for deviation in deviations]
        sum_squared_deviations = math.fsum(squared_deviations)
        variance = sum_squared_deviations / len(values)
        standard_deviation = math.sqrt(variance)
    except (OverflowError, ValueError) as exc:
        raise ValueError(
            "These values are too large to calculate standard deviation safely."
        ) from exc

    calculated_values = [
        mean_value,
        *deviations,
        *squared_deviations,
        sum_squared_deviations,
        variance,
        standard_deviation,
    ]
    if not all(math.isfinite(value) for value in calculated_values):
        raise ValueError(
            "These values are too large to calculate standard deviation safely."
        )

    return {
        "calculated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "operation": "standard_deviation",
        "original_values": list(values),
        "calculation_method": "Population standard deviation",
        "intermediate_values": {
            "number_of_observations": len(values),
            "mean": mean_value,
            "deviations_from_mean": deviations,
            "squared_deviations": squared_deviations,
            "sum_of_squared_deviations": sum_squared_deviations,
            "population_variance": variance,
        },
        "formulas": {
            "mean": "sum(values) / number_of_observations",
            "deviation": "value - mean",
            "squared_deviation": "deviation ** 2",
            "population_variance": (
                "sum(squared_deviations) / number_of_observations"
            ),
            "population_standard_deviation": "sqrt(population_variance)",
        },
        "result": {"population_standard_deviation": standard_deviation},
    }


def calculate_iqr(values: Sequence[float]) -> tuple[float, float, float]:
    """Return Q1, Q3, and the interquartile range using the Tukey median-split method."""
    record = calculate_iqr_details(values)
    result = record["result"]
    return result["q1"], result["q3"], result["iqr"]


def calculate_iqr_details(values: Sequence[float]) -> dict:
    """Calculate Q1, Q3, and IQR and return a complete history record."""
    if len(values) < 4:
        raise ValueError("IQR requires at least 4 numbers.")

    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2

    if len(sorted_values) % 2 == 0:
        lower_half = sorted_values[:midpoint]
        upper_half = sorted_values[midpoint:]
    else:
        lower_half = sorted_values[:midpoint]
        upper_half = sorted_values[midpoint + 1 :]

    q1 = median(lower_half)
    q3 = median(upper_half)
    iqr = q3 - q1
    if not all(math.isfinite(value) for value in (q1, q3, iqr)):
        raise ValueError("These values are too large to calculate IQR safely.")

    return {
        "calculated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "operation": "iqr",
        "original_values": list(values),
        "sorted_values": sorted_values,
        "calculation_method": (
            "Tukey median-split: exclude the overall median when the list length is odd"
        ),
        "intermediate_values": {
            "lower_half": lower_half,
            "upper_half": upper_half,
            "q1": q1,
            "q3": q3,
        },
        "formulas": {
            "q1": "median(lower_half)",
            "q3": "median(upper_half)",
            "iqr": "q3 - q1",
        },
        "result": {"q1": q1, "q3": q3, "iqr": iqr},
    }
