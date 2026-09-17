# BottomLine

The decision blocks that follow the header: the bottom line (BLUF), up to four KPI tiles, and the decision requested.

## Consumer provides
- `.kt-bluf` with a `.kt-eyebrow` and one paragraph of 45 words or fewer that states the recommendation before any context.
- `.kt-tiles` holding two to four `.kt-tile` blocks, each a mono `.kt-tile__v` and a `.kt-tile__l` label with its unit.
- `.kt-ask` with the action, then a `dl` of Amount, Owner and By.

## Rules
- Every figure is bound to a workbook cell through the memo pipeline (`memo/` in the repository); none is typed by hand.
- A figure inside a sentence keeps the body face and takes weight 600 (`.kt-fig`). Tiles, tables and meta values use mono.
- KPI tiles take an ink top rule, not the accent, to protect the accent budget.
- More than four tiles is not allowed.
- The ask names an action, an owner, a date and an amount.
