import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .calculations import (
    calculate_iqr_details,
    calculate_population_standard_deviation_details,
)
from .json_history import read_calculation_history, save_calculation_record


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statistical Calculator")

    def test_standard_deviation_page_loads(self):
        response = self.client.get(reverse("standard_deviation"))
        self.assertEqual(response.status_code, 200)

    def test_iqr_page_loads(self):
        response = self.client.get(reverse("iqr"))
        self.assertEqual(response.status_code, 200)


class CalculationLogicTests(TestCase):
    def setUp(self):
        self.history_directory = tempfile.TemporaryDirectory()
        self.history_path = (
            Path(self.history_directory.name) / "calculation_history.json"
        )
        self.save_history = patch(
            "calculator.views.save_calculation_record",
            side_effect=lambda record: save_calculation_record(record, self.history_path),
        )
        self.save_history.start()
        self.addCleanup(self.save_history.stop)
        self.addCleanup(self.history_directory.cleanup)

    def test_standard_deviation_valid_input(self):
        response = self.client.post(
            reverse("standard_deviation"),
            {"numbers": "1, 2, 3, 4, 5"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Population Standard Deviation")
        self.assertContains(response, "1.4142")
        records = read_calculation_history(self.history_path)
        record = records[0]
        self.assertEqual(record["operation"], "standard_deviation")
        self.assertEqual(record["original_values"], [1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(record["intermediate_values"]["mean"], 3.0)
        self.assertAlmostEqual(
            record["intermediate_values"]["sum_of_squared_deviations"], 10.0
        )
        self.assertAlmostEqual(
            record["result"]["population_standard_deviation"], 10**0.5 / 5**0.5
        )

    def test_iqr_valid_input(self):
        response = self.client.post(
            reverse("iqr"),
            {"numbers": "1, 2, 3, 4, 5, 6, 7, 8, 9"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Q1")
        self.assertContains(response, "Q3")
        self.assertContains(response, "IQR")
        self.assertContains(response, "5.0")
        record = read_calculation_history(self.history_path)[0]
        self.assertEqual(
            record["sorted_values"], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        )
        self.assertEqual(record["result"], {"q1": 2.5, "q3": 7.5, "iqr": 5.0})

    def test_invalid_input_is_rejected(self):
        response = self.client.post(
            reverse("standard_deviation"),
            {"numbers": "1, two, 3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not a valid number")
        self.assertEqual(read_calculation_history(self.history_path), [])

    def test_empty_input_is_rejected(self):
        response = self.client.post(
            reverse("standard_deviation"),
            {"numbers": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter numbers before submitting")
        self.assertEqual(read_calculation_history(self.history_path), [])

    def test_insufficient_values_are_rejected(self):
        response = self.client.post(
            reverse("iqr"),
            {"numbers": "1, 2, 3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IQR requires at least 4 numbers")
        self.assertEqual(read_calculation_history(self.history_path), [])

    def test_post_and_get_behaviour(self):
        get_response = self.client.get(reverse("standard_deviation"))
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(
            reverse("standard_deviation"),
            {"numbers": "10, 20, 30, 40, 50"},
            follow=True,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "Entered numbers")


class CalculationRecordTests(TestCase):
    def test_standard_deviation_record_contains_intermediate_values(self):
        record = calculate_population_standard_deviation_details([1, 2, 3, 4, 5])
        intermediate = record["intermediate_values"]

        self.assertEqual(intermediate["number_of_observations"], 5)
        self.assertEqual(intermediate["mean"], 3)
        self.assertEqual(intermediate["deviations_from_mean"], [-2, -1, 0, 1, 2])
        self.assertEqual(intermediate["squared_deviations"], [4, 1, 0, 1, 4])
        self.assertEqual(intermediate["sum_of_squared_deviations"], 10)
        self.assertEqual(intermediate["population_variance"], 2)
        self.assertAlmostEqual(
            record["result"]["population_standard_deviation"], 2**0.5
        )

    def test_iqr_record_contains_sorted_values_and_quartile_method(self):
        record = calculate_iqr_details([9, 1, 5, 3, 7, 2, 8, 4, 6])

        self.assertEqual(record["sorted_values"], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(record["intermediate_values"]["lower_half"], [1, 2, 3, 4])
        self.assertEqual(record["intermediate_values"]["upper_half"], [6, 7, 8, 9])
        self.assertEqual(record["result"], {"q1": 2.5, "q3": 7.5, "iqr": 5.0})
        self.assertIn("Tukey median-split", record["calculation_method"])
        self.assertIn("T", record["calculated_at"])


class JsonHistoryTests(TestCase):
    def test_missing_and_empty_files_are_empty_history(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calculation_history.json"
            self.assertEqual(read_calculation_history(path), [])

            path.write_text("  \n", encoding="utf-8")
            self.assertEqual(read_calculation_history(path), [])

    def test_records_are_appended_without_removing_existing_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calculation_history.json"
            first_record = {"operation": "standard_deviation", "result": {"value": 1}}
            second_record = {"operation": "iqr", "result": {"value": 2}}

            save_calculation_record(first_record, path)
            save_calculation_record(second_record, path)

            self.assertEqual(
                read_calculation_history(path), [first_record, second_record]
            )
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                [first_record, second_record],
            )

    def test_non_finite_json_values_are_not_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calculation_history.json"
            with self.assertRaises(ValueError):
                save_calculation_record({"result": float("nan")}, path)
            self.assertFalse(path.exists())
