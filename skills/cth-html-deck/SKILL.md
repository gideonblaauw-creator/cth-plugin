---
name: cth-html-deck
description: >
  Builds an interactive HTML slide deck (menu, keyboard, citations, EN/ES,
  ?print PDF) for CleantechHUB, REIN Hubs, or AIC, and stops before the HITL
  publish to decks.cleantechhub.net. Use when: HTML deck, slide deck,
  presentación, meeting deck, donor deck, rewrite a deck. Do not use when:
  Nexus one-pagers (nexus-onepager), grant packs (cth-grant), client proposals
  (cth-proposal-build), or diagrams (diagram-design). Supersedes
  cth-html-deck-visual.
license: MIT
metadata:
  version: "1.0.0"
  category: programs
---

# CTH HTML deck

Every deck this skill builds is an interactive 1920×1080 stage, every figure has a source, and the public URL is `https://decks.cleantechhub.net/<slug>/` only after Gideon says yes.

This skill supersedes `cth-html-deck-visual` (locked 19 Sep 2026). Do not copy `vercel-deploy-umber-ten` and do not create a Vercel project. Photo slides still use that skill's scrim and glass, because the reference deck does.

**Reference implementation** (not on `main`): branch `meetings-2026-10-13-b4b`, folder `decks/meetings-2026-10-13/b4b/`. Read `shell/deck.css`, `shell/deck.js`, `shell/head.html`, `build.sh`, `render-deck.py`, `SOURCES.md`, and `slides/` before writing a new shell. Live copy: `https://decks.cleantechhub.net/b4b-cth-2026-10-13/`.

## Workflow

1. **Pick the brand context** — One of CleantechHUB, REIN Hubs, or AIC (Americas Innovation Council). Read that brand section below. Done when: the ticket names one context and the stage tokens match it.
2. **Copy the shell, then extend it** — Start from the B4B `shell/`. Keep menu, arrows, dots, expand cards, lightbox, questions toggle, and `?print`. Add the EN/ES switch, optional tabs, and chart rules the reference does not ship. Done when: `build.sh` emits one self-contained `index.html`.
3. **Launch micro-parallel Hands** — One Hands per slide group, plus a shell Hands, an assembler, and a verifier who did not build the deck. Done when: each job has its own bc-id and an exclusive write path.
4. **Source every figure** — Inline citation link, a SOURCES slide, and `SOURCES.md`. Unknowns are `[PENDIENTE]`. Hypotheses are labelled. Done when: a number that is not in `SOURCES.md` is either labelled Hipótesis or marked `[PENDIENTE]`.
5. **Assemble, then check** — Assembler runs `build.sh`. The verifier Hands runs the acceptance list and writes `CHECK.md`. Done when: `CHECK.md` records pass or a named fail for every check.
6. **Stop before publish** — The PR names the slug and the future URL. Done when: nothing has been uploaded to Appwrite or Vercel.

Default Understanding Lab tier is 0. Plant a lab only when the ticket sets `tier: 1` or `tier: 2`.

External use of the deck stays **Awaiting Gideon's approval** until Gideon clears it. Put that line in the footer of a working deck. A submission deck does not carry a DRAFT watermark.

## Folder

```
decks/<event>/<name>/
  shell/head.html
  shell/deck.css
  shell/deck.js
  slides/NN-slug.html
  build.sh
  render-deck.py
  SOURCES.md
  PENDIENTES.md
  index.html          # assembler output
  CHECK.md            # verifier output
```

`build.sh` inlines `shell/deck.css` and `shell/deck.js` into `index.html` and concatenates `slides/*.html` in filename order inside `.deck`. Chrome (menu, dots, questions, lightbox) is appended by the script, as in the B4B `build.sh`.

## 1. Always interactive

The stage is 1920×1080 inside `.deck-frame`. Screen scale is `min(viewportWidth / 1920, viewportHeight / 1080) * 0.96`, applied as `transform: scale()` on `.deck-stage`, with `.deck-frame` sized to that scaled box so `overflow: hidden` does not clip the letterbox.

