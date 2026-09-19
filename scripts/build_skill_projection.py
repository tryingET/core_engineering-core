#!/usr/bin/env python3
"""Build the pi skill projection from engineering-core lanes and disciplines.

This is the DELIVERY LAYER: engineering-core's value realizes when its guidance
enters agent context at the moment of need. Pi loads skills from skills/
directories; this generator projects every lane and discipline doc into a
skill whose description carries the doc's own read_when triggers, plus skill
PROFILES (lane-scoped bundles) that the agent registry / dispatch skillProfile
surface can materialize per agent.

Deterministic: same inputs -> same bytes. Run with --check in CI.

Output layout (generated; do not hand-edit):
  skills/ec-lane-<id>/SKILL.md        one per lane (incl. lane addenda)
  skills/ec-discipline-<id>/SKILL.md  one per discipline
  skills/profiles.json                named bundles for dispatch skill profiles
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANES_DIR = ROOT / "lanes"
DISCIPLINES_DIR = ROOT / "disciplines"
OUT_DIR = ROOT / "skills"
PROFILE_SCHEMA = "engineering-core.skill-profiles/1"
FLEET_ROOT_ENV = "ENGINEERING_CORE_FLEET_ROOT"

# Renaming a published profile requires adding old-key -> new-key here for one
# engineering-core release. Aliases must point directly to canonical profiles.
DEPRECATED_ALIASES: dict[str, str] = {}

# Budget discipline: the v3/v3b pilots showed small high-signal guidance wins
# and dumps lose. Cap projected skill bodies hard.
MAX_BODY_BYTES = 12_000
TRUNCATION_NOTE = "\n\n[projected skill truncated; read the full doc in engineering-core]\n"

# Disciplines selected by default when nothing narrower is declared (must match
# adoption.infer_repo_selection defaults).
DEFAULT_DISCIPLINES = [
    "validation", "testing", "security-privacy", "documentation",
    "dependency-governance",
]


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    block = text[4:end]
    body = text[end + 5:]
    meta: dict = {}
    current_key = None
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and current_key:
            meta.setdefault(current_key, [])
            if isinstance(meta[current_key], list):
                meta[current_key].append(stripped[2:].strip().strip('"'))
        elif ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if value == "":
                current_key = key
                meta[key] = []
            else:
                meta[key] = value
                current_key = None
    return meta, body


def skill_front_matter(name: str, description: str) -> str:
    # JSON strings are YAML-compatible scalars. Quote/escape descriptions so
    # `[ec-*]`, colons, quotes and newlines cannot change frontmatter structure.
    # ASCII escapes also keep Unicode line separators on one physical line.
    return f"---\nname: {name}\ndescription: {json.dumps(description)}\n---\n"


def build_description(kind: str, ident: str, meta: dict) -> str:
    summary = meta.get("summary", f"engineering-core {kind} {ident} guidance")
    triggers = meta.get("read_when", [])
    if isinstance(triggers, str):
        triggers = [triggers]
    trigger_text = " Load when: " + "; ".join(triggers) if triggers else ""
    description = f"[ec-{kind}] {summary}{trigger_text}"
    if len(description) > 950:
        description = description[:947] + "..."
    return description


def project_doc(kind: str, ident: str, path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    meta, _body = parse_front_matter(text)
    name = f"ec-{kind}-{ident}"
    description = build_description(kind, ident, meta)
    body = text
    if len(body.encode()) > MAX_BODY_BYTES:
        cut = body.encode()[:MAX_BODY_BYTES].decode("utf-8", errors="ignore")
        body = cut + TRUNCATION_NOTE
    skill = skill_front_matter(name, description) + "\n" + body
    if not body.endswith("\n"):
        skill += "\n"
    return name, skill


def lane_id(filename: str) -> str:
    stem = filename.removeprefix("engineering-").removesuffix(".md")
    return stem


def discipline_id(filename: str) -> str:
    return filename.removesuffix(".md")


def build_profiles(
    lane_skills: dict[str, str], discipline_skills: dict[str, str]
) -> dict[str, object]:
    profiles: dict[str, list[str]] = {}
    base_defaults = [discipline_skills[d] for d in DEFAULT_DISCIPLINES if d in discipline_skills]
    for lane, skill_name in lane_skills.items():
        base = lane.replace("-frontend", "").replace("-cuda", "").split(".")[0]
        members = [skill_name]
        if base != lane and base in lane_skills:
            members.append(lane_skills[base])
        members.extend(base_defaults)
        profiles[f"ec-{lane}"] = sorted(set(members))
    profiles["ec-defaults"] = sorted(base_defaults)
    profiles["ec-full"] = sorted(set(lane_skills.values()) | set(discipline_skills.values()))
    return {
        "schema": PROFILE_SCHEMA,
        "profiles": profiles,
        "deprecated_aliases": dict(sorted(DEPRECATED_ALIASES.items())),
    }


def validate_profile_interface(document: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(document, dict):
        return ["profile interface must be an object"]
    if document.get("schema") != PROFILE_SCHEMA:
        problems.append(f"profile interface schema must be {PROFILE_SCHEMA!r}")
    profiles = document.get("profiles")
    aliases = document.get("deprecated_aliases")
    if not isinstance(profiles, dict):
        problems.append("profile interface profiles must be an object")
        profiles = {}
    if not isinstance(aliases, dict):
        problems.append("profile interface deprecated_aliases must be an object")
        aliases = {}
    for profile, members in profiles.items():
        if not isinstance(profile, str) or not profile:
            problems.append("profile keys must be non-empty strings")
            continue
        if not isinstance(members, list) or not members or not all(
            isinstance(member, str) and member for member in members
        ):
            problems.append(f"profile {profile!r} must contain non-empty skill names")
        elif len(members) != len(set(members)):
            problems.append(f"profile {profile!r} contains duplicate skills")
    for alias, target in aliases.items():
        if not isinstance(alias, str) or not alias or not isinstance(target, str) or not target:
            problems.append("deprecated aliases and targets must be non-empty strings")
            continue
        if alias in profiles:
            problems.append(f"deprecated alias {alias!r} collides with a canonical profile")
        if target not in profiles:
            problems.append(f"deprecated alias {alias!r} targets unknown profile {target!r}")
    return problems


def validate_fleet_references(
    fleet_root: Path, document: object
) -> tuple[list[str], list[str]]:
    """Validate skills.profile in each immediate child agent.json, without writes."""
    interface_problems = validate_profile_interface(document)
    if interface_problems:
        return ([f"profile-interface: {problem}" for problem in interface_problems], [])
    assert isinstance(document, dict)
    profiles = document["profiles"]
    aliases = document["deprecated_aliases"]
    assert isinstance(profiles, dict) and isinstance(aliases, dict)

    if not fleet_root.is_dir():
        return ([
            f"fleet-profile: repo={fleet_root} profile=<unreadable>: "
            "fleet root is not a directory"
        ], [])
    manifests = sorted(fleet_root.glob("*/agent.json"))
    if not manifests:
        return ([
            f"fleet-profile: repo={fleet_root} profile=<missing>: no agent.json files found"
        ], [])

    problems: list[str] = []
    warnings: list[str] = []
    for manifest_path in manifests:
        repo = manifest_path.parent
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            problems.append(
                f"fleet-profile: repo={repo} profile=<unreadable>: invalid agent.json: {exc}"
            )
            continue
        skills = manifest.get("skills") if isinstance(manifest, dict) else None
        profile = skills.get("profile") if isinstance(skills, dict) else None
        if not isinstance(profile, str) or not profile:
            problems.append(
                f"fleet-profile: repo={repo} profile={profile!r}: "
                "skills.profile must be a non-empty string"
            )
            continue
        if profile in profiles:
            continue
        target = aliases.get(profile)
        if isinstance(target, str) and target in profiles:
            warnings.append(
                f"fleet-profile: repo={repo} profile={profile!r}: "
                f"deprecated alias; use {target!r}"
            )
            continue
        problems.append(
            f"fleet-profile: repo={repo} profile={profile!r}: unknown profile"
        )
    return problems, warnings


def render_projection() -> tuple[dict[Path, bytes], dict[str, int]]:
    lane_skills: dict[str, str] = {}
    discipline_skills: dict[str, str] = {}
    rendered: dict[Path, bytes] = {}
    for path in sorted(LANES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        ident = lane_id(path.name)
        name, content = project_doc("lane", ident, path)
        lane_skills[ident] = name
        rendered[OUT_DIR / name / "SKILL.md"] = content.encode()
    for path in sorted(DISCIPLINES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        ident = discipline_id(path.name)
        name, content = project_doc("discipline", ident, path)
        discipline_skills[ident] = name
        rendered[OUT_DIR / name / "SKILL.md"] = content.encode()
    interface = build_profiles(lane_skills, discipline_skills)
    rendered[OUT_DIR / "profiles.json"] = (
        json.dumps(interface, indent=2, sort_keys=True) + "\n"
    ).encode()
    profiles = interface["profiles"]
    assert isinstance(profiles, dict)
    return rendered, {
        "lanes": len(lane_skills),
        "disciplines": len(discipline_skills),
        "skills": len(lane_skills) + len(discipline_skills),
        "profiles": len(profiles),
    }


def generate() -> dict[str, object]:
    rendered, summary = render_projection()
    for path, payload in rendered.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    return {**summary, "files": list(rendered)}


def check(fleet_root: Path | None = None) -> int:
    rendered, summary = render_projection()
    problems = [
        f"stale projection: {path.relative_to(ROOT)}"
        for path, expected in rendered.items()
        if not path.is_file() or path.read_bytes() != expected
    ]
    second_render, _ = render_projection()
    if rendered != second_render:
        problems.append("nondeterministic projection output")

    interface = json.loads(rendered[OUT_DIR / "profiles.json"])
    problems.extend(f"profile-interface: {p}" for p in validate_profile_interface(interface))
    warnings: list[str] = []
    if fleet_root is not None:
        fleet_problems, warnings = validate_fleet_references(fleet_root, interface)
        problems.extend(fleet_problems)
    for warning in warnings:
        print(warning, file=sys.stderr)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 2
    fleet_note = f"; fleet={fleet_root}" if fleet_root is not None else ""
    print(
        f"engineering-core skill projection is current "
        f"({summary['skills']} skills, {summary['profiles']} profiles{fleet_note})"
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--fleet-root",
        type=Path,
        default=Path(os.environ[FLEET_ROOT_ENV]) if os.environ.get(FLEET_ROOT_ENV) else None,
        help=f"validate immediate child agent.json files (or set {FLEET_ROOT_ENV})",
    )
    args = parser.parse_args()
    if args.fleet_root is not None and not args.check:
        parser.error("--fleet-root requires --check")
    if args.check:
        raise SystemExit(check(args.fleet_root))
    summary = generate()
    print(
        f"projected {summary['skills']} skills "
        f"({summary['lanes']} lanes, {summary['disciplines']} disciplines) "
        f"and {summary['profiles']} profiles into {OUT_DIR.relative_to(ROOT)}/"
    )


if __name__ == "__main__":
    main()
