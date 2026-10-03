#!/usr/bin/env python3
"""Validate a CTH wire diagram YAML spec (wire v1)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required") from exc

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_DIR / "schemas" / "wire.schema.json"
DEFAULT_LANES = ["gideon", "orchestrator", "desks", "hands", "tools"]


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("spec root must be a mapping")
    return data


def validate_structure(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if spec.get("wire") != 1:
        errors.append("wire must be 1")
    for key in ("id", "title", "lang", "layout", "nodes", "edges"):
        if key not in spec:
            errors.append(f"missing required field: {key}")
    if "lang" in spec and spec["lang"] not in {"en", "es", "en+es"}:
        errors.append("lang must be en, es, or en+es")
    if "layout" in spec and spec["layout"] not in {"lanes", "flow", "before-after"}:
        errors.append("layout must be lanes, flow, or before-after")
    nodes = spec.get("nodes")
    edges = spec.get("edges")
    if nodes is not None and not isinstance(nodes, list):
        errors.append("nodes must be a list")
    if edges is not None and not isinstance(edges, list):
        errors.append("edges must be a list")
    return errors


def validate_graph(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lanes = spec.get("lanes") or DEFAULT_LANES
    if not isinstance(lanes, list):
        errors.append("lanes must be a list when provided")
        return errors
    lane_set = set(lanes)
    nodes = spec.get("nodes") or []
    edges = spec.get("edges") or []
    node_ids: list[str] = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"node {index} must be a mapping")
            continue
        nid = node.get("id")
        if not isinstance(nid, str) or not nid:
            errors.append(f"node {index} missing id")
            continue
        node_ids.append(nid)
        lane = node.get("lane")
        if lane not in lane_set:
            errors.append(f"node {nid!r} lane {lane!r} is not in lanes")
        status = node.get("status")
        if status not in {"done", "waiting", "blocked", "hold"}:
            errors.append(f"node {nid!r} has invalid status {status!r}")
    dupes = {nid for nid in node_ids if node_ids.count(nid) > 1}
    if dupes:
        errors.append(f"duplicate node ids: {', '.join(sorted(dupes))}")
    id_set = set(node_ids)
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edge {index} must be a mapping")
            continue
        src = edge.get("from")
        dst = edge.get("to")
        kind = edge.get("kind")
        if kind not in {"ask", "ticket", "hitl", "data"}:
            errors.append(f"edge {index} kind must be ask|ticket|hitl|data")
        if src not in id_set:
            errors.append(f"edge {index} from {src!r} does not resolve to a node")
        if dst not in id_set:
            errors.append(f"edge {index} to {dst!r} does not resolve to a node")
    return errors


def validate_spec_dict(spec: dict[str, Any]) -> list[str]:
    errors = validate_structure(spec)
    if errors:
        return errors
    return validate_graph(spec)


def validate_spec_path(path: Path) -> list[str]:
    try:
        spec = load_spec(path)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [str(exc)]
    return validate_spec_dict(spec)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specs", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.specs:
        errors = validate_spec_path(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
