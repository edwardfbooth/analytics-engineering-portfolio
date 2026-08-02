"""
Phase 1 - Session 1 - Exercise 1: Functions & Type Hints

Implement every function below. Requirements:
- Full type hints on every parameter and return value.
- A docstring with a one-line summary, plus Args/Returns/Raises where relevant.
- No third-party imports (stdlib only, and you shouldn't need any imports at all here).

Run this file directly to self-check: `python 01_functions_and_types.py`
The __main__ block below runs asserts against your implementations. No output = all good.
"""

from __future__ import annotations


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.
    """
    return (celsius * 9)/5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius.

    Args:
        fahrenheit: Temperature in degrees Fahrenheit.

    Returns:
        Temperature in degrees Celsius.
    """
    return round((fahrenheit - 32) * 5/9)


def mean(values: list[float]) -> float:
    """Compute the arithmetic mean of a list of numbers.

    Args:
        values: Non-empty list of numbers.

    Returns:
        The arithmetic mean.

    Raises:
        ValueError: If `values` is empty.
    """
    if not values: 
        raise ValueError("values must not be empty")
    return sum(values)/len(values)


def median(values: list[float]) -> float:
    """Compute the median of a list of numbers.

    Args:
        values: Non-empty list of numbers.

    Returns:
        The median value. For an even-length list, the average of the two
        middle values.

    Raises:
        ValueError: If `values` is empty.
    """
    if not values:
        raise ValueError("values must not be empty")
    sorted_vals = sorted(values)
    mid_numb = len(values)//2
    if len(values) % 2 == 0:
        return (sorted_vals[mid_numb] + sorted_vals[mid_numb-1])/2
    return sorted_vals[mid_numb]


def clamp(value: float, low: float, high: float) -> float:
    """Restrict `value` to the inclusive range [low, high].

    Args:
        value: The value to clamp.
        low: Lower bound (inclusive).
        high: Upper bound (inclusive).

    Returns:
        `low` if value < low, `high` if value > high, else `value` unchanged.

    Raises:
        ValueError: If `low` is greater than `high`.
    """
    if low > high:
        raise ValueError("Invalid range")
    elif value > high:
        return high
    elif value < low:
        return low
    return value


def is_within_range(value: float, low: float, high: float) -> bool:
    """Check whether `value` falls within the inclusive range [low, high].

    Args:
        value: The value to check.
        low: Lower bound (inclusive).
        high: Upper bound (inclusive).

    Returns:
        True if low <= value <= high, else False.
    """
    if value > high or value < low:
        return False
    return True


if __name__ == "__main__":
    # --- celsius_to_fahrenheit / fahrenheit_to_celsius ---
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert round(fahrenheit_to_celsius(32), 5) == 0
    assert round(fahrenheit_to_celsius(212), 5) == 100

    # --- mean ---
    assert mean([1, 2, 3]) == 2
    assert mean([10]) == 10
    try:
        mean([])
        raise AssertionError("mean([]) should have raised ValueError")
    except ValueError:
        pass

    # --- median ---
    assert median([1, 3, 2]) == 2          # odd length
    assert median([1, 2, 3, 4]) == 2.5     # even length
    original = [5, 1, 3]
    median(original)
    assert original == [5, 1, 3], "median() must not mutate the input list"
    try:
        median([])
        raise AssertionError("median([]) should have raised ValueError")
    except ValueError:
        pass

    # --- clamp ---
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    try:
        clamp(5, 10, 0)
        raise AssertionError("clamp() with low > high should have raised ValueError")
    except ValueError:
        pass

    # --- is_within_range ---
    assert is_within_range(5, 0, 10) is True
    assert is_within_range(-1, 0, 10) is False
    assert is_within_range(0, 0, 10) is True   # boundary inclusive
    assert is_within_range(10, 0, 10) is True  # boundary inclusive

    print("All checks passed.")
