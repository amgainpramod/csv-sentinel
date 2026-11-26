from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from validate_csv import validate_csv


class ValidateCsvTests(unittest.TestCase):
    def validate(self, contents: str) -> list[str]:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "orders.csv"
            path.write_text(contents, encoding="utf-8")
            return validate_csv(path)

    def test_valid_order(self):
        self.assertEqual(self.validate(
            "order_id,customer_email,order_date\n1001,alex@example.com,2024-02-29\n"
        ), [])

    def test_reports_duplicate_and_invalid_date_on_same_line(self):
        issues = self.validate(
            "order_id,customer_email,order_date\n"
            "1001,alex@example.com,2026-02-28\n"
            " 1001 ,alex@example.com,2026-02-29\n"
        )
        self.assertEqual(issues, [
            "Line 3: duplicate order_id '1001' (first seen on line 2).",
            "Line 3: order_date must be a valid YYYY-MM-DD date.",
        ])

    def test_date_requires_hyphens(self):
        self.assertEqual(self.validate(
            "order_id,customer_email,order_date\n1001,alex@example.com,20261126\n"
        ), ["Line 2: order_date must be a valid YYYY-MM-DD date."])

    def test_blank_fields_only_report_required_issues(self):
        self.assertEqual(self.validate(
            "order_id,customer_email,order_date\n ,alex@example.com, \n"
        ), ["Line 2: order_id is required.", "Line 2: order_date is required."])
