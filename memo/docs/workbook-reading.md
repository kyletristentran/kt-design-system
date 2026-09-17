# Reading the workbook (Steps 1–2)

## Running the extractor

```bash
python assets/extract_workbook.py source.xlsx -o workbook.json
python assets/extract_workbook.py source.xlsx -o pl.json --sheet "P&L"     # one tab
python assets/extract_workbook.py big.xlsx -o wb.json --max-rows 1200      # raise the cap
```

Output shape:

```json
{ "source_file": "...", "warnings": [...], "named_ranges": [...],
  "sheets": [{ "name": "P&L", "dimensions": "20 rows x 5 cols",
    "tables":  [{ "columns": [...], "column_kinds": [...], "rows": [[...]],
                  "row_traces": [[...]], "range": "B4:E13", "header_row": 4 }],
    "figures": [{ "label": "Requested capital", "value": 340000,
                  "trace": "Summary!C4", "kind": "currency" }],
    "formulas": [{ "trace": "P&L!C13", "formula": "=C7-C12", "value": 157000 }] }]}
```

## How detection works, and where it fails

**Tables** are found by scanning for a row with ≥ 2 text cells and ≤ 1 number (a header), then consuming rows below it until an empty row or a row with no numbers in the header's columns. This finds ordinary financial tables reliably. It misses:

- Tables with a merged or multi-row header — only the last header row is captured. Read the raw range yourself and write `columns` by hand in the memo spec.
- Tables whose first column is numeric (dates as row labels). The header heuristic may skip them.
- Two tables stacked with no blank row between them — they merge into one.
- Transposed layouts (periods down the side). Nothing detects this; transpose it yourself when you write the exhibit.

**Figures** are label-then-number pairs: a text cell with a number within three columns to its right. This is how summary tabs and assumption blocks are built, so it works well there and produces noise on dense grids. Capped at 80 per sheet.

`column_kinds` comes from the cell's Excel number format, not from the value. A percentage stored as `0.62` and formatted `0.0%` reads as `percent`; the same value formatted `General` reads as `number`. When the source workbook is sloppily formatted, set `column_kinds` explicitly in the exhibit rather than trusting the guess.

## Empty values mean the workbook was never recalculated

openpyxl writes formulas as strings with no cached result. A file that another tool wrote — including a workbook you just built — reads back `None` for every formula cell.

```bash
python LibreOffice headless (`soffice --headless --convert-to xlsx`) source.xlsx
```

Re-extract after recalculating. If figures are still `null`, the cell is genuinely empty or the formula errored.

**Caveat carried from the xlsx skill:** a workbook that links to another file loses those links when re-saved and recalculated. If formulas read like `='[1]Sheet'!$B$2`, copy the cached values out before touching the file.

## Reconciliation: the step that earns the fee

Before writing anything, look for the same quantity carried in two places. The common patterns:

| Pattern | How it shows up | What to do |
|---|---|---|
| Summary tab stale against the model | Summary hardcodes a figure the detail tab now computes differently | Use the conservative one, flag it |
| Scenario tab not rebuilt | Base case disagrees with the P&L | Say which drives the stated return |
| Rounding presented as precision | $118,500 vs $118,472 | Not a discrepancy; round consistently and move on |
| Period mismatch | "Year 1" means calendar on one tab, fiscal on another | Flag it — this one is usually a real error |
| Sign convention flip | Costs positive on one tab, negative on another | Normalize in the exhibit, note it |

A quick way to surface candidates:

```python
import json, collections
d = json.load(open("workbook.json"))
by_val = collections.defaultdict(list)
for s in d["sheets"]:
    for f in s["figures"]:
        if isinstance(f["value"], (int, float)) and abs(f["value"]) > 1:
            by_val[round(float(f["value"]), 2)].append((f["label"], f["trace"]))
# labels that SHOULD match but don't share a value are the interesting case:
# scan for the same label word appearing at different values
seen = collections.defaultdict(list)
for s in d["sheets"]:
    for f in s["figures"]:
        seen[f["label"].strip().lower()].append((f["value"], f["trace"]))
for label, hits in seen.items():
    vals = {v for v, _ in hits}
    if len(hits) > 1 and len(vals) > 1:
        print("MISMATCH", label, hits)
```

Same-label-different-value is the highest-yield check. Cross-tab quantities with *different* labels ("Year 1 EBITDA" vs "EBITDA") need your judgment — the script cannot see that they mean the same thing.

Every conflict you keep goes in `reconciliation[]`, phrased so a reader who has never opened the workbook understands what disagrees and which number this memo relied on.
