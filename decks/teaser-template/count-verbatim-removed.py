#!/usr/bin/env python3
"""Count stored Spanish verbatim fields no longer rendered (template policy)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count_page(data: dict) -> dict:
    gap_q = sum(1 for g in data.get("gaps", []) if (g.get("report_evidence") or {}).get("quote_es"))
    match_q = sum(
        1 for g in data.get("gaps", []) for m in g.get("matches", []) if m.get("public_quote")
    )
    snap = (data.get("snapshot") or {}).get("report_evidence") or {}
    snap_q = 1 if snap.get("quote_es") else 0
    per_gap = []
    for g in data.get("gaps", []):
        n = 0
        if (g.get("report_evidence") or {}).get("quote_es"):
            n += 1
        n += sum(1 for m in g.get("matches", []) if m.get("public_quote"))
        per_gap.append(n)
    return {
        "gap_report_quotes": gap_q,
        "match_public_quotes": match_q,
        "snapshot_quotes": snap_q,
        "total_not_rendered": gap_q + match_q + snap_q,
        "per_gap": per_gap,
    }


def main() -> None:
    import sys

    out = {}
    for p in sorted(ROOT.glob("*-teaser/data.json")):
        slug = p.parent.name.replace("-teaser", "")
        out[slug] = count_page(json.loads(p.read_text()))
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
