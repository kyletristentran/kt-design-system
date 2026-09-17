This system covers kyletran.dev, internal tools and dashboards, and the CRE deliverables built for Kytex (reports, tables, decks, memos and email). It combines the KT CRE standard, with the Powder Blue accent adopted on 2026-09-10, with the editorial type and square card patterns already in production on kyletran.dev.

## Principles

- The neutral ramp does most of the work. Use `ink`, `ink-secondary`, `ink-muted` and `ink-label` on `surface`, `surface-page` and `surface-raised`. If a design seems to need another color, it usually needs another step on the ramp.
- The accent marks meaning: the active tab, the key figure, the approved row, the section break. Keep `accent` to about 5% of any view. Six accent marks on one page means five are wrong.
- Structure comes from rules, not boxes: `rule` hairlines, `rule-strong` control borders, a 2px `rule-divider` above totals, a 3px accent rule under the page header on page one only.
- Status is semantic and never borrows the accent. `positive`, `caution` and `negative` appear as 8px squares, 2px top rules, badges or text color, never as a fill behind body copy.
- Mono is for machine output: figures, IDs, cell references, file names.

## Content

- Write in a professional, academic register. No slogans, taglines or sales framing. State figures plainly with their unit and period ("NOI, YTD", "$4,812,300", "vs budget").
- Headings are plain descriptive labels: "Selected Work", "Pausing the loop when the canvas is off-screen". Never an imperative or an epigram.
- Sentence case in body copy and headings inside tools. Title case for page and section titles on kyletran.dev. Uppercase only through the `label`, `eyebrow`, `nav` and `button` styles.
- Button labels are verb first, two words at most: "Approve budget", "Export", "Reject".
- Errors state the cause and the fix: "Column F is text. Convert it to numbers and re-upload."
- Every table and chart names its source and as-of date in the `caption` style.
- No emoji in any output.
- Samples and demos use invented properties and are labeled FICTITIOUS DATA. Never show a real portfolio's name or figures.

## Color

