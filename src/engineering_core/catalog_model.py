from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any, Iterable

CATALOG_COLLECTIONS = ("lanes", "disciplines", "templates")
REQUIRED_ENTRY_FIELDS = ("id", "kind", "category", "file", "path", "description")
PILOT_CATALOG_FILE = "catalog.pilots.json"


def package_catalog_path() -> Path:
    return Path(resources.files("engineering_core").joinpath("catalog.json"))


def package_pilot_catalog_path() -> Path:
    return Path(resources.files("engineering_core").joinpath(PILOT_CATALOG_FILE))


def repository_catalog_path(repo_root: Path) -> Path:
    return repo_root / "catalog.json"


def repository_pilot_catalog_path(repo_root: Path) -> Path:
    return repo_root / PILOT_CATALOG_FILE


def canonical_catalog_path(repo_root: Path) -> Path:
    return repo_root / "src" / "engineering_core" / "catalog.json"


def canonical_pilot_catalog_path(repo_root: Path) -> Path:
    return repo_root / "src" / "engineering_core" / PILOT_CATALOG_FILE


def _read_catalog(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"catalog must be a JSON object: {path}")
    return value


def _entry_ids(entries: list[Any]) -> set[str]:
    return {
        entry["id"]
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }


def merge_catalog(base: dict[str, Any], overlay: dict[str, Any] | None) -> dict[str, Any]:
    if overlay is None:
        return base
    merged = json.loads(json.dumps(base))
    for collection in (*CATALOG_COLLECTIONS, "profiles"):
        incoming = overlay.get(collection, [])
        if not isinstance(incoming, list):
            raise ValueError(f"pilot catalog collection must be a list: {collection}")
        target = merged.setdefault(collection, [])
        if not isinstance(target, list):
            raise ValueError(f"base catalog collection must be a list: {collection}")
        duplicates = sorted(_entry_ids(target) & _entry_ids(incoming))
        if duplicates:
            raise ValueError(
                f"pilot catalog duplicates {collection} id(s): {', '.join(duplicates)}"
            )
        target.extend(incoming)
    merged["pilot_catalog"] = {
        "schema_version": overlay.get("schema_version", "1"),
        "status": overlay.get("status", "pilot"),
        "description": overlay.get("description", ""),
    }
    return merged


def load_catalog(repo_root: Path | None = None, *, prefer_repo: bool = False) -> dict[str, Any]:
    if repo_root is not None and prefer_repo:
        repo_path = repository_catalog_path(repo_root)
        if repo_path.exists():
            overlay_path = repository_pilot_catalog_path(repo_root)
            overlay = _read_catalog(overlay_path) if overlay_path.exists() else None
            return merge_catalog(_read_catalog(repo_path), overlay)
    overlay_path = package_pilot_catalog_path()
    overlay = _read_catalog(overlay_path) if overlay_path.exists() else None
    return merge_catalog(_read_catalog(package_catalog_path()), overlay)


def collection_entries(catalog: dict[str, Any], collection: str) -> list[dict[str, Any]]:
    raw = catalog.get(collection, [])
    if not isinstance(raw, list):
        return []
    return [entry for entry in raw if isinstance(entry, dict)]


def collection_ids(catalog: dict[str, Any], collection: str) -> tuple[str, ...]:
    return tuple(
        entry["id"]
        for entry in collection_entries(catalog, collection)
        if isinstance(entry.get("id"), str)
    )


def collection_file_map(catalog: dict[str, Any], collection: str) -> dict[str, str]:
    return {
        entry["id"]: entry["file"]
        for entry in collection_entries(catalog, collection)
        if isinstance(entry.get("id"), str) and isinstance(entry.get("file"), str)
    }


