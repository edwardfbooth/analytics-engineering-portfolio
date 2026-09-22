"""
Session 3 - Exercise 2: .loc vs .iloc.

.loc  -> label/condition-based access. Slices are INCLUSIVE on both ends.
.iloc -> position-based (integer) access. Slices are EXCLUSIVE on the end,
         exactly like normal Python list slicing.

Mixing these up is the pandas equivalent of the return/break/continue
confusion from session 1: both "select some rows," but they answer
different questions ("which rows satisfy this condition" vs "give me rows
3 through 5, positionally").
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_orders() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "orders.csv")


def first_n_rows_iloc(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Return the first n rows using .iloc (position-based).
    """
    return df.iloc[:n]


def select_columns_loc(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Return only the given columns, all rows, using .loc.
    """
    return df.loc[:, columns]


def row_by_order_id(df: pd.DataFrame, order_id: str) -> pd.Series:
    """
    Return the single row matching order_id, as a Series, using .loc with a
    boolean condition - NOT by assuming order_id lines up with the row's
    positional index (it won't, once anything upstream filters or sorts).
    """
    matches = df.loc[df["order_id"] == order_id]
    return matches.iloc[0]


def last_two_columns_iloc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the last two columns, all rows, using .iloc with negative
    indexing - same negative-index trick as Python lists/strings.

    TODO: implement with df.iloc[:, -2:].
    """
    return df.iloc[:, -2:]

if __name__ == "__main__":
    orders = load_orders()

    head3 = first_n_rows_iloc(orders, 3)
    assert len(head3) == 3
    assert head3.equals(orders.iloc[:3])

    subset = select_columns_loc(orders, ["order_id", "product_id", "quantity"])
    assert list(subset.columns) == ["order_id", "product_id", "quantity"]
    assert len(subset) == len(orders)

    first_id = orders.iloc[0]["order_id"]
    row = row_by_order_id(orders, first_id)
    assert row["order_id"] == first_id

    last_cols = last_two_columns_iloc(orders)
    assert list(last_cols.columns) == list(orders.columns[-2:])

    print("All checks passed.")