Nothing inside `.deck-stage` is set below 24px. That includes citations, chart labels, and chrome copied into the stage. `.nav-hint` and `#slide-dots` stay outside `.deck-stage`, as siblings after `.deck-viewport` in the B4B `build.sh`. `.nav-hint` may be `font-size: 14px` and is `display: none` under `body.print-all`. `#slide-dots button` may be 14×14px and must not set `font-size`. No painted size inside `.deck-stage` is below 24px.

| Control | Contract |
|---|---|
| Index | `#btn-menu` toggles `#deck-menu`. List is built from each slide's `data-menu-title`. Escape or backdrop closes it. |
| Arrows | ArrowRight, Space, and PageDown go forward. ArrowLeft and PageUp go back. A click on the right half of the frame goes forward; the left half goes back. Ignore the click when the target is a link, button, card, tab, or lightbox control. |
| Dots | `#slide-dots` has one button per slide. `aria-current="true"` on the active dot. |
| Hash | `#1` is the first slide. `history.replaceState` keeps the hash in sync. |
| Expandable cards | `.expand-card` contains `.expand-trigger` and `.expand-body`. The trigger sets `aria-expanded`. |
| Lightbox | `.lightbox-open` carries `data-src` and `data-caption`. `#lightbox` opens. Escape, the close button, or the backdrop closes it. |
| Questions | `#btn-questions` toggles `body.show-questions` and `aria-pressed`. `.ask-collapsible` is hidden until that class is on. |
| Tabs (optional) | Use only when one slide has mutually exclusive views. Markup: `.tab-set`, `[role="tablist"]`, `[role="tab"]`, `[role="tabpanel"]`. Arrow keys inside the tablist move tabs and do not change slides. |
| Charts | Quantitative slides use an inline `<svg class="chart">` inside the stage. No chart bitmap, no invented series. Axis and value labels are at least 24px. If the series is unknown, draw the frame and write `[PENDIENTE]`. |
| EN/ES | Always. `.lang-en` and `.lang-es` pairs, a toggle `[data-lang="en"]` / `[data-lang="es"]`, `document.documentElement.lang`, and `localStorage` key `cth-deck-lang`. Numbers and locked facts are identical in both languages. Missing copy is `[PENDIENTE]`, not a guessed sentence. Default language is the room language on the ticket. |
| `?print` | `?print` or `#print` adds `body.print-all`, marks every `.slide` active, opens every `.expand-body`, forces `show-questions`, and hides chrome, menu, and lightbox. Print the active language only, so PDF pages equal slides. `@page` size is 1920px 1080px, margin 0. |

Ship `.chart` and `.tab-set` rules in `shell/deck.css` on every deck, including a deck that uses neither yet. Labels inside `.chart` stay at least 24px.

`render-deck.py` opens `index.html?print` in Chromium at 1920×1080, screenshots each `.deck .slide`, and builds the PDF with img2pdf at 508 mm × 285.75 mm. Count slides from the DOM. Do not hardcode the B4B count of 9.

Photo slides (CleantechHUB context) use `.slide.has-photo::before` for a theme-correct cover image and `::after` for the bottom scrim `linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.4) 40%, rgba(0,0,0,0.85) 75%, rgba(0,0,0,0.95) 100%)`. `.glass` is fill `rgba(255,255,255,0.09)`, 1px border `rgba(255,255,255,0.12)`, `backdrop-filter: blur(8px)`, radius 12px. `.weight-box` is fill `rgba(255,255,255,0.07)` with the same border and no blur. A solid brand-color stage is valid when the slide is not a photo slide. Match the photo to the subject. Agroforestry is canopy and producers, not leftover solar.

## 2. Sources

Every figure is sourced. A figure is an `img`, an `svg.chart`, a `.figure`, or a numeric callout (`.stat`, `.amt`, or a sentence that states a count, date, sum, or percent).

