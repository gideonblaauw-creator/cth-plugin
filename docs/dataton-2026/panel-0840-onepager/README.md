# Panel 08:40 · Datatón 24 nov 2026 — one-pager

Spanish A4 panel brief for Gideon to email 08:40 panelists. **Awaiting Gideon's approval** before send.

## Build

```bash
python3 build-render.py
./self-check.sh
```

Requires Playwright Chromium (`python3 -m playwright install chromium`) and local Poppler utils on `PATH` (see `self-check.sh`).

## Artifacts

| File | Role |
|------|------|
| `panel-0840-dataton-24nov.html` | Source (Open Sans `@font-face`, agenda v5 letterhead layout, Datalab endorsed logo) |
| `Panel-0840-Dataton-24nov.pdf` | Print PDF |
| `Panel-0840-Dataton-24nov.png` | 200 dpi full page |
| `Panel-0840-Dataton-24nov-crop-g-logo.png` | Crop: Datalab mark + double-storey *g* in title band |
| `fonts/` | Google Open Sans v3.003 static TTFs + `OFL.txt` |

Layout references: agenda PR #176 (`d0b2ede2`), Datalab Option A endorsed mark PR #134 (`aa1902ac`).