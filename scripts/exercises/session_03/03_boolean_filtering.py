"""
Session 3 - Exercise 3: Boolean filtering.

SQL:     WHERE region = 'Sudeste' AND quantity > 2
pandas:  df[(df["region"] == "Sudeste") & (df["quantity"] > 2)]

Two rules that don't exist in plain Python, and that will bite you exactly
like the `except TypeError or ValueError` bug from session 2 bit you there:

1. Use `&` / `|`, never `and` / `or`, to combine boolean Series. `and`/`or`
   raise `ValueError: The truth value of a Series is ambiguous` - pandas
   can't tell if you mean "all values" or "any value" true, so it refuses
   to guess.
2. Parenthesize every individual condition. `&` binds tighter than `==`,
   so `df.a == 1 & df.b == 2` parses wrong (as `df.a == (1 & df.b) == 2`).
   Always: `(df.a == 1) & (df.b == 2)`.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_orders() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "orders.csv")


def filter_by_region_and_quantity(
    df: pd.DataFrame, region: str, min_quantity: int
) -> pd.DataFrame:
    """
    Return orders where region == `region` AND quantity >= min_quantity.
    """
    return df[(df["region"] == region) & (df["quantity"] >= min_quantity)]


def filter_by_regions(df: pd.DataFrame, regions: list[str]) -> pd.DataFrame:
    """
    Return orders whose region is one of `regions`.
    """
    return df[df["region"].isin(regions)]


def filter_by_product_prefix(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    Return orders whose product_id starts with `prefix` (e.g. "P00").
    """
    return df[df["product_id"].str.startswith(prefix)]


def filter_south_or_high_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return orders where region == "Sul" OR quantity > 5.
    """
    return df[(df["region"] == "Sul") | (df["quantity"] > 5)]

if __name__ == "__main__":
    orders = load_orders()

    r1 = filter_by_region_and_quantity(orders, "Sudeste", 2)
    assert len(r1) > 0
    assert (r1["region"] == "Sudeste").all()
    assert (r1["quantity"] >= 2).all()

    r2 = filter_by_regions(orders, ["Sul", "Norte"])
    assert len(r2) > 0
    assert r2["region"].isin(["Sul", "Norte"]).all()

    r3 = filter_by_product_prefix(orders, "P00")
    assert len(r3) > 0
    assert r3["product_id"].str.startswith("P00").all()

    r4 = filter_south_or_high_quantity(orders)
    assert len(r4) > 0
    assert ((r4["region"] == "Sul") | (r4["quantity"] > 5)).all()

    print("All checks passed.")
