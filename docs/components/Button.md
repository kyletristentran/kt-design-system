# Button

Buttons trigger one action; the primary variant is filled with `accent` and set in `on-accent` ink.

## Consumer provides
- A `<button>` (or `<a>` for navigation) with `class="kt-btn"` plus at most one variant: `kt-btn--secondary`, `kt-btn--ghost`, `kt-btn--danger`.
- Optional size `kt-btn--sm` or `kt-btn--lg`; `kt-btn--square` for kyletran.dev surfaces, which use `radius-none`.
- The label text. The class uppercases it; write it in sentence case in source.

## Rules
- One primary button per view.
- Labels are verb first, two words at most: Approve budget, Export, Reject. Never "Submit" or a sentence.
- Type on `accent` is always `on-accent` (#242424). Never white.
- Disabled uses the `disabled` attribute, which paints `surface-fill` with `ink-disabled`.
- Danger is for destructive actions only and never sits beside a primary button.
