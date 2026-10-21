# A1 — Live deck audit, decks.cleantechhub.net

Audit date: 19 October 2026. Method: `curl` only. No browser, and no login. Each slug below returned HTTP 200 `text/html`. Linked CSS, JavaScript, JSON, PDF, and image URLs were checked with a ranged request. A matching content type counts as present. `text/html` on a non-HTML path counts as the Appwrite `index.html` fallback.

Canonical public path: `https://decks.cleantechhub.net/<slug>/`. A sample wiki URL, `https://wiki.cleantechhub.net/decks/apc-cth-2026-10-07/`, returned 301 to the same path on this host. `https://decks.cleantechhub.net/` returned 401 with an empty body. The thirteen slug pages stay open.

`?print` does not change the file the server sends. On `apc-cth-2026-10-07`, the plain URL and `?print` both returned 56,157 bytes. Print behaviour is client-side, where it exists.

`teclogi-financial-model` is not one of the thirteen. The migration report marks it blocked, and it has no slug here.

Brand classes use the live paint, not the meeting title.

- **CTH** means the deck-visual five: `#0C498A`, `#B2EEFA`, `#9DC384`, `#669348`, `#69B5FA`, with Open Sans. None of the thirteen uses the foundation tokens `#2D6A4F`, `#1B4332`, `#95D5B2`, or Inter as the deck face. Inter appears only on the AIC deck.
- **REIN Hubs** means a green and orange system with a REIN logo.
- **AIC** means the Americas Innovation Council dark and gold system.
- **Other** was not needed. Client names (Teclogi, PASO, CEE, APC, Bridge for Billions) sit on a CTH or REIN frame.

No served file contains a generator comment. `build.sh`, `build.mjs`, `package.json`, and `README.md` on every slug return the deck HTML (fallback). The migration report, not the live tree, says a local `build.sh` was run for APC, CEE, Bridge for Billions, Epic Angels, and Matamala, and that `node build.mjs` wrote the AIC WebP files before upload.

## One row per deck

