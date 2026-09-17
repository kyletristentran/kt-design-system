# PageFrame

The page frame repeats on every page of a memo: a full-bleed ink band with the document class and subject, and a footer with confidentiality on the left and page N of M on the right.

## Consumer provides
- `.kt-band` at the top of the page and `.kt-footer` at the bottom, with two spans.
- In PDF output, the frame comes from the Chromium header and footer templates in `memo/render_memo.py`, because Chromium does not repeat CSS margin boxes or fixed elements.

## Rules
- US Letter portrait, 0.7in sides, 0.78in top, 0.62in bottom. Wide schedules take a landscape page at 0.45in sides.
- The footer text never goes below 8.5pt.
- File names follow `{PREFIX}_{REF}_{PERIOD}_v{N}.pdf`.
