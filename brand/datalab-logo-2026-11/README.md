# CTH Data Lab logo + pre-event social kit (Nov 2026)

**Status:** Draft · **Awaiting Gideon's approval** before any use, posting, or deploy.

Soft-launch visuals for **CTH Data Lab** (Earth Observatory, Tue 24 Nov 2026). Source: Granola Air4U meeting 4 Nov 2026 (Hands ticket; not copied into this repo).

**Logo decision (4 Nov 2026):** Option **B · layers** (stacked planes / sandboxes / governance stack) is the final mark.

## Final logo files

| File | Use |
|------|-----|
| `logo/datalab-logo.svg` | Master vector (layers mark + **Data Lab** wordmark, Titillium Web Bold) |
| `logo/datalab-logo-light.png` | Deep blue / green artwork for light backgrounds |
| `logo/datalab-logo-dark.png` | Cyan / sky-blue remap for dark backgrounds |

Wordmark: **Data Lab** (Titillium Web Bold). Sub-brand mark only; does **not** replace or redraw the official CleantechHUB logo.

**Palette on the mark:** Deep Blue `#0C498A`, Light Green `#9DC384`, Sky Blue `#69B5FA`, Forest Green `#669348` (accent bar).

## Archived concepts

Options A (data grid) and C (flow network) live under `archive/logo/` for reference only. Do not use for launch.

## Social templates

- `social/post-1080x1080.*` · square feed (layers mark on deep blue field; white headlines).
- `social/post-1200x627.*` · link preview / landscape (cyan field, deep blue copy and headlines).

Copy on templates is limited to ticket-approved lines only. Partner and CTH logo areas are labelled placeholders.

## Brand tokens (Manual de Marca Jan 2024, this kit)

| Name | Hex | Used for |
|------|-----|----------|
| Deep Blue | `#0C498A` | Primary fields, wordmark (light logos), body on cyan |
| Light Cyan | `#B2EEFA` | Accents, landscape background, grid mute (light) |
| Light Green | `#9DC384` | Layer / accent |
| Forest Green | `#669348` | Nodes, tagline accent |
| Sky Blue | `#69B5FA` | Grid highlight / mute on dark fields |
| White | `#FFFFFF` | Text on deep blue fields, placeholder boxes |

**Typography:** Titillium Web Bold (titles / wordmark), Open Sans (body on social templates). PNG renders use OFL files in `scripts/fonts/` (see `scripts/fonts/OFL.txt`). SVG and `preview.html` also link Google Fonts for browser preview.

No gradients, purple, red, or gray fills. All shape fills are fully opaque brand colours.

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

## Preview

Open `preview.html` in a browser to review the final logo, social layouts, and archived options on light and dark surfaces.