| Slug | Slides | Structure and types | Interactivity | Sourcing | Brand | Stage and frame | Build hints | Hosting path |
|---|---|---|---|---|---|---|---|---|
| `cth-clp26` | 10 scroll sections, not paged | Hero, sponsors (hidden until data), journey, stories, built, mentors (hidden), jury (hidden), Watt_son, CLP27 ask, explorer | EN/ES buttons, `data-i18n`, `localStorage` key `clp26lang`. Sticky section nav and burger. Story tabs (`role="tablist"`). Timeline, filters, range, checkboxes, sortable table, drawer, video modal. Charts: Chart.js 4.5.1 (horizontal bar, bar funnel, doughnut), D3 7.9.0 Mercator map, topojson-client 3.1.0. Enter plays a video. Escape closes the drawer. No slide keys, no lightbox, no `?print` | PDF downloads EN and ES. Foot note via `data-i18n`. No sources slide. 102 startups in `data/startups.json` | CTH. Open Sans and PT Sans. Tokens `--blue #0C498A`, `--cyan #B2EEFA`, `--lgreen #9DC384`, `--green #669348`, `--sky #69B5FA`. Logos `img/logo.png` and `img/logo-white.png`. Circle favicon | Fluid scroll, wrap 1,180 px. No `.deck-frame`. No fixed stage | Multi-file: `index.html`, `styles.css`, `app.js`, `lib/chart.umd.js`, `lib/d3.min.js`, `lib/topojson-client.min.js`, `data/*.json`, `pdf/`, `img/`. No generator comment. `build.sh` is fallback HTML | `https://decks.cleantechhub.net/cth-clp26/` |
| `cth-clp26-rein` | 10 scroll sections, not paged | Same section ids as `cth-clp26`, plus a REIN frame line on the hero | Same interaction model, same Chart.js, D3, and topojson builds. Same `localStorage` key `clp26lang` on this origin, so the two CLP decks share a language flag | Same PDF pair and explorer. No sources slide | REIN Hubs. Open Sans body, Poppins headings (CSS also names Source Sans 3, which is not loaded). Tokens `--g #335D4F`, `--o #FF6633`, `--ink #222A27`, `--gray #5F6663`, `--line #C9D6D1`, `--bg #F1F5F3`. Logos `img/rein-logo-header.png` and `img/rein-logo.png`. Text lockup “REIN Hubs · PVBLIC × CleantechHUB” | Fluid scroll, wrap 1,180 px. No `.deck-frame` | Same multi-file layout as `cth-clp26`. CSS comment: “REIN Hubs brand”. `build.sh` is fallback HTML | `https://decks.cleantechhub.net/cth-clp26-rein/` |
| `teclogi-jose-arrebol` | 9 paged slides | Comments label them: title, context, received, five ask items (EBITDA, working capital, org, drivers, figure), ask. Cover, context, case cards, tables, close | Arrow keys, space, Page Up and Page Down, hash `#n`, on-screen arrows, swipe. No EN/ES, no tabs, no lightbox, no index menu, no `?print` flag | No sources slide and no footnotes. Figures sit in the slide copy | CTH. Open Sans (stack names PT Sans, which is not loaded). Tokens `--deep #0C498A`, `--cyan #B2EEFA`, `--lgreen #9DC384`, `--green #669348`, `--sky #69B5FA`. Logo is a data-URI image, alt “CleantechHUB”. Tagline on the ask slide | Fixed stage 1,280 × 720 px inside `.stage`. Scale `min(width/1280, height/720)`. Print page 1,280 × 720 px. No `.deck-frame` | One HTML file, about 3.0 MB, photos inlined as data URIs. No generator comment. `build.sh` is fallback HTML | `https://decks.cleantechhub.net/teclogi-jose-arrebol/` |
| `cpi-juntos-cth` | 16 paged slides | Comments: cover, opportunity, precedent, three added diagram and case slides, why together, data, technology, structure, v2 diagram, pilots, roles, decisions, calendar, close | Arrow keys, space, Page Up and Page Down, Home, End, hash, dots, prev and next, swipe. No EN/ES, no tabs, no lightbox (figures open in a new tab), no `?print` flag | Visible “Fuentes” and “Fuente” lines with links on several slides. No sources slide. Three local figures returned PNG or SVG | CTH, with a “× PASO Colombia” lockup. Open Sans (PT Sans named, not loaded). Same five deck-visual colours, `--fgreen` for `#669348`. White inline SVG wordmark | Slides fill the viewport. Scrim matches the deck-visual gradient. Print page 16 in × 9 in. No `.deck-frame` | One HTML file, about 1.2 MB, ten photos inlined. Three external figures in `img/`. No generator comment | `https://decks.cleantechhub.net/cpi-juntos-cth/` |
| `cth-rein-funding-oct2026` | Not paged. One table, 10 rows | Header, filter band, sortable opportunity table, footer | Search box, verdict filter, source filter, click a column to sort, click a row to open a detail row. No EN/ES, no charts, no keyboard pager, no `?print` | Each detail row links an official page. Footer states deadlines were re-verified 15 October 2026. No sources slide | REIN Hubs. Poppins body, Lora headings. Tokens `--db #335D4F`, `--or #F1562A`, `--lo #FC987C`, `--gr #E2E2E2`, `--ink #080808`, `--mu #5F6360`. Logo is a Wix PNG, alt “REIN Hubs” | Fluid page, no stage, no `.deck-frame` | One HTML file, CSS and JS inline, data array in the page. No generator comment. Amounts stay in the live table and are not copied here | `https://decks.cleantechhub.net/cth-rein-funding-oct2026/` |
| `cth-epic-angels-2026-10-15` | 10 paged slides | Cover, context, CTH overview, Nexus, Datalab, 18-startup case, pipeline case, programmes, ask, index | `.deck-frame` shell. Arrows, space, Page Up and Page Down, click halves, hash. Chrome: Índice menu, dots, “Mostrar preguntas”. Expandable cards. Lightbox on four screenshots. Escape closes menu and lightbox. `?print` and `#print` add `print-all` | `.src` lines and linked citations. No dedicated sources slide. External PDF on nexus.cleantechhub.net returned `application/pdf` | CTH. Open Sans. Deck-visual five as `--deep`, `--cyan`, `--green`, `--forest`, `--sky`. Text wordmark and tagline. No logo file | 1,920 × 1,080 px. Scale `min(vw/1920, vh/1080) * 0.96`. `.deck-viewport` > `.deck-frame` > `.deck-stage` | One HTML file, CSS and JS inline. No generator comment. Migration report: local `build.sh`. Live `build.sh` is fallback HTML. Screenshot PNGs returned `image/png` | `https://decks.cleantechhub.net/cth-epic-angels-2026-10-15/` |
| `matamala-brief-2026-10-13` | 9 paged slides | Cover, profile, ODS Cero, data, partnership, proposals, reference images, ask, risks and index | Same chrome as Epic Angels: index menu, dots, question toggle, expandable cards, lightbox, arrow keys, `?print` | `.src` lines. No sources slide. Five Emprende UP PNGs returned `image/png`. Unreferenced `img/emprende-up/mapa-actores.png` still falls back to HTML | CTH. Open Sans. Same deck-visual tokens and text wordmark as Epic Angels | 1,920 × 1,080 px with `.deck-frame` and the same 0.96 scale | One HTML file. No generator comment. Migration report: local `build.sh`. Live `build.sh` is fallback HTML | `https://decks.cleantechhub.net/matamala-brief-2026-10-13/` |
| `b4b-cth-2026-10-13` | 9 paged slides | Cover, Conecta and fund context, fit hypothesis, REIN context, Nexus, Datalab, ask, next steps, index | Same chrome as Epic Angels and Matamala, including lightbox and expandable cards | `.src` lines and a “Fuentes” link pair. Slide copy points at `SOURCES.md`, which is not a served file. No sources slide | CTH. Open Sans. Same deck-visual tokens and text wordmark | 1,920 × 1,080 px with `.deck-frame` and the same 0.96 scale | One HTML file. No generator comment. Migration report: local `build.sh`. Live `build.sh` is fallback HTML | `https://decks.cleantechhub.net/b4b-cth-2026-10-13/` |
| `teclogi-brief-2026-10-13` | 1 canvas, two columns | Header, status card, investor table, open items, ask block, footer. Not a pager | None. No keys, no toggle, no EN/ES, no chart library | Footer names the Monday board, Gmail, and a standup. No sources slide. `brief.pdf` is on the host as `application/pdf` and is not linked from the HTML | CTH. Open Sans (PT Sans named, not loaded). Same five colours as literals, not custom properties. Text “CleantechHUB” and the tagline. No logo file | Locked 1,920 × 1,080 px, `overflow: hidden`, `@page` the same size. No scale script. No `.deck-frame` | One HTML file, CSS inline. No generator comment | `https://decks.cleantechhub.net/teclogi-brief-2026-10-13/` |
| `aic-q1-2027-packages` | 7 scroll sections, not paged | Hero, why, event picker, tier picker, city picker, visa and timing notes, closing band. Sticky summary aside | EN/ES buttons and `data-i18n`. Choice is in memory only (no `localStorage`). Default Spanish. Anchor nav. Radio cards, TDX checkbox, `<details>` calculation, mailto call to action. Enter and Space activate a card. Parallax. No slide keys, no lightbox, no `?print`, no chart library (CSS visa bars only) | Footer and calculation note name public sources and Unsplash photographers. No sources slide and no footnote element | AIC. Cormorant Garamond display, Inter body. See the AIC section below. Type wordmark “AIC” plus “Americas Innovation Council”. `favicon.svg` | Fluid. Wrap `min(1240px, 92vw)`. Hero is at least one viewport tall. No `.deck-frame` | `index.html`, `styles.css`, `app.js`, `favicon.svg`, `img/*.webp`. No generator comment. `build.mjs` and `package.json` are fallback HTML. Sample WebP files, including event and tier images, returned `image/webp` | `https://decks.cleantechhub.net/aic-q1-2027-packages/` |
| `cee-cth-2026-10-14` | 13 paged slides | Cover with two logos, photo beat, actors, alliance, Otrosí, datathon, journey, live lab, vitrina, access, roadmap, ask, close | `.deck-frame` shell. Arrows, space, Page Up and Page Down, click halves, hash, `?print`. No index menu, no lightbox, no expandable cards, no EN/ES | `.sources-col` exists only in CSS. No sources slide and no `.src` lines in the markup | CTH, co-branded. Open Sans and PT Sans, both loaded. Deck-visual five. Logos `img/logo-cth-white.svg` and `img/logo-cee-externado.png` | 1,920 × 1,080 px with `.deck-frame` and the same 0.96 scale | One HTML file plus `img/` JPEG, PNG, and SVG. All checked image URLs returned an image type. No generator comment. Migration report: local `build.sh`, 13 slides | `https://decks.cleantechhub.net/cee-cth-2026-10-14/` |
| `apc-cth-2026-10-07` | 21 paged slides | Cover, agenda, who we are, live demo, programmes, four Datalab environments, Nexus filter, projects, cases, fit, ask, sources | `.deck-frame` shell. Arrows, space, Page Up and Page Down, click halves, hash, `?print`. No index menu, no lightbox, no expandable cards, no EN/ES | Per-slide `.src` lines, plus slide 21 “Fuentes públicas” (`.sources-col`) | CTH. Open Sans and PT Sans, both loaded. Deck-visual five. Text wordmark and tagline. No logo file | 1,920 × 1,080 px with `.deck-frame` and the same 0.96 scale. `?print` confirmed same byte size as the plain URL | One HTML file plus `img/`. Checked JPEG, PNG, and WebP URLs returned image types. No generator comment. Migration report: local `build.sh`, 21 slides | `https://decks.cleantechhub.net/apc-cth-2026-10-07/` |
| `cpi-lab-backbone-cth` | 10 paged slides | Title, problem and ask, who is who, where money sits, two diagram slides, demand, stack, peer comps, roles and gate | EN/ES buttons. Every line is `data-en` and `data-es`. `localStorage` key `cpi-backbone-lang`, default Spanish. Arrows, space, click halves. Print CSS only, no `?print` flag. No tabs, no lightbox, no index menu | `.footnotes` on the diagram slides and one citation line (MinMinas, July 2026). No sources slide | CTH, co-brand text “CleantechHUB × PASO Colombia”. Open Sans, loaded alone. Deck-visual five. No logo image. Tagline in the last footnote | Slides fill the viewport. Photos are Unsplash URLs in `data-bg`, at 1,920 px wide in the query string. No `.deck-frame` | One HTML file, CSS and JS inline. No generator comment. No local image files | `https://decks.cleantechhub.net/cpi-lab-backbone-cth/` |

