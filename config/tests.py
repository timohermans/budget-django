import unittest
from datetime import date

from config.dates import subtract_one_month


class DatesTestCase(unittest.TestCase):
    def test_subtract_one_month__when_february__returns_january(self):
        test_cases = [
            (date(2025, 2, 1), date(2025, 1, 1)),
            (date(2025, 1, 1), date(2024, 12, 1)),
            (date(2025, 3, 31), date(2025, 2, 28)),
        ]

        for (input_date, expected_date) in test_cases:
            with self.subTest(f"{input_date.year}-{input_date.month}-{input_date.day} -> {expected_date.year}-{expected_date.month}-{expected_date.day}"):
                result = subtract_one_month(input_date)
                self.assertEqual(expected_date, result)
