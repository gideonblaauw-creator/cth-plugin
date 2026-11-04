#!/usr/bin/env bash
# Build data/co2.json from canonical CSV for static fetch in app.js.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
CSV="$REPO/research/nexus-co2/co2.csv"
OUT="$ROOT/data/co2.json"

python3 << PY
import csv, json
from pathlib import Path
rows = []
with open("$CSV", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        r["value_tco2e"] = float(r["value_tco2e"])
        rows.append(r)
Path("$OUT").write_text(json.dumps({"rows": rows, "coverage": {
    "portfolio": 174,
    "websitesChecked": 126,
    "noWebsite": 48,
    "unreachable": 22,
    "decksInManifest": 47,
    "decksWithCo2Extract": 17
}}, indent=2) + "\n", encoding="utf-8")
print("Wrote", "$OUT", "with", len(rows), "rows")
PY
