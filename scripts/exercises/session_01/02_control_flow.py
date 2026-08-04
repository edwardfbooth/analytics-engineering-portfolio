"""
Phase 1 - Session 1 - Exercise 2: Control Flow

Implement every function below using if/elif/else, for, and while loops.
Do NOT use list/dict comprehensions here - that's next session's topic
(session 2: error handling, stdlib csv/json, comprehensions). Use plain
loops with .append() / dict assignment instead, deliberately.

Run this file directly to self-check: `python 02_control_flow.py`
"""

from __future__ import annotations


def classify_reading(value: float) -> str:
    """Classify a sensor reading into a severity band.

    Bands (lower bound inclusive):
        value < 10          -> "LOW"
        10 <= value < 30     -> "NORMAL"
        30 <= value < 50     -> "HIGH"
        value >= 50          -> "CRITICAL"

    Args:
        value: The sensor reading.

    Returns:
        One of "LOW", "NORMAL", "HIGH", "CRITICAL".
    """
    if value < 10:
        return 'LOW'
    elif 10 <= value < 30:
        return 'NORMAL'
    elif 30 <= value < 50:
        return 'HIGH'
    return 'CRITICAL'


def batch_status_summary(statuses: list[str]) -> dict[str, int]:
    """Count occurrences of each status string in a list.

    Args:
        statuses: List of status strings, e.g. ["OK", "WARN", "OK", "FAIL"].

    Returns:
        Dict mapping each distinct status to its count, e.g.
        {"OK": 2, "WARN": 1, "FAIL": 1}.
    """
    counts = {}
    for status in statuses:
        if status in counts:
            counts[status] += 1
        else:
            counts[status] = 1
    return counts


def find_first_failure(records: list[dict]) -> int | None:
    """Find the index of the first record whose 'status' is 'FAIL'.

    Args:
        records: List of dicts, each expected to have a 'status' key.

    Returns:
        The index of the first record with status == "FAIL", or None if
        there isn't one.
    """
    for index, record in enumerate(records):
        if record["status"] == "FAIL":
            return index
    return None


def retry_countdown(attempts: int) -> list[str]:
    """Simulate a retry countdown, returning one log line per attempt.

    Counts down from `attempts` to 1, producing a line like
    "Attempt 3 of 3..." for each step, in descending order.

    Args:
        attempts: Total number of attempts, must be >= 1.

    Returns:
        List of log line strings, one per attempt, highest attempt number first.

    Raises:
        ValueError: If attempts < 1.
    """

    if total_attempts < 1:
            raise ValueError("attempts is smaller than 1")
    total_attempts = attempts
    lines = []
    while attempts >= 1:
        lines.append(f"Attempt {attempts} of {total_attempts}...")
        attempts -= 1
    return lines


if __name__ == "__main__":
    # --- classify_reading ---
    assert classify_reading(5) == "LOW"
    assert classify_reading(9.99) == "LOW"
    assert classify_reading(10) == "NORMAL"
    assert classify_reading(29.99) == "NORMAL"
    assert classify_reading(30) == "HIGH"
    assert classify_reading(49.99) == "HIGH"
    assert classify_reading(50) == "CRITICAL"
    assert classify_reading(1000) == "CRITICAL"

    # --- batch_status_summary ---
    result = batch_status_summary(["OK", "WARN", "OK", "FAIL", "OK"])
    assert result == {"OK": 3, "WARN": 1, "FAIL": 1}
    assert batch_status_summary([]) == {}

    # --- find_first_failure ---
    records = [{"status": "OK"}, {"status": "WARN"}, {"status": "FAIL"}, {"status": "FAIL"}]
    assert find_first_failure(records) == 2
    assert find_first_failure([{"status": "OK"}]) is None
    assert find_first_failure([]) is None

    # --- retry_countdown ---
    lines = retry_countdown(3)
    assert lines == [
        "Attempt 3 of 3...",
        "Attempt 2 of 3...",
        "Attempt 1 of 3...",
    ]
    assert retry_countdown(1) == ["Attempt 1 of 1..."]
    try:
        retry_countdown(0)
        raise AssertionError("retry_countdown(0) should have raised ValueError")
    except ValueError:
        pass

    print("All checks passed.")
