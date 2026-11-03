# Promigas demo — i18n (ES default · EN toggle)

**Scope:** `services/energy-coop/demo-promigas/` only.

## Files changed

| File | Role |
|------|------|
| `services/energy-coop/demo-promigas/i18n.js` | ES/EN string tables, `localStorage` + `?lang=en|es`, `CthI18n.applyDom()` |
| `services/energy-coop/demo-promigas/index.html` | `data-i18n` / `data-i18n-html` / `data-i18n-aria` markers; fixed top-right ES \| EN toggle; map/wizard strings via `CthI18n.t()` |
| `docs/energy-coop/demo-promigas-i18n.md` | This note |

## How the toggle works

1. **Default:** Spanish on first load (no stored preference).
2. **Fixed control:** `#lang-toggle` (top-right, CTH green active state on white pill).
3. **Persistence:** `localStorage` key `cth-demo-promigas-lang` (`es` \| `en`).
4. **URL override:** `?lang=en` or `?lang=es` on load (also written to `localStorage` when chosen via toggle).
5. **Markup:** Static copy uses `data-i18n` / `data-i18n-html`; Leaflet popups, wizard options, CEOF flow steps, and post-click button labels refresh on `CthI18n.onChange`.

## Strings intentionally left untranslated

| Area | Reason |
|------|--------|
| OpenStreetMap tile labels and attribution (`© OpenStreetMap`, place names) | Third-party map tiles |
| KPI / citation **link anchor text** where it matches the source document title (e.g. `Informe IMPE 2025 (PDF)`, `Boletín ICEE 2024 (UPME)`, `Guía del Gas`, `CLSA sector energético`, university / media link labels) | Proper names / published titles |
| Map popup source labels (`FENOGE + MinEnergía`, `Gutami + Holland House`, etc.) | Citation labels tied to sources |
| Numeric values, kWp/MW figures, dates, org names (Promigas, FENOGE, Gutami, IE Chiricoco, Uninorte, …) | Per fact-check scope |
| `fundacionpromigas.org.co` domain in Paiva popup | URL display |
| kWp size buttons (`10 kWp`, …) | Units + numbers only |

## Per-screen coverage

| Screen | ES | EN | Gaps |
|--------|----|----|------|
| 1 Paiva | Complete UI | Complete UI | Map tiles only (see table) |
| 2 La Guajira | Complete UI | Complete UI | Popups refresh on toggle; map tiles unchanged |
| 3 Cooperative simulation | Complete UI | Complete UI | kWp button labels unchanged (numeric) |
| 4 Meta 2030 | Complete UI | Complete UI | Some proposal bullet `<strong>` emphasis folded into plain strings (wording unchanged) |

## Verification (2026-11-03)

- `python3 -m http.server 8765` in `services/energy-coop/demo-promigas/`
- Headless Chrome: `index.html`, `index.html?lang=en`, hashes `#0`–`#3` — no layout breakage observed; default ES without query param.
