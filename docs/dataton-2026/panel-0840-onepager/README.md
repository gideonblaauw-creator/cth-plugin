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
| `assets/logos/datalab-lockup.png` | Datalab datagrid + *powered by* + `cleantechhub-official.png` (from trimmed SVG) |
| `Panel-0840-proof-cobrand-300dpi.png` | 300 dpi crop: full co-brand row |
| `Panel-0840-proof-g-from-pdf-200dpi.png` | 200 dpi crop: *programa* from the rendered page |
| `Panel-0840-proof-g-from-ttf-200dpi.png` | Same word from `fonts/OpenSans-Regular.ttf` |
| `fonts/` | Google Open Sans v3.003 static TTFs + `OFL.txt` |

The embedded *g* in the PDF must match the committed TTF *g* point for point: **double-storey (binocular) g, same outline as the committed v3.003 TTF** (not DejaVu single-storey). Proof crops come from `prove-font-g.py`.

Layout references: agenda PR #176 (`d0b2ede2`), Datalab Option A endorsed mark PR #134 (`aa1902ac`).