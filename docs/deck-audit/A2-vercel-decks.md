# A2 — Sep–Oct 2026 CleantechHUB decks on Vercel

Audit date: 19 Oct 2026. Read-only. Public `curl` against the live hosts, then the built HTML on the source branches in this repo, plus one public GitHub file where the live body was not served. Nothing was deployed. No pull request.

## Method

Every known host was requested with `curl -sS -L` on 19 Oct 2026, 21:02 UTC, including `/?print=1`. Wayback CDX (`web.archive.org/cdx`) for the same hosts returned `[]`.

All nine known hosts, plus `https://teclogi-financial-model.vercel.app`, answered **HTTP 402** with `x-vercel-error: DEPLOYMENT_DISABLED` and the body `Payment required`. The hostname is allocated. The HTML is not public. Slide counts below are from the last built `index.html` on the named git branch, or from the public Energy Coops file. They are not a re-measurement of the disabled Vercel response.

| Host | HTTP | Vercel error | Content used |
|---|---|---|---|
| `apc-cth-2026-10-07.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | `origin/apc-2026-10-07` @ `17d3795`, `decks/apc-2026-10-07/index.html` |
| `b4b-cth-2026-10-13.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | `origin/meetings-2026-10-13-b4b` @ `7cb3f08`, `decks/meetings-2026-10-13/b4b/index.html` |
| `matamala-brief-2026-10-13.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | `origin/meetings-2026-10-13-matamala` @ `a13a0eb`, deck `index.html` and `brief.html` |
| `teclogi-jose-2026-10-13.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | No copy in this repo |
| `teclogi-brief-2026-10-13.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | No copy in this repo |
| `epic-angels-cth-2026-10-16.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | No copy in this repo |
| `energy-coops-cth.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | Public `gideonblaauw-creator/energy-coops-cth` @ `c8fc515` (`index.html`) |
| `grp-ic-2026-application.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | No copy in this repo |
| `teclogi-financial-model.vercel.app` | 402 | `DEPLOYMENT_DISABLED` | No copy in this repo |

`git log -S teclogi-financial-model` on this repo is empty. GitHub code search `teclogi-financial-model user:gideonblaauw-creator` returned `total_count: 0`. The ten repositories visible to this token do not contain that name. A same-name GitHub repo URL returned 404.

Guessed hosts that returned **404** `DEPLOYMENT_NOT_FOUND`: `cee-datathon-2026-10-14.vercel.app`, `cee-datathon-cth-2026-10-14.vercel.app`, `matamala-cth-2026-10-13.vercel.app`, `teclogi-financial-model-2026.vercel.app`, `energy-sprint-cohort.vercel.app`, `epic-angels.vercel.app`, `grp-ic.vercel.app`, `teclogi.vercel.app`, `teclogi-cth.vercel.app`.

## Common pattern

The October meeting decks that can be read (APC, Bridge for Billions, Matamala deck, and the CEE source deck) share one shell.

- Language is Spanish (`<html lang="es">`). There is no EN/ES toggle.
- `build.sh` concatenates `shell/head.html`, inlined `shell/deck.css`, every `slides/*.html` in sort order, and inlined `shell/deck.js` into one `index.html`. Photos stay in `img/` and are not inlined.
- DOM is `.deck-viewport` > `.deck-frame` > `.deck-stage` > `.deck#deck` > `section.slide`.
- Stage size is `--stage-w: 1920px` and `--stage-h: 1080px`. `@page { size: 1920px 1080px; margin: 0; }`.
- The **0.96 deck-frame** is JavaScript, not a CSS variable. `scaleStage()` sets `scale = Math.min(vw / 1920, vh / 1080) * 0.96`, writes that scale onto `.deck-frame` width and height, and sets `.deck-stage { transform: scale(...) }` with `transform-origin: top left`. `?print` and `#print` skip scaling and add `body.print-all`, which shows every slide. `@media print` does the same.
- One slide has `.active`. Navigation is Arrow keys, Space, Page Up/Down, hash `#N`, and a click on the left or right half of the stage. A fixed hint reads `← → · espacio · clic`.
- Slide types are a cover, a badge plus title, glass cards and grids, optional full-bleed photo (`.has-photo` with `--bg`), a footer, and a `.slide-num` filled as `n / total`.
- Citations are a `.src` line on the slide, a sibling `SOURCES.md`, and, on APC only, a closing sources slide.
- `[PENDIENTE]` is a dashed chip, class `.pendiente`.
- Export is Playwright at 1920×1080: one PNG per slide, then a PDF. APC calls `page.pdf`. Bridge for Billions and Matamala stitch the PNGs with `img2pdf` at 508 mm × 285.75 mm (1920×1080 px at 96 dpi). The print URL is `index.html?print`.
- Tokens are a blue meeting palette, not the CleantechHUB brand green:

