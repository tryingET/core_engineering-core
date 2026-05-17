# Discipline — Accessibility

## Purpose

Ensure user-facing surfaces are perceivable, operable, understandable, and robust across languages, frameworks, devices, assistive technologies, and rendering models.

## Load when

- A repo ships UI, docs, dashboards, CLI/TUI interaction, native UI, visualizations, generated HTML/PDF, or media-heavy interaction.
- A change affects focus, keyboard behavior, semantic structure, forms, navigation, motion, contrast, charts, or errors.

## Non-negotiable baseline

- Keyboard or equivalent non-pointer operation.
- Visible focus indication.
- Programmatic names for controls.
- Correct reading/navigation order.
- Color is never the only carrier of meaning.
- Text contrast meets the declared target.
- Form errors are associated with fields and recoverable.
- Motion can be reduced or disabled.
- Status changes are announced when needed.
- No keyboard traps.
- Components expose semantic role/state/value through the host platform.
- Content survives zoom, reflow, localization, and text scaling.
- Destructive actions have confirmation or recovery proportional to risk.

## Platform rule

Prefer native semantic controls. Add ARIA or platform accessibility metadata only when native semantics are insufficient. Never use ARIA to disguise broken interaction.

## Surface matrix

| Surface | Preferred primitive | Required accessibility posture |
|---|---|---|
| Web HTML | native elements first | DOM semantics, labels, focus, ARIA only when needed |
| SPA frameworks | semantic components | generated DOM remains accessible |
| Server-rendered UI | semantic HTML + server events | focus and announcements survive updates |
| Docs/static sites | headings/nav/tables/code semantics | navigable structure and readable code blocks |
| CLI/TUI | text labels, shortcuts, focus model | terminal/screen-reader compatibility where possible |
| Native desktop/mobile | platform widgets first | UIA/AX/AT-SPI/platform semantics |
| Canvas/WebGL/custom renderers | semantic overlay/fallback | documented non-visual/keyboard strategy |

## Testing posture

Automated checks find classes of defects; they do not prove accessibility.

Use:

- lint/static checks where available
- axe or equivalent for web surfaces
- keyboard-only smoke checks
- screen reader/platform semantic checks for critical flows
- reduced-motion checks for animated flows
- human review for novel interactions

## Decision rules

- If a control can be a native button/link/input, make it one.
- If custom rendering hides semantics, provide an accessible overlay or equivalent alternate control surface.
- If a flow changes content asynchronously, decide whether focus moves, status announces, or the user remains in context.
- If animation is meaningful, provide an alternate non-motion meaning channel.

## Failure modes

- canvas-only dashboards with no textual alternative
- icon-only controls without accessible names
- custom modals/dropdowns/tabs missing expected keyboard behavior
- focus lost after async transitions
- error messages visible but not associated
- “passes axe” treated as complete accessibility