def _duplicate_values(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_catalog(
    catalog: dict[str, Any],
    *,
    repo_root: Path | None = None,
    check_paths: bool = False,
) -> list[str]:
    errors: list[str] = []

    for field in ("name", "version", "cli"):
        if not isinstance(catalog.get(field), str) or not catalog[field]:
            errors.append(f"catalog.missing-top-level-field:{field}")

    all_ids: dict[str, set[str]] = {}
    for collection in CATALOG_COLLECTIONS:
        raw = catalog.get(collection)
        if not isinstance(raw, list):
            errors.append(f"catalog.invalid-collection:{collection}")
            all_ids[collection] = set()
            continue

        entries = collection_entries(catalog, collection)
        ids = [entry.get("id") for entry in entries if isinstance(entry.get("id"), str)]
        all_ids[collection] = set(ids)
        for duplicate in _duplicate_values(ids):
            errors.append(f"catalog.duplicate-id:{collection}:{duplicate}")

        for index, entry in enumerate(entries):
            entry_id = entry.get("id") if isinstance(entry.get("id"), str) else f"index-{index}"
            for field in REQUIRED_ENTRY_FIELDS:
                if not isinstance(entry.get(field), str) or not entry[field]:
                    errors.append(f"catalog.missing-entry-field:{collection}:{entry_id}:{field}")
            if check_paths and repo_root is not None:
                candidates = [
                    repo_root / str(entry.get("path", "")),
                    repo_root / "src" / "engineering_core" / collection / str(entry.get("file", "")),
                    repo_root / collection / str(entry.get("file", "")),
                ]
                if not any(candidate.exists() for candidate in candidates):
                    errors.append(f"catalog.missing-path:{collection}:{entry_id}")

    lane_ids = all_ids.get("lanes", set())
    discipline_ids = all_ids.get("disciplines", set())
    known_requirements = lane_ids | discipline_ids
    for entry in collection_entries(catalog, "lanes"):
        entry_id = str(entry.get("id", "<unknown>"))
        requires = entry.get("requires", [])
        if not isinstance(requires, list):
            errors.append(f"catalog.invalid-requires:lanes:{entry_id}")
            continue
        for requirement in requires:
            if not isinstance(requirement, str) or requirement not in known_requirements:
                errors.append(f"catalog.unknown-requirement:lanes:{entry_id}:{requirement}")

    profiles = catalog.get("profiles", [])
    if not isinstance(profiles, list):
        errors.append("catalog.invalid-collection:profiles")
        profiles = []
    profile_ids = [
        profile.get("id")
        for profile in profiles
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    ]
    for duplicate in _duplicate_values(profile_ids):
        errors.append(f"catalog.duplicate-id:profiles:{duplicate}")
    for profile in profiles:
        if not isinstance(profile, dict):
            errors.append("catalog.invalid-profile-entry")
            continue
        profile_id = profile.get("id") if isinstance(profile.get("id"), str) else "<unknown>"
        for lane in profile.get("lanes", []):
            if lane not in lane_ids:
                errors.append(f"catalog.unknown-profile-lane:{profile_id}:{lane}")
        for discipline in profile.get("disciplines", []):
            if discipline not in discipline_ids:
                errors.append(f"catalog.unknown-profile-discipline:{profile_id}:{discipline}")

    return sorted(set(errors))


def _projection_pairs(repo_root: Path) -> list[tuple[Path, Path]]:
    pairs = [(canonical_catalog_path(repo_root), repository_catalog_path(repo_root))]
    pilot = canonical_pilot_catalog_path(repo_root)
    if pilot.exists():
        pairs.append((pilot, repository_pilot_catalog_path(repo_root)))
    return pairs


def catalog_projection_matches(repo_root: Path) -> bool:
    return all(
        canonical.exists()
        and projection.exists()
        and canonical.read_bytes() == projection.read_bytes()
        for canonical, projection in _projection_pairs(repo_root)
    )


def sync_catalog_projection(repo_root: Path, *, apply: bool = False) -> bool:
    drifted = False
    for canonical, projection in _projection_pairs(repo_root):
        if not canonical.exists():
            raise FileNotFoundError(f"canonical catalog not found: {canonical}")
        canonical_bytes = canonical.read_bytes()
        pair_drifted = not projection.exists() or projection.read_bytes() != canonical_bytes
        drifted = drifted or pair_drifted
        if apply and pair_drifted:
            projection.parent.mkdir(parents=True, exist_ok=True)
            projection.write_bytes(canonical_bytes)
    return drifted


_PACKAGED_CATALOG = load_catalog()
LANES = collection_ids(_PACKAGED_CATALOG, "lanes")
LANE_FILES = collection_file_map(_PACKAGED_CATALOG, "lanes")
DISCIPLINES = collection_ids(_PACKAGED_CATALOG, "disciplines")
DISCIPLINE_FILES = collection_file_map(_PACKAGED_CATALOG, "disciplines")
TEMPLATES = collection_ids(_PACKAGED_CATALOG, "templates")
TEMPLATE_FILES = collection_file_map(_PACKAGED_CATALOG, "templates")
