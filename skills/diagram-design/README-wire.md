# Wire diagram renderer (MVP)

Callable harness lane diagrams on top of **diagram-design**. Specs are YAML (`wire: 1`); outputs are self-contained HTML, deterministic SVG, Markdown tables, and optional PNG.

## Quick start

```bash
cd skills/diagram-design
python3 scripts/validate_spec.py fixtures/wire/team-report-wire.yaml
python3 scripts/wire.py fixtures/wire/team-report-wire.yaml --out /tmp/wire --png --svg --html --md
python3 scripts/self_check.py /tmp/wire/team-report-wire.html
python3 scripts/test_wire_fixtures.py
```

PNG export requires Playwright:

```bash
pip install playwright
playwright install chromium
```

## Files

| Path | Role |
|---|---|
| `schemas/wire.schema.json` | JSON Schema for spec v1 |
| `scripts/validate_spec.py` | Validator (unique ids, edges, lanes) |
| `scripts/render_wire.py` | Layout + SVG/HTML/MD |
| `scripts/export_png.py` | Playwright PNG (scale 2, solid paper) |
| `scripts/wire.py` | CLI entry point |
| `fixtures/wire/` | Valid fixtures + `broken/` negative cases |
| `assets/fonts/wire/` | Vendored OFL woff2 (offline headless) |
| `references/type-wire.md` | Authoring reference |

## Fonts

Geist, Geist Mono, and Instrument Serif woff2 files are vendored from Fontsource (OFL). Wire output never loads Google Fonts.
