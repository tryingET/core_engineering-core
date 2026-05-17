# Discipline — Design System

## Purpose

Make user-facing surfaces coherent without binding every repo to one framework. A design system is not a component library. It is the governed relationship between tokens, components, interaction states, motion, accessibility, assets, and product meaning.

## Load when

- A repo ships user-facing UI, generated docs, dashboards, native tools, CLI/TUI interaction, or reusable UI components.
- A repo changes visual tokens, themes, motion, icons, charts, or interaction states.
- A repo consumes or exports design assets.

## Invariants

1. **Tokens before repetition** — repeated visual constants become tokens.
2. **Semantic tokens before raw values** — product code uses `action.primary.bg`, not `blue500`.
3. **State is part of design** — focus, hover, active, selected, loading, error, disabled, empty, success, warning, and destructive states are designed explicitly.
4. **Accessibility is not downstream polish** — contrast, focus, keyboard, reduced motion, and names are component contract requirements.
5. **Motion must mean something** — animation either communicates state, guides attention, teaches interaction, or stays out.
6. **Platform affordances survive abstraction** — native web/terminal/desktop/mobile semantics must not be erased by visual consistency.

## Token tiers

```text
primitive tokens   raw palette, type scale, spacing, radius, duration
semantic tokens    intent-bearing aliases: action, danger, surface, focus, text
component tokens   local affordances: button.primary.bg, card.border, chart.series.1
```

Required token metadata:

- purpose
- allowed surfaces
- light/dark/high-contrast behavior
- contrast assumptions
- deprecation/replacement path
- platform mapping when relevant

## Component contract

Reusable components document:

- purpose and non-purpose
- variants and supported combinations
- accessible name behavior
- keyboard/focus behavior
- role/state/value semantics
- all visual states
- layout and responsiveness
- localization/text expansion behavior
- reduced-motion behavior
- examples and anti-examples
- required tests

A component is not done when it looks correct. It is done when its public contract is operable, named, testable, and documented.

## Motion and interactive assets

Use CSS/SVG for simple state transitions, icons, and static decoration.

Use Rive or equivalent interactive animation when motion carries product behavior:

- guided demos
- calibration affordances
- coaching feedback
- stateful reward/unlock moments
- animated visual explanations

For state-driven animation, document:

- asset location
- state-machine inputs/events
- code boundary that drives the animation
- reduced-motion fallback
- accessibility fallback for non-visual users

## Validation

Minimum checks for design-system changes:

- token references compile or generate successfully
- contrast checked for affected semantic tokens
- keyboard/focus behavior checked for affected interactive components
- reduced-motion behavior checked for affected motion
- screenshots or visual review artifacts for large visual changes

## Failure modes

- token names describe appearance instead of meaning
- dark mode is inversion rather than semantic review
- disabled controls offer no explanation or recovery path
- visual consistency destroys platform semantics
- animation blocks comprehension or ignores reduced motion
- component variants multiply faster than contracts
