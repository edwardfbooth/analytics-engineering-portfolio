"""
Session 2, Exercise 5 -- capstone: error handling + csv + json + comprehensions.

Joins the messy orders CSV to the JSON product catalog, dropping orders
that fail validation (exercise 1/2 logic) or reference a product_id not
present in the catalog, then aggregates revenue by category.

This is a hand-rolled join + group-by. Session 3 replaces the hand-rolled
join with pandas.merge and the manual aggregation loop below with
groupby().sum() -- worth remembering what it looks like without the
library, since that's the operation pandas is actually doing under the
hood.
"""

from __future__ import annotations

import json
import os
import csv

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

ORDERS_PATH = os.path.join(DATA_DIR, "orders_raw.csv")
CATALOG_PATH = os.path.join(DATA_DIR, "product_catalog.json")
REPORT_PATH = os.path.join(OUTPUT_DIR, "revenue_report.json")


def load_and_join(orders_path: str, catalog_path: str) -> list[dict]:
    """
    Read orders and the product catalog, and join them into enriched rows.

    Steps:
        1. Read orders_path as CSV and keep only valid rows (same rule as
           exercise 2: quantity parses as a positive int, unit_price
           parses as a positive float). You can re-implement that logic
           inline here, or import read_orders/filter_valid_orders from
           02_csv_basics.py -- your call.
        2. Read catalog_path as JSON and build a product_id -> product
           dict lookup (a dict comprehension, per exercise 4).
        3. For each valid order, look up its product_id in that lookup.
           If found, produce an enriched dict: the order's fields plus a
           "category" key from the matched product. If not found (the
           catalog doesn't have that product_id), skip that order --
           don't raise, a dangling reference shouldn't crash the batch.

    Args:
        orders_path: path to the orders CSV.
        catalog_path: path to the catalog JSON.

    Returns:
        List of enriched order dicts, each with at least: order_id,
        product_id, quantity (int), unit_price (float), category.
    """
    with open(orders_path, mode='r', newline="", encoding='utf-8') as file:
        orders = list(csv.DictReader(file))

    filtered_orders = []
    for order in orders:
        try:
            quantity = int(order["quantity"])
            unit_price = float(order["unit_price"])
        except ValueError:
            continue
        if quantity <= 0 or unit_price <= 0:
            continue
        valid_order = {**order, "quantity": quantity, "unit_price": unit_price}
        filtered_orders.append(valid_order)
    
    with open(catalog_path, 'r', encoding='utf-8') as file:
        catalog = json.load(file)

    products = {product["product_id"]: product for product in catalog["products"]}

    enriched_orders = [{**order, "category":products[order["product_id"]]["category"]} for order in filtered_orders if order["product_id"] in products]

    return enriched_orders

def revenue_by_category(enriched_orders: list[dict]) -> dict[str, float]:
    """
    Aggregate quantity * unit_price by category.

    This one is deliberately NOT a comprehension: a running total per
    category needs a mutable accumulator you update across iterations,
    and a comprehension can't do that cleanly (each iteration would need
    to see the running state of previous ones). Use a plain for-loop with
    `.get(category, 0.0)`, or a `collections.defaultdict(float)`.

    Args:
        enriched_orders: output of load_and_join.

    Returns:
        Dict mapping category name to total revenue, rounded to 2 decimals.
    """
    aggregates = {}
    for order in enriched_orders:
        total = order["unit_price"] * order["quantity"]
        aggregates[order["category"]] = aggregates.get(order["category"], 0.0) + total
    return {category: round(total,2) for category, total in aggregates.items()}

def write_report(report: dict, path: str) -> None:
    """
    Write the revenue-by-category report to a JSON file, indent=2.

    Create the parent directory first if it doesn't exist.

    Args:
        report: the dict returned by revenue_by_category.
        path: destination file path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    enriched = load_and_join(ORDERS_PATH, CATALOG_PATH)
    assert len(enriched) == 4, f"expected 4 enriched orders, got {len(enriched)}"
    assert all("category" in o for o in enriched)
    assert {o["order_id"] for o in enriched} == {"1", "3", "5", "8"}

    report = revenue_by_category(enriched)
    assert abs(report["Electronics"] - 119.40) < 0.01, report
    assert abs(report["Office"] - 25.50) < 0.01, report
    assert "Home" not in report

    write_report(report, REPORT_PATH)
    assert os.path.exists(REPORT_PATH)
    with open(REPORT_PATH, encoding="utf-8") as f:
        written = json.load(f)
    assert abs(written["Electronics"] - 119.40) < 0.01

    print("05_capstone_messy_data.py: all self-checks passed")
