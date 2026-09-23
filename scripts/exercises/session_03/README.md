# Session 3 — Pandas I (Series/DataFrame, `loc`/`iloc`, filtering, dtypes)

Week 7 of Phase 1. Budget: 4h. Sessions 1–2 ran over (2.06x on session 1) —
plan for slippage, log the actual, don't treat it as failure.

## Before you start

1. Add pandas to `requirements.txt` (first third-party dep in this repo):
   ```
   pandas>=2.2,<3.0
   ```
   Then `pip install -r requirements.txt`.
2. `git checkout -b session-03-pandas-i`.
3. Drop this whole `session_03/` folder (including `data/`) into
   `scripts/exercises/`.
4. Before calling any file done: `grep -rn "raise NotImplementedError" scripts/exercises/session_03/` should return nothing.

## Concept bridge: pandas ↔ SQL

You already think in SQL — use it as the anchor, not a fresh mental model:

- DataFrame ≈ a result set / table. Series ≈ a single column.
- `.loc[condition]` ≈ `WHERE` — label- or condition-based access.
- `.iloc[n]` ≈ purely positional access ("row 3"), no SQL equivalent —
  SQL result sets aren't ordered-and-indexable by default, DataFrames are.
- Boolean masking (`df[df.x > 5]`) ≈ `WHERE x > 5`.
- dtypes ≈ column types in a schema, except pandas infers them at load
  time from whatever's in the file, and gets it wrong constantly — a DDL
  statement doesn't have that problem.

**Where the analogy breaks, and where the session-2 bug pattern comes
back:** SQL's `AND`/`OR` work directly on boolean expressions. Pandas
boolean masks need `&`/`|`, with every condition parenthesized — plain
`and`/`or` on a Series raises `ValueError: The truth value of a Series is
ambiguous`. Same underlying mistake as `except TypeError or ValueError` in
session 2 (translating "either of these" into the wrong operator) — pandas
just has a different, stricter set of operators for it than core Python.
You'll almost certainly hit this in exercise 03. That's expected — read the
error, it's telling you exactly what's wrong.

## Time blocks (target, not a deadline)

| Block | ~Time | File | Focus |
|---|---|---|---|
| 1 | 60 min | `01_series_and_dataframe_basics.py` | Building Series/DataFrames, reading dtypes |
| 2 | 60 min | `02_loc_iloc_selection.py` | `.loc` vs `.iloc` |
| 3 | 60 min | `03_boolean_filtering.py` | `&`/`\|`, `.isin()`, `.str` accessor |
| 4 | 60 min | `04_dtypes_intro.py` | Coercing `object` → `float`/`bool` |

## Watch for (carried forward from sessions 1–2, now in pandas form)

- `and`/`or` instead of `&`/`|` in a boolean mask (see above) — and every
  individual condition parenthesized, since `&` binds tighter than `==`.
- Chained indexing (`df[mask]["col"] = value`) silently modifying a copy,
  not the original — pandas raises `SettingWithCopyWarning` when this
  happens. Full treatment is session 6; for now, the fix is always
  `df.loc[mask, "col"] = value` in one step, not two.
- `.loc` is label-based and slice-inclusive on both ends. `.iloc` is
  position-based and slice-exclusive, exactly like a Python list. Mixing
  these up is the pandas version of session 1's `return`/`break`/`continue`
  confusion — both "select some rows," different rules for which ones.
- Self-timebox 5 minutes on a bug before asking. Still the rule.

## Acceptance checklist

- [ ] `01`: builds a DataFrame from a dict of lists and from the CSVs; can
      state each column's dtype and explain *why* `unit_price` and
      `in_stock` load as `object` rather than numeric/bool.
- [ ] `02`: performs the same row/column selection correctly with both
      `.loc` and `.iloc`, and can say in one sentence when you'd reach for
      each.
- [ ] `03`: filters `orders.csv` on 2+ conditions with `&`/`|` and correct
      parenthesization, plus `.isin()` and a `.str` filter — without
      needing to fall back on `and`/`or`.
- [ ] `04`: converts `unit_price` from `"$29.99"` (object) to a real
      `float64` column, and `in_stock` from `"yes"/"no"` to `bool`, without
      mutating the input DataFrame.
- [ ] All four files run standalone (`python 0X_....py`) with every assert
      passing.
- [ ] `grep -rn "raise NotImplementedError"` in the session folder is empty.
- [ ] One commit per exercise file, PR opened, self-reviewed, merged.

## Check-in

Same protocol as sessions 1–2: actual time vs. 4h budget, what was
easy/shaky, link to the PR. I'll fold it into the Session Log and update
the trend line in Current State.
