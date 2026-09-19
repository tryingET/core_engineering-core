"""Synthetic G4-B environment; never acquires or republishes owner evidence."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import tempfile
from contextlib import ExitStack, contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def synthetic_cycle(ge, cycle_id: str, disposition: str) -> dict:
    """A valid test record, not a copy or claim of a participant's live cycle."""
    return {
        "schema": ge.SCHEMA,
        "stage": "g4-live-cycle",
        "template_digest": ge.template_digest(),
        "cycle_id": cycle_id,
        "candidate": "synthetic-test-candidate",
        "candidate_identity": ge.UNASSIGNED,
        "origin_group": "synthetic-origin",
        "pilot_groups": ["synthetic-peer"],
        "participant_disposition": {"disposition": "supports", "evidence_supported": True},
        "content_owner_decision": {
            "decision": disposition,
            "decided_by": "engineering_core_content_owner",
            "coerced": False,
        },
        "final_state": {
            "disposition": disposition,
            "preserved_lineage": [{"ref": "synthetic-prior", "immutable": True}],
        },
        "minimum_decision_record": {key: "synthetic" for key in ge.MINIMUM_DECISION_RECORD},
        "pilot_bounds": {
            "opt_in": True,
            "bounded": True,
            "expiry_or_review_event": "synthetic-review-event",
            "can_become_default_silently": False,
        },
        "rollback_drill": {
            "restored_exact_prior_stable_selection": True,
            "history_preserved": True,
        },
        "distribution_status": "not_distributed",
        "adoption_status": "not_adopted",
    }


@contextmanager
def synthetic_workspace(gv):
    """Patch only data bindings; retain real Git, cycle validation and digests."""
    with ExitStack() as stack:
        workspace = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix="ec-g4b-")))
        root = workspace / "core" / "engineering-core"
        root.mkdir(parents=True)
        home = workspace / "home"
        home.mkdir()
        hooks = workspace / "empty-hooks"
        hooks.mkdir()
        # Neither inherited Git overrides nor user hooks/signing affect fixtures.
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        env.update({
            "HOME": str(home), "XDG_CONFIG_HOME": str(home),
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull, "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z",
        })
        stack.enter_context(patch.dict(os.environ, env, clear=True))

        def git(*args):
            return subprocess.run(
                ["git", "-C", str(root), *args], check=True,
                capture_output=True, text=True,
            ).stdout.strip()

        git("init", "--initial-branch=main", f"--template={hooks}", "--object-format=sha1")
        git("config", "core.hooksPath", str(hooks))
        git("config", "user.name", "Synthetic Fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "commit.gpgsign", "false")
        git("commit", "--allow-empty", "-m", "synthetic candidate")
        candidate = git("rev-parse", "HEAD")
        git("branch", gv.CANDIDATE_BRANCH, candidate)
        git("commit", "--allow-empty", "-m", "synthetic main")
        assert git("rev-parse", "main") != candidate

        ge = gv.load_ge()
        lineage = copy.deepcopy(gv.LINEAGE)
        for index, item in enumerate(lineage):
            item["cycle_id"] = f"synthetic-cycle-{index}"
            cycle = synthetic_cycle(ge, item["cycle_id"], item["disposition"])
            item["cycle_digest"] = ge.validate_cycle(cycle)["cycle_digest"]
            path = (root / item["path"]).resolve()
            if not path.is_relative_to(workspace):
                raise ValueError("fixture escaped temporary workspace")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(cycle), encoding="utf-8")

        stack.enter_context(patch.object(gv, "CANDIDATE_COMMIT", candidate))
        stack.enter_context(patch.object(gv, "LINEAGE", lineage))
        yield SimpleNamespace(
            root=root, workspace=workspace, git=git,
            record=gv.emit_record(root), candidate=candidate, lineage=lineage,
        )