## Common pattern

Eight of the thirteen are paged CTH decks in the deck-visual palette, not the foundation green.

Five of those eight share one shell. APC, CEE, Bridge for Billions, Epic Angels, and Matamala each use a single HTML file. The tree is `.deck-viewport`, `.deck-frame`, `.deck-stage`, then `section.slide`. The stage is 1,920 × 1,080 px. The script scales it with `min(viewport width / 1920, viewport height / 1080) * 0.96`, and skips scaling in print mode. Custom properties are `--deep #0C498A`, `--cyan #B2EEFA`, `--green #9DC384`, `--forest #669348`, `--sky #69B5FA`, and `--white #FFFFFF`. The face is Open Sans. APC and CEE also load PT Sans. Cover and footer use the words “CleantechHUB” and “Inspira. Actúa. Transforma.” Keyboard support is Arrow Left, Arrow Right, space, Page Up, and Page Down, plus a click on either half. The hash is `#1`, `#2`, and so on. `?print` or `#print` adds `body.print-all` and shows every slide. There is no chart library and no EN/ES switch. There is no generator comment. A live `build.sh` is not on the host.

Three of those five add the same chrome. Bridge for Billions, Epic Angels, and Matamala have an Índice button, a dot nav, a “Mostrar preguntas” toggle, expandable cards, a screenshot lightbox, and Escape to close the menu or the lightbox. The last slide is an index. APC and CEE are the same frame without that chrome. APC is the only frame deck with a sources slide.