| Token | Hex | Role in these decks |
|---|---|---|
| `--deep` | `#0C498A` | Stage gradient, numbers, chrome |
| `--cyan` | `#B2EEFA` | Titles, chips, links |
| `--green` | `#9DC384` | Secondary accent |
| `--forest` | `#669348` | Rare accent |
| `--sky` | `#69B5FA` | Secondary dashed chip |
| `--white` | `#FFFFFF` | Text |
| Page ground | `#051a33` | Viewport behind the stage |

- Type is **Open Sans** (weights 400, 600, 700) from Google Fonts. APC and CEE also load **PT Sans** and list it in `--font`. None of the readable files set `font-family` to Inter.
- None of the readable files use `#2D6A4F`, `#1B4332`, or `#95D5B2`.
- There is no tab widget and no chart library (`canvas` count is 0). Diagrams, when present, are inline SVG or CSS grids.

`shell/deck.css` and `shell/deck.js` on the Bridge for Billions branch and the Matamala branch are byte-identical. `build.sh` on those two branches is also byte-identical. APC `build.sh` and the CEE `build.sh` match each other and omit the later chrome.

## Outliers

1. **Live body is unavailable.** Every requested host is paused with HTTP 402 `DEPLOYMENT_DISABLED` (`Payment required`). A 404 would mean the name was never deployed. These names were deployed and are now disabled. `?print=1` returns the same 402.
2. **Brand.** The readable decks do not use the CleantechHUB brand skill palette or Inter. They use the blue meeting palette and Open Sans / PT Sans.
3. **APC (7 Oct) is the base shell.** No index, no dots, no lightbox, no expandable cards, no question toggle. PT Sans is in the font stack. Slide 21 is a real sources slide (`Fuentes públicas`) plus per-slide `.src` lines. On 7 Oct the visible `[PENDIENTE]` chips were wrapped in HTML comments (`OCULTO 7 oct 2026`); one `[en construcción]` chip remains on the MubOn line. `render-deck.py` refuses any count other than 21 and writes `APC-CTH-2026-10-07.pdf` with Playwright `page.pdf`. `smoke-layout.py` checks the letterbox at 1366×768 and 1512×982. There is no `vercel.json`. Branches `apc-2026-10-07-a` through `-d` are partial slide packs, not the 21-slide file.
4. **Bridge for Billions and the Matamala deck (13 Oct) add chrome.** `build.sh` injects an Índice dialog (`data-menu-title`), slide dots, a `Mostrar preguntas` toggle (`body.show-questions`), and a lightbox. Expandable cards (`.expand-card` / `.expand-trigger` / `.expand-body`) start closed; `?print` forces them open. Font stack is Open Sans only. There is no sources slide. Footnotes use `.src` or `.cite`. PDF is PNG plus `img2pdf`, with a hard count of 9. Matamala is the only one of this pair with `vercel.json` (`cleanUrls: true`, `trailingSlash: false`).
5. **Matamala brief is not a deck.** `brief.html` equals `decks/meetings-2026-10-13/matamala/meeting-brief.html` (sha256 `88b425b5…`). English, six scrolling sections, sticky nav, four `<details class="partner-card">` cards, no `.deck-frame`, no 1920 stage, no 0.96 scale. `?print` adds `html.print-mode`, opens every card, and prints near A4 (`max-width: 210mm`). Eight visible `[PENDIENTE]` lines. The Vercel project name is `matamala-brief`. Because the host returns 402, the file at `/` is not observable. A static deploy of `matamala-deck/` would serve the 9-slide deck at `/` and this brief at `/brief`.
6. **Energy Coops is an older print stack (28 Aug 2026).** It is not in this repo. Ten `section.slide` pages at **297 mm × 210 mm** (A4 landscape), stacked in `.deck-container`, all visible at once. No JavaScript navigation, no `.deck-frame`, no 0.96 scale, no `?print` flag. Print is `@page { size: A4 landscape }` and `@media print`. Spanish title plus a static English `.subtitle-en`. Photo gutter, metric boxes, and tables. One source line (Strategie Belangenbehartiging, 15 Jan 2026). No `[PENDIENTE]`. `vercel.json` is `{"cleanUrls": true}`. Commit message: “Deploy rebuilt Energy Coop deck with photo backgrounds.”
7. **CEE Externado (source only).** Same APC shell, plus `?review`, which reveals `.pendiente` (hidden by default; amber `#FFD166`; CSS prefix `PENDIENTE · `). Thirteen slides. One inline SVG (alliance triangle), not a chart library. No sources slide; `SOURCES.md` sits beside the deck. Build notes in `decks/cee-datathon-2026-10-14/README.md`: `tools/gen.py` writes slides, `tools/render.js` writes PNG, a review pass, an overflow check, and the PDF. Probes of `cee-datathon-2026-10-14.vercel.app` and `cee-datathon-cth-2026-10-14.vercel.app` returned 404. No confirmed live host.
8. **Five hosts have no readable body:** Teclogi José, Teclogi brief, Epic Angels, GRP IC 2026 application, and `teclogi-financial-model`. Slide count, chrome, tokens, and `[PENDIENTE]` usage are unknown from public `curl`.

