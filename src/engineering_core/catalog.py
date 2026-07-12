from __future__ import annotations

import os
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

from engineering_core.safe_io import SafeInputError, read_bounded_json


@dataclass(frozen=True)
class CatalogItem:
    id: str
    file: str
    kind: str
    requires: tuple[str, ...] = ()


@dataclass(frozen=True)
class CatalogProtocols:
    engineering_plan: str
    advice_request: str
    advice_response: str
    evidence_receipt: str
    recommendation_disposition: str
    evidence_reconciliation: str = "engineering-evidence-reconciliation-v1"


@dataclass(frozen=True)
class Catalog:
    raw: dict[str, Any]
    lanes: tuple[CatalogItem, ...]
    disciplines: tuple[CatalogItem, ...]
    templates: tuple[CatalogItem, ...]
    protocols: CatalogProtocols

    @property
    def version(self) -> str:
        return self.raw["version"]

    def ids(self, collection: str) -> tuple[str, ...]:
        return tuple(item.id for item in getattr(self, collection))

    def files(self, collection: str) -> dict[str, str]:
        return {item.id: item.file for item in getattr(self, collection)}


def _items(raw: dict[str, Any], key: str) -> tuple[CatalogItem, ...]:
    value = raw.get(key)
    if not isinstance(value, list):
        raise ValueError(f"catalog.{key} must be an array")
    result: list[CatalogItem] = []
    seen: set[str] = set()
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise ValueError(f"catalog.{key}[{index}] must be an object")
        item_id, file, kind = entry.get("id"), entry.get("file"), entry.get("kind")
        if not all(isinstance(item, str) and item for item in (item_id, file, kind)):
            raise ValueError(f"catalog.{key}[{index}] requires non-empty id, file, and kind")
        if item_id in seen:
            raise ValueError(f"duplicate catalog {key} id: {item_id}")
        seen.add(item_id)
        requires = entry.get("requires", [])
        if not isinstance(requires, list) or not all(isinstance(item, str) for item in requires):
            raise ValueError(f"catalog.{key}[{index}].requires must be an array of strings")
        result.append(CatalogItem(item_id, file, kind, tuple(requires)))
    return tuple(result)


def parse_catalog(raw: Any) -> Catalog:
    if not isinstance(raw, dict):
        raise ValueError("catalog must be an object")
    if not isinstance(raw.get("version"), str) or not raw["version"] or len(raw["version"].encode("utf-8")) > 4096:
        raise ValueError("catalog.version must be bounded non-empty text")
    protocol_raw = raw.get("protocols")
    required = ("engineering_plan", "advice_request", "advice_response")
    if not isinstance(protocol_raw, dict) or not all(isinstance(protocol_raw.get(key), str) and protocol_raw[key] and len(protocol_raw[key].encode("utf-8")) <= 4096 for key in required):
        raise ValueError("catalog.protocols is missing required protocol identifiers")
    optional = ("evidence_receipt", "recommendation_disposition", "evidence_reconciliation")
    if any(key in protocol_raw and (not isinstance(protocol_raw[key], str) or not protocol_raw[key] or len(protocol_raw[key].encode("utf-8")) > 4096) for key in optional):
        raise ValueError("catalog.protocols closed-loop identifiers must be non-empty strings")
    # v0.5 catalogs predate closed-loop protocol metadata. Keep existing
    # catalog/plan/scan consumers compatible while doctor reports the version
    # mismatch separately when such a catalog is selected.
    protocols = CatalogProtocols(
        *(protocol_raw[key] for key in required),
        protocol_raw.get("evidence_receipt", "engineering-evidence-receipt-v1"),
        protocol_raw.get("recommendation_disposition", "engineering-recommendation-disposition-v1"),
        protocol_raw.get("evidence_reconciliation", "engineering-evidence-reconciliation-v1"),
    )
    catalog = Catalog(raw, _items(raw, "lanes"), _items(raw, "disciplines"), _items(raw, "templates"), protocols)
    known = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
    for item in (*catalog.lanes, *catalog.disciplines):
        unknown = set(item.requires) - known
        if unknown:
            raise ValueError(f"catalog {item.kind} {item.id} has unknown requirement(s): {', '.join(sorted(unknown))}")
    profile_ids: set[str] = set()
    for profile in raw.get("profiles", []):
        if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
            raise ValueError("catalog profiles must be objects with an id")
        if profile["id"] in profile_ids:
            raise ValueError(f"duplicate catalog profile id: {profile['id']}")
        profile_ids.add(profile["id"])
        for key in ("lanes", "disciplines"):
            values = profile.get(key, [])
            if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                raise ValueError(f"catalog profile {profile['id']}.{key} must be an array of strings")
            allowed = set(catalog.ids(key))
            unknown = set(values) - allowed
            if unknown:
                raise ValueError(f"catalog profile {profile['id']} has unknown {key}: {', '.join(sorted(unknown))}")
    return catalog


def _load_catalog_path(path: Path) -> Catalog:
    try:
        value, _ = read_bounded_json(path, max_bytes=2_097_152)
    except SafeInputError as exc:
        raise ValueError(f"catalog input rejected: {exc}") from exc
    return parse_catalog(value)


def load_catalog(repo_root: Path | None = None, *, prefer_repo: bool = False) -> Catalog:
    path = Path(repo_root) / "catalog.json" if repo_root is not None and prefer_repo else None
    if path is None or not os.path.lexists(path):
        path = Path(resources.files("engineering_core").joinpath("catalog.json"))
    return _load_catalog_path(path)


def load_catalog_history(version: str, repo_root: Path | None = None, *, prefer_repo: bool = False) -> Catalog:
    filename = f"{version}.json"
    path = Path(repo_root) / "catalog-history" / filename if repo_root is not None and prefer_repo else None
    if path is None or not os.path.lexists(path):
        path = Path(resources.files("engineering_core").joinpath("catalog-history", filename))
    return _load_catalog_path(path)
