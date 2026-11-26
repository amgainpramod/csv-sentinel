import argparse
import csv
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

        for row in reader:
            for column in REQUIRED_COLUMNS:
                if not (row.get(column) or "").strip():
                    issues.append(f"Line {reader.line_num}: {column} is required.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check required fields in an orders CSV.")
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

    print("All required fields are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
