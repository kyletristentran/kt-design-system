# KT Design System

Design tokens, a component stylesheet and usage guidelines for [kyletran.dev](https://kyletran.dev), my internal tools and dashboards, and the commercial real estate deliverables I produce (reports, tables, decks, memos and email).

The system combines two sources. The first is the KT CRE brand standard, which sets the neutral ramp, the Powder Blue accent (`#B6D0E2`), the number formats and the rules for tables, documents and slides. The second is the production CSS of kyletran.dev, which contributes the Crimson Text and Open Sans pairing, the square project and credential cards, the featured-case layout and the site navigation.

## Contents

| Path | Description |
| --- | --- |
| `tokens/tokens.json` | Source of truth: 45 color tokens in light and dark themes, 18 type styles in three families, spacing, radius, shadow and stroke tokens. Each token carries a usage note. |
| `css/tokens.css` | The tokens as CSS custom properties, with `data-theme` and `prefers-color-scheme` switching, plus a `.t-<style>` class for each type style. |
| `css/kt.css` | Component classes (`kt-btn`, `kt-field`, `kt-badge`, `kt-kpi`, `kt-table`, `kt-project` and others). It uses token variables only. |
| `docs/brand-book.md` | Usage rules for color, type, layout, content, identity and each output format. |
| `docs/components/` | One guideline file per component, covering the markup a consumer provides and the rules. |
| `preview/index.html` | A static showcase of every component with a theme toggle. |

## Usage

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Open+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/kt.css">

<div class="kt-kpi kt-kpi--accent">
  <div class="kt-kpi__label">NOI, YTD</div>
  <div class="kt-kpi__value">$4,812,300</div>
  <div class="kt-kpi__delta"><span class="kt-up">▲ 3.4%</span> vs budget</div>
</div>
```

Set `data-theme="dark"` on `<html>` to force the dark theme. Without the attribute, the page follows the operating system setting. To view the showcase locally, run `python3 -m http.server` from the repository root and open `/preview/`.

## Design decisions

- **Accent contrast.** Powder Blue measures 1.6:1 against white, so on light surfaces it appears only as a filled area with dark type. Thin strokes use `accent-line` (`#6B97B8`) and accent text uses `accent-deep` (`#3E6A8A`). On dark surfaces the accent works for fills, strokes and text.
- **Two corner regimes.** kyletran.dev uses square corners throughout. Tools and dashboards use the Fluent radii of 2, 4 and 6px.
- **Office output.** Word, Excel, PowerPoint and Outlook files use Segoe UI and Consolas, which ship with Office, so the files render the same on other machines.
- **Known contrast gaps.** Two source values fall below WCAG thresholds and are kept as they are: `rule-strong` control borders (1.5:1) and the `caution` fill color on white (4.4:1). The usage notes describe how each is compensated.

Sample figures in the previews are fictitious.

## License

MIT