## Per deck

### 1. APC Colombia — `https://apc-cth-2026-10-07.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`. `?print=1` same.
- **Source:** `decks/apc-2026-10-07/` on `origin/apc-2026-10-07` (`17d3795`, 7 Oct 2026). Built file sha256 `e90e5224b575854a6d15bcc40d12fea324623111c51e45a261136adf1ecdd27a` (56,157 bytes).
- **Slides:** 21. Title: `CleantechHUB × APC Colombia · 7 oct 2026`.

| # | Title | Type |
|---|---|---|
| 01 | CleantechHUB × APC Colombia | Cover, photo |
| 02 | Agenda | Numbered list |
| 03 | Quiénes somos | Photo + `.src` |
| 04 | Demo en vivo · Datalab (4 min) | Deep gradient |
| 05 | Programas · de la idea al mercado | Photo + cards |
| 06 | Lo que acaban de ver | Deep + `.src` |
| 07 | Entorno 1 · Datalab | Live capture |
| 08 | Entorno 2 · Datathon | Live capture |
| 09 | Entorno 3 · Living lab | Live capture |
| 10 | Entorno 4 · Producto cliente | Live capture |
| 11 | Filtro Epic Angels en Nexus | Deep + `.src` |
| 12 | Proyectos · plataformas vivas | Photo |
| 13 | PNUD · AFCIA | Gradient + `.src` |
| 14 | AuRA | Photo |
| 15 | Energy Coops × CPI Global Innovation Lab for Climate Finance 2026 | Photo |
| 16 | Startups del portafolio CTH que accedieron a financiación | Photo |
| 17 | Caso Proplanet | Photo + `.src` |
| 18 | MubOn · WEIA · Bio Natural Solutions | No photo + `.src` |
| 19 | Encaje con la convocatoria APC | No photo + `.src` |
| 20 | La solicitud a APC | Photo, numbered ask |
| 21 | Fuentes públicas | Sources slide, two columns of links |

