# Notice

A notice reports one event: the title states the fact and the body states the action.

## Consumer provides
- `.kt-notice` with an optional `kt-notice--ok|--warn|--bad`, a `.kt-notice__title` and a `.kt-notice__body`.
- A leading `.kt-square` in the matching status color.

## Rules
- Status shows as a 2px top rule and a square; the body fill stays `surface-raised`, never a semantic fill behind copy.
- No exclamation marks. Errors state the cause and the fix.
