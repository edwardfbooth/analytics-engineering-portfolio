"""
Session 2, Exercise 4 -- comprehensions.

Covers: list, dict, and set comprehensions; a filter condition inside a
comprehension; a nested comprehension; a generator expression.

No external data needed -- all inputs are constructed in the self-check
block, so this file runs standalone.
"""

from __future__ import annotations


def squares_of_evens(numbers: list[int]) -> list[int]:
    """
    Return the square of every even number in `numbers`, in order.

    The canonical single-line comprehension: a transform (`n * n`) plus a
    filter (`n % 2 == 0`) in one expression. Implement this as one list
    comprehension, not a for-loop with `.append()`.

    Args:
        numbers: input integers, any order, may include negatives.

    Returns:
        Squares of the even numbers, same relative order as the input.
    """
    squares_of_evens = [n * n for n in numbers if n % 2 == 0]
    return squares_of_evens


def price_lookup(products: list[dict]) -> dict[str, float]:
    """
    Build a name -> price lookup from a list of product dicts.

    Each product dict has "name" and "price" keys. Implement as a dict
    comprehension: `{expr_key: expr_value for item in products}`.

    Args:
        products: list of dicts, each with "name" (str) and "price" (float).

    Returns:
        Dict mapping product name to price.
    """
    product_price = {product["name"]: product["price"] for product in products}
    return product_price


def unique_categories(products: list[dict]) -> set[str]:
    """
    Return the set of distinct category values across all products.

    Implement as a set comprehension -- the right tool whenever you need
    "all the distinct X values" and don't care about order or duplicates.

    Args:
        products: list of dicts, each with a "category" key.

    Returns:
        Set of unique category strings.
    """
    categories = {product["category"] for product in products}
    return categories


def flatten_nested_orders(orders_by_customer: dict[str, list[dict]]) -> list[dict]:
    """
    Flatten a dict of customer -> list of orders into one list of orders,
    tagging each order with which customer it belongs to.

    orders_by_customer looks like:
        {"Ana": [{"order_id": 1, "total": 59.7}], "Bruno": [...]}

    Each dict in the output should be the original order dict plus a
    "customer" key -- `{**order, "customer": name}` is the pattern.
    Implement as a single nested comprehension: customers in the outer
    loop, that customer's orders in the inner loop.

    Args:
        orders_by_customer: mapping of customer name to their list of
            order dicts.

    Returns:
        Flat list of order dicts, each carrying a "customer" key. Result
        order follows the input dict's iteration order, then each
        customer's list order.
    """
    orders = [{**order, "customer":customer} for customer, orders in orders_by_customer.items() for order in orders]
    return orders


def sum_over_threshold(numbers: list[float], threshold: float) -> float:
    """
    Sum every number strictly greater than `threshold`.

    Implement with a generator expression passed directly to sum()
    (`sum(n for n in numbers if n > threshold)`), not a list
    comprehension. For a pure reduction like this, the generator never
    materializes the intermediate list -- worth building the habit now,
    even at toy data sizes, because the habit is what matters once the
    lists stop being toy-sized.

    Args:
        numbers: input numbers.
        threshold: exclusive lower bound.

    Returns:
        Sum of all numbers > threshold. 0.0 if none qualify.
    """
    result = sum(n for n in numbers if n > threshold)
    return result

if __name__ == "__main__":
    assert squares_of_evens([1, 2, 3, 4, 5, 6]) == [4, 16, 36]
    assert squares_of_evens([-4, -3, -2]) == [16, 4]

    products = [
        {"name": "Wireless Mouse", "category": "Electronics", "price": 19.90},
        {"name": "Notebook Stand", "category": "Office", "price": 25.50},
        {"name": "USB-C Cable", "category": "Electronics", "price": 12.00},
    ]
    assert price_lookup(products) == {
        "Wireless Mouse": 19.90,
        "Notebook Stand": 25.50,
        "USB-C Cable": 12.00,
    }
    assert unique_categories(products) == {"Electronics", "Office"}

    orders_by_customer = {
        "Ana": [{"order_id": 1, "total": 59.7}, {"order_id": 5, "total": 25.5}],
        "Bruno": [{"order_id": 8, "total": 19.9}],
    }
    flat = flatten_nested_orders(orders_by_customer)
    assert len(flat) == 3
    assert flat[0] == {"order_id": 1, "total": 59.7, "customer": "Ana"}
    assert flat[2] == {"order_id": 8, "total": 19.9, "customer": "Bruno"}

    assert sum_over_threshold([10, 20, 30, 40], 15) == 90
    assert sum_over_threshold([1, 2, 3], 100) == 0.0

    print("04_comprehensions.py: all self-checks passed")
