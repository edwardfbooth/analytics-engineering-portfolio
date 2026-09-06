"""
Session 2, Exercise 1 -- Error handling.

Covers: try/except/else/finally, catching specific exceptions (never a
bare `except:`), re-raising with context (`raise ... from e`), and a
custom exception class for a business-rule violation.

Convention: implement each function where you see `# TODO`. Don't change
function signatures or the self-check block at the bottom -- those
asserts are your acceptance test. Run this file directly to check your
work: `python 01_error_handling.py`.
"""

from __future__ import annotations


class InvalidOrderError(Exception):
    """Raised when an order quantity fails business validation."""


def safe_divide(a: float, b: float) -> float:
    """
    Divide a by b, converting a ZeroDivisionError into a clearer ValueError.

    This is the standard "translate a low-level exception into a
    domain-meaningful one" pattern: callers of this function shouldn't
    need to know it's implemented with division under the hood, and they
    should get a message that says what actually went wrong instead of a
    bare ZeroDivisionError.

    Args:
        a: numerator.
        b: denominator.

    Returns:
        a / b as a float.

    Raises:
        ValueError: if b is zero. Must use `raise ... from e` so the
            original ZeroDivisionError is preserved in the traceback
            chain (check: the new exception's `__cause__` should be set).
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError("b must be a nonzero number") from e


def parse_int_or_default(value: str, default: int = 0) -> int:
    """
    Parse a string as an int, falling back to a default on failure.

    Demonstrates try/except/else: the `else` clause should hold the
    "parsing worked" path, not the fallback logic -- the fallback belongs
    in `except`. Putting success-path code in `else` instead of after the
    try block is what makes the distinction between "this line might
    raise" and "this line runs only if nothing raised" explicit to a
    reader.

    Args:
        value: the string to parse.
        default: value to return if parsing fails.

    Returns:
        The parsed int, or `default` if `value` is not a valid int.
    """
    try:
        result = int(value)
    except ValueError:
        return default
    else: 
        return result


def validate_order_quantity(quantity: int) -> int:
    """
    Validate that a quantity is usable for an order line.

    A quantity is valid if it is a positive int (> 0). Anything else --
    wrong type, zero, negative -- is a business-rule violation, not a
    Python type error, so it should surface as our own InvalidOrderError
    rather than leaking a generic TypeError or ValueError to the caller.

    Args:
        quantity: the quantity to validate.

    Returns:
        quantity, unchanged, if valid.

    Raises:
        InvalidOrderError: if quantity is not an int, or is <= 0.
    """
    if not isinstance(quantity, int) or quantity <= 0:
        raise InvalidOrderError(f"quantity must be a positive int, got {quantity!r}")
    return quantity
    


def parse_all_or_report(values: list[str]) -> tuple[list[int], list[str]]:
    """
    Parse a list of strings into ints, separating hits from misses.

    Walk `values` once. For each item that parses cleanly, append the int
    to the results list. For each item that fails, append a message
    (f"could not parse {item!r}") to the errors list instead -- do not
    stop at the first failure. This is a shape you'll reuse constantly:
    partial success over a batch, with failures collected instead of
    raised.

    Careful, this is where session 1's control-flow trap shows up again:
    use `continue` to move to the next item after logging an error, not
    `break` (which would abandon the rest of the batch) and not a bare
    `return` (which would exit the function early, dropping everything
    after the first bad item).

    Args:
        values: raw strings to parse.

    Returns:
        A tuple of (parsed_ints, error_messages).
    """
    parsed = []
    errors = []
    for item in values:
        try:
            parsed.append(int(item))
        except ValueError:
            errors.append(f"could not parse {item!r}")
            continue
    return parsed, errors
    


if __name__ == "__main__":
    # safe_divide
    assert safe_divide(10, 2) == 5.0
    try:
        safe_divide(1, 0)
        raise AssertionError("expected ValueError")
    except ValueError as e:
        assert e.__cause__ is not None, "use `raise ... from e` to preserve the original exception"

    # parse_int_or_default
    assert parse_int_or_default("42") == 42
    assert parse_int_or_default("not a number") == 0
    assert parse_int_or_default("not a number", default=-1) == -1

    # validate_order_quantity
    assert validate_order_quantity(3) == 3
    for bad in (0, -5, "3"):
        try:
            validate_order_quantity(bad)
            raise AssertionError(f"expected InvalidOrderError for {bad!r}")
        except InvalidOrderError:
            pass

    # parse_all_or_report
    parsed, errors = parse_all_or_report(["1", "2", "x", "4", "y"])
    assert parsed == [1, 2, 4]
    assert len(errors) == 2
    assert "x" in errors[0]

    print("01_error_handling.py: all self-checks passed")
