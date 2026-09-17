# QA gate (Step 5)

Run in this order. Do not deliver on a green verifier alone — half of what goes wrong is visible only in the rendered page.

```bash
python assets/verify_memo.py memo.json source.xlsx     # must print PASS
python assets/render_memo.py memo.json -o memo.pdf
pdftoppm -jpeg -r 110 memo.pdf pg                       # then Read every pg-*.jpg
```

Use `--strict` to make warnings blocking. Use `--keep-html` on `render_memo.py` when a layout defect needs debugging in the browser.

## Verifier codes

| Code | Severity | Meaning and fix |
|---|---|---|
| **F1** | FAIL | A figure has no resolvable `Sheet!Cell` trace. Every figure needs one; if the number is external, it is a secondary-tier citation and belongs in prose with its source named, not in `figures`. |
| **F2** | FAIL | The memo's value no longer matches the cell. Either the workbook changed (re-extract and update) or you typed the value by hand (find it in the extract). "Cell is empty" almost always means the workbook needs `recalc.py`. |
| **F3** | FAIL | A `[[token]]` in prose is not defined in `figures`. Usually a typo in the token name. |
| **F4** | FAIL | A bare numeric literal was typed into prose. Bind it to a figure, or — for a genuinely non-workbook number like a fiscal year — add the string to `allow_literals`. Lone digits are permitted, so "Year 1" and "month six" need no exemption. |
| **S1** | FAIL | No BLUF, or over 45 words. A memo without a bottom line is a status report. |
| **S2** | WARN | No decision requested. Accept only if the memo is informational by design — and say so in the ask block. |
| **S3** | WARN | An exhibit is never cited by a section. Cut the exhibit or make the claim it supports. |
| **S4** | WARN | A figure is defined but never used. Dead weight in the trace index. |
| **S5** | WARN | The BLUF hedges. State the claim and own it. |
| **S6** | WARN | Exhibit labels do not ascend in citation order. Relabel so the reader meets A first. |

## Brand gate (KT CRE)

- [ ] Every colour traces to `brand.json`. No stray hex in `memo.css`.
- [ ] Accent occupies ≤ ~5% of the surface: letterhead rule, BLUF rule, decision block rule, bar fill, all in `#6B97B8`. Nothing else blue.
- [ ] No white type on `#B6D0E2`. In the legal register the accent is rules only.
- [ ] Table headers are ink `#242424` with white type — never accent-filled.
- [ ] Zebra `#FAFAFA`; totals carry a 2pt `#242424` top rule.
- [ ] Currency `$#,##0` (cents only under $1,000); percent `0.0%` including zero; multiples `0.00x`; dates `yyyy-mm-dd`.
- [ ] Negatives in parentheses **and** `#B10E1C` — two channels, not one.
- [ ] Semantic colours appear as border, rule, or text only; never as a fill behind body copy.
- [ ] No figure below 8.5pt anywhere, including schedules, the footer, and the trace index.
- [ ] Charts: single baseline, no gridlines, no gradient, source line present.
- [ ] The mark is square, carries its accent underscore, and is not on an accent field.
- [ ] Footer confidentiality and `Page N of M` on every page; band on every page.
- [ ] Filename follows `{PREFIX}_{REF}_{PERIOD}_v{N}.pdf`.
- [ ] Demo files use the KTFORD identity with invented **industrial** properties, labelled `FICTITIOUS DATA`.

### The greyscale test

```python
from PIL import Image
Image.open("pg-3.jpg").convert("L").save("gs-3.jpg")   # then Read it
```

If any distinction disappears — a status, a variance sign, a highlighted row — the
document was relying on colour to carry meaning and needs a second channel: a
symbol, a rule, or a label. This is the real gate; a committee package gets printed.

## Read the pages

Things the verifier cannot see:

- [ ] A table runs past the right margin, or an exhibit split across a page (it should have moved whole)
- [ ] Column widths are even and figures are legible at arm's length
- [ ] The classification bar, section numbering, and attestation block are present
- [ ] No office, retail, or other non-industrial asset class appears anywhere
- [ ] A section heading sits alone at the foot of a page
- [ ] A bar chart implies a comparison that is not valid (non-commensurable rows)
- [ ] A chart's label column truncates with an ellipsis
- [ ] The KPI row compresses — more than four tiles, or a value too long for its tile
- [ ] Trace marks run in ascending order from the BLUF forward (they should start at 1)
- [ ] The reconciliation block reads as a flag, not as decoration
- [ ] The footer carries the right org and subject on every page
- [ ] Classification appears on page one
- [ ] Nothing on the last page but the trace index and the sign-off

## Content pass

- [ ] The BLUF names an action, an amount, and a reason — in that order
- [ ] Every section heading is a claim, not a topic
- [ ] Every claim with a number has that number bound to a cell
- [ ] Every cross-tab discrepancy found in Step 2 is disclosed, not buried
- [ ] The conservative figure was chosen where two conflicted, and the memo says which
- [ ] At least one risk response is a trigger and a decision, not a reassurance
- [ ] The ask has an owner and a date
- [ ] No paragraph over five lines

## Delivering

Ship the PDF. Ship `memo.json` alongside it whenever the memo will be revised or re-run against an updated workbook — regenerating is then:

```bash
python assets/verify_memo.py memo.json updated.xlsx && \
python assets/render_memo.py memo.json -o memo.pdf
```

If the workbook changed materially, F2 will name exactly which figures moved. That failure list is the changelog.
