"""
Session 2, Exercise 2 -- stdlib `csv` module.

Covers: csv.DictReader, csv.DictWriter, validating rows on read (reusing
the error-handling instincts from exercise 1), and writing cleaned data
back out.

Source data: data/orders_raw.csv -- intentionally messy: one row with a
missing quantity, one with a negative price, one with a non-numeric
quantity, plus one row referencing a product that doesn't exist in the
catalog (that last one is valid *here* -- it only gets dropped in
exercise 5, once the catalog join is in play).
"""

from __future__ import annotations

import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

ORDERS_PATH = os.path.join(DATA_DIR, "orders_raw.csv")
CLEANED_PATH = os.path.join(OUTPUT_DIR, "cleaned_orders.csv")


def read_orders(path: str) -> list[dict]:
    """
    Read a CSV of order lines into a list of dicts, one dict per row.

    Use csv.DictReader so each row comes back keyed by the header column
    names (order_id, product_id, quantity, unit_price, customer) rather
    than by position -- that's the whole point of DictReader over plain
    csv.reader for tabular data with a header row.

    Args:
        path: path to the CSV file.

    Returns:
        A list of dicts, one per data row. Values stay as raw strings --
        no type conversion here, that's the next function's job.
    """
    orders = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def filter_valid_orders(orders: list[dict]) -> list[dict]:
    """
    Keep only rows where quantity and unit_price are both usable numbers.

    A row is valid if `quantity` parses as a positive int AND
    `unit_price` parses as a positive float. Convert both fields on the
    returned dicts (don't leave them as strings) so downstream code
    doesn't have to reparse them. Rows that fail either check are
    dropped -- don't raise, just skip them; a single bad CSV row
    shouldn't crash a batch job.

    Watch the classic session-1 trap when you build each cleaned dict:
    use the row's actual value for a field (`row["quantity"]`), not a
    literal copy of the key name.

    Args:
        orders: raw rows as returned by read_orders (string values).

    Returns:
        A new list of dicts with only valid rows, quantity as int and
        unit_price as float. All other fields pass through unchanged.
    """
    valid = []
    for row in orders:
        try: 
            quantity = int(row["quantity"]) 
            unit_price = float(row["unit_price"])
        except ValueError:
            continue
        if quantity <= 0 or unit_price <= 0:
            continue
        new_row = dict(row) 
        new_row["quantity"] = quantity
        new_row["unit_price"] = unit_price
        valid.append(new_row)
    return valid


def write_cleaned_orders(orders: list[dict], path: str) -> None:
    """
    Write cleaned order rows to a CSV file using csv.DictWriter.

    Create the parent directory first if it doesn't exist yet -- this is
    what keeps `output/` generated-but-not-committed (it's covered by the
    repo's `.gitignore` pattern for `scripts/exercises/*/output/`).
    Column order in the output file should match `orders[0].keys()`.

    Args:
        orders: cleaned order dicts (as returned by filter_valid_orders).
        path: destination file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    headers = orders[0].keys()
    with open(path, mode="w",newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(orders)
    return 


if __name__ == "__main__":
    raw = read_orders(ORDERS_PATH)
    assert len(raw) == 8, f"expected 8 raw rows, got {len(raw)}"
    assert raw[0]["order_id"] == "1"
    assert isinstance(raw[0]["quantity"], str), "read_orders should not convert types"

    valid = filter_valid_orders(raw)
    assert len(valid) == 5, f"expected 5 valid rows, got {len(valid)}"
    assert all(isinstance(o["quantity"], int) for o in valid)
    assert all(isinstance(o["unit_price"], float) for o in valid)

    total_revenue = sum(o["quantity"] * o["unit_price"] for o in valid)
    assert abs(total_revenue - 174.90) < 0.01, f"expected 174.90, got {total_revenue}"

    write_cleaned_orders(valid, CLEANED_PATH)
    assert os.path.exists(CLEANED_PATH)
    with open(CLEANED_PATH, newline="", encoding="utf-8") as f:
        written = list(csv.DictReader(f))
    assert len(written) == 5

    print("02_csv_basics.py: all self-checks passed")
