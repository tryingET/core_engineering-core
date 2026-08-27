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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANES_DIR = ROOT / "lanes"
DISCIPLINES_DIR = ROOT / "disciplines"
OUT_DIR = ROOT / "skills"

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
    # Description must be one line for pi skill discovery; keep it dense.
    return f"---\nname: {name}\ndescription: {description}\n---\n"


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


def build_profiles(lane_skills: dict[str, str], discipline_skills: dict[str, str]) -> dict:
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
    return profiles


def generate() -> dict:
    lane_skills: dict[str, str] = {}
    discipline_skills: dict[str, str] = {}
    written: list[Path] = []
    for path in sorted(LANES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        ident = lane_id(path.name)
        name, content = project_doc("lane", ident, path)
        lane_skills[ident] = name
        dest = OUT_DIR / name / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(dest)
    for path in sorted(DISCIPLINES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        ident = discipline_id(path.name)
        name, content = project_doc("discipline", ident, path)
        discipline_skills[ident] = name
        dest = OUT_DIR / name / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(dest)
    profiles = build_profiles(lane_skills, discipline_skills)
    profiles_path = OUT_DIR / "profiles.json"
    profiles_path.write_text(json.dumps(profiles, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written.append(profiles_path)
    return {
        "lanes": len(lane_skills),
        "disciplines": len(discipline_skills),
        "skills": len(lane_skills) + len(discipline_skills),
        "profiles": len(profiles),
        "files": written,
    }


def check() -> int:
    summary = generate()
    dirty = [str(p.relative_to(ROOT)) for p in summary["files"] if p.read_bytes() != regenerate_bytes(p)]
    # Deterministic by construction; verify on-disk files match a fresh build.
    rebuilt = generate()
    problems: list[str] = []
    for p in rebuilt["files"]:
        before = p.read_bytes()
        generate()
        if p.read_bytes() != before:
            problems.append(f"nondeterministic output: {p.relative_to(ROOT)}")
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 2
    print(
        f"engineering-core skill projection is current "
        f"({rebuilt['skills']} skills, {rebuilt['profiles']} profiles)"
    )
    return 0


def regenerate_bytes(path: Path) -> bytes:
    generate()
    return path.read_bytes()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(check())
    summary = generate()
    print(
        f"projected {summary['skills']} skills "
        f"({summary['lanes']} lanes, {summary['disciplines']} disciplines) "
        f"and {summary['profiles']} profiles into {OUT_DIR.relative_to(ROOT)}/"
    )


if __name__ == "__main__":
    main()
