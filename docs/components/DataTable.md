# DataTable

The data table sets labels in sans and figures in right-aligned tabular mono, with an ink header row and a 2px divider above the total.

## Consumer provides
- `.kt-table-wrap` around `<table class="kt-table">` with `thead`, `tbody` and an optional `tfoot` total row.
- `class="kt-num"` on every numeric cell and its header.
- A `.kt-source` line under the table naming the source and as-of date.

## Rules
- Light theme: header is `table-head` ink with white labels, never accent. Dark theme: a plain row with a 2px `accent` rule beneath.
- Zebra uses `surface-raised`; hover uses `table-hover`.
- Currency `$#,##0`, cents only under $1,000. Percent `0.0%`, including zero. Dates `yyyy-mm-dd`.
- Never mix sans and mono inside one number column.
- One total row per block, never orphaned across a page break.