The other three paged CTH decks (Teclogi Jose, CPI Juntos, CPI backbone) use the same five colours, Open Sans, a full-bleed photo, a bottom scrim, and glass panels. They do not use `.deck-frame`. They page with arrow keys. Juntos and the backbone cite sources on the slide. Jose does not.

What the eight share, and the scroll sites do not, is a pager, a dark or photo slide, and no Chart.js.

## Outliers

**AIC is a different product.** `aic-q1-2027-packages` is a scrolling trip configurator, not a 16:9 deck. It is the only serif display face, the only Inter body, the only dark and gold palette, and the only AIC wordmark. Language does not persist. Detail is in the next section.

**Two REIN palettes, not one.** `cth-clp26-rein` uses `#335D4F` and `#FF6633`, with Poppins headings, on the CLP scroll site. `cth-rein-funding-oct2026` uses `#335D4F`, `#F1562A`, and `#FC987C`, with Lora headings, on a one-page filterable table. Both use a REIN logo. The orange is not the same hex. Neither deck uses the CTH five. The funding page is English only. The CLP REIN page is EN/ES.

**CLP is a microsite, twice.** `cth-clp26` and `cth-clp26-rein` are the only decks with Chart.js, D3, and topojson. They are the only ones with a startup JSON file (102 rows), a world topology, and downloadable report PDFs. They do not page. They do not use ClimateLaunchpad campaign green `#00A651` or yellow `#FFC425`. The CTH edition uses the deck-visual blue. The REIN edition recolours the same layout. Both write `localStorage` key `clp26lang`. On `decks.cleantechhub.net` that key is shared, so a language choice on one CLP deck changes the other.

