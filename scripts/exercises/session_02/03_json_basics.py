"""
Session 2, Exercise 3 -- stdlib `json` module.

Covers: json.load/json.dump, handling json.JSONDecodeError explicitly,
and navigating nested structures without mixing up literal keys and
variables.

Source data:
    data/product_catalog.json          (valid)
    data/product_catalog_broken.json   (deliberately invalid -- trailing
                                         comma before a closing bracket)
"""

from __future__ import annotations

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

CATALOG_PATH = os.path.join(DATA_DIR, "product_catalog.json")
BROKEN_CATALOG_PATH = os.path.join(DATA_DIR, "product_catalog_broken.json")
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "catalog_summary.json")


def load_catalog(path: str) -> dict:
    """
    Load a product catalog JSON file.

    This is the "let it fail loudly" version: if the file is missing or
    the JSON is malformed, let FileNotFoundError / json.JSONDecodeError
    propagate -- don't catch them here. load_catalog_safe below is where
    you handle those cases gracefully. Keeping both versions side by side
    is deliberate: sometimes a caller wants the crash (a broken deploy
    config should fail fast and loud), sometimes it wants a fallback.

    Args:
        path: path to the catalog JSON file.

    Returns:
        The parsed catalog as a dict.
    """
    with open(path, "r", encoding="utf-8") as file:
        catalog = json.load(file)
    return catalog


def load_catalog_safe(path: str) -> dict | None:
    """
    Load a product catalog JSON file, returning None instead of raising.

    Catch FileNotFoundError and json.JSONDecodeError explicitly (two
    except clauses, or one clause with a tuple -- your call, but both
    must be named; no bare `except:`). Print one line describing which
    failure occurred before returning None, so a human running this
    script still sees what went wrong.

    Args:
        path: path to the catalog JSON file.

    Returns:
        The parsed catalog dict, or None if the file is missing or the
        JSON is invalid.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            catalog = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"An error occurred: {e}")
        return None
    return catalog


def get_products_by_category(catalog: dict, category: str) -> list[dict]:
    """
    Return all products in the catalog matching a given category.

    catalog["products"] is a list of dicts, each with a "category" key.
    Watch the session-1 trap here: you're comparing each product's
    *category value* (`product["category"]`) against the `category`
    argument -- not the literal string "category" against anything.

    Args:
        catalog: a loaded catalog dict (as returned by load_catalog).
        category: the category name to filter on, e.g. "Electronics".

    Returns:
        A list of product dicts whose "category" matches, in original
        order. Empty list if none match.
    """
    products = []
    for product in catalog["products"]:
        if product["category"] == category:
            products.append(product)
    return products


def save_summary(catalog: dict, path: str) -> None:
    """
    Write a small summary of the catalog to a JSON file.

    Summary shape:
        {
          "store": <catalog["store"]>,
          "product_count": <int>,
          "categories": <sorted list of unique category names>
        }

    Use json.dump with indent=2 so the output is human-readable. Create
    the parent directory first if it doesn't exist.

    Args:
        catalog: a loaded catalog dict.
        path: destination file path.
    """
    categories = set()
    for product in catalog["products"]:
        categories.add(product["category"])
    summary = {
        "store": catalog["store"],
        "product_count": len(catalog["products"]),
        "categories": sorted(categories)
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode="w",encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    catalog = load_catalog(CATALOG_PATH)
    assert catalog["store"] == "Loja Synthetic Retail"
    assert len(catalog["products"]) == 4

    try:
        load_catalog(BROKEN_CATALOG_PATH)
        raise AssertionError("expected json.JSONDecodeError")
    except json.JSONDecodeError:
        pass

    assert load_catalog_safe(BROKEN_CATALOG_PATH) is None
    assert load_catalog_safe(os.path.join(DATA_DIR, "does_not_exist.json")) is None
    assert load_catalog_safe(CATALOG_PATH) is not None

    electronics = get_products_by_category(catalog, "Electronics")
    assert len(electronics) == 2
    assert {p["product_id"] for p in electronics} == {"P001", "P003"}
    assert get_products_by_category(catalog, "Nonexistent") == []

    save_summary(catalog, SUMMARY_PATH)
    assert os.path.exists(SUMMARY_PATH)
    with open(SUMMARY_PATH, encoding="utf-8") as f:
        summary = json.load(f)
    assert summary["product_count"] == 4
    assert summary["categories"] == ["Electronics", "Home", "Office"]

    print("03_json_basics.py: all self-checks passed")