- **Interactivity:** arrows, Space, click-halves, hash, `?print` / `#print`. No tabs, toggle, expandable cards, charts, EN/ES switch, index, or lightbox.
- **Citations:** per-slide `.src` (12) and slide 21. Sibling files `SOURCES.md` and `PENDIENTES.md`, plus `notes/*-SOURCES.md` and `notes/*-PENDIENTES.md`.
- **Brand:** meeting palette above. `--font: 'Open Sans', 'PT Sans', sans-serif`. Google Fonts Open Sans 400/600/700 and PT Sans 400/700.
- **Stage:** 1920×1080. Frame scale × 0.96 in `shell/deck.js`.
- **Build:** `build.sh` → `index.html`. `render-deck.py` (Playwright Chromium, viewport 1920×1080, `?print`, 21 PNGs in `png/`, `page.pdf` → `APC-CTH-2026-10-07.pdf`). `smoke-layout.py` for letterbox. No `vercel.json` in the tree.
- **`[PENDIENTE]`:** eight chips remain only inside HTML comments. Screen shows none of those chips. One visible `<span class="pendiente">[en construcción]</span>` on the MubOn URL. `PENDIENTES.md` still lists the hidden gaps (WEIA and Bio Natural Solutions finance, RTE / public accounts, five departments, application status, philanthropy-route status).

### 2. Bridge for Billions — `https://b4b-cth-2026-10-13.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`.
- **Source:** `decks/meetings-2026-10-13/b4b/` on `origin/meetings-2026-10-13-b4b` (`7cb3f08`, 13 Oct 2026). sha256 `2b8709dbd405eec427e1b9e83d51f0bedac5f45b6dab6dd853882e5cf69d5afb` (50,379 bytes).
- **Slides:** 9. Title: `CleantechHUB × Bridge for Billions · 13 oct 2026`. All sections are `.slide-deep` (no photo class).

| # | `data-menu-title` | Extras |
|---|---|---|
| 01 | Portada | `[PENDIENTE]` |
| 02 | Encaje CTH × B4B | Expand cards + `.src` |
| 03 | Conecta / Fondo Verde Catalítico | Expand cards + `.src` |
| 04 | CTH × B4B vía Conecta | Expand cards + `.src` |
| 05 | REIN Hubs | `[PENDIENTE]` + `.src` |
| 06 | Nexus + Epic Angels | `.src` |
| 07 | Datalab (4 entornos) | Lightbox + `.src` |
| 08 | Preguntas de colaboración | Question block |
| 09 | Próximos pasos | Expand + lightbox + `[PENDIENTE — fecha]` |

- **Interactivity:** base arrows and click-halves, plus Índice, dot nav, question toggle, expandable cards, lightbox (Escape closes menu and lightbox). `?print` opens expand bodies and question blocks and hides chrome. No tabs, charts, or EN/ES switch.
- **Citations:** `.src` / `.cite` on slides 02–09. No sources slide. Sibling `SOURCES.md` and `PENDIENTES.md`.
- **Brand:** same meeting hexes. `--font: 'Open Sans', sans-serif` only.
- **Stage:** 1920×1080 and × 0.96, same function as APC.
- **Build:** chrome-injecting `build.sh`. `render-deck.py` expects 9 slides, writes `png/01.png`–`09.png`, then `CTH-B4B-2026-10-13.pdf` via `img2pdf` at 508 mm × 285.75 mm. No `vercel.json`.
- **`[PENDIENTE]`:** six visible chips (Conecta–FVC link, financial relation, 2026–2027 eligibility, hub operating detail, follow-up date). CSS shows them in the presentation, unlike CEE.

### 3. Matamala — `https://matamala-brief-2026-10-13.vercel.app`

Two artifacts share the folder `decks/meetings-2026-10-13/matamala-deck/` on `origin/meetings-2026-10-13-matamala` (`a13a0eb`, 13 Oct 2026). Live HTML was not served, so which file is `/` is not proven. `vercel.json` in that folder only sets clean URLs.

#### 3a. Deck `index.html`

- sha256 `f34a736d41aa420f324a648c26248cf6c51d98676b704e53264a0d9b32085e74` (51,203 bytes).
- **Slides:** 9. Title: `CleantechHUB × ODS Cero · Datalab · 13 oct 2026`. Shell CSS, JS, and `build.sh` match Bridge for Billions byte for byte.
- **Menu:** Portada; Christian Matamala; ODS Cero · servicios; ODS Cero · datos y red; Encaje Datalab (hipótesis); Modelo de alianza (propuestas); Referencia Emprende UP; Preguntas de colaboración; Riesgos y PENDIENTES.
- **Interactivity:** same chrome as Bridge for Billions. Lightbox is used on the cover, data, fit, partnership, Emprende UP gallery, and risks slides. Expand cards on services, partnership, and risks.
- **Citations:** `.src` on every slide. No sources slide. Sibling `SOURCES.md`. `render-deck.py` writes `CTH-Matamala-ODS-Cero-2026-10-13.pdf` (9 pages, `img2pdf`).
- **Brand and stage:** identical to Bridge for Billions (Open Sans, 1920×1080, × 0.96).
- **`[PENDIENTE]`:** 14 visible bracket chips. Slide 09 is the risks list.

