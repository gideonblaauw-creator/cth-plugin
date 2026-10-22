#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = "Who shaped this snapshot"
ES = "Quién elaboró este snapshot"

for p in sorted(ROOT.glob("*-teaser/data.json")):
    data = json.loads(p.read_text())
    data.setdefault("ui", {}).setdefault("en", {})["team.title"] = EN
    data.setdefault("ui", {}).setdefault("es", {})["team.title"] = ES
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(p.parent.name)