**The Teclogi brief is one locked page.** `teclogi-brief-2026-10-13` is a 1,920 × 1,080 px canvas with no scale script and no pager. It is English. `brief.pdf` is on the host and is not linked from the HTML.

**Stage sizes diverge.** The frame family is 1,920 × 1,080 px inside `.deck-frame`. Teclogi Jose is 1,280 × 720 px inside `.stage`. CPI Juntos and the CPI backbone fill the viewport and have no frame. The brief is a fixed page with no frame. AIC, both CLP sites, and the REIN table do not have a stage.

**EN/ES is rare.** Only three decks switch language: both CLP sites (`data-i18n`, shared `clp26lang`), the CPI backbone (`data-en` / `data-es`, key `cpi-backbone-lang`), and AIC (`data-i18n`, no storage). The other nine are one language. The funding table and the Teclogi brief are English. The rest of the one-language decks are Spanish.

**Sourcing is uneven.** APC has a real sources slide. CPI Juntos and the CPI backbone put citations on the slide. The frame chrome decks use short `.src` lines. Bridge for Billions mentions `SOURCES.md`, which is not served. CEE has unused `.sources-col` CSS and no source lines. Teclogi Jose has none. CLP points at PDFs and the explorer instead of a sources slide. AIC names sources in the footer and in a disclosure, not as footnotes.

**Lightbox and index menu are a trio.** Only Bridge for Billions, Epic Angels, and Matamala have both. APC, the largest deck, has neither.

**Charts.** Only the two CLP decks load a chart library. AIC draws three visa bars in CSS. Everyone else uses tables, cards, or inline SVG diagrams.

**Matamala placeholder path.** The live HTML does not reference `mapa-actores.png`. Requesting that path still returns 200 `text/html` (the deck itself), because the site fallback is `index.html`. The five real Emprende UP PNGs are images.

**Photos.** Frame decks and CEE and APC use local files under `img/`. Those checked files returned image types. Teclogi Jose and CPI Juntos inline photos as data URIs. The CPI backbone hotlinks Unsplash. AIC serves local WebP sets (640, 1,280, 1,920, and for the hero bands also 2,560). The migration report says those WebP files were fetched from Unsplash at build time. The live page does not call Unsplash.

**No foundation green.** A search of the served CSS and HTML did not find `#2D6A4F` or `#1B4332` as a brand token. CTH decks here follow the HTML deck-visual five, not `skills/cleantechhub-brand`.

## AIC brand, for a future `aic-brand` skill

