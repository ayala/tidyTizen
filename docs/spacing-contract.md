# Spacing contract

Spacing is part of tidyTizen's functional definition. It applies to every existing and future screen, not only to previously reported components.

## Required gutters

- Icon, logo, status dot, checkmark, thumbnail, remote glyph, or swatch beside text: at least 16 px of visible edge-to-edge space.
- Attribution marks and descriptive rows: at least 24 px.
- Adjacent compact controls: at least 20 px.
- Adjacent controls in the black Home tray: at least 40 px, including focused scale states.
- Adjacent sections or unrelated groups must have a visibly larger gutter than items within a group.

These are minimums, not target values. Optical balance can require more space.

## Implementation rule

Use a deliberate layout gutter on the element that owns the relationship. Do not rely on spaces in text, glyph side-bearings, transparent pixels inside an asset, absolute-position coincidence, inherited `gap`, or a margin that only works for one label length. Account for transforms, focus growth, font metrics, localization, and the 1920 × 1080 stage scale.

The target Tizen 6 browser does not reliably apply flexbox `gap`. Any production flex layout that depends on separation must include a Tizen-compatible sibling margin (for example, `.item + .item { margin-top: ... }` or `margin-left`) and the rendered TV state must be checked. Desktop support for `gap` is not sufficient. The Curate, All Apps and Settings tray uses a 40 px sibling margin and must retain that visible edge-to-edge gutter after focus scaling.

## Verification rule

For every UI change:

1. Identify all adjacent visual pairs introduced or affected by the change.
2. Inspect Text, Icons, and Icons + Text variants where applicable.
3. Inspect focused and unfocused states and both List and Dock layouts where applicable.
4. Measure `getBoundingClientRect()` edges for the visible children, not only their parent boxes or declared CSS values.
5. Add or update a browser assertion that fails when the visible gutter falls below this contract.
6. Exercise performance-sensitive layout changes on the QN800A before describing them as complete.

A passing screenshot at one state does not override a failed geometry measurement in another state.
