# Tabs

Tabs switch views inside a tool; the active tab is ink and bold with a 2px `accent-line` underline.

## Consumer provides
- A `.kt-tabs` container with `role="tablist"` and `<button class="kt-tab" role="tab" aria-selected>` children.
- Optionally a `.kt-crumb` breadcrumb above, with the current page in `<strong>`.

## Rules
- Five primary items at most.
- Only the active tab carries the accent.
- Tab labels are nouns in sentence case.
