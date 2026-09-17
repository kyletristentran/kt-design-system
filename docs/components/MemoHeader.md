# MemoHeader

The memo header opens page one: classification bar, letterhead with mark and address, 3pt `accent-line` rule, document class, title and the To / From / Date / Ref grid.

## Consumer provides
- A `.kt-paper` page containing, in order: `.kt-classbar`, `.kt-letterhead` (a `.kt-lockup` and `.kt-letterhead__addr`), `hr.kt-rule-accent`, a `.kt-eyebrow` document class, `h1.kt-memo-title` and `.kt-meta`.
- Meta values: recipient, author, date as `yyyy-mm-dd` and a reference in class-year-sequence form (`CR-26-0118`), both in `kt-meta__v--mono`.

## Rules
- The letterhead and accent rule appear on page one only; continuation pages carry the band and footer from PageFrame.
- The accent rule uses `accent-line` so it holds on white paper and in print.
- The title names the property and the decision in plain words. No slogans.
- Samples use the KTFORD identity with invented industrial properties and are labeled FICTITIOUS DATA.
