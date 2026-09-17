# SiteNav

The portfolio navigation bar sits under the band with a 3px `accent-line` top rule; the current page gets `surface-fill` and a 3px ink underline.

## Consumer provides
- `<nav class="kt-nav">` with a `<ul>` of links; `aria-current="page"` on the active link.

## Rules
- Uppercase labels in the `nav` style, one word each.
- Five items is the limit this system allows; kyletran.dev currently runs six (Overview, Projects, Experience, About, Newsletter, Contact).
- Below 768px the list collapses into a stacked menu.
