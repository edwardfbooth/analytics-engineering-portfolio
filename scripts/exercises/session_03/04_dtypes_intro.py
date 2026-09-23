"""
Session 3 - Exercise 4: dtypes and type coercion (intro).

Exercise 01 showed that unit_price loads as `object` (it's the string
"$29.99", not the float 29.99) and in_stock loads as `object` ("yes"/"no"
text, not a bool). That's the normal state of real-world CSV data - pandas'
type inference only kicks in on columns that are already unambiguously
parseable as numbers.

Full messy-data cleaning (missing values, duplicates, mixed formats) is
session 4. This is the narrower slice: fixing dtypes on data that's
otherwise clean, which is a precondition for anything numeric later - you
can't sum a string column, and depending on what you write, pandas won't
always error clearly; it may just do the wrong thing silently (string
concatenation instead of addition).
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_products() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "products.csv")


def price_to_float(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a COPY of df with unit_price converted from "$29.99" (str) to
    29.99 (float64). Must not mutate the DataFrame the caller passed in.
    """
    out = df.copy()
    out["unit_price"] = out["unit_price"].str.replace("$", "", regex=False).astype(float)
    return out


def in_stock_to_bool(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a COPY of df with in_stock converted from "yes"/"no" (str) to
    True/False (bool). Must not mutate the DataFrame the caller passed in.
    """
    out = df.copy()
    out["in_stock"] = out["in_stock"].map({"yes": True, "no": False})
    return out


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Apply both conversions above and return the fully-typed DataFrame."""
    return in_stock_to_bool(price_to_float(df))


if __name__ == "__main__":
    products = load_products()
    assert products["unit_price"].dtype == object  # confirm the trap first

    priced = price_to_float(products)
    assert priced["unit_price"].dtype.kind == "f"
    assert priced.loc[priced["product_id"] == "P001", "unit_price"].iloc[0] == 29.99

    stocked = in_stock_to_bool(products)
    assert stocked["in_stock"].dtype == bool

    clean = clean_products(products)
    assert clean["unit_price"].dtype.kind == "f"
    assert clean["in_stock"].dtype == bool

    # original must be untouched - functions return copies, never mutate in place
    assert products["unit_price"].dtype == object
    assert products["in_stock"].dtype == object

    total_value = clean["unit_price"].sum()
    assert total_value > 0
    print(f"Total catalog value if 1 unit each: ${total_value:.2f}")
    print("All checks passed.")