- Put a visible link on the same slide: `<a class="cite">` or `.fact-link a`, `target="_blank"`, `rel="noopener"`, at least 24px. The `href` is the page that states the fact.
- Add a **SOURCES** slide (`data-menu-title` contains `SOURCES` or `Fuentes`) that lists the same URLs as `SOURCES.md`. A2 found that Bridge for Billions and Matamala stop at per-slide `.src` / `.cite` plus `SOURCES.md`. APC slide 21 (`Fuentes públicas`) is the slide to copy. This skill requires both the slide and the file.
- `SOURCES.md` is a table: fact, URL. It lives next to `build.sh`.
- Unknowns are the literal token `[PENDIENTE]`, on the slide and in `PENDIENTES.md`, as a visible `.pendiente` chip. CEE hid those chips until `?review`. APC wrapped some in HTML comments. This skill shows the chip.
- A hypothesis carries a visible label `Hipótesis` or `Hypothesis` (class `hypo-badge`). It is not written as a fact.
- Do not invent a number, a name, a date, or a causal link to fill a gap. REIN Hubs dollar amounts are never cited, in either language.

Slide numbers, the meeting date in the footer, and the copyright year do not need a source row. Every other numeral does.

## 3. Brand, chosen per context

One context per deck. Do not mix palettes. Co-brand only when the ticket says so.

### CleantechHUB

Read `skills/cleantechhub-brand/SKILL.md` for voice, logo, and the tagline "Inspira. Actúa. Transforma."

Stage tokens are the Manual de Marca (Jan 2024) five in `skills/cleantechhub-brand/brand_dna.yaml`, set as:

```css
:root {
  --deep: #0C498A;
  --cyan: #B2EEFA;
  --green: #9DC384;
  --forest: #669348;
  --sky: #69B5FA;
  --white: #FFFFFF;
  --page: #051a33; /* letterbox behind the stage, not a sixth brand color */
  --stage-w: 1920px;
  --stage-h: 1080px;
  --font: 'Open Sans', 'PT Sans', sans-serif;
}
```

Load Open Sans (400, 600, 700) from the Google Fonts stylesheet in `shell/head.html`. The stage face is Open Sans for titles and body. The green and Inter block at the top of `skills/cleantechhub-brand/SKILL.md` is for other artifacts. HTML decks do not use `#2D6A4F`, `#1B4332`, or `#95D5B2`.

### REIN Hubs

There is no `skills/rein-hubs-brand/SKILL.md` on `main`. Take the six hexes and the credit line from A1 `cth-clp26-rein`. Body is Open Sans. Headings may be Poppins. Source Sans 3 may be named and is not loaded. Do not add Arial. Do not cite pvblic.org or a factsheet. Credit line: "REIN Hubs · PVBLIC × CleantechHUB".

| Role | Hex |
|---|---|
| REIN Green | `#335D4F` |
| REIN Orange | `#FF6633` |
| Text | `#222A27` |
| Gray | `#5F6663` |
| Line | `#C9D6D1` |
| Background | `#F1F5F3` |

Do not use CleantechHUB blues as the primary. Read `skills/rein-hubs-comms/SKILL.md`: REIN HOLD, and never cite REIN Hubs dollar amounts. If a `rein-hubs-brand` skill lands later, it wins on color and type. The dollar-amount ban and REIN HOLD still win.

### AIC

Read `skills/aic-brand/SKILL.md`. That file is a **PROPOSAL**. Observed ink `#070c18`, gold `#c9a45c`, Cormorant Garamond, Inter, and the type-only mark are filled in. Every other row in `skills/aic-brand/SKILL.md` stays `[PENDIENTE]` until Gideon adopts the proposal. Keep this comment at the top of `shell/deck.css` until then:

```css
/* AIC brand PROPOSAL — tokens [PENDIENTE] */
```

AIC is not CleantechHUB. No CTH lime, no CTH blues as primary, no CleantechHUB wordmark unless the ticket is an explicit co-brand. The live AIC page is a 7-section configurator, not this shell (A1). A ticket that asks for an AIC slide deck still uses the 1920 stage, the 0.96 scale, and the 24px floor. An AIC slide deck uses `cth-deck-lang`. It does not copy the configurator's in-memory toggle. Host an AIC deck on `decks.cleantechhub.net` only when the ticket says so.

## 4. Hosting (HITL)

Canonical public URL: `https://decks.cleantechhub.net/<slug>/`.

A1 records Appwrite project `cth-decks`. Caddy strips `/<slug>/` and proxies to the site. The root returned HTTP 401 with an empty body. Slug pages stayed public. One wiki sample, `/decks/apc-cth-2026-10-07/`, returned 301 to this host. A missing asset that returns `text/html` is the `index.html` fallback. A1 did not open the VPS. Team, framework, adapter, install, build, output directory, `_APP_DOMAIN_SITES`, the root auth scheme, and any tar-size cap stay `[PENDIENTE]`. Do not write a megabyte number. Epic Angels left unreferenced `png/` renders and a local PDF out of the upload (A1). Do the same when the tree is large.

