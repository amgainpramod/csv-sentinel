import argparse
import csv
from datetime import date
from pathlib import Path


REQUIRED_COLUMNS = ("order_id", "customer_email", "order_date")


def validate_csv(path: Path) -> list[str]:
    issues = []
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        headers = reader.fieldnames or []
        missing_headers = [column for column in REQUIRED_COLUMNS if column not in headers]
        if missing_headers:
            return [f"Missing required columns: {', '.join(missing_headers)}"]
        if len(headers) != len(set(headers)):
            return ["Column names must be unique."]

        first_seen = {}
        for row in reader:
            values = {column: (row.get(column) or "").strip() for column in REQUIRED_COLUMNS}
            for column in REQUIRED_COLUMNS:
                if not values[column]:
                    issues.append(f"Line {reader.line_num}: {column} is required.")

            order_id = values["order_id"]
            if order_id:
                first_line = first_seen.setdefault(order_id, reader.line_num)
                if first_line != reader.line_num:
                    issues.append(
                        f"Line {reader.line_num}: duplicate order_id {order_id!r} "
                        f"(first seen on line {first_line})."
                    )

            order_date = values["order_date"]
            if order_date:
                try:
                    parsed_date = date.fromisoformat(order_date)
                    if parsed_date.isoformat() != order_date:
                        raise ValueError("Expected YYYY-MM-DD")
                except ValueError:
                    issues.append(f"Line {reader.line_num}: order_date must be a valid YYYY-MM-DD date.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check required fields, order IDs, and dates in an orders CSV.")
    parser.add_argument("path", type=Path, help="Path to the orders CSV")
    args = parser.parse_args()

    try:
        issues = validate_csv(args.path)
    except (OSError, UnicodeError, csv.Error) as error:
        parser.exit(2, f"Could not read CSV: {error}\n")

    for issue in issues:
        print(issue)
    if issues:
        print(f"Found {len(issues)} issue(s).")
        return 1

    print("No validation issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
