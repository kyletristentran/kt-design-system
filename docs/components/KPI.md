# KPI

A KPI block states one figure with its label and a delta measured against a named basis.

## Consumer provides
- `.kt-kpi` with a treatment: `kt-kpi--accent` (the figure the view was opened for, one per view), `kt-kpi--stub` (supporting figures), `kt-kpi--alert` (one per row at most).
- Children `.kt-kpi__label`, `.kt-kpi__value`, `.kt-kpi__delta`.
- A delta wrapped in `.kt-up` or `.kt-down` with ▲ or ▼, followed by its basis (vs budget, QoQ, vs prior year).

## Rules
- A delta without a basis is not allowed.
- Figures carry their unit and period in the label.
- Use `figure-lg` (mono) instead of the sans value when the figure is a raw system value such as an ID.
- Sample figures are FICTITIOUS DATA.
