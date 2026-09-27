from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.adoption import ADOPTION_JOURNAL, apply_plan
from engineering_core.adoption_cli import main as adoption_main
from engineering_core.adoption_pin import plan_pin

OLD = "3fc8387274dddccbae3d7fab80954ad483c9b681"
NEW = "5be0f0a294014f2f7aee1ca5adcb6f3c76553e11"
GH = "https://github.com/tryingET/core_engineering-core"
OLD_SRC = f"git+{GH}.git@{OLD}"
NEW_SRC = f"git+{GH}.git@{NEW}"

# Shaped like a v0.12.0 fleet repo (lehrplan-viz): hand-written keys, prettier-style
# one-line arrays, quoted --from sources, and a hand-written local doc.
TAG_POLICY = f"""{{
  "engineering_core": {{
    "tool": "engineering-core",
    "repository": "{GH}",
    "ref": "v0.12.0",
    "release_pin": {{
      "kind": "git-commit",
      "ref": "v0.12.0",
      "resolved_commit": "{OLD}",
      "source": "{OLD_SRC}"
    }},
    "lane": "py",
    "disciplines": ["validation", "testing"],
    "command": "uv tool -n run --from '{OLD_SRC}' engineering-core show py",
    "lint_command": "uv tool run --from ruff==0.13.0 ruff check .",
    "notes": "Größe zählt"
  }},
  "lane": "py"
}}
"""

TAG_DOC = f"""---
summary: "Repo-local engineering-core adoption for demo."
---

# demo engineering guidance

Hand-written context that a pin move must keep.

Release pin: `v0.12.0` (`{OLD}`).

```bash
uv tool -n run --from '{OLD_SRC}' engineering-core show py
```

Up to v0.12.0, `--ref` was ignored whenever a pin existed.
"""


