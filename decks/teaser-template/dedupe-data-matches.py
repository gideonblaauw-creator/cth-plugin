#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(n: str) -> str:
    return (n or "").strip().lower()


for p in sorted(ROOT.glob("*-teaser/data.json")):
    data = json.loads(p.read_text())
    for g in data.get("gaps") or []:
        seen = set()
        out = []
        for m in g.get("matches") or []:
            k = norm(m.get("name", ""))
            if not k or k in seen:
                continue
            seen.add(k)
            out.append(m)
        g["matches"] = out
        g["match_count"] = len(out)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
