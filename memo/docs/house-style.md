# House style (Step 4)

This skill renders in the **KT CRE Design System**. `memo.css` is a downstream
consumer of the KT tokens (`../tokens/tokens.json`) — every hex in it comes from
that file. Do not introduce a colour that is not there.

To re-skin, edit the accent tokens at the top of `memo.css`
(`--accent-deep`, `--accent`, `--accent-line`, `--accent-tint`, `--accent-wash`) and the identity
defaults in `render_memo.py`. Nothing else names a colour.

## Direction

Corporate-legal register: austere, ruled, formal. The document opens with a
`PRIVILEGED AND CONFIDENTIAL` bar above the letterhead, numbers its sections
`1. 2. 3.`, states the decision in a **ruled** block rather than a tinted panel,
and closes with a signature-ruled *Prepared and reviewed* attestation. Body text
runs full measure so prose aligns to the same rules the tables do.

The house identity is **KTFORD**. The portfolio is **all industrial** — no
sample, profile name, or worked example may reference office, retail,
multifamily, or any other asset class. Leasing profiles are industrial subtypes:
warehouse, flex, distribution.

## The five invariants, as they land here

1. **Accent carries meaning, never decoration.** In a memo the Kytex Powder Blue budget is spent on exactly four things: the 3pt letterhead rule, the BLUF left rule, the decision block's left rule, and the bar fill. On white paper each of these uses the line tone `#6B97B8` (3.1:1), because `#B6D0E2` measures 1.6:1 against white. Exhibit ids and the trace index keys use deep accent `#3E6A8A` as text. The mark underscore sits on ink and keeps `#B6D0E2`. Nothing else is blue.
2. **Type on an accent field is always ink.** In the legal register the accent appears only as rules, so no field carries type at all — and white type on `#B6D0E2` never occurs.
3. **Mono is machine truth** — but the rule's stated reason is column alignment ("never mix the two inside a single number column"). So Consolas carries figures in **tables, KPI tiles, meta values, and the trace index**; a bound figure inside running prose keeps the body face and takes its emphasis from weight 600. Running prose has no column to align, and the reference document sets inline figures the same way.
4. **Structure comes from rules, not boxes.** 1px `#E0E0E0` hairline under section heads and the meta grid, 2pt ink divider above KPI tiles and total rows, 3pt accent rule under the letterhead. Two bordered blocks exist in the whole document: the decision block and the reconciliation callout, both square-cornered.
5. **Status is semantic, never brand.** Negative figures take `#B10E1C` *as text inside parentheses*, so the sign survives greyscale. The reconciliation callout uses caution `#A16E00` as border and label only — never as a fill behind body copy.

## Type

| Role | Face | Size |
|---|---|---|
| Body | Segoe UI (bundled fallback: Open Sans) | 10pt / 1.45 |
| Title | Segoe UI 700 | 15pt |
| Section head | Segoe UI 700 + 1px hairline, numbered | 11pt |
| Eyebrow / label | Segoe UI 700, uppercase, tracked | 8.5pt |
| Table body | Segoe UI (text) · Consolas (figures) | 9.5pt |
| Table header | Segoe UI 700 uppercase, white on ink | 8.5pt |
| Schedule figures | Consolas | 8.5pt |
| Trace index | Consolas | 9pt |

**Density is bought from padding and leading, never from figure size.** A number
the reader has to squint at is worse than a second page. When a schedule will
not fit, take the width back from the label column, cell padding, and the
landscape margins before touching type — and if it still will not fit, let it
run to another page.

**Figures never go below 8.5pt.** The brand's px label values (10px ≈ 7.5pt) come from the screen scale and are raised in print. Superscript trace marks stay off by default — at a legible size they overwhelm the prose. See "Reader copy vs audit copy" below.

Segoe UI and Consolas ship on the Office machines these documents are read on, so the CSS names them first. Open Sans and Inconsolata are bundled under the OFL as the fallback, so a Linux or CI render still looks right. Open Sans is Steve Matteson's, as Segoe UI is — the closest open analogue.

## Page

US Letter portrait, 0.7in sides / 0.78in top (band) / 0.62in bottom (footer). Wide schedules take a landscape page at 0.45in sides.

The **repeating page frame** lives in the Chromium header and footer templates, not in CSS: Chromium ignores CSS margin-box content and does not repeat `position: fixed` elements in print. The header is a full-bleed ink band carrying document class and subject; the footer is a 1px hairline over confidentiality (left) and `Page N of M` (right).

