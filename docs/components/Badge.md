# Badge

A status badge reports state with a word and a semantic color; status colors never borrow the accent.

## Consumer provides
- `<span class="kt-badge kt-badge--ok|--warn|--bad">` with a one- or two-word state. No modifier means idle.
- Optionally a leading `.kt-square` in the matching color.

## Rules
- The word carries the meaning; color is the second signal, so the badge still reads in greyscale print.
- Semantic colors appear as badges, 8px squares, 2px top rules or text color, never as a fill behind body copy.
- Uppercase is applied by the class.
