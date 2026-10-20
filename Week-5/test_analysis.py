import contextlib
import io
import unittest
from unittest.mock import patch

from analysis import analyze, compare_countries_for_period
from data_preparation import prepare_records
from presentation import prompt_country, prompt_year_range, present_period_comparison


def prepared_sample():
    return prepare_records(
        [
            {"date": "2020-01-01", "duration": "1:00", "country": "USA"},
            {"date": "2021-12-31", "duration": "2:00", "country": "USA"},
            {"date": "2019-12-31", "duration": "3:00", "country": "Russia"},
            {"date": "2022-01-01", "duration": "4:00", "country": "Russia"},
        ]
    )


class AnalysisTests(unittest.TestCase):
    def test_period_comparison_includes_both_boundary_years(self):
        comparison = compare_countries_for_period(
            prepared_sample(), "USA", "Russia", 2020, 2021
        )

        self.assertEqual(comparison.country_a.eva_count, 2)
        self.assertEqual(comparison.country_a.total_duration_hours, 3.0)
        self.assertEqual(comparison.country_a.average_duration_hours, 1.5)
        self.assertEqual(comparison.country_b.eva_count, 0)
        self.assertEqual(comparison.country_b.total_duration_hours, 0.0)
        self.assertIsNone(comparison.country_b.average_duration_hours)
        self.assertEqual(comparison.greater_total_country, "USA")

    def test_equal_period_totals_report_tie(self):
        records = prepare_records(
            [
                {"date": "2020-01-01", "duration": "1:30", "country": "USA"},
                {"date": "2020-12-31", "duration": "1:30", "country": "Russia"},
            ]
        )
        comparison = compare_countries_for_period(records, "USA", "Russia", 2020, 2020)
        self.assertEqual(comparison.greater_total_country, "Tie")

    def test_existing_category_and_country_analysis(self):
        result = analyze(prepared_sample(), "USA", "Russia")
        self.assertEqual(result.category_counts, {"Short": 3, "Standard": 1, "Long": 0})
        self.assertEqual(result.first_country_total, 3.0)
        self.assertEqual(result.second_country_total, 7.0)
        self.assertEqual(result.greater_country, "Russia")

    def test_invalid_country_and_reversed_year_range_are_reprompted(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["Atlantis", "America"]):
            with contextlib.redirect_stdout(output):
                country = prompt_country("Country: ", ["Russia", "USA"])
        self.assertEqual(country, "USA")
        self.assertIn("Unknown country", output.getvalue())

        output = io.StringIO()
        with patch("builtins.input", side_effect=["2021", "2020", "2020", "2021"]):
            with contextlib.redirect_stdout(output):
                years = prompt_year_range()
        self.assertEqual(years, (2020, 2021))
        self.assertIn("Invalid year range", output.getvalue())

    def test_empty_country_average_is_presented_as_unavailable(self):
        comparison = compare_countries_for_period(
            prepared_sample(), "USA", "Russia", 2020, 2021
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            present_period_comparison(comparison)
        self.assertIn("Average EVA duration: unavailable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
