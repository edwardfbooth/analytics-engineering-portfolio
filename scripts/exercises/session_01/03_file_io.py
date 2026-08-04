"""
Phase 1 - Session 1 - Exercise 3: File I/O

Reads data/sensor_readings.txt (deliberately messy) and produces a clean
report of the valid rows.

IMPORTANT (path): this script expects the data file at
    <this file's folder>/data/sensor_readings.txt
When you copy these exercises into scripts/exercises/session_01/, make sure
sensor_readings.txt lives in a `data/` subfolder next to this script.

Run this file directly to self-check: `python 03_file_io.py`
"""

from __future__ import annotations

from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "sensor_readings.txt"
REPORT_PATH = Path(__file__).parent / "output" / "session01_valid_readings_report.txt"


def read_readings(path: Path) -> list[str]:
    """Read every line of a text file into a list, stripped of whitespace.

    Args:
        path: Path to the file to read.

    Returns:
        List of lines with leading/trailing whitespace removed. Blank lines
        and comment lines (starting with '#') are still included here -
        filtering happens in `load_readings`, not here.

    Raises:
        FileNotFoundError: If `path` does not exist (let this propagate,
            don't swallow it - a missing input file is a real failure the
            caller needs to know about).
    """
    lines = []
    with path.open("r") as file:
        for line in file:
            lines.append(line.strip())
        return lines


def parse_line(line: str) -> dict | None:
    """Parse one '|'-delimited sensor reading line.

    Expected format: "timestamp|sensor_id|value|status" (exactly 4 fields,
    value must be castable to float).

    Args:
        line: A single already-stripped line (may be malformed).

    Returns:
        Dict with keys "timestamp" (str), "sensor_id" (str), "value" (float),
        "status" (str) if the line is well-formed, otherwise None.
    """
    fields = line.split("|") 
    if len(fields) != 4:
        return None
    timestamp = fields[0]
    sensor_id = fields[1]
    try:
        value = float(fields[2])
    except ValueError:
        return None
    status = fields[3]
    records = {
        "timestamp" : timestamp,
        "sensor_id" : sensor_id,
        "value" : value,
        "status" : status
    }
    return records


def load_readings(path: Path) -> list[dict]:
    """Load and parse all valid readings from a sensor log file.

    Skips blank lines, comment lines (starting with '#'), and any line
    that `parse_line` can't parse. Must not raise on malformed data - only
    a missing file should raise (propagated from `read_readings`).

    Args:
        path: Path to the sensor log file.

    Returns:
        List of valid reading dicts, in file order.
    """
    lines = read_readings(path)
    parsed = []
    for line in lines:
        if not line.strip() or line.startswith("#"): 
            continue
        record = parse_line(line)
        if parse_line(line) is None:
            continue
        parsed.append(record)
    return parsed


def write_report(records: list[dict], out_path: Path) -> None:
    """Write a plain-text report of valid readings to `out_path`.

    Creates the parent directory if it doesn't exist. One line per record,
    format: "{timestamp} | {sensor_id} | {value} | {status}".
    Ends with a final line: "Total valid readings: {n}".

    Args:
        records: List of reading dicts as produced by `load_readings`.
        out_path: Destination file path.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as file:
        for record in records:
            file.write(f'{record["timestamp"]} | {record["sensor_id"]} | {record["value"]} | {record["status"]}\n')
        file.write(f'Total valid readings: {len(records)}')


if __name__ == "__main__":
    lines = read_readings(DATA_PATH)
    assert isinstance(lines, list)
    assert any(line.startswith("#") for line in lines), "comment lines should still be present here"

    assert parse_line("2026-07-01T08:00:00|S1|22.4|OK") == {
        "timestamp": "2026-07-01T08:00:00",
        "sensor_id": "S1",
        "value": 22.4,
        "status": "OK",
    }
    assert parse_line("2026-07-01T08:25:00|S2||OK") is None          # empty value
    assert parse_line("2026-07-01T08:30:00|S3|N/A|WARN") is None     # non-numeric value
    assert parse_line("2026-07-01T08:35:00|S1|23.1") is None         # missing status field
    assert parse_line("this line is just garbage") is None           # wrong shape entirely
    assert parse_line("# a comment") is None

    records = load_readings(DATA_PATH)
    assert len(records) == 17, f"expected 17 valid readings, got {len(records)}"
    assert all(isinstance(r["value"], float) for r in records)

    write_report(records, REPORT_PATH)
    assert REPORT_PATH.exists()
    report_text = REPORT_PATH.read_text()
    assert "Total valid readings: 17" in report_text

    print("All checks passed.")