#### 3b. Brief `brief.html`

- Not a slide deck. sha256 `88b425b5c275bb3909bcf35a4b9ad29573900ecca2d4257f09c227bb6c650690` (23,983 bytes). Same bytes as `decks/meetings-2026-10-13/matamala/meeting-brief.html`.
- **Title:** `Collaboration brief — ODS Cero × Datalab · CleantechHUB`. `lang="en"`.
- **Structure:** sticky section index and six sections (Christian, ODS Cero, Datalab fit, partnership model, talking points, risks). Four expandable `<details>` partner cards (A Chile data provider, B local datathon, C referral, D governance).
- **Interactivity:** in-page nav and `<details>`. No tabs, charts, lightbox, arrows, or EN/ES toggle (the document is English only).
- **Citations:** footer points at `sources.md` and tells the reader to add `?print`. Many links (41 anchors). Class `.src` is used as source lines inside the prose.
- **Brand:** same hexes, renamed `--cth-blue`, `--cth-sky`, `--cth-sage`, `--cth-green`, `--cth-accent`, plus text `#1a2e3b` and muted `#3d5566`. Open Sans. Page ground `#eef4f9`. Not the green brand palette.
- **Stage:** none. No 0.96 frame. Screen column max 920 px. Print max-width 210 mm.
- **Build:** hand-written HTML. No `build.sh` for the brief. The deck `build.sh` does not emit `brief.html`.
- **`[PENDIENTE]`:** eight visible chips, all in section 6 (contract path, open-data maturity, consent, title on official charts, Holland House venue, prior relationship, investment figures, Colombia operations).

### 4. Teclogi José — `https://teclogi-jose-2026-10-13.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`. Body is the 78-byte Vercel payment text, not HTML.
- **Source:** no branch, path, or filename in this repo. Not in the public Energy Coops or Energy Sprint repos.
- **Slide count, chrome, citations, tokens, stage, build, `[PENDIENTE]`:** unknown.

### 5. Teclogi brief — `https://teclogi-brief-2026-10-13.vercel.app`

- Same 402 and the same source gap as Teclogi José. Content unknown.

### 6. Epic Angels — `https://epic-angels-cth-2026-10-16.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`. `epic-angels.vercel.app` is 404, so the dated name is the one that exists.
- **Source:** none in this repo. The APC deck has a slide named “Filtro Epic Angels en Nexus”, and Bridge for Billions has “Nexus + Epic Angels”. Those are slides inside other decks, not this host.
- Content of this host is unknown.

### 7. Energy Coops — `https://energy-coops-cth.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`.
- **Source:** public repo `gideonblaauw-creator/energy-coops-cth`, commit `c8fc515` (28 Aug 2026). File `index.html`, sha256 `7d6bc88240d282cda1de50553fc51b4a5fcfdd3dfb070641f888d57c7f45dae2` (43,793 bytes). `vercel.json`: `{"cleanUrls": true}`.
- **Slides:** 10, all painted at once (scroll), not a single-slide stage.

| # | Title | Type |
|---|---|---|
| 01 | Cooperativas Energéticas en Colombia | Cover, photo, four meta cells. Date on the slide: Friday 28 Aug 2026, Holland House, Bogotá |
| 02 | El Desafío de la Transición Energética Territorial | Photo gutter, 3 cards, English subtitle |
| 03 | La Referencia Neerlandesa: Energie Samen | Cards + the only source line |
| 04 | CleantechHUB × PASO Colombia: Construcción de Pipeline | Partnership cards |
| 05 | Alineación Estratégica con Pilares de Política Nacional | Policy cards |
| 06 | Ecosistema Neerlandés | Channel cards |
| 07 | Arquitectura del Piloto Asociativo Demostrativo | 4-stage roadmap |
| 08 | Estrategia de Interlocución Gubernamental | Table / cards |
| 09 | Plan de Acción Inmediato y Acuerdos de Trabajo | Action list |
| 10 | Construyendo Energía Comunitaria Sostenible | Close |