Publish is band 4. Hands do not deploy.

1. Ship the static tree in the repo PR. `index.html` is self-contained. Images sit beside it.
2. Wait for Gideon's yes in the owning chat.
3. Infra overwrites that slug on the existing Appwrite project. Same URL after every update. Ask Gideon to hard-refresh.
4. Do not create a Vercel project. Do not add `vercel.json`. On 19 Oct 2026 at 21:02 UTC, A2's nine known hosts plus `teclogi-financial-model.vercel.app` returned HTTP 402 `DEPLOYMENT_DISABLED`. Guessed names in that audit returned 404 `DEPLOYMENT_NOT_FOUND`. Leave the known hosts paused.
5. The root auth scheme stays `[PENDIENTE]`. Do not copy credentials into git, a ticket, or a skill.
6. Epic Angels left unreferenced `png/` renders and a local PDF out of the upload (A1). Do the same when the tree is large. Do not write a megabyte number.
7. After publish, `curl -sI` the slug and every linked asset. HTML, CSS, JS, images, and PDFs must be HTTP 200 with the matching content type. An `index.html` fallback that returns HTML for a missing image is a fail.
8. The URL can be public and still unsent. Do not send it to the room until Gideon says yes.

`teclogi-financial-model` has no slug on this host. A1's migration note marks it BLOCKED (Next.js). A2 found HTTP 402 and no readable source. Leave it out of this static shell.

## 5. Build — micro-parallel Hands

Read `skills/harness/SKILL.md` before launch. Repo and build Hands use `composer-2.5` with `fast=true` (t1263u). Mechanical checks may use `gemini-3.7-flash`. Review, eval, or brand judgment with no model is HOLD: flag Gideon. Do not fill Sonnet, Opus, or Haiku.

Launch the jobs together. Do not finish one and queue the rest. Stay near eight live Hands. If the slide count needs more, ping Orchestrator before launch.

| Hands | Exclusive write path | Does not write |
|---|---|---|
| Shell | `shell/`, `build.sh`, `render-deck.py` | `slides/`, `index.html` |
| One per slide group | That group's `slides/NN-*.html` only | Other slides, `shell/` |
| Assembler | Runs `build.sh`, commits `index.html` | Slide prose, shell rules |
| Verifier | `CHECK.md` only | Shell, slides, `index.html` |

The verifier is a different Cloud Hands (different bc-id) that did not commit the shell, the slides, or the assembly. Maker ≠ checker. Group slides in batches of about three or four, named in the ticket before launch. The assembler runs after those commits are on the branch.

## 6. Acceptance

The verifier records each row in `CHECK.md`. A fail names the slide and the rule.

| Check | Pass |
|---|---|
| Clipped sides | At 1920×1080, 1512×982, 1366×768, and 1280×800, every text node inside `.slide` sits inside the slide box. 1366×768 and 1512×982 are the APC `smoke-layout.py` widths (A2). Print screenshots show even margins and no cut words on the left or right edge. |
| Minimum type | Fail any `font-size` under 24px that can match a node inside `.deck-stage`. Pass `.nav-hint` at 14px only when it is outside `.deck-stage` and hidden in `body.print-all`. Pass a 14×14px dot only when `#slide-dots` is outside `.deck-stage` and the rule sets no `font-size`. |
| Citation per figure | Every `img`, `svg.chart`, `.figure`, and numeric callout has a visible `a.cite` or `.fact-link a` on that slide. The link is in the DOM, not in an HTML comment, and it is shown in screen mode without `?review`. |
| SOURCES slide | A slide `data-menu-title` contains `SOURCES` or `Fuentes`, and its links match `SOURCES.md`. |
| No invented numbers | Every numeral other than the slide index (`n / total`), the meeting date in the footer, and the copyright year is in `SOURCES.md`, inside `.hypo-badge`, or is the literal `[PENDIENTE]`. |
| PDF | `render-deck.py` page count equals the number of `.slide` elements. |
| curl 200 | Before HITL: a local static server returns 200 for `index.html`. After Gideon authorizes publish: `curl -sI https://decks.cleantechhub.net/<slug>/` is HTTP 200 `text/html`, and linked assets are 200 with the right type. Hands do not publish in order to turn this row green. |
| EN/ES | Pass when every sentence has `.lang-en` and `.lang-es`, the toggle sets `document.documentElement.lang` and `localStorage` key `cth-deck-lang`, the same numerals appear in both languages, and missing copy is the text `[PENDIENTE]`. ClimateLaunchpad may keep `clp26lang`. The funding table is out of scope. |
| Keyboard | ArrowRight advances, ArrowLeft returns, Space, Page Up, and Page Down move the same way. Click halves advance or return, and are ignored on a link, button, card, tab, or lightbox control. Hash `#1` is the first slide. Escape closes the menu and the lightbox. The index lists every `data-menu-title`. |
| Brand tokens | Each required `grep -F` prints a match. Each absent-hex `grep -F` prints nothing. Skip the cross-brand absent grep only when the ticket names a co-brand, and record that exception in `CHECK.md`. |

