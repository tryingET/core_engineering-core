#!/usr/bin/env python3
# summary: "Exercises capability declarations, doctor reports, population scanning, CLI behavior, and fail-closed input bounds in deterministic fixtures."
# read_when:
#   - "Changing capability contracts, doctor observations, capability population scanning, or their CLI exposure."

"""Deterministic orchestration over public capability APIs; defines no product semantics."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.capability_scan import PopulationError, build_capability_scan, resolve_population
from engineering_core.doctor import build_doctor


def policy(capabilities: dict | None, ref: str = "v0.6.0") -> dict:
    core = {"ref": ref, "lane": "py", "disciplines": [], "consumer_command": "touch MUST_NOT_EXIST"}
    if capabilities is not None:
        core["capability_contract"] = {"version": "engineering-core-capabilities-v1", "capabilities": capabilities}
    return {"engineering_core": core}


def rejected(function) -> bool:
    try:
        function()
    except PopulationError:
        return True
    return False


def cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-c", "from engineering_core.cli import main; main()", *args],
        cwd=ROOT, env=env, text=True, capture_output=True, check=False,
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        definitions = {
            "absent": None,
            "valid": {
                "planning": {"status": "declared", "schema": "engineering-plan-v1"},
                "advisor": {"status": "declared", "request_schema": "engineering-advice-request-v1", "response_schema": "engineering-advice-response-v1"},
                "closed_loop": {"status": "declared", "receipt_schema": "engineering-evidence-receipt-v1", "disposition_schema": "engineering-recommendation-disposition-v1"},
            },
            "wrong-schema": {"planning": {"status": "declared", "schema": "wrong"}},
        }
        repos: list[Path] = []
        for name, declaration in definitions.items():
            repo = root / name
            (repo / "policy").mkdir(parents=True)
            (repo / "policy/engineering-lane.json").write_text(json.dumps(policy(declaration)))
            repos.append(repo)
        unsupported = root / "unsupported"
        (unsupported / "policy").mkdir(parents=True)
        value = policy({})
        value["engineering_core"]["capability_contract"]["version"] = "future"
        (unsupported / "policy/engineering-lane.json").write_text(json.dumps(value))
        repos.append(unsupported)
        mismatch = root / "pin-mismatch"
        (mismatch / "policy").mkdir(parents=True)
        (mismatch / "policy/engineering-lane.json").write_text(json.dumps(policy({}, "v0.5.0")))
        repos.append(mismatch)
        missing = root / "missing"

        repo_file = root / "repos.txt"
        repo_file.write_text("# explicit owner population\n\nvalid\nabsent\n")
        policy_before = {path: (path / "policy/engineering-lane.json").read_bytes() for path in repos}
        population = resolve_population(repos + [repos[0], missing], [repo_file])
        first = build_capability_scan(population)
        second = build_capability_scan(list(reversed(population)))
        assert first == second
        assert first["completeness"] == "partial" and first["failures"]
        assert not (root / "MUST_NOT_EXIST").exists()
        statuses = {item["repository"]: item["status"] for item in first["records"]}
        assert statuses[str(root / "valid")] == "degraded"
        assert statuses[str(root / "wrong-schema")] == "blocked"
        assert build_doctor(root / "absent")["status"] == "degraded"
        assert build_doctor(mismatch)["pin_posture"] == "released-mismatch"
        assert build_capability_scan([])["population"]["count"] == 0

        bad = root / "bad"
        bad.write_bytes(b"x\x00y")
        oversized = root / "oversized"
        oversized.write_bytes(b"x" * 1_048_577)
        target = root / "target"
        target.write_text("valid\n")
        link = root / "link"
        link.symlink_to(target)
        assert rejected(lambda: resolve_population([], [bad]))
        assert rejected(lambda: resolve_population([], [oversized]))
        assert rejected(lambda: resolve_population([], [link]))
        assert rejected(lambda: resolve_population([repos[0], repos[1]], [], max_repositories=1))
        if hasattr(os, "mkfifo"):
            fifo = root / "fifo"
            os.mkfifo(fifo)
            assert rejected(lambda: resolve_population([], [fifo]))

        catalog_root = root / "catalog"
        catalog_root.mkdir()
        raw_catalog = json.loads((ROOT / "catalog.json").read_text())
        raw_catalog["version"] = "9.9.9"
        (catalog_root / "catalog.json").write_text(json.dumps(raw_catalog))
        assert build_doctor(repos[0], repo_root=catalog_root, prefer_repo=True)["status"] == "blocked"

        assert cli("doctor", "--repo", str(repos[0]), "--repo-root", str(ROOT), "--prefer-repo").returncode == 0
        assert cli("scan-capabilities").returncode == 2
        assert cli("scan-capabilities", "--repo", str(missing), "--repo-root", str(ROOT), "--prefer-repo").returncode == 1
        partial = cli("scan-capabilities", "--repo", str(repos[0]), "--repo", str(missing), "--repo-root", str(ROOT), "--prefer-repo")
        assert partial.returncode == 0 and json.loads(partial.stdout)["completeness"] == "partial"

        assert all((path / "policy/engineering-lane.json").read_bytes() == content for path, content in policy_before.items())
        assert not any(root.rglob("*.receipt.json")) and not any(root.rglob("*.patch"))
        output = {
            "schema": "engineering-capability-dogfood-v1", "status": "ok",
            "records": len(first["records"]), "deterministic": True,
            "cli_exit_contract_verified": True, "path_probes_verified": True,
            "consumer_commands_executed": False, "external_models_invoked": False,
            "policy_or_evidence_mutations": False, "mutations_performed": [],
        }
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
