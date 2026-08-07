"""
Phase 1 - Session 1 - Capstone: Sensor Readings Report

Wires together exercises 1-3: load data/sensor_readings.txt, classify each
valid reading, aggregate counts per classification and per sensor, write a
report file, and print a short summary to stdout.

You may import your functions from the sibling exercise files (same-folder
relative imports work when this is run as a plain script) or just copy the
two or three functions you actually need in here. Either is a legitimate
choice at this stage - the awkwardness of not having a real package
structure yet is intentional, it's what session 9 (packaging) fixes.

Run: `python 04_capstone_readings_report.py`
"""

from __future__ import annotations

from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "sensor_readings.txt"
REPORT_PATH = Path(__file__).parent / "output" / "session01_report.txt"


# --- Reuse from 03_file_io.py (copy your working implementations here, or import them) ---

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

    See 03_file_io.py for the full spec. Copy/import your implementation.
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


# --- Reuse from 02_control_flow.py ---

def classify_reading(value: float) -> str:
    """Classify a sensor reading into a severity band.

    See 02_control_flow.py for the full spec. Copy/import your implementation.
    """
    if value < 10:
            return 'LOW'
    elif 10 <= value < 30:
            return 'NORMAL'
    elif 30 <= value < 50:
            return 'HIGH'
    return 'CRITICAL'


# --- New for the capstone ---

def build_summary(records: list[dict]) -> dict:
    """Aggregate classified readings into summary counts.

    Args:
        records: List of valid reading dicts (from `load_readings`), each
            with at least "sensor_id" and "value" keys.

    Returns:
        Dict with two keys:
            "by_classification": dict mapping classification label
                ("LOW"/"NORMAL"/"HIGH"/"CRITICAL") to count.
            "by_sensor": dict mapping sensor_id to count of readings.
        Both built with manual loops, not comprehensions.
    """
    by_classification = {}
    by_sensor = {} 
    for record in records:
        reading = classify_reading(record["value"])
        if reading in by_classification:
            by_classification[reading] += 1
        else:
            by_classification[reading] = 1
        if record["sensor_id"] in by_sensor:
            by_sensor[record["sensor_id"]] += 1
        else:
            by_sensor[record["sensor_id"]] = 1
    return {"by_classification": by_classification, "by_sensor": by_sensor}



def write_summary_report(summary: dict, total_readings: int, out_path: Path) -> None:
    """Write the aggregated summary to a plain-text report file.

    Format (exact section headers matter for the self-check below):

        Sensor Readings Report
        ======================
        Total valid readings: {n}

        By classification:
          LOW: {count}
          NORMAL: {count}
          ...

        By sensor:
          S1: {count}
          ...

    Args:
        summary: Output of `build_summary`.
        total_readings: Total number of valid readings processed.
        out_path: Destination file path (parent dir created if missing).
    """
    # TODO: implement, mkdir(parents=True, exist_ok=True) on out_path.parent first
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as file:
        file.write(f"Sensor Reading Reports\n ======================\n Total valid readings {total_readings}\n\n")
        file.write(f"By classification:\n")
        for label, count in summary["by_classification"].items():
            file.write(f" {label}:{count}\n")
        file.write(f"By sensor:\n")
        for label, count in summary["by_sensor"].items():
            file.write(f" {label}:{count}\n")


def main() -> None:
    records = load_readings(DATA_PATH)
    summary = build_summary(records)
    write_summary_report(summary, total_readings=len(records), out_path=REPORT_PATH)

    print(f"Processed {len(records)} valid readings from {DATA_PATH.name}")
    print("By classification:", summary["by_classification"])
    print("By sensor:", summary["by_sensor"])
    print(f"Report written to {REPORT_PATH}")


if __name__ == "__main__":
    main()

    # --- self-check ---
    records = load_readings(DATA_PATH)
    assert len(records) == 17
    summary = build_summary(records)
    assert sum(summary["by_classification"].values()) == 17
    assert sum(summary["by_sensor"].values()) == 17
    assert set(summary["by_sensor"].keys()) == {"S1", "S2", "S3", "S4"}
    assert REPORT_PATH.exists()
    print("All checks passed.")