CleantechHUB. Each required command must print a match. Each absent command must print nothing:

```bash
grep -F '#0C498A' shell/deck.css
grep -F '#B2EEFA' shell/deck.css
grep -F '#9DC384' shell/deck.css
grep -F '#669348' shell/deck.css
grep -F '#69B5FA' shell/deck.css
grep -F 'Open Sans' shell/head.html
grep -F '#2D6A4F' shell/deck.css slides/*.html
grep -F '#1B4332' shell/deck.css slides/*.html
grep -F '#95D5B2' shell/deck.css slides/*.html
grep -F 'font-family' shell/deck.css shell/head.html slides/*.html | grep -F 'Inter'
```

REIN Hubs. Each required command must print a match. Each absent command must print nothing. Skip the absent commands on a ticketed co-brand:

```bash
grep -F '#335D4F' shell/deck.css
grep -F '#FF6633' shell/deck.css
grep -F '#222A27' shell/deck.css
grep -F '#5F6663' shell/deck.css
grep -F '#C9D6D1' shell/deck.css
grep -F '#F1F5F3' shell/deck.css
grep -F '#0C498A' shell/deck.css
grep -F '#B2EEFA' shell/deck.css
grep -F '#69B5FA' shell/deck.css
grep -F '#9DC384' shell/deck.css
grep -F '#669348' shell/deck.css
grep -F '#2D6A4F' shell/deck.css
grep -F '#95D5B2' shell/deck.css
grep -F '#1B4332' shell/deck.css
grep -F '#F1562A' shell/deck.css
grep -F '#FC987C' shell/deck.css
```

AIC. The proposal comment must print a match. Each absent command must print nothing. Skip the absent commands on a ticketed co-brand:

```bash
grep -F 'AIC brand PROPOSAL' shell/deck.css
grep -F '#070c18' shell/deck.css
grep -F '#c9a45c' shell/deck.css
grep -F '#0C498A' shell/deck.css
grep -F '#B2EEFA' shell/deck.css
grep -F '#69B5FA' shell/deck.css
grep -F '#9DC384' shell/deck.css
grep -F '#669348' shell/deck.css
grep -F '#2D6A4F' shell/deck.css
grep -F '#1B4332' shell/deck.css
grep -F '#95D5B2' shell/deck.css
grep -F '#335D4F' shell/deck.css
grep -F '#FF6633' shell/deck.css
grep -F '#F1562A' shell/deck.css
```

## Outliers (A1)

A1 measured the thirteen live slugs (`docs/deck-audit/A1-decks-cleantechhub.md`, branch `deck-skill-audit-a1` @ `0c39db1`). A new paged deck still uses the 1920 shell. Two live products do not.

**Allowed exception — ClimateLaunchpad scroll pages.** `cth-clp26` and `cth-clp26-rein` are scroll microsites, not 16:9 decks. They may keep Chart.js 4.5.1, D3 7.9.0, topojson-client 3.1.0, story tabs, and the EN/ES switch (`localStorage` key `clp26lang`, shared by both slugs on this host). They have no `.deck-frame`, no `?print`, and no sources slide. They do not use ClimateLaunchpad campaign green `#00A651` or yellow `#FFC425`. The CleantechHUB edition uses the deck-visual five. The REIN edition uses `#335D4F` and `#FF6633`, with Poppins headings. Chart.js and D3 are non-compliant on a paged deck. A new meeting deck uses inline SVG.

