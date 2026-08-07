# Phase 1 — Session 1 (Week 5): venv/pip + Python Fundamentals

Budget: 4h. Topics: venv/pip/requirements.txt, functions, type hints, docstrings, control flow, file I/O.

Destination in repo: `scripts/exercises/session_01/` — put this file, the four exercise scripts, and `data/sensor_readings.txt` in that folder structure once you copy them over.

---

## 0. Environment setup (20-30 min)

From the repo root:

**macOS/Linux/WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

**Windows (PowerShell):**
```powershell
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Verify:
```bash
python --version
which python   # or `where python` on Windows — must point inside venv/
```

`requirements.txt` stays empty this session — no third-party packages needed yet (pandas arrives session 3, pytest session 7). Just confirm it's still committed and `.gitignore` is still excluding `venv/`.

Checkpoint: `git status` should show a clean tree before you start writing code, and `venv/` should NOT show up as untracked.

---

## 1. Functions & type hints (45 min) — `01_functions_and_types.py`

Implement every `TODO`. No third-party imports. Each function needs a one-line docstring summary plus `Args`/`Returns`/`Raises` where relevant. Run the file directly (`python 01_functions_and_types.py`) — the `__main__` block has asserts that should all pass silently.

Functions: `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `mean`, `median`, `clamp`, `is_within_range`.

`mean`/`median` must raise `ValueError` on an empty list — don't let it crash on an unhandled `ZeroDivisionError` or `IndexError`. This is a light preview of session 2's error handling, not the main event.

---

## 2. Control flow (45 min) — `02_control_flow.py`

Functions: `classify_reading`, `batch_status_summary`, `find_first_failure`, `retry_countdown`.

Thresholds for `classify_reading`: `< 10` → `"LOW"`, `10-30` → `"NORMAL"`, `30-50` → `"HIGH"`, `> 50` → `"CRITICAL"` (boundaries inclusive on the lower bound of each band).

Use manual loops with `dict`, not comprehensions — those are session 2's topic, stay disciplined about not reaching for syntax you haven't formally covered yet.

---

## 3. File I/O (60 min) — `03_file_io.py`

Reads `data/sensor_readings.txt` — a deliberately messy synthetic log (blank lines, a comment line, missing fields, non-numeric values, extra whitespace).

Functions: `read_readings` (raw lines via `with open(...)`), `parse_line` (returns a `dict` or `None` on malformed input — this is where the light `try/except` from part 1 shows up again, on `float()` casting), `load_readings` (combines the two, skips malformed rows, should not crash on the bad data), `write_report` (writes a plain-text summary to a new file via `with open(..., "w")`).

Acceptance: running the file against `data/sensor_readings.txt` should silently skip every malformed line and produce a report file with only valid rows — no unhandled exceptions.

---

## 4. Capstone (45-60 min) — `04_capstone_readings_report.py`

Wire parts 1-3 together: load `data/sensor_readings.txt`, classify each valid reading, produce counts per classification and per sensor, write `output/session01_report.txt`, print a short summary to stdout.

You can import from the sibling files (same-folder relative imports work fine when run as a script) or just copy the two or three functions you need. Either is fine — this friction is intentional, it's the reason session 9 exists (packaging/project structure).

---

## 5. PR workflow (15-20 min)

```bash
git checkout -b phase1/session-01-fundamentals
git add scripts/exercises/session_01
git commit -m "Phase 1 session 1: fundamentals + file I/O exercises"
git push -u origin phase1/session-01-fundamentals
```
Open the PR against `main`, self-review the diff before merging (branch protection will block a direct push anyway).

---

## Acceptance checklist

- [ ] venv created, activated, `pip` upgraded, `requirements.txt` unchanged (still empty)
- [ ] All four exercise files run with no unhandled exceptions
- [ ] Every function has a type-hinted signature and a docstring
- [ ] `mean`/`median` raise `ValueError` on empty input, not a crash
- [ ] `03_file_io.py` skips malformed lines without crashing
- [ ] Capstone produces `output/session01_report.txt`
- [ ] Branch pushed, PR opened, merged through the Phase 0 workflow

## Report back with

Actual time vs. 4h budget, what felt easy/shaky, link to the PR/commit.
