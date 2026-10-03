#!/usr/bin/env python3
"""Flag source facts missing from a wire brief."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s\)\]>\"']+", re.I)
BC_ID_RE = re.compile(r"\bbc[-_]?[a-z0-9]{6,}\b", re.I)
DATE_RE = re.compile(
    r"\b(\d{4}-\d{2}-\d{2}|\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b",
    re.I,
)
NUMBER_RE = re.compile(
    r"\b(\d+(?:\.\d+)?(?:%|k|K|M)?)\b"
)
# Capitalized multi-word or single proper-like tokens (min length 2)
ENTITY_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+|[A-Z][a-z]{2,})\b")

STOP_ENTITIES = {
    "The", "This", "That", "When", "What", "Where", "How", "Yeah", "So", "If",
    "English", "Spanish", "Oct", "Example", "Goal", "Actors", "Steps", "Status",
    "Locks", "Unknown", "Scope",
}


def extract_facts(text: str) -> dict[str, set[str]]:
    urls = set(URL_RE.findall(text))
    bc_ids = {m.group(0) for m in BC_ID_RE.finditer(text)}
    dates = set(DATE_RE.findall(text))
    dates = {d[0] if isinstance(d, tuple) else d for d in dates}
    numbers = set(NUMBER_RE.findall(text))
    entities: set[str] = set()
    for m in ENTITY_RE.finditer(text):
        ent = m.group(1).strip()
        if ent in STOP_ENTITIES:
            continue
        if ent.lower() in {"github", "vps"}:
            entities.add(ent)
            continue
        entities.add(ent)
    return {
        "urls": urls,
        "bc_ids": bc_ids,
        "dates": dates,
        "numbers": numbers,
        "entities": entities,
    }


def normalize_for_search(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def fact_in_brief(fact: str, brief: str) -> bool:
    if not fact:
        return True
    b = brief.lower()
    f = fact.lower()
    if f in b:
        return True
    # Numbers: allow comma variants
    if re.fullmatch(r"[\d.]+%?", fact) and fact.rstrip("%") in b.replace(",", ""):
        return True
    return False


def compare(source: str, brief: str) -> dict:
    src = extract_facts(source)
    missing: dict[str, list[str]] = {
        "urls": [],
        "bc_ids": [],
        "dates": [],
        "numbers": [],
        "entities": [],
    }
    for kind, values in src.items():
        for val in sorted(values):
            if not fact_in_brief(val, brief):
                missing[kind].append(val)
    total = sum(len(v) for v in missing.values())
    return {"missing": missing, "summary": {"missing_count": total}}


def human_report(report: dict) -> str:
    lines = [
        f"Fact check: {report['summary']['missing_count']} missing fact(s) in brief",
        "",
    ]
    for kind, vals in report["missing"].items():
        if not vals:
            continue
        lines.append(f"{kind}:")
        for v in vals:
            lines.append(f"  - {v}")
    if report["summary"]["missing_count"] == 0:
        lines.append("All extracted source facts appear in the brief.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare source transcript to brief.md")
    parser.add_argument("source", type=Path, help="Source transcript path")
    parser.add_argument("brief", type=Path, help="Brief markdown path")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    brief = args.brief.read_text(encoding="utf-8")
    report = compare(source, brief)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(human_report(report))
        print("\n--- JSON ---")
        print(json.dumps(report, indent=2))
    return 0 if report["summary"]["missing_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
