"""Move a consumer's engineering-core release pin and nothing else (AK6101).

`init`/`migrate` regenerate the whole adoption: they rewrite the policy with sorted keys
and replace an unmanaged docs/engineering.local.md, which destroys hand-written repo
content on every fleet repo. `pin` edits only the pin: `ref`, `release_pin`,
`repository`, the `--from` source of every engineering-core command, and the pin
mentions in the local doc. Key order, formatting and every other key stay as they were.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from engineering_core.adoption import (
    CANONICAL_REPOSITORY,
    AdoptionPlan,
    _change,
    _text,
    load_json,
)
from engineering_core.adoption_scan import ENGINEERING_DOC, ENGINEERING_POLICY, extract_policy
from engineering_core.repository_facts import validate_repository_argument

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_ANY_SHA40 = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
# --from '<src>' | --from "<src>" | --from <src>
_FROM = re.compile(r"--from (?:'([^']*)'|\"([^\"]*)\"|([^\s'\"]+))")
_OURS = re.compile(r"engineering[-_]core", re.IGNORECASE)
# Old tags move only on the pin line itself, so history ("Up to v0.12.0, ...") stays put.
_PIN_LINE = re.compile(r"release[ _-]pin", re.IGNORECASE)


def _is_canonical(repository: Any) -> bool:
    return isinstance(repository, str) and repository.removesuffix(".git").rstrip("/") == CANONICAL_REPOSITORY


def _rewrite_sources(text: str, source: str, old_commits: set[str]) -> str:
    """Point every `--from <engineering-core source>` at `source`, keeping its quoting."""

    def replace(match: re.Match[str]) -> str:
        found = next(group for group in match.groups() if group is not None)
        if not _OURS.search(found):
            return match.group(0)
        old_commits.update(_ANY_SHA40.findall(found))
        if match.group(1) is not None:
            return f"--from '{source}'"
        if match.group(2) is not None:
            return f'--from "{source}"'
        return f"--from {source}"

    return _FROM.sub(replace, text)


def _rewrite_strings(value: Any, source: str, old_commits: set[str]) -> Any:
    if isinstance(value, str):
        return _rewrite_sources(value, source, old_commits)
    if isinstance(value, list):
        return [_rewrite_strings(item, source, old_commits) for item in value]
    if isinstance(value, dict):
        return {key: _rewrite_strings(item, source, old_commits) for key, item in value.items()}
    return value


def _string_edits(before: Any, after: Any, edits: dict[str, str]) -> bool:
    """Collect old->new string literals; False when the structure itself changed."""
    if isinstance(before, dict) and isinstance(after, dict):
        if list(before) != list(after):
            return False
        return all(_string_edits(before[key], after[key], edits) for key in before)
    if isinstance(before, list) and isinstance(after, list):
        if len(before) != len(after):
            return False
        return all(_string_edits(old, new, edits) for old, new in zip(before, after))
    if isinstance(before, str) and isinstance(after, str):
        if before != after:
            if edits.get(before, after) != after:
                return False
            edits[before] = after
        return True
    return before == after


def _indent(text: str) -> int:
    match = re.search(r"^( +)\"", text, re.MULTILINE)
    return len(match.group(1)) if match else 2


def _render_policy(text: str, before: dict[str, Any], after: dict[str, Any]) -> str | None:
    """Edit changed string values in place; re-render only when keys were added."""
    edits: dict[str, str] = {}
    if _string_edits(before, after, edits):
        rendered = text
        for old, new in edits.items():
            rendered = rendered.replace(
                json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False)
            )
        return rendered if json.loads(rendered) == after else None
    rendered = json.dumps(after, indent=_indent(text), ensure_ascii=False)
    return rendered + "\n" if text.endswith("\n") else rendered


def _move_tag(line: str, old_tags: set[str], ref: str) -> str:
    for tag in old_tags:
        line = re.sub(rf"(?<![\w.]){re.escape(tag)}(?!\w|\.\d)", ref, line)
    return line


def _render_doc(text: str, source: str, ref: str, commit: str, old_commits: set[str], old_tags: set[str]) -> str:
    lines = []
    for line in text.splitlines(keepends=True):
        rewritten = _rewrite_sources(line, source, old_commits)
        had_commit = any(old in rewritten for old in old_commits)
        for old in old_commits:
            rewritten = rewritten.replace(old, commit)
        if had_commit or _PIN_LINE.search(rewritten):
            rewritten = _move_tag(rewritten, old_tags, ref)
        lines.append(rewritten)
    return "".join(lines)


def plan_pin(repo_root: Path, *, ref: str, ref_commit: str) -> AdoptionPlan:
    repo_root = validate_repository_argument(repo_root)
    if not ref or not ref.strip():
        raise ValueError("--ref must name the release tag, for example v0.12.1")
    if not _SHA40.fullmatch(ref_commit):
        raise ValueError("--ref-commit must be a full 40-character lowercase commit SHA")
    policy_path = repo_root / ENGINEERING_POLICY
    policy_text = _text(policy_path)
    policy, error = load_json(policy_path)
    ec = policy.get("engineering_core") if policy else None
    if policy_text is None or error or not isinstance(ec, dict):
        reason = error or f"{ENGINEERING_POLICY} has no engineering_core object"
        return AdoptionPlan(str(repo_root), "pin", [], [], [], [f"cannot move the pin: {reason}; adopt with init first"])
    _ec, lanes, _status, _stack, disciplines, _ref, _commands = extract_policy(policy)

    source = f"git+{CANONICAL_REPOSITORY}.git@{ref_commit}"
    old_pin = ec.get("release_pin") if isinstance(ec.get("release_pin"), dict) else {}
    old_commits = {value for value in (ec.get("ref"), old_pin.get("ref"), old_pin.get("resolved_commit"))
                   if isinstance(value, str) and _SHA40.fullmatch(value)}
    old_tags = {value for value in (ec.get("ref"), old_pin.get("ref"))
                if isinstance(value, str) and value and not _SHA40.fullmatch(value) and value != ref}

    def shaped(current: Any) -> str:
        # A repo whose validator requires a raw SHA ref keeps that shape.
        return ref_commit if isinstance(current, str) and _SHA40.fullmatch(current) else ref

    moved = {key: (_rewrite_strings(value, source, old_commits) if key != "release_pin" else value)
             for key, value in ec.items()}
    moved["ref"] = shaped(ec.get("ref"))
    if not _is_canonical(ec.get("repository")):
        moved["repository"] = CANONICAL_REPOSITORY
    moved["release_pin"] = {**old_pin, "kind": "git-commit", "ref": shaped(old_pin.get("ref")),
                            "resolved_commit": ref_commit, "source": source}
    old_commits.discard(ref_commit)
    after_policy = {**policy, "engineering_core": moved}

    conflicts: list[str] = []
    policy_after = _render_policy(policy_text, policy, after_policy)
    if policy_after is None:
        conflicts.append(
            f"{ENGINEERING_POLICY}: the pin values could not be edited in place (an old pin value is reused "
            "by another key, or the file escapes characters differently); move the pin by hand"
        )
        policy_after = policy_text

    doc_path = repo_root / ENGINEERING_DOC
    doc_before = _text(doc_path)
    doc_after = None if doc_before is None else _render_doc(doc_before, source, ref, ref_commit, old_commits, old_tags)

    changes = [change for change in (
        _change(policy_path, repo_root, policy_text, policy_after),
        _change(doc_path, repo_root, doc_before, doc_after),
    ) if change is not None]
    return AdoptionPlan(str(repo_root), "pin", lanes, disciplines, changes, conflicts)
