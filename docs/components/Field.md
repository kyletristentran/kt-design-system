# Field

A labeled text input; numeric inputs are right-aligned mono on `accent-wash`, the same fill that marks hand-entered cells in Excel.

## Consumer provides
- A `.kt-field` wrapper holding a `<label for>` and an `<input class="kt-input">`.
- `kt-input--numeric` for figures, rates and IDs.
- `aria-invalid="true"` plus a `.kt-field__error` line when validation fails; `.kt-field__hint` for guidance.

## Rules
- Label sits above the field in the `label` style. Never use placeholder text as the label.
- Focus paints a 2px `focus` halo with an `ink` border. Never remove it.
- Error text states the cause and the fix ("Month must be 01 to 12. Use yyyy-mm-dd."), not an apology.
- Control borders use `rule-strong`, which is below 3:1; the visible label and focus ring carry the affordance.