`skills/aic-comms` still marks the AIC brand as pending, and it already says not to mix CleantechHUB lime into AIC. This deck is the only live AIC-branded piece on this host. The tokens below are copied from `styles.css`, `favicon.svg`, and the header markup. They are a proposal, not a published skill.

**Name.** Americas Innovation Council. Short mark: AIC. Sites named in the footer: `joinaic.com` and `americasinnovationcouncil.com`.

**Type.** Display and the “AIC” monogram: Cormorant Garamond, weights 500, 600, and 700, plus italic 500 and 600. Fallback: Times New Roman, then serif. CSS: `--serif`. Body, navigation, and buttons: Inter, weights 300, 400, 500, and 600. Fallback: system-ui, then Segoe UI, then sans-serif. CSS: `--sans`. Buttons are uppercase, letter-spacing `0.14em`. Eyebrows are uppercase Inter, letter-spacing `0.28em`, in gold.

**Colour tokens, from `:root`.**

| Token | Hex or value | Role on this deck |
|---|---|---|
| `--ink` | `#070c18` | Page background, theme-color, favicon fill |
| `--navy` | `#0c1528` | Event cards |
| `--navy2` | `#111d36` | Second navy |
| `--ivory` | `#f4efe6` | Body text |
| `--muted` | `#a9b1c3` | Secondary text, brand name |
| `--dim` | `#7d869a` | Fine print |
| `--gold` | `#c9a45c` | Eyebrows, selected border, step numbers |
| `--champ` | `#e6cf9f` | Links, italic emphasis, favicon letters |
| `--gold-d` | `#9c7a3c` | Deep gold |
| `--plat` | `#c9d3e3` | Platinum, premium tier |
| `--line` | `rgba(217,192,143,.18)` | Hairline on the gold hue |

Gold button fill, not a token: `linear-gradient(135deg, #f3e2b8 0%, #d8b56f 45%, #b48a43 100%)`, label `#1a1206`. Luxury card base uses `#160f05`, `#2a1d0a`, `#120c05`, and `#0b0804`. Tier surfaces also use `#0f1a30` and `#121f3a`.

**Logo.** There is no image logo. The header is a text lockup: “AIC” in Cormorant Garamond, then a gold-tint rule, then “Americas Innovation Council” in small tracked Inter. The footer repeats the monogram larger. The favicon is inline SVG: a 64 × 64 rounded rectangle, fill `#070c18`, radius 14, and the letters AIC in Georgia, 24 px, weight 600, fill `#e6cf9f`. Do not place the CleantechHUB mark, the deck-visual cyan, or `#95D5B2` on this system.

**Photography.** Full-bleed WebP, object-fit cover, with a dark ink scrim. Glass cards use a white wash around 7 percent, a gold-tint border, and blur. That is the AIC reading of “photo plus glass”, not the CTH cyan glass.

**Language.** Spanish is the default. An EN | ES pill sits in the top bar. Copy lives in `app.js` as `ES` and `EN` maps, written into `[data-i18n]`. The choice is not stored.

**Voice on this page.** Formal Spanish and English for financial leaders. Prices are labelled indicative. The page says AIC curates trips and is not an official partner of the conferences. A call to action opens a mailto. It does not send by itself.

## Hosting, as checked

| Check | Result |
|---|---|
| Thirteen slug indexes | 200 `text/html` |
| `https://decks.cleantechhub.net/` | 401, empty body |
| Wiki `/decks/apc-cth-2026-10-07/` | 301 to `https://decks.cleantechhub.net/apc-cth-2026-10-07/` |
| `apc-cth-2026-10-07/?print` | 200, same 56,157 bytes as the plain URL |
| `build.sh` on every slug | 200 `text/html` (fallback), same size as that deck’s index |
| Referenced CSS, JS, JSON, PDF, PNG, JPEG, WebP, SVG | Matching content type |
| `matamala` `mapa-actores.png` | 200 `text/html` fallback. Not referenced by the live page |
| `teclogi-brief` `brief.pdf` | 206 `application/pdf`. Not linked from the HTML |

The migration report describes the upstream as Appwrite project `cth-decks`, with Caddy stripping `/<slug>/` and proxying to the site. This audit did not open the VPS. It only fetched the public URLs.
