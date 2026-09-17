# Memo pipeline

This folder turns an Excel workbook into a decision memo PDF in the KT design system. Every figure in the memo is bound to the workbook cell it came from, and the build fails if a figure no longer matches its cell.

```
source.xlsx --extract_workbook.py--> workbook.json --(analyst)--> memo.json
memo.json + source.xlsx --verify_memo.py--> PASS / FAIL
memo.json --render_memo.py--> memo.pdf
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python extract_workbook.py source.xlsx -o workbook.json
python verify_memo.py memo.json source.xlsx          # must print PASS
python render_memo.py memo.json -o memo.pdf          # --marks for an audit copy
```

If an extracted figure reads `null` where the workbook shows a number, the file was saved without cached formula values. Open and save it in Excel, or recalculate it headless with LibreOffice, before extracting.

## The memo spec

`example_memo.json` shows the full shape. Prose never contains a typed number; it references `[[token]]` entries in `figures`, and each figure carries `value`, `kind` (`currency`, `percent`, `number`, `multiple` or `date`), `trace` (`Sheet!Cell`) and `label`. Exhibits are either data tables (with an optional bar chart) or `"type": "schedule"` for ARGUS-shaped reports. `meta` sets the letterhead and page frame.

`sample/KTFORD_CR-26-0118_2026-08_v1.pdf` is the example rendered from `example_memo.json`. Its source workbook is not included, so `verify_memo.py` cannot be run against it. All names and figures in it are fictitious.

## Files

| File | Purpose |
| --- | --- |
| `extract_workbook.py` | Maps every sheet: tables, labeled scalars, formulas, and an A1 trace for each value. |
| `verify_memo.py` | Reopens the workbook and checks every bound figure, token, exhibit order and the BLUF length. |
| `render_memo.py` | Substitutes figures, builds exhibits and schedules, and prints the PDF through headless Chromium with the repeating band and footer. |
| `memo_template.html`, `memo.css` | Page structure and print styles, using the KT tokens. |
| `fonts/` | Open Sans and Inconsolata (SIL Open Font License), used when Segoe UI and Consolas are not installed. |
| `docs/` | Memo structure, house style, workbook reading and the pre-delivery QA checklist. |
