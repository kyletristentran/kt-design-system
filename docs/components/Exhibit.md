# Exhibit

An exhibit is the evidence for one claim: a caption with its source range, an ink-header data table and, where the rows share a unit, a bar chart.

## Consumer provides
- `.kt-exhibit` with a `.kt-exhibit__cap` (`.kt-exhibit__id` "Exhibit A" plus title, and a mono `.kt-exhibit__src` range such as `Scenarios!B4:E7`).
- `table.kt-data` with `class="n"` on numeric cells, `tr.total` on subtotal and total rows, and `neg` on negative cells.
- Optionally `.kt-bars` rows and a `.kt-exhibit__note` naming the source.

## Rules
- Exhibit letters ascend in the order the prose cites them.
- Header row is ink with white labels, never accent. Label column 34%, value columns equal.
- Negatives print as `($0.06)` in `negative`; the parentheses keep the sign in greyscale.
- Chart only rows that share a unit and direction. One baseline, no gridlines, no gradient, fill `viz-1`.
- An exhibit never splits across a page; the whole block moves.
