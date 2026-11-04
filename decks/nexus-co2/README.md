# Nexus CO₂ impact deck (draft)

Self-reported CO₂ figures from Nexus startups — websites (`research/nexus-co2/co2.csv`) and investor decks (`research/nexus-co2/co2-decks.csv`).

- **Shell:** `decks/_templates/clp26-rein-shell/` (PR #126) — topbar navigation, `imp-grid` / `growth-card` styling, explorer filters, Chart.js bar chart, sortable table.
- **Brand:** CleantechHUB palette via template `styles.css` (`#335D4F`, `#FF6633`, Open Sans / Poppins).
- **Publish:** Do not deploy to `decks.cleantechhub.net` without Gideon's GO.

## Build

```bash
cd decks/nexus-co2 && ./build.sh
```

Generates `data/co2.json` from the repo CSV.

## Local preview

```bash
cd decks/nexus-co2 && python3 -m http.server 8765
```

Open http://127.0.0.1:8765/index.html (`fetch` requires HTTP, not `file://`).

## Screenshots (1440×900)

With the server running:

```bash
python3 capture-slides.py
```

Writes PNGs to `/opt/cursor/artifacts/nexus-co2-slides/`.