**Non-compliant as a deck — REIN funding table.** `cth-rein-funding-oct2026` is one filterable table. It has no stage, no pager, and no EN/ES switch. Its orange is `#F1562A` and `#FC987C`, not the factsheet orange `#FF6633`. Headings are Lora. Body is Poppins. Leave it as a table page. Do not restyle it into 1920 slides unless the ticket says so. Do not copy its dollar amounts into any deck.

## Audit

A1 and A2 are both in this branch.

- A1: `docs/deck-audit/A1-decks-cleantechhub.md` and `docs/deck-audit/A1.json` (`deck-skill-audit-a1` @ `0c39db1`, 19 Oct 2026). Curl of the thirteen slugs on `decks.cleantechhub.net`.
- A2: `docs/deck-audit/A2-vercel-decks.md` and `docs/deck-audit/A2.json` (`deck-skill-audit-a2` @ `16f5251`, 19 Oct 2026 21:02 UTC).

This skill keeps those findings:

- Readable Oct 2026 shells (APC, Bridge for Billions, Matamala deck, CEE) use the Manual de Marca blues and Open Sans. They do not use `#2D6A4F`, `#1B4332`, `#95D5B2`, or Inter. The letterbox is `#051a33`. A1 found the same five on the live CTH slugs, and no foundation green.
- Only APC has a sources slide, on the live host and in source (A1). Bridge for Billions and Matamala share the chrome shell (index, dots, questions, lightbox, expand cards) and have no sources slide. This skill keeps that chrome and adds the APC sources slide.
- EN/ES exists on four live slugs (A1 rows): `cth-clp26`, `cth-clp26-rein`, `cpi-lab-backbone-cth`, and `aic-q1-2027-packages`. The other nine are one language. The frame shells have no switch. This skill still requires one on a new paged deck.
- Those frame shells have no chart library. This skill ships `.tab-set` and inline SVG `.chart` rules. Chart.js and D3 stay on the ClimateLaunchpad exception above.
- B4B and Matamala `shell/deck.css`, `shell/deck.js`, and `build.sh` are the shell to copy. APC is the earlier shell without that chrome.
- Energy Coops is A4 landscape with no `.deck-frame`. The Matamala `brief.html` is a scrolling page. Neither is this shell.
- On 19 Oct 2026 at 21:02 UTC, A2's nine known hosts plus `teclogi-financial-model.vercel.app` returned HTTP 402 `DEPLOYMENT_DISABLED`. Guessed names in that audit returned 404 `DEPLOYMENT_NOT_FOUND`. New decks go to `decks.cleantechhub.net`.

Index: `docs/deck-audit/README.md`.

## Do not use when

- A Nexus startup one-pager → `nexus-onepager`
- A grant or donor narrative → `cth-grant`
- A commercial client proposal → `cth-proposal-build`
- An editorial diagram or wire → `diagram-design`
- A generic HTML-to-PDF of a non-deck page → `html-to-pdf`
- Deploying an existing protected Vercel app → leave it. New decks do not go to Vercel.

## Related skills

| Skill | When |
|---|---|
| `cleantechhub-brand` | Voice, logo, tagline. Stage colors come from `brand_dna.yaml`, not the green CSS block. |
| `aic-brand` | AIC context. Proposal only. |
| `rein-hubs-comms` | REIN HOLD and the dollar-amount ban. |
| `harness` | Tickets, model lock, maker ≠ checker, HITL. |
| `html-to-pdf` | Non-deck HTML. Deck PDFs use `render-deck.py`. |

## References

- Branch `meetings-2026-10-13-b4b`, `decks/meetings-2026-10-13/b4b/` — shell, build, render, sources.
- `docs/deck-audit/README.md` — audit index. A1 and A2 are both merged.
- `skills/cleantechhub-brand/brand_dna.yaml` — Manual de Marca stage tokens.
- `skills/aic-brand/SKILL.md` — AIC proposal.
