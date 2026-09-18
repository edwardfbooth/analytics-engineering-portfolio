# Session 2 — Error handling, stdlib `csv`/`json`, comprehensions

Phase 1, week 6. Budget: 4h. Session 1 ran 8h15 (2.06x over) — treat that
as a pacing warning, not a target. If you're past 5h and not done, stop,
commit what passes, and roll the rest into a follow-up rather than
burning the whole evening on it.

## Setup

```bash
cd ~/projects/analytics-engineering-portfolio
git checkout -b session-02-error-handling-csv-json
cd scripts/exercises/session_02
python --version   # no new deps this session, stdlib only
```

Each exercise file is a skeleton: function signatures + docstrings are
written, bodies are `raise NotImplementedError`. Implement each function,
then run the file directly — the `if __name__ == "__main__":` block at
the bottom is your self-check.

```bash
python 01_error_handling.py
```

No output until every assert passes; then you'll see
`"0X_....py: all self-checks passed"`. An `AssertionError` means either
your implementation is wrong or you haven't finished it yet — read the
message, it's usually specific about which check failed.

Generated output (cleaned CSVs, JSON reports) lands in `output/`, which
is gitignored — nothing to clean up manually.

## Debugging rule (from session 1)

Self-timebox 5 minutes on a bug: read the error, form one hypothesis,
try it. If it's not fixed in 5 minutes, that's the signal to ask, not a
failure.

## Time blocks (4h total)

| Block | Time | File | Focus |
|---|---|---|---|
| Warm-up | 15 min | — | Re-read session 1's recurring-bug list below before touching code |
| 1 | 45 min | `01_error_handling.py` | try/except/else/finally, custom exception, `raise ... from e` |
| 2 | 45 min | `02_csv_basics.py` | `csv.DictReader`/`DictWriter`, validating rows on read |
| 3 | 45 min | `03_json_basics.py` | `json.load`/`dump`, `JSONDecodeError`, nested lookups |
| 4 | 45 min | `04_comprehensions.py` | list/dict/set comprehensions, nested comprehension, generator expression |
| 5 | 45 min | `05_capstone_messy_data.py` | hand-rolled join + group-by, tying all four together |
| Wrap-up | 30 min | — | Self-review diff, commit, open PR, merge |

## Recurring bug patterns from session 1 — watch for these

- Augmented assignment typos: `=+` instead of `+=`.
- Literal string key vs. evaluated variable/expression as a dict key
  (`d["field"]` vs. `d[record["field"]]`) — this bit again in exercise 2
  and 3 on purpose; it's a conceptual gap worth over-practicing, not a
  one-off typo.
- `return`/`break`/`continue` confusion — exercise 1's `parse_all_or_report`
  is built specifically to catch this.

## Acceptance checklist

- [ ] All five files run standalone (`python 0X_*.py`) and print
      `all self-checks passed` with no `AssertionError` or unhandled
      exception.
- [ ] Can explain, without looking it up, when `else` vs. `finally` runs
      relative to `except` in a try block.
- [ ] Every `except` clause in your code names a specific exception —
      zero bare `except:` anywhere in the five files.
- [ ] Used `raise ... from e` at least once and can explain what it's
      for (preserving the original traceback vs. silently swallowing it).
- [ ] Used `csv.DictReader`/`DictWriter` and `json.load`/`dump` without
      needing to look up the API.
- [ ] Wrote at least one list, one dict, and one set comprehension
      unaided, plus the nested comprehension in exercise 4.
- [ ] Can explain why `revenue_by_category` in exercise 5 is a for-loop
      and not a comprehension.
- [ ] Zero hits on the session-1 recurring-bug list above, or if hit,
      self-caught within the 5-minute debugging timebox.
- [ ] One commit per exercise file on the feature branch; PR opened,
      self-reviewed, merged to close the session.

## Check-in (report at close)

Actual time vs. 4h budget, what felt easy/shaky, link to the PR.