The letterhead — square mark with a 10%-height accent underscore, wordmark, right-aligned address block, then the 3pt accent rule — is in the document flow, so it appears on page one only, exactly as the document rules require.

## Exhibits

- Caption is `Exhibit A · Title` left, source range in Consolas right.
- Label ids in **citation order**; the verifier warns (S6) when they do not ascend.
- Header row: ink `#242424` fill, white uppercase — **never accent-filled**.
- Zebra `#FAFAFA` on even body rows. `total_rows` gives a 2pt ink top rule and `#F5F5F5` fill.
- **An exhibit never splits.** If it does not fit in the remaining space the whole block moves to the next page. A table cut across a fold is harder to read than a page with white at the bottom, and a reader comparing rows should never have to turn back. Chromium still breaks a table taller than a full page, which is unavoidable; `thead` repeats in that case.
- Columns are **even** — `table-layout: fixed`, label column 34% on data tables and 128pt on schedules, every value column an equal share.
- Negatives render as `($0.06)` in `#B10E1C` — parentheses are the second channel that survives greyscale.

## Schedules — the ARGUS report shape

`"type": "schedule"` renders the report shape every CRE reader already knows: a
label column, right-aligned value columns, blocks with subtotals. One primitive
covers both a thirteen-column monthly tenant cash flow and a two-column market
leasing profile comparison — the only difference is column count and whether the
values are numbers or literals like `Continue Prior`.

```json
{"id":"E","type":"schedule","title":"…","source":"Tenant CF!B4:O10",
 "stub":"For the months","periods":["Jan-26", "…"],"total_label":"Total",
 "meta_lines":["Property · amounts in USD","Forecast data only"],
 "decimals":2,
 "groups":[{"label":"Rental revenue","rows":[
   {"label":"Base rent","values":[0,0,11458],"total":114583},
   {"label":"Total rental revenue","values":[…],"total":80208,"kind":"sub"}]}],
 "note":"Results displayed are based on forecast data only."}
```

Row `kind`: `detail` (default, indented, zebra) · `sub` (hairline above) · `net`
(ink rules above and below, fill) · `grp` (implicit from a group label) ·
`spacer` · `dtl` / `dtlhdr` for the trailing details block.

- **More than eight columns takes its own landscape page** automatically, via the named `@page wide` rule. Chromium honours this only with `prefer_css_page_size`, which the renderer sets.
- **Four columns or fewer narrows to 74%** — a two-column schedule stretched full width leaves a canyon between label and value.
- **Pin `decimals` on any column whose values share a unit.** A rate column that renders `$22` beside `$20.50` reads as an error.
- **Zero renders bare only in a count column**; in a currency column it carries the unit its neighbours do.
- Schedules run at 8.5pt with a 9pt label column. Width comes from a 128pt label column, 4pt cell padding, and 0.45in landscape margins — not from shrinking the figures.

### Charts

A `chart` block draws CSS bars against a single ink baseline: no gridlines, no gradient, no 3D, no rounded caps. The fill is the first categorical colour, `#6B97B8` on paper. A source line prints beneath — a figure with no provenance is not evidence.

Add one only when every charted row is **commensurable** (same unit, same direction) and comparison across rows is the point. A three-row scenario table earns a chart; a nine-row P&L does not, and a table mixing a cost PSF with a revenue PSF must not be charted on one axis.

## Reader copy vs audit copy

By default the body reads clean and the appendix carries the full audit trail. Pass `--marks` (or `"trace_marks": true`) to stamp a superscript trace mark beside every bound figure — the audit copy, for the reviewer who wants to walk each number back to its cell without flipping to the appendix. Both copies verify identically.

## Anti-patterns

| Banned | Why |
|---|---|
| Accent-filled table headers | Header is ink; accent there blows the budget and fails the invariant |
| White type on `#B6D0E2` | Light field — fails contrast |
| A chart of non-commensurable rows | Actively misleading |
| A red or green filled row to flag status | Figure carries the colour; the row stays neutral so the eye can still scan |
| Any type below 9pt | Absolute floor |
| Exhibits cited out of alphabetical order | Reader loses the thread |
| More than four KPI tiles | The row compresses and the point is lost |
| A "Conclusion" restating the BLUF | The BLUF already did it; end on the risks or the ask |
| Real entity names or figures in a demo | Fixtures rule — use the KTFORD identity, invented industrial properties, label `FICTITIOUS DATA` |
| Office, retail, or any non-industrial asset class | The portfolio is all industrial |
| Splitting an exhibit across a page break | Move the whole block instead |
