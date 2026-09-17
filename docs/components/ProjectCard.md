# ProjectCard

The project card presents one case study on kyletran.dev: a band-colored media header, meta line, serif title, description, tool tags and a link.

## Consumer provides
- An `<a class="kt-project">` linking to the case study.
- `.kt-project__media` with a cover image (`<img>` fills it) or left as a `band` block.
- `.kt-project__meta` (source and term), `.kt-project__title`, `.kt-project__desc`, `.kt-project__tags` of `kt-tag--solid`, and `.kt-project__link`.

## Rules
- Square corners (`radius-none`) and `shadow-card`; hover lifts 4px and turns the border `accent-line`.
- The description states what was built and with what data. No marketing lines.
- Metrics in the description must match the current resume.
