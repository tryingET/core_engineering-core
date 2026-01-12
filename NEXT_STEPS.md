# NEXT_STEPS

## Short list

- Decide whether Python lane should include a concrete `typecheck` script example (e.g. `ty`) alongside `lint`/`format`
- Cut a patch release + tag after any lane change that downstream repos should pick up
- Periodic audit: `rg -n "\\bmypy\\b" -S` / `rg -n "\\bty\\b" -S` to keep type-check guidance consistent
