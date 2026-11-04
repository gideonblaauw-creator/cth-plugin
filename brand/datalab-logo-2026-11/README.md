# CTH Data Lab logo + pre-event social kit (Nov 2026)

**Status:** Draft — **Awaiting Gideon's approval** before any use, posting, or deploy.

Soft-launch visuals for **CTH Data Lab** (Earth Observatory, Tue 24 Nov 2026). Source: Granola Air4U meeting 4 Nov 2026 (Hands ticket; not copied into this repo).

## Concepts (logo options)

| File | Idea | Palette use |
|------|------|-------------|
| `logo/option-a.svg` | **Data grid** — 4×4 cell matrix; one sky-blue and one forest-green accent cell | Deep Blue + Sky Blue + Forest Green |
| `logo/option-b.svg` | **Layers** — three stacked planes (sandboxes / governance stack) | Deep Blue, Light Green, Sky Blue |
| `logo/option-c.svg` | **Flow network** — nodes and links (datasets → insight) | Deep Blue, Forest Green, Sky Blue, Light Green |

Wordmark on all options: **Data Lab** (Titillium Web Bold). These are sub-brand marks only; they do **not** replace or redraw the official CleantechHUB logo.

**Light PNG** (`*-light.png`): deep blue / green artwork for light backgrounds.  
**Dark PNG** (`*-dark.png`): cyan / light green remap for dark backgrounds (generated via `scripts/render-png.mjs`).

## Social templates

- `social/post-1080x1080.*` — square feed (option A grid mark, deep blue field).
- `social/post-1200x627.*` — link preview / landscape (cyan field + deep blue sidebar).

Copy on templates is limited to ticket-approved lines only. Partner and CTH logo areas are labelled placeholders.

## Brand tokens (Manual de Marca Jan 2024 — this kit)

| Name | Hex | Used for |
|------|-----|----------|
| Deep Blue | `#0C498A` | Primary fields, wordmark (light logos) |
| Light Cyan | `#B2EEFA` | Accents, landscape background |
| Light Green | `#9DC384` | Layer / accent |
| Forest Green | `#669348` | Nodes, tagline accent |
| Sky Blue | `#69B5FA` | Grid highlight |
| White | `#FFFFFF` | Text on dark fields, placeholder boxes |

**Typography:** Titillium Web Bold (titles / wordmark), Open Sans (body on social templates). Fonts referenced via Google Fonts in SVG and `preview.html`.

No gradients, purple, red, or gray fills in deliverables.

## Regenerate PNGs

```bash
cd brand/datalab-logo-2026-11/scripts
npm install @resvg/resvg-js
node render-png.mjs
```

Logos export at **1024 px** width, transparent background. Social PNGs match SVG viewBox dimensions.

## PENDIENTE

- Event **time** and **venue**
- Official **CTH logo** asset file (placeholder boxes on social templates)
- Partner logos (**Externado**, partner referred as **Marlene**, **Air4U**) and permission to use them
- Exact **third pre-event post** date (first Thu 5 or Fri 6 Nov 2026, then Mon 23 Nov noted in source; third post unspecified)
- Final **post copy** (Socials desk)
- Which logo option (A / B / C) to lock for launch

## Preview

Open `preview.html` in a browser to compare options and social layouts on light and dark surfaces.
