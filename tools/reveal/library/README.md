# CTH reveal slide-type library (Job A)

Twenty-six approved slide layouts for `tools/reveal/`, rendered from YAML outlines via Nunjucks templates in `types/<slug>.njk`. Shared styles live in `library.scss` (imported by `theme/cleantechhub.scss`). Contract: `schema.json`.

Catalog decks: `catalog.yaml` (EN) and `catalog.es.yaml` (ES) — one slide per type, **Example** content only.

| Slug | Name | When to use | Census refs | Tier |
|------|------|-------------|-------------|------|
| `cover` | Cover | Open every deck; title, client, date, optional hero. | `DAGDKveFU4c` 1; all 20 decks | core |
| `statement` | Statement | Manifesto, pull quote, or breathing-room message. | `DAGDKveFU4c` 2; `DAGfZDLXS30` 2–3 | core |
| `title-bullets` | Title + bullets | Section explainer with bullets or two columns. | `DAGhFpnbtsU` 9–20; `DAGiSJ91egk` 5+ | core |
| `key-facts` | Key facts | 3–6 icon facts in a grid. | `DAGiSJ91egk` 3,7…; `DAGkDsqKVCM` 4 | core |
| `stat-band` | Stat band | 3–4 KPI tiles with required source. | `DAGWZK6E3XQ` 3–4; `DAGg4DgEdIQ` 10 | core |
| `logo-wall` | Logo wall | Partner, client, or portfolio logos. | `DAGt6UqljlI` 8–9; `DAGlaKQZ3hI` 23–24 | core |
| `map` | Regional map | LATAM / Colombia / CA / global map + pins. | `DAGWZK6E3XQ` 5; `DAGDKveFU4c` 17 | core |
| `team-grid` | Team grid | People portraits with names and roles. | `DAGDKveFU4c` 20–22; `DAGiSJ91egk` 4+ | core |
| `contact` | Contact | Named contacts, emails, link chips. | `DAGDKveFU4c` 32; `DAGhFpnbtsU` 10 | core |
| `process` | Process / route | 3–6 numbered methodology steps. | `DAGg4DgEdIQ` 5–9; `DAGfZDLXS30` 8–11 | core |
| `timeline` | Timeline | Dated agenda or schedule. | `DAGmKtmeuus` 15–18; `DAGlaKQZ3hI` 17–18 | core |
| `case-cards` | Case cards | 2–6 startup/client cards. | `DAGDKveFU4c` 13; `DAGWZK6E3XQ` 10 | core |
| `chart-proof` | Chart + proof | Bar/line/pie/funnel stub + proof + **source**. | `DAGDKveFU4c` 4; `DAGWZK6E3XQ` 20 | extended |
| `programme-trio` | Programme trio | 3–4 programme modules (Ideación → Crecimiento). | `DAGg4DgEdIQ` 17–19; `DAGDKveFU4c` 5–6 | extended |
| `closing` | Closing | Thanks, QR, URL. | `DAGDKveFU4c` 33–34; `DAGfZDLXS30` 56–58 | extended |
| `showcase` | Showcase | Narrative + 1–4 photos. | `DAGmKtmeuus` 8–9; `DAGkDsqKVCM` 8–9 | extended |
| `data-table` | Data table | Budget/fee table with **source**. | `DAGhFpnbtsU` 7–8; `DAGWZK6E3XQ` 22 | extended |
| `ecosystem` | Ecosystem / model | Stakeholder / support model diagram. | `DAGixYIQ77w` 5; `DAGiBQEk004` 5 | extended |
| `section-title` | Section title | Mid-deck chapter break. | `DAGiSJ91egk` 2,6…; `DAGfZDLXS30` 4 | extended |
| `media-proof` | Media proof | Press/social proof mockup + link. | `DAGDKveFU4c` 26–27 | **variant** |
| `partner-cards` | Partner cards | Logo + blurb cards (not bare wall). | `DAGfZDLXS30` 6,48–49 | **variant** |
| `partner-profile` | Partner profile | Featured hub/startup with photo + logo. | `DAGHT3gEGGE` 4–23; `DAGDKveFU4c` 7–10 | **variant** |
| `testimonial` | Testimonial | Single or multi quote layout. | `DAGDKveFU4c` 16,25; `DAGg4DgEdIQ` 39 | **variant** |
| `focus-areas` | Focus areas | Sector photo strips. | `DAGDKveFU4c` 19; `DAGg4DgEdIQ` 41 | **variant** |
| `offer` | Offer / package | Price callout + includes list. | `DAGlaKQZ3hI` 10–16; `DAGixYIQ77w` 15–16 | **variant** |
| `contents` | Contents | Numbered TOC beside image. | `DAGixYIQ77w` 2; `DAGiBQEk004` 2 | **variant** |

## Template engine

**Nunjucks** (`types/*.njk`): already used in the Node reveal toolchain, supports loops/partials for YAML-driven outlines, and keeps templates readable for Job B’s `render-outline.js` without adding a second engine.

## Brand palette (library only)

`library.scss` uses only **#0C498A**, **#B2EEFA**, **#9DC384**, **#669348**, **#69B5FA**, **#FFFFFF**, with **Open Sans** and **PT Sans**. Legacy forest-green tokens in `theme/cleantechhub.scss` are a separate theme fix.

## Files (Job A scope)

- `types/<slug>.njk` — 26 layout templates
- `library.scss` — DivInc-style component CSS (CTH brand tokens)
- `schema.json` — outline field contract (do not rename fields)
- `catalog.yaml`, `catalog.es.yaml` — example catalog outlines
- `README.md` — this table
- `theme/cleantechhub.scss` — one `@import` of `library.scss`
