#!/usr/bin/env python3
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "celsia-teaser" / "data.json"
data = json.loads(p.read_text())
data.get("nexus", {}).pop("KIMSA", None)
for g in data.get("gaps") or []:
    before = len(g.get("matches") or [])
    g["matches"] = [m for m in g.get("matches") or [] if m.get("name") != "KIMSA"]
    if len(g["matches"]) != before:
        g["match_count"] = len(g["matches"])
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print("KIMSA removed from Celsia; gap 1 match_count", data["gaps"][0]["match_count"])
