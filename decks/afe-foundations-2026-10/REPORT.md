# AFE Foundations deck — visual pass report

**Branch:** `cursor/afe-foundations-mockup` · **PR:** #92  
**Deck:** `decks/afe-foundations-2026-10/index.html` · **Stage:** 1280×720

## Slides (13)

| # | Slide | Visual notes |
|---|--------|----------------|
| 1 | Portada | Full-bleed `hero-cover.jpg` + glass panel |
| 2 | Por qué ahora | Full-bleed `hero-rural.jpg` section band |
| 3 | Quiénes somos | Solid deep blue |
| 4 | Trayectoria | Stat tiles + CLP band + `clp-colombia.jpg` |
| 5 | Aliados y partners | **New** — `cth-partners-section.jpg` from cleantechhub.net |
| 6 | Portafolio | `nexus-portfolio.jpg` + four Nexus/academy cards |
| 7 | Lo que escuchamos | Solid deep blue |
| 8 | Área 1 · Co-financiar cohortes | Solid deep blue |
| 9 | Área 2 · Blended finance | Solid deep blue |
| 10 | Datalab | `hero-data.jpg` + `datalab-live.jpg` + `datalab-site.jpg` |
| 11 | AuRA (en estructuración) | Solid deep blue |
| 12 | Cómo empezamos | Solid deep blue |
| 13 | Equipo + CTA | Full-bleed `hero-energy.jpg` |

> Note: partners slide adds one slide vs. the original 12-slide mock-up; all prior slides and PENDIENTE chips are preserved.

## Images in `img/`

| File | Source |
|------|--------|
| `hero-cover.jpg` | Unsplash — Matthew Henry (wind / nature) |
| `hero-rural.jpg` | Unsplash — Geranimo (rural field) |
| `hero-data.jpg` | Unsplash — Luke Chesser (analytics) |
| `hero-energy.jpg` | Unsplash — American Public Power Association (solar) |
| `nexus-portfolio.jpg` | Playwright capture — https://nexus.cleantechhub.net/p/startup-portfolio (1440×900) |
| `clp-colombia.jpg` | Playwright capture — https://climatelaunchpad.org/countries/colombia/ |
| `cth-partners-section.jpg` | Playwright capture — https://cleantechhub.net/ (scrolled to partners area) |
| `datalab-live.jpg` | Copied from `decks/apc-2026-10-07/img/b-live-datalab.png` (branch `apc-2026-10-07`) |
| `datalab-site.jpg` | Playwright capture — https://datalab.cleantechhub.net |

All JPGs are compressed to ≤ ~400 KB where possible.

## Failed / partial captures

| Target | Outcome |
|--------|---------|
| `climatelaunchpad.org/countries/colombia/` (first pass, `networkidle`) | **Failed** — timeout; **recovered** with `domcontentloaded` → `clp-colombia.jpg` |
| `cleantechhub.net` full-page partners (first pass) | **Failed** — timeout; **recovered** viewport scroll capture → `cth-partners-section.jpg` |
| `nexus …?epic=1` | Captured (`nexus-epic.jpg`) but **not used** on slide (portfolio view used instead); file removed from repo to avoid unused assets |
| Teclogi on Nexus | **Not listed** in Nexus search; card text from **cleantechhub.net/academy** only |

## PENDIENTE chips (unchanged intent)

- Por qué ahora: national climate/rural/finance figures; philanthropy vs. impact data
- Quiénes somos · Datalab: public Datalab page copy
- Portafolio · Teclogi: Series A terms/figures; other cards financial detail
- Área 1: calendar, costs, selection criteria
- Área 2: tickets, instruments, legal terms
- Datalab: metrics/units/frequency; board report template
- AuRA: scope, indicators, amounts, timeline (program **en estructuración**, not signed)
- Cómo empezamos · Datalab pilot scope
- Equipo · Angélica Díaz detailed public role

## Style changes

- Removed blue–green **gradient** on `.slide.plain` (solid `#0C498A` only)
- CTH five-colour palette, Titillium + Open Sans, local `assets/cth-logo.png`
- Photo slides keep dark scrim + glass (no off-palette gradients on content slides)

## Preview artifacts

Saved under `/opt/cursor/artifacts/`:

- `afe-preview-cover.png` (slide 1)
- `afe-preview-trayectoria.png` (slide 4)
- `afe-preview-portafolio.png` (slide 6)
- `afe-preview-datalab.png` (slide 10)
