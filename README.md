# Statistical Calculator

A beginner-friendly Django project that calculates population standard deviation and interquartile range (IQR) from comma-separated numbers.

## Features

- Home page with operation selection
- Population standard deviation calculator
- IQR calculator with Q1, Q3, and IQR output
- Complete calculation records appended to `calculation_history.json`
- Django form validation for invalid values and insufficient data
- Simple templates and clean backend separation
- Automated tests with Django's built-in test runner

## Quartile Method Used

This project uses the Tukey median-split method:

1. Sort the values from smallest to largest.
2. Split the sorted list into lower and upper halves.
3. If there is an odd number of values, exclude the median from both halves.
4. Find the median of the lower half (Q1) and the median of the upper half (Q3).
5. IQR = Q3 - Q1.

This method is simple, consistent, and suitable for beginner Django projects.

## Minimum Number of Values

- Standard deviation: at least 2 values
- IQR: at least 4 values

## Project Structure

```text
statistical_calculator/
├── manage.py
├── README.md
├── calculation_history.json  # created after the first successful calculation
├── statistical_calculator/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── calculator/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── calculations.py
    ├── forms.py
    ├── json_history.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── calculator/
            ├── home.html
            ├── calculator.html
            └── result.html
```

## Setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\activate    # Windows PowerShell
```

3. Install Django:

```bash
python -m pip install Django
```

4. Start the development server:

```bash
python manage.py runserver
```

5. Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Example Inputs and Outputs

### Standard Deviation

Input:

```text
1, 2, 3, 4, 5
```

Population standard deviation:

```text
1.4142
```

### IQR

Input:

```text
1, 2, 3, 4, 5, 6, 7, 8, 9
```

Output:

- Q1 = 2.5
- Q3 = 7.5
- IQR = 5.0

## Running Tests

```bash
python manage.py test
```

## Calculation History JSON

Each valid calculation is saved as one object in the top-level JSON list. The file
is created in the project root when the first calculation succeeds. Missing or
empty files start as an empty history, and each new record is appended without
removing earlier records. Invalid form submissions are never saved.

A Standard Deviation record contains:

```json
{
  "calculated_at": "2026-10-13T23:00:00+05:30",
  "operation": "standard_deviation",
  "original_values": [1.0, 2.0, 3.0, 4.0, 5.0],
  "calculation_method": "Population standard deviation",
  "intermediate_values": {
    "number_of_observations": 5,
    "mean": 3.0,
    "deviations_from_mean": [-2.0, -1.0, 0.0, 1.0, 2.0],
    "squared_deviations": [4.0, 1.0, 0.0, 1.0, 4.0],
    "sum_of_squared_deviations": 10.0,
    "population_variance": 2.0
  },
  "formulas": {
    "mean": "sum(values) / number_of_observations",
    "deviation": "value - mean",
    "squared_deviation": "deviation ** 2",
    "population_variance": "sum(squared_deviations) / number_of_observations",
    "population_standard_deviation": "sqrt(population_variance)"
  },
  "result": {
    "population_standard_deviation": 1.4142135623730951
  }
}
```

An IQR record keeps the entered order in `original_values` and the sorted order in
`sorted_values`. It also saves the lower and upper halves used by the selected
quartile method:

```json
{
  "calculated_at": "2026-10-13T23:00:00+05:30",
  "operation": "iqr",
  "original_values": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
  "sorted_values": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
  "calculation_method": "Tukey median-split: exclude the overall median when the list length is odd",
  "intermediate_values": {
    "lower_half": [1.0, 2.0, 3.0, 4.0],
    "upper_half": [6.0, 7.0, 8.0, 9.0],
    "q1": 2.5,
    "q3": 7.5
  },
  "formulas": {
    "q1": "median(lower_half)",
    "q3": "median(upper_half)",
    "iqr": "q3 - q1"
  },
  "result": {"q1": 2.5, "q3": 7.5, "iqr": 5.0}
}
```

### Checking the arithmetic by hand

For the standard deviation sample above, the deviations are `[-2, -1, 0, 1, 2]`;
their squares sum to `10`. Divide by `n = 5` to get population variance `2`, then
take its square root to get approximately `1.4142`. The web page rounds this
display to four decimal places; the JSON record preserves the full Python float.

For IQR, the odd-sized list's overall median (`5`) is left out of both halves.
The lower half has median `(2 + 3) / 2 = 2.5` and the upper half has median
`(7 + 8) / 2 = 7.5`; therefore `IQR = 7.5 - 2.5 = 5.0`.

The JSON I/O is isolated in `calculator/json_history.py`; mathematical details
are created in `calculator/calculations.py`. The local history file is plain
text, so open it in an editor or inspect it with:

```bash
python -m json.tool calculation_history.json
```

## Learning Notes

This project demonstrates how Django works in practice:

- URLs route browser requests to views
- Views receive GET and POST requests
- Forms validate input
- Calculation functions handle pure Python logic
- Templates display the final result
- Context passes values from backend to frontend

## Future Improvements

- Add a clear error summary near the form
- Move history to a database if the project later needs concurrent users or richer searches
- Improve styling with CSS layouts
- Include more stats functions such as mean and median