class PinTests(unittest.TestCase):
    def repo(self, tmp: str, policy: str, doc: str | None = None) -> Path:
        root = Path(tmp)
        (root / "policy").mkdir()
        (root / "policy/engineering-lane.json").write_text(policy, encoding="utf-8")
        if doc is not None:
            (root / "docs").mkdir()
            (root / "docs/engineering.local.md").write_text(doc, encoding="utf-8")
        return root

    def after(self, plan, suffix: str) -> str:
        return next(c.after for c in plan.changes if c.path.endswith(suffix))

    def test_tag_pin_moves_in_place_and_keeps_everything_else(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # Given a v0.12.0 repo with a hand-written doc
            repo = self.repo(tmp, TAG_POLICY, TAG_DOC)
            # When the pin moves to v0.12.1
            plan = plan_pin(repo, ref="v0.12.1", ref_commit=NEW)
        self.assertEqual(plan.conflicts, [])
        policy = self.after(plan, "engineering-lane.json")
        # Then the policy differs only in the pin values, with its formatting intact
        expected = (TAG_POLICY.replace(OLD, NEW).replace('"v0.12.0"', '"v0.12.1"'))
        self.assertEqual(policy, expected)
        self.assertIn('"disciplines": ["validation", "testing"]', policy)
        self.assertIn("ruff==0.13.0", policy)
        self.assertIn("Größe", policy)
        # And the doc keeps its content; only the pin line and the source move
        doc = self.after(plan, "engineering.local.md")
        self.assertIn("Hand-written context that a pin move must keep.", doc)
        self.assertIn(f"Release pin: `v0.12.1` (`{NEW}`).", doc)
        self.assertIn(f"--from '{NEW_SRC}' engineering-core show py", doc)
        self.assertIn("Up to v0.12.0, `--ref` was ignored", doc)
        self.assertNotIn(OLD, doc)

    def test_sha_shaped_pin_keeps_its_shape(self) -> None:
        # Given a pi-extensions-style pin whose validator requires a raw SHA ref and bare --from
        policy = json.dumps({"engineering_core": {
            "repository": f"{GH}.git", "ref": OLD,
            "release_pin": {"kind": "git-commit", "ref": OLD, "resolved_commit": OLD, "source": OLD_SRC},
            "command": f"uv tool run --from {OLD_SRC} engineering-core show pi-ts --prefer-repo",
        }}, indent=2) + "\n"
        doc = f"- Shared guidance comes from `engineering-core` v0.8.0 at immutable commit `{OLD}`.\n"
        with tempfile.TemporaryDirectory() as tmp:
            plan = plan_pin(self.repo(tmp, policy, doc), ref="v0.12.1", ref_commit=NEW)
        ec = json.loads(self.after(plan, "engineering-lane.json"))["engineering_core"]
        # Then ref stays a SHA, the .git repository is kept, and the command stays unquoted
        self.assertEqual(ec["ref"], NEW)
        self.assertEqual(ec["release_pin"]["ref"], NEW)
        self.assertEqual(ec["repository"], f"{GH}.git")
        self.assertEqual(ec["command"], f"uv tool run --from {NEW_SRC} engineering-core show pi-ts --prefer-repo")
        self.assertEqual(self.after(plan, "engineering.local.md"),
                         f"- Shared guidance comes from `engineering-core` v0.8.0 at immutable commit `{NEW}`.\n")

    def test_workspace_local_pin_becomes_portable(self) -> None:
        # Given an unpinned repo that runs engineering-core from a local path
        policy = json.dumps({"engineering_core": {
            "repository": "/home/me/ai-society/core/engineering-core", "ref": "v0.7.0",
            "catalog_command": "uv tool run --from git+file:///home/me/ai-society/core/engineering-core@v0.7.0 engineering-core catalog",
            "lint_command": "uv tool run --from ruff ruff check .",
        }}, indent=2) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            plan = plan_pin(self.repo(tmp, policy), ref="v0.12.1", ref_commit=NEW)
        ec = json.loads(self.after(plan, "engineering-lane.json"))["engineering_core"]
        # Then it gets the canonical repository, a release_pin, and portable sources
        self.assertEqual(ec["repository"], GH)
        self.assertEqual(ec["release_pin"], {"kind": "git-commit", "ref": "v0.12.1", "resolved_commit": NEW, "source": NEW_SRC})
        self.assertEqual(ec["catalog_command"], f"uv tool run --from {NEW_SRC} engineering-core catalog")
        self.assertEqual(ec["lint_command"], "uv tool run --from ruff ruff check .")
        self.assertEqual(list(ec)[:2], ["repository", "ref"])

    def test_second_run_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.repo(tmp, TAG_POLICY, TAG_DOC)
            apply_plan(plan_pin(repo, ref="v0.12.1", ref_commit=NEW), journal=False)
            again = plan_pin(repo, ref="v0.12.1", ref_commit=NEW)
        self.assertEqual(again.changes, [])
        self.assertEqual(again.conflicts, [])

    def test_reused_old_value_is_a_conflict_not_a_guess(self) -> None:
        # Given another key that happens to hold the old tag with a different meaning
        policy = TAG_POLICY.replace('"lane": "py",\n', '"lane": "py",\n    "min_version": "v0.12.0",\n', 1)
        with tempfile.TemporaryDirectory() as tmp:
            plan = plan_pin(self.repo(tmp, policy), ref="v0.12.1", ref_commit=NEW)
        # Then the plan refuses instead of rewriting min_version
        self.assertTrue(any("by hand" in c for c in plan.conflicts), plan.conflicts)

    def test_bad_input_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            with self.assertRaisesRegex(ValueError, "40-character"):
                plan_pin(repo, ref="v0.12.1", ref_commit="5be0f0a")
            plan = plan_pin(repo, ref="v0.12.1", ref_commit=NEW)
        self.assertTrue(any("init first" in c for c in plan.conflicts), plan.conflicts)

    def test_cli_is_dry_run_until_apply_and_writes_no_journal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.repo(tmp, TAG_POLICY, TAG_DOC)
            argv = ["pin", "--repo", str(repo), "--ref", "v0.12.1", "--ref-commit", NEW, "--format", "json"]
            with redirect_stdout(io.StringIO()) as out:
                adoption_main(argv)
            self.assertFalse(json.loads(out.getvalue())["applied"])
            self.assertIn(OLD, (repo / "policy/engineering-lane.json").read_text(encoding="utf-8"))
            with redirect_stdout(io.StringIO()):
                adoption_main([*argv, "--apply"])
            self.assertIn(NEW, (repo / "policy/engineering-lane.json").read_text(encoding="utf-8"))
            self.assertFalse((repo / ADOPTION_JOURNAL).exists())


if __name__ == "__main__":
    unittest.main()
