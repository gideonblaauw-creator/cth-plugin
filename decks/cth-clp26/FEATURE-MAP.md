# FEATURE-MAP — `cth-clp26` (CLP26 scroll microsite)

**Slug:** `cth-clp26`  
**Public URL:** [https://decks.cleantechhub.net/cth-clp26/](https://decks.cleantechhub.net/cth-clp26/)  
**Repo folder:** `decks/cth-clp26/` (this map; sync the live static tree here before editing)  
**Format role:** Reference layout for **interactive scroll decks** (multi-file microsites). Paged 1920×1080 decks use `decks/<slug>/shell/` per `decks/rein-academic-city-ghana/PLAN.md`, not this map.

**Primary sources in this repo**

| Source | What it proves |
|---|---|
| `docs/deck-audit/A1-decks-cleantechhub.md` and `docs/deck-audit/A1.json` | Live structure, assets, interactivity (branch `deck-skill-audit-a1`, commit `0c39db1`, 19 Oct 2026) |
| `decks/earth-observatory-externado-2026-10/README.md` + `styles.css` | CLP26 shell clone notes and shared CSS selectors (branch `cursor/earth-observatory-externado`, commit `3c15488`) |
| `docs/infra/caddy/decks.cleantechhub.net.caddy` | Host routing for this slug |
| `skills/cleantechhub-brand/brand_dna.yaml` | Stage colour tokens for the CTH edition |
| `skills/clp26-brand/SKILL.md` | Campaign palette (not used as the deck face) |
| `decks/rein-academic-city-ghana/CHECK.md` | curl / asset verification pattern (paged deck; adapt paths below) |

---

## 1. Parts (slides and components)

This product is **10 scroll sections**, not paged slides. There is no `.deck-frame`, no slide hash pager, and no `?print` mode (A1 audit).

### 1.1 Sections (“slides”)

| # | Section (A1 name) | Typical `id` | Markup shell | CSS block (in `styles.css`) |
|---|-------------------|--------------|--------------|-----------------------------|
| 1 | Hero | `#hero` | `section.hero` | `/* hero */` — `.hero`, `.hero-inner`, `.hero-block`, `.eyebrow`, `.lead`, `.lead2`, `.stats`, `.stat`, `.num`, `.ctas`, `.btn` |
| 2 | Sponsors (hidden until data) | `#sponsors` | `section.sponsors` | `/* sponsors */` — `.sp-grid`, `.sp-tile`, `.hosts` |
| 3 | Journey | `#journey` | `section.sec` + timeline | `/* timeline */` — `.tl`, `.tl-item`, `.tl-detail`, `.yt` (lite YouTube) |
| 4 | Stories | `#stories` | `section.sec` + tabs | `/* stories */` — `.story-tabs`, `.story`, `.path`, `.tag` |
| 5 | Built | `#built` | `section.sec` | `/* built */` — `.bcard`, `.chip`, `.gitem`, `.grid` |
| 6 | Mentors (hidden until data) | `#mentors` | `section.sec` + people | `/* people */` — `.people-head`, `.pgroups`, `.pgroup`; clickable rows use `/* clickable people + person drawer */` |
| 7 | Jury (hidden until data) | `#jury` | same people pattern | `.roles`, `.role-card`, `.role-dr` (`/* role card (reusable) */`) |
| 8 | Watt_son | `#watt_son` | `section.sec` | `/* bot */` — `.bot`, `.bot-card`, `.bot-grid`, `.bot-stats` |
| 9 | CLP27 ask | `#clp27` (or `#clp27-ask`) | `section.sec` + CTA | `/* CTA */`, `/* CLP27 */` — `.cta`, `.ways`, `.benefits-t`, `.ticks` |
| 10 | Explorer | `#explorer` | `section.sec` | `/* explorer */`, `/* explorer list panel */` — `.filters`, `#map`, `.tbl`, `.list-panel`, `.card`, `.stg`, `.downloads`, `.dl-btns` |

`cth-clp26-rein` reuses the **same section ids** plus a REIN frame line on the hero (A1 audit).

### 1.2 Chrome (not a “slide”)

| Part | File | Selectors / nodes |
|---|---|---|
| Sticky top bar | `index.html` | `header.topbar#top`, `a.brand` → `img` (`img/logo.png`) |
| Section nav | `index.html` | `nav.nav#nav` (anchor links `#hero` … `#explorer`); mobile `#burger` toggles `.nav.open` |
| Title bar / eyebrow | `index.html` + `styles.css` | `.eyebrow`, `.eyebrow.dark`; section titles `h2` inside `.sec` |
| EN/ES switch | `index.html` + `app.js` | `.lang` group; `button[data-lang="en"]` / `[data-lang="es"]`, class `.on` on active |
| i18n strings | `index.html` | `[data-i18n]` (A1 audit); footer note via `data-i18n` |
| Footer | `index.html` | `footer.foot` — `.tag`, links (`/* footer */`) |

### 1.3 Stat tiles

| Part | Location | Selectors |
|---|---|---|
| Hero stats | `#hero` | `.stats` grid, `.stat`, `.num[data-count]`, `.lbl` |
| Bot stats | `#watt_son` | `.bot-stats`, `b` numerals |
| Impact / stage chips | `#explorer` | `.stg`, `.s0`–`.s4`, `.badge` |

### 1.4 Card grids and tables

| Part | Selectors |
|---|---|
| Built cards | `.bcard`, `.grid`, `.gitem` |
| Sponsor tiles | `.sp-grid`, `.sp-tile` |
| Role cards | `.roles`, `.role-card`, `.role-dr` |
| Explorer filters | `.filters`, `input[type=search]`, `select`, `.chip` toggles |
| Sortable startup table | `.table-wrap`, `.tbl`, `th` (click to sort), `tbody tr` |
| Map + list split | `#map` (D3 SVG), `.list-panel`, `.list-head` |

### 1.5 Timeline

| Part | Selectors / behaviour |
|---|---|
| Horizontal timeline | `.tl`, `.tl-item`, `.dot`, `.on` state |
| Detail pane | `.tl-detail`, optional `.yt` embed |
| Keyboard | Enter on focused video control plays; Escape closes drawer (A1) |

### 1.6 Story tabs

| Part | Selectors |
|---|---|
| Tab list | `.story-tabs`, `[role="tablist"]`, `button.on` |
| Panels | `.story`, `.path span.on` |

### 1.7 Nav (scroll index)

| Part | Selectors / JS |
|---|---|
| Sticky nav | `#nav a`, `.act` on active section |
| Scroll spy | `app.js`: `IntersectionObserver` on `section[id]`, syncs `#nav a.act` (see EO clone `app.js` lines 1–30 on branch `cursor/earth-observatory-externado`) |
| Mobile | `#burger` → `#nav.open` |

### 1.8 Drawer and video modal

| Part | Selectors |
|---|---|
| Scrim | `.scrim` |
| Startup / person drawer | `.drawer`, `.x` close, `Escape` closes (A1) |
| Video modal | `.modal`, `.modal .vid iframe` |

### 1.9 JS modules

| File | Role |
|---|---|
| `app.js` | Nav burger, scroll-spy, stat counters (`[data-count]`), story tabs, timeline, explorer filters/sort, drawer/modal, Chart.js and D3 init, `localStorage` key **`clp26lang`** (shared with `cth-clp26-rein` on `decks.cleantechhub.net`) |
| `lib/chart.umd.js` | Chart.js **4.5.1** — horizontal bar, bar funnel, doughnut (A1) |
| `lib/d3.min.js` | D3 **7.9.0** — `geoMercator` map in `#map` |
| `lib/topojson-client.min.js` | topojson-client **3.1.0** — world topology for map |

No slide keyboard pager, no lightbox, no `?print` (A1).

### 1.10 CSS tokens

| File | Tokens / layout |
|---|---|
| `styles.css` | `:root` — `--blue`, `--cyan`, `--lgreen`, `--green`, `--sky`, `--white`, `--font`; layout `.wrap` **max-width 1180px**, `.sec` vertical padding; `html { scroll-padding-top: 70px }` (EO clone `styles.css`) |

### 1.11 Assets

| Path | Role |
|---|---|
| `img/logo.png`, `img/logo-white.png` | CleantechHUB logos (A1) |
| Inline SVG | Circle favicon in `index.html` `<link rel="icon" href="data:image/svg+xml,...">` (EO clone head pattern) |
| `data/startups.json` | **102** startup rows for explorer (A1) |
| `data/*.json` | Other chart/map payloads |
| `pdf/` | Downloadable EN/ES report PDFs (linked from page; A1 sourcing) |
| `img/` | Photos, sponsor marks, map-related assets |

---

## 2. Where each part lives (file and selector)

**Multi-file layout (A1 `build.layout`):**

```
decks/cth-clp26/
  index.html          # sections, chrome, chart canvases, data-i18n
  styles.css          # all component rules (see §1)
  app.js              # behaviour + Chart/D3
  lib/chart.umd.js
  lib/d3.min.js
  lib/topojson-client.min.js
  data/*.json         # incl. data/startups.json (102 rows)
  pdf/                # public report downloads
  img/                # logos and media
  FEATURE-MAP.md      # this file
```

**Hosting (not in repo):** Appwrite static site `cth-clp26` in project `cth-decks`; Caddy reverse-proxies `Host: cth-clp26.sites.localhost` → `127.0.0.1:9080` (`docs/infra/caddy/decks.cleantechhub.net.caddy`).

**Clone decks:** Copy the tree above, keep **relative** URLs (`styles.css`, `app.js`, `lib/…`, `data/…`, `img/…`). EO fork adds `eo-extra.css` / `data/eo-deck.json` — do not treat those as part of the canonical CLP26 map.

---

## 3. Rules

### Brand tokens (CTH edition)

Use the **deck-visual five** from `skills/cleantechhub-brand/brand_dna.yaml` / A1 audit — not foundation green `#2D6A4F`, `#1B4332`, `#95D5B2`, and not Inter as the deck face:

| Token | Hex |
|---|---|
| `--blue` / Deep Blue | `#0C498A` |
| `--cyan` / Light Cyan | `#B2EEFA` |
| `--lgreen` / Light Green | `#9DC384` |
| `--green` / Forest Green | `#669348` |
| `--sky` / Sky Blue | `#69B5FA` |

Do **not** paint this public deck with ClimateLaunchpad campaign `#00A651` / `#FFC425` from `skills/clp26-brand/SKILL.md` (A1 outlier note).

### Fonts

Open Sans and PT Sans — loaded from Google Fonts in `index.html` (A1; EO clone `index.html` head).

### Logo

- Header: `img/logo.png` (alt CleantechHUB).
- On dark bands: `img/logo-white.png`.
- Favicon: inline SVG circle (EO clone pattern).

Capitalize **CleantechHUB** (one word, capital H-U-B) in copy.

### No prices on public pages

This slug is a **public** campaign microsite (no Caddy `basic_auth` on `/cth-clp26/*`). Do not publish ticket prices, REIN Hubs dollar amounts, or confidential fee tables on the HTML or linked PDFs served here. REIN funding tables belong on their own slug (`cth-rein-funding-oct2026`), not copied into CLP26.

### Confidential decks server-only

Working files (`build.sh`, `sources/`, draft JSON, internal PDFs) stay **off** the public host. For **disk-served** clones (see §4), Caddy must 404 anything outside the public allow-list. Appwrite-hosted `cth-clp26` has **no** `@nondeck` block in Caddy today — rely on upload discipline; disk clones must add a guard.

### External voice

Public copy remains **Awaiting Gideon's approval** until Gideon clears it (`CLAUDE.md` approval gate).

---

## 4. How to verify

### 4.1 Logged-out `curl` 200 (page and assets)

After publish (or against a local static server on the repo tree):

```bash
BASE="https://decks.cleantechhub.net/cth-clp26"
curl -sI "$BASE/" | head -1          # expect HTTP/2 200, text/html
curl -sI "$BASE/styles.css" | head -1
curl -sI "$BASE/app.js" | head -1
curl -sI "$BASE/lib/chart.umd.js" | head -1
curl -sI "$BASE/lib/d3.min.js" | head -1
curl -sI "$BASE/lib/topojson-client.min.js" | head -1
curl -sI "$BASE/data/startups.json" | head -1
curl -sI "$BASE/img/logo.png" | head -1
```

**Pass criteria (A1 method):** HTML, CSS, JS, JSON, PDF, and images return **200** with matching `Content-Type`. A missing asset that returns **`text/html`** is an Appwrite **`index.html` fallback** — treat as **fail** (A1 audit introduction).

**Note:** Site-wide OAuth in front of `decks.cleantechhub.net` may return **302** to `auth.cleantechhub.net` for anonymous `curl` even when the slug is configured as open in Caddy. Resolve auth at the edge before using this check in CI; A1 (19 Oct 2026) recorded **200** without login.

Local pattern (from `decks/rein-academic-city-ghana/CHECK.md`):

```bash
cd decks/cth-clp26
python3 -m http.server 8765
curl -sI "http://127.0.0.1:8765/index.html"
```

### 4.2 Per-section screenshots

Capture one full-viewport PNG per scroll section (10 total). EO clone tooling on branch `cursor/earth-observatory-externado`:

- `screenshot-deck.mjs` — Playwright scroll captures.
- `review-side-by-side.mjs` — compares against reference site at `CLP26_ROOT` (defaults to `/tmp/clp26/site`).

Adapt scroll positions to `#hero`, `#sponsors`, … `#explorer`.

### 4.3 Caddy 404-guard paths (disk-hosted clones)

`cth-clp26` on production uses **Appwrite** reverse proxy — **no** path guard in `docs/infra/caddy/decks.cleantechhub.net.caddy`.

When cloning to **`file_server`** under `/opt/cth-decks/<slug>/`, copy the **public allow-list** pattern from `rein-academic-city-ghana`:

```282:287:docs/infra/caddy/decks.cleantechhub.net.caddy
	@ghana_nondeck not path / /index.html /shell/*.css /shell/*.js /fonts/* /slides/*.html
	handle @ghana_nondeck {
		respond "Not found" 404
	}
	root * /opt/cth-decks/rein-academic-city-ghana
```

**CLP26 microsite allow-list (derive from §2 layout):**

```
/  /index.html
/styles.css  /app.js
/lib/*       /data/*       /img/*       /pdf/*
```

Any **new top-level directory** (for example `/fonts/` or `/scripts/`) must be added to the `@…_nondeck` matcher before deploy, or the guard will 404 public assets.

---

## 5. Known traps

| Trap | Detail |
|---|---|
| **Caddy guard too narrow** | Disk-hosted clones 404 new asset paths. Appwrite slugs have no guard — do not upload secrets to the site root. |
| **Appwrite index fallback** | Wrong path returns HTML 200; breaks `curl` content-type checks (A1). |
| **`build.sh` on host** | Requesting `/build.sh` (or other missing paths) may return the deck HTML fallback (A1). Do not treat 200 as success without checking `Content-Type`. |
| **Cache busting** | Browsers cache `app.js`, JSON, and `lib/*`. Bump query strings or filenames when data changes; hard-refresh after deploy. |
| **Relative paths** | Keep links relative so the same tree works on `decks.cleantechhub.net/<slug>/` and local `python3 -m http.server`. |
| **Shared language key** | `localStorage` key **`clp26lang`** is shared with `cth-clp26-rein` on this origin — language flips affect both decks (A1). |
| **Wrong deck family** | Do not add `.deck-frame`, slide dots, or `?print` — those belong to paged decks (`decks/rein-academic-city-ghana/`). |
| **Chart libraries on paged decks** | Chart.js / D3 are allowed **only** on CLP scroll clones (exception documented in `skills/cth-html-deck/SKILL.md` on branch `deck-skill-audit-a1`). |

---

## 6. Related hosting snippet

```34:41:docs/infra/caddy/decks.cleantechhub.net.caddy
handle /cth-clp26 {
	redir * /cth-clp26/ 308
}
handle_path /cth-clp26/* {
	header X-Robots-Tag "noindex, nofollow"
	reverse_proxy 127.0.0.1:9080 {
		header_up Host cth-clp26.sites.localhost
	}
}
```

Wiki paths `/decks/cth-clp26/` redirect to this host (A1 audit).
