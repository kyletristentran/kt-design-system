# Schedule

The schedule is the ARGUS report shape: a label column, right-aligned mono value columns, and grouped blocks with subtotals and a net line.

## Consumer provides
- `table.kt-sched` with `th.lab` for the stub and `.tot` on the total column.
- Row classes: `grp` (block label), `detail` (indented; add `zebra` on alternate rows), `sub` (hairline above), `net` (ink rules above and below, fill).
- `.kt-sched-lines` for property and unit lines above, `.kt-sched-note` below.

## Rules
- Figures stay at 8.5pt or larger. Width comes from the 128pt label column, 4pt cell padding and landscape margins, not smaller type.
- More than eight columns takes its own landscape page; four or fewer narrows to 74% width.
- Pin decimals on any column whose values share a unit.
