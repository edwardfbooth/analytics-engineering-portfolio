"""
Session 3 - Exercise 1: Series & DataFrame basics.

Sessions 1-2 used dicts-of-dicts and lists-of-dicts as your data structures
(catalog, orders, aggregates). A pandas DataFrame is the columnar version of
that same shape: instead of looping over a list of row-dicts, you operate on
whole columns (Series) at once.

This file: build a DataFrame two ways (from a dict of lists, and from a real
CSV), then answer the question pandas forces on you with every real dataset -
"what dtype is this, and why."
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def products_from_dict() -> pd.DataFrame:
    """
    Build a small DataFrame directly from a dict of lists (no file I/O).

    This is the "you already understand this shape" on-ramp - same logical
    structure as a list of row-dicts, just transposed into columns.
    """
    data = {
        "product_id": ["P001", "P002", "P003"],
        "name": ["Wireless Mouse", "Mechanical Keyboard", "USB-C Cable"],
        "category": ["Electronics", "Electronics", "Electronics"],
        "unit_price": [29.99, 89.50, 12.00],
    }
    return pd.DataFrame(data)


def load_products(path: Path = DATA_DIR / "products.csv") -> pd.DataFrame:
    """Load the full products dataset from CSV. No cleaning yet - that's session 4."""
    return pd.read_csv(path)


def load_orders(path: Path = DATA_DIR / "orders.csv") -> pd.DataFrame:
    """Load the full orders dataset from CSV. No cleaning yet - that's session 4."""
    return pd.read_csv(path)


def describe_dtypes(df: pd.DataFrame) -> dict[str, str]:
    """Return a {column_name: dtype_as_string} mapping for every column in df."""
    return {col: str(dtype) for col, dtype in df.dtypes.items()}


if __name__ == "__main__":
    # -- products_from_dict --
    df1 = products_from_dict()
    assert list(df1.columns) == ["product_id", "name", "category", "unit_price"]
    assert len(df1) == 3
    assert df1["unit_price"].dtype.kind == "f"  # float

    # -- load_products / load_orders --
    products = load_products()
    orders = load_orders()
    assert len(products) == 15, f"expected 15 products, got {len(products)}"
    assert len(orders) == 25, f"expected 25 orders, got {len(orders)}"

    # -- describe_dtypes --
    dtypes = describe_dtypes(products)
    assert dtypes["product_id"] == "object"   # strings load as 'object'
    assert dtypes["unit_price"] == "object"   # "$29.99" is a string, not a float - the trap
    assert dtypes["in_stock"] == "object"     # "yes"/"no" text, not bool

    order_dtypes = describe_dtypes(orders)
    assert order_dtypes["quantity"] == "int64"      # this one parses clean
    assert order_dtypes["order_date"] == "object"   # dates load as strings until you say otherwise

    print("All checks passed.")
    print(products.head())
    print(describe_dtypes(products))
