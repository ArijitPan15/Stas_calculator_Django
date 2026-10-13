# Statistical Calculator

A web-based statistical calculator built with **Python and Django** that calculates **Population Standard Deviation** and **Interquartile Range (IQR)** from comma-separated numeric input. The project demonstrates Django views, forms, templates, input validation, separation of calculation logic, and saving detailed calculation records to a JSON file.

## Features

- **Population Standard Deviation:** Calculates the population standard deviation for a list of numbers.
- **Interquartile Range (IQR):** Calculates the first quartile (Q1), third quartile (Q3), and IQR.
- **Input validation:** Handles empty input, invalid values, missing values between commas, `NaN`, and infinity.
- **Minimum data checks:** Requires at least 2 numbers for standard deviation and 4 numbers for IQR.
- **Calculation history:** Saves successful calculations, formulas, intermediate values, timestamps, and results to `calculation_history.json`.
- **Result pages:** Displays calculation results in browser-rendered Django templates.
- **Automated tests:** Uses Django's built-in test runner.

## Tech Stack

- **Language:** Python
- **Web framework:** Django
- **Frontend:** HTML and Django Templates
- **History storage:** JSON file
- **Database configuration:** SQLite (Django default configuration)
- **Testing:** Django Test Framework

## Calculations

### 1. Population Standard Deviation

Population standard deviation measures how spread out the values are around their mean.

\[
\sigma = \sqrt{\frac{\sum_{i=1}^{N}(x_i-\mu)^2}{N}}
\]

Where:
- `N` is the number of values.
- `xᵢ` is an individual value.
- `μ` is the population mean.
- `σ` is the population standard deviation.

**Example input**

```text
1, 2, 3, 4, 5
```

**Result:** `1.4142` (rounded to four decimal places)

### 2. Interquartile Range (IQR)

IQR measures the spread of the middle 50% of a sorted dataset.

\[
IQR = Q_3 - Q_1
\]

This project uses the **Tukey median-split method**:
1. Sort the values in ascending order.
2. Split the sorted values into lower and upper halves.
3. If the number of values is odd, exclude the overall median from both halves.
4. Calculate Q1 as the median of the lower half.
5. Calculate Q3 as the median of the upper half.
6. Subtract Q1 from Q3 to obtain the IQR.

**Example input**

```text
1, 2, 3, 4, 5, 6, 7, 8, 9
```

**Results**
- Q1: `2.5`
- Q3: `7.5`
- IQR: `5.0`

> Quartile values can differ between software packages because different quartile methods exist. This project uses the Tukey median-split method described above.

## Project Structure

```text
Stas_calculator/
├── manage.py
├── README.md
├── calculation_history.json
├── db.sqlite3
├── calculator/
│   ├── migrations/
│   ├── templates/
│   │   └── calculator/
│   │       ├── home.html
│   │       ├── calculator.html
│   │       └── result.html
│   ├── calculations.py
│   ├── forms.py
│   ├── json_history.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── statistical_calculator/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

**Important files**
- `calculations.py` — parsing and statistical calculations.
- `forms.py` — validates the numbers submitted by the user.
- `views.py` — handles browser requests and prepares result pages.
- `urls.py` — maps URL paths to views.
- `json_history.py` — saves calculation records to JSON.
- `templates/` — contains the HTML pages.
- `tests.py` — contains automated tests.
- `calculation_history.json` — stores successful calculation history; it may be created when the first successful calculation is saved.

## Getting Started

### Prerequisites

- Python installed on your computer.
- A terminal or command prompt.
- `pip`, Python's package installer.

### 1. Download or clone the project

Open a terminal in the project directory, where `manage.py` is located.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install Django

```bash
python -m pip install Django
```

If the project includes a `requirements.txt` file, you can install its dependencies with:

```bash
python -m pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Open the application

Visit:

```text
http://127.0.0.1:8000/
```

Stop the development server with `Ctrl + C`.

## How to Use

1. Open the application's home page.
2. Select the Standard Deviation or IQR calculator.
3. Enter numbers separated by commas, for example: `10, 20, 30, 40`.
4. Submit the form.
5. View the calculated result.
6. After a successful calculation, the application attempts to append a detailed record to `calculation_history.json`.

## Calculation History

Each successful calculation can store:
- Timestamp and operation name.
- Original input values.
- Calculation method.
- Intermediate values used in the calculation.
- Formula descriptions.
- Final result.

The JSON file can be inspected in a terminal with:

```bash
python -m json.tool calculation_history.json
```

The history is stored in a local JSON file rather than in a database model. Keep a backup if you need to preserve it. In a multi-user or production deployment, a database-backed history would generally be more suitable.

## Running Tests

Run the project's automated tests with:

```bash
python manage.py test
```

## What I Learned

This project provides practice with:
- Building a web application using Django.
- Routing requests through URLs and views.
- Handling form submissions with GET and POST requests.
- Validating and parsing user input.
- Separating mathematical logic from web logic.
- Rendering dynamic results using Django templates.
- Reading and writing JSON data with Python.
- Writing and running automated tests.

## Possible Future Improvements

- Add more statistical operations, such as mean, median, variance, and range.
- Add a history page to browse previous calculations.
- Allow users to download calculation results as a JSON or CSV file.
- Improve responsive styling and accessibility.
- Add database-backed history and user-specific records.
- Deploy the application using production-ready Django settings.

## Security and Deployment Notes

This project is intended for local development and learning. Before deploying it publicly:
- Set `DEBUG = False`.
- Store `SECRET_KEY` in an environment variable and replace the development key.
- Configure `ALLOWED_HOSTS`.
- Review Django's deployment checklist.
- Avoid committing virtual environments, local databases, or sensitive configuration to version control.

## License

No license is specified yet. Add a `LICENSE` file if you want to define how others may use, modify, and distribute this project.