- **Interactivity:** none in JavaScript. No tabs, toggles, expandable cards, lightbox, index, arrows, hash routing, or `?print`. English is a subtitle under the Spanish title, not a switch. “Charts” are metric boxes and a styled table, not a canvas.
- **Citations:** one footer line on the Dutch-benchmark slide: Strategie Belangenbehartiging Jaargang 2026 (15 Jan 2026). No sources slide and no `SOURCES.md` in that repo root.
- **Brand:** `--deep #0C498A`, `--cyan #B2EEFA`, `--lgreen #9DC384`, `--fgreen #669348`, `--sky #69B5FA`. Open Sans and PT Sans, including italics. A five-band top bar repeats those hexes. Still not the green CleantechHUB brand tokens.
- **Stage:** 297 mm × 210 mm per page. No `.deck-frame`. No 0.96 scale.
- **Build:** single HTML file plus `img/`. No `build.sh` and no `render-deck.py` in the repo. Print CSS is the export path.
- **`[PENDIENTE]`:** none.

### 8. GRP IC 2026 application — `https://grp-ic-2026-application.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`. `grp-ic.vercel.app` is 404.
- **Source:** none in this repo. Content unknown. This audit does not treat the GRP comms skill as the deck.

### 9. Teclogi financial model — `https://teclogi-financial-model.vercel.app`

- **Live:** 402 `DEPLOYMENT_DISABLED`. The undated name is a real Vercel project. `teclogi-financial-model-2026.vercel.app` is 404.
- **Search:** not in `cth-plugin` history. GitHub code search for the owner returned 0 hits. `https://github.com/gideonblaauw-creator/teclogi-financial-model` returned 404. No `build.sh`, slide list, or brand tokens can be read.
- **What it is:** unknown. The name says financial model, not a meeting deck. Do not assume the 1920 shell.

## Related host, not in the requested list

`https://energy-sprint-cohort-cth.vercel.app` also returned 402 `DEPLOYMENT_DISABLED` on the same pass. The public repo `energy-sprint-cohort-cth` is an English impact dashboard (`Energy Sprint Cohort — Impact Dashboard`), not a `.deck-frame` deck: zero `section.slide`, no 1920 stage, no 0.96 scale. Tokens reuse the blue palette under longer names (`--deep-blue`, `--light-cyan`, `--light-green`, `--forest-green`, `--sky-blue`). Open Sans is loaded; PT Sans is named in `font-family`. Three `[PENDIENTE]` strings. It is outside the nine hosts above and is not Teclogi.

## CEE source deck (no confirmed Vercel host)

Included because it is the same October shell and a Sep–Oct branch (`origin/cee-datathon-2026-10-14` @ `3fb3437`). It is not evidence that a Vercel project is still up.

- **Slides:** 13. Title: `CEE Externado × CleantechHUB · 14 oct 2026`. sha256 `395f2d2744cfcb616a6d122d9a8a3c6defd6d73854874c32c6ed2c8e831b147f`.
- **List:** cover; “El proyecto en una mirada” (four KPIs); Actores; La alianza (inline SVG triangle); El Otrosí; Datathon propósito (photo; three steps, the first titled Negocios digitales); Del informe al tablero; El Data Lab ya funciona; Vitrina; Datos que se comparten con reglas; De hoy a la Climate Data Week; Lo que proponemos acordar; close (“Inspira. Actúa. Transforma.”).
- **Interactivity:** APC navigation plus `?review`. No index, dots, lightbox, or expand cards.
- **Citations:** no `.src` lines and no sources slide. `SOURCES.md` and `PENDIENTES.md` are siblings. Eighteen `.pendiente` sentences are in the HTML and hidden until `?review`.
- **Brand and stage:** APC tokens, including PT Sans, 1920×1080, × 0.96.
- **Build:** `build.sh` matches APC. Render path is `tools/render.js`, not `render-deck.py`.
