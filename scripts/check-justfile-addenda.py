#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LANES_DIR = REPO_ROOT / "src" / "tech_stack_core" / "lanes"
LANES = ("py", "ts", "pi-ts", "go", "cpp", "rust", "elixir")
MAIN_TEMPLATE = "tech-stack-{lane}.md"
ADDENDUM_TEMPLATE = "tech-stack-{lane}.justfile.md"
HEADER = "## Conditionally loaded addenda"
TRIGGER_LINES = (
    "- `Justfile` is missing",
    "- the standardized targets are absent or drifting",
    "- you are explicitly establishing or reconciling the repo-local `Justfile`",
)


def fail(message: str) -> None:
    print(f"fail: {message}", file=sys.stderr)
    raise SystemExit(1)


for lane in LANES:
    main_path = LANES_DIR / MAIN_TEMPLATE.format(lane=lane)
    addendum_path = LANES_DIR / ADDENDUM_TEMPLATE.format(lane=lane)

    if not main_path.exists():
        fail(f"missing lane doc: {main_path}")
    if not addendum_path.exists():
        fail(f"missing Justfile addendum: {addendum_path}")

    text = main_path.read_text(encoding="utf-8")
    if HEADER not in text:
        fail(f"lane doc missing conditional addenda header: {main_path}")
    for line in TRIGGER_LINES:
        if line not in text:
            fail(f"lane doc missing trigger line {line!r}: {main_path}")

    expected_companion = f"- `{addendum_path.name}`"
    if expected_companion not in text:
        fail(f"lane doc missing companion reference {expected_companion!r}: {main_path}")

    addendum_text = addendum_path.read_text(encoding="utf-8")
    if "standardized Justfile addendum" not in addendum_text:
        fail(f"addendum missing title marker: {addendum_path}")
    if "## Recommended target mappings" not in addendum_text:
        fail(f"addendum missing target mapping section: {addendum_path}")

readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
if "tech-stack-<lane>.justfile.md" not in readme:
    fail("README missing generic Justfile companion convention")

print("ok: Justfile addenda are present and linked consistently")
