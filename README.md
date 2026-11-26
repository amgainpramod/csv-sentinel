# CSV Sentinel

CSV Sentinel is a Python command-line tool that checks an orders CSV before import. It reports missing required columns, blank required fields, repeated order IDs, and invalid dates.

## Run the demo

Run these commands from the repository folder. Use Python 3.10 or later. The tool uses only the standard library.

```sh
python validate_csv.py examples/orders-invalid.csv
```

```text
Line 3: customer_email is required.
Line 4: duplicate order_id '1001' (first seen on line 2).
Line 4: order_date must be a valid YYYY-MM-DD date.
Found 3 issue(s).
```

```sh
python validate_csv.py examples/orders-clean.csv
```

```text
No validation issues found.
```

The required columns are `order_id`, `customer_email`, and `order_date`. Dates use `YYYY-MM-DD`. The email check verifies that the field contains a value.

| Exit code | Meaning |
| --- | --- |
| `0` | Validation passed |
| `1` | Validation found issues |
| `2` | The command could not read the file or received invalid arguments |

## How it works

`csv.DictReader` maps values to column names. The validator trims whitespace and keeps a dictionary of the first line on which each order ID appeared, so a duplicate report can point to both records. It reads the input one record at a time and retains the reported issues for the CLI to print.

## Run the tests

```sh
python -m unittest -v
```