- Page ground is `surface-page`; cards and tables sit on `surface`. The header band, hero and spotlight use `band` with `on-band` text.
- `accent` (#B6D0E2) is a light blue and fails as text or a thin line on white (1.6:1). On light surfaces:
  - use `accent` only as a filled area, with `on-accent` type (9.7:1), never white type;
  - use `accent-line` for thin strokes on `surface`: the tab underline, section square, KPI top rule and nav top rule;
  - use `accent-deep` for accent-colored text and links.
- On dark surfaces (`band`, and the whole dark theme) `accent` works for fills, strokes and text.
- `accent-wash` marks hand-entered inputs, in the interface and in Excel.
- Chart series follow `viz-1` through `viz-6` in order. `viz-6` grey is "other" and always last. Forecast series drop to `viz-6`. Group any tail beyond six categories rather than adding colors.
- Status text uses the `-text` tokens. `caution` itself is 4.4:1 on white, so caution copy uses `caution-text`.
- `rule-strong` control borders are 1.5:1 in both themes, kept from the source. Every control has a visible label and the `focus` ring.

## Dark theme

The dark theme is for interfaces inside a dark host, such as Claude desktop in dark mode, chat widgets and dark dashboards. Documents, slides, email and Excel stay light.

- Leave the page transparent so the host shows through; `surface` (#161616) is the stand-in for previews. Use no outer card, background or shadow. All shadow tokens resolve to `none`.
- Raised rows, zebra and fills are low-alpha white (`surface-raised`, `surface-fill`). Rules are `rgba(255,255,255,0.08)` and `0.14`.
- The table header becomes a plain `table-head` row with `table-head-text` labels and a 2px `accent` rule beneath.
- Type on an accent fill stays `on-accent` ink. The mark becomes an `ink` (#EDEDED) square with dark initials.
- Detect the host theme at runtime rather than hardcoding one; default to dark when detection fails. Date and time inputs set `color-scheme: dark`.

## Type

- Three families. `serif` (Crimson Text) sets the hero and section titles on kyletran.dev: `hero-title`, `section-title`, `section-title-sm`, and card titles. `sans` (Open Sans) sets everything else. `mono` (the Consolas stack) sets figures.
- Open Sans (400, 400 italic, 600, 700) and Inconsolata (400, 700) ship with this system as files under the SIL Open Font License, so PDF and CI renders match. Crimson Text, and Open Sans 500 for the nav, load from Google Fonts: `https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Open+Sans:wght@400;500;600;700&display=swap`.
- Office files (Word, Excel, PowerPoint, Outlook) use Segoe UI and Consolas, which ship with Office. The `sans` stack falls back to Segoe UI for the same reason.
- Interface body is `body` (14px); long-form reading on kyletran.dev is `body-lg` (16px). `small` sets table cells. Nothing smaller than `micro` (9px), which is the print floor.
- All currency, percentages and dates use tabular numerals. Never mix sans and mono within one number column.
- Number formats: currency `$#,##0` (cents only under $1,000); percent `0.0%`, including zero; multiples `0.00x`; dates `yyyy-mm-dd`.

## Layout, shape and depth

- Spacing steps are `space-1` to `space-8` (4, 8, 12, 16, 22, 26, 34, 46). Card padding is `space-5` to `space-7`; sections sit `space-6` apart.
- Two corner regimes. kyletran.dev is square: buttons, project cards and credential cards use `radius-none`. Tools and dashboards use Fluent radii: `radius-chip` for tags, `radius-control` for buttons and inputs, `radius-card` for cards and bordered tables. The mark is always square.
- Depth in tools is `shadow-rest`, `shadow-hover` and `shadow-shell`. Portfolio cards use `shadow-card` and lift 4px on hover with `shadow-card-hover`. Never stack shadows, and never pair a heavy shadow with a heavy border.
- Motion is limited to 150ms color and border transitions in tools and a 300ms lift on portfolio cards. Respect `prefers-reduced-motion`.
- No horizontal scroll at 375px. Wide tables scroll inside `.kt-table-wrap`.
- Focus is a solid 2px `focus` outline with a 2px offset: `accent-deep` on light (5.5:1 on `surface-page`), `accent` on dark.

## Identity

- The mark is a square `ink` field with the initials KT in bold sans and an `accent` underscore at 10% of its height. Clear space equals its height. Never place it on an `accent` field. The mark is set in type; the system carries no drawn logo file.
- The default lockup is mark plus wordmark ("Kyle Tran"). The mark alone is for favicons, slide corners and email mastheads at 40px or less.
- Company deliverables for Kytex set "KX" in the same mark.

## Iconography

- kyletran.dev uses Font Awesome 6.5 (solid and brands) for contact and file icons: `fa-envelope`, `fa-file-pdf`, `fa-arrow-right`, `fa-github`.
- Tools use inline SVG at 16 or 20px with a 1.5px stroke in `currentColor`, Lucide or Fluent geometry, one set per artifact.
- No emoji and no icon fonts inside tools.

## Per format

- Tables and Excel: `table-head` ink header with white labels, `surface-raised` zebra, `table-hover`, a 2px `rule-divider` above totals, frozen header row, `accent-wash` on input cells.
- Charts: one baseline, no gridlines, no gradients, no 3D; series in `viz` order.
- Documents other than memos: US Letter, 0.75in margins, 11pt body, 9pt floor. An `accent-line` rule under the letterhead on page one, `rule-strong` on continuation pages, and a footer with confidentiality and page N of M. File names follow `{PREFIX}_{REF}_{PERIOD}_v{N}.pdf`.
- Slides: 16:9, `ink` or white backgrounds only, `accent` fields with `on-accent` type only on section breaks. 24px minimum and 30px body at 1920 by 1080. Each headline states a finding, each data slide names its source, and no table runs past eight rows.
- Email: 600px, every style inlined, nested tables, no images, scripts or web fonts. Body 15px on 25px. The button is `on-accent` on `accent`; accent label text is `accent-deep` on `accent-wash`. Include a hidden preheader under 85 characters, the postal address and an unsubscribe link.

## Memoranda

Decision memos built from a workbook (capital requests, investment committee packages, variance explanations, close packages) follow the corporate-legal register below. The pipeline that produces them lives in `memo/` in the repository.

- No figure is typed into prose. Prose references `[[token]]` entries, each bound to a `Sheet!Cell`; `verify_memo.py` reopens the workbook and fails the build when a value no longer matches.
- Order on page one: PageFrame band, MemoHeader (classification bar, letterhead, `accent-line` rule, document class, title, meta grid), BottomLine (BLUF of 45 words or fewer, up to four KPI tiles, decision requested), then numbered MemoSection blocks, each defending one of three supports with an Exhibit.
- Close with the Reconciliation callout when tabs disagree, the risks table, the Attestation block and the trace index on its own page. No Conclusion section.
- Paper is always light. The accent budget is four marks, all in `accent-line`: the letterhead rule, the BLUF rule, the decision-block rule and the bar fill. Exhibit letters and trace keys use `accent-deep`. The mark underscore sits on ink and keeps `accent`.
- Type runs in the Memo (print) styles: `memo-body` 10pt, `memo-small` 9.5pt in tables, `memo-label` and `memo-figure` 8.5pt. Figures never go below 8.5pt; buy density from padding and leading instead.
- In a sentence, a bound figure keeps the body face at weight 600. Tables, tiles, meta values and the trace index set figures in mono.
- Negatives print in parentheses and in `negative`, so the sign survives greyscale. Reconciliation uses `caution` for border and label only.
- Exhibit letters ascend in citation order. An exhibit never splits across a page. Chart only rows that share a unit.
- Schedules with more than eight columns take a landscape page; four or fewer narrow to 74% width.
- When two tabs disagree, use the more conservative figure, say which, and list the conflict in the Reconciliation callout.
- Render, then read every page and run the greyscale test before sending. File names follow `{PREFIX}_{REF}_{PERIOD}_v{N}.pdf`.
- Samples use the KTFORD identity with invented industrial properties only, labeled FICTITIOUS DATA.
