#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "contracts/standing-agent/provider-contract-v1.json").read_text())
envelope = json.loads((ROOT / "contracts/standing-agent/ec-adoption-steward.v1.json").read_text())
errors: list[str] = []
if contract.get("provider_id") != "engineering-core": errors.append("provider_id")
if contract.get("owned_namespace") != "engineering-core/ec-*": errors.append("namespace")
if contract.get("compatibility", {}).get("fleet_default_unchanged") is not True: errors.append("fleet default")
payload = envelope.get("payload", {})
raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
actual = "sha256:" + hashlib.sha256(raw).hexdigest()
if envelope.get("payload_ref") != actual: errors.append("payload_ref")
if payload.get("qualified_profile_id") != "engineering-core/ec-adoption-steward": errors.append("profile id")
trees = payload.get("skill_trees", [])
if len(trees) != 5: errors.append("profile must contain exactly five complete skill trees")
for tree in trees:
    if not tree.get("tree_ref", "").startswith("git-tree-sha1:"): errors.append("tree identity")
    if tree.get("invocation_policy", {}).get("preserve_on_materialization") is not True: errors.append("invocation policy")
if "engineering-core/ec-full" not in payload.get("prohibited_for_first_pilot", []): errors.append("ec-full prohibition")
if errors:
    raise SystemExit("FAIL: " + "; ".join(errors))
print("PASS: engineering-core provider contract and ec-adoption-steward publication")
