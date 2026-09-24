# CleantechHUB brand mapping (diagram-design)

CleantechHUB Presentations uses the **Manual de Marca 2024** five-color palette from `skills/cleantechhub-brand/brand_dna.yaml`. This file maps those brand colors to diagram-design **semantic roles** in `style-guide.md`.

## Brand colors → semantic roles

| Brand name | Hex | Semantic role(s) |
|---|---|---|
| Deep Blue | `#0C498A` | `ink` (light mode), `paper` (dark mode), deep panels |
| Light Cyan | `#B2EEFA` | `paper` (light mode), `ink` on dark panels, dark-mode secondary text |
| Light Green | `#9DC384` | `accent`, `accent-tint` (focal nodes — replaces upstream rust `#eb6c36`) |
| Forest Green | `#669348` | `muted`, default arrow strokes |
| Sky Blue | `#69B5FA` | `link`, HTTP/API arrows, `rule-solid` emphasis |

## Upstream default → CTH (do not ship stone+rust)

| Upstream (stone+rust) | CTH replacement |
|---|---|
| Paper `#f5f5f5` | Light Cyan `#B2EEFA` |
| Ink `#2d3142` | Deep Blue `#0C498A` |
| Accent `#eb6c36` | Light Green `#9DC384` |
| Muted `#4f5d75` | Forest Green `#669348` |
| Link `#2e5aa8` | Sky Blue `#69B5FA` |

## Typography note

General CleantechHUB web copy often uses Inter or Open Sans / PT Sans (`brand_dna.yaml`). Diagram-design keeps the editorial **Geist + Instrument Serif** stack from the upstream skill for layout consistency across type references. External slide decks may swap the Google Fonts link per `cleantechhub-brand` when Gideon requests strict Manual de Marca typography on a one-off.

## Presentations desk

- **Owner:** Presentations desk (Hands tickets for HTML+SVG diagrams).
- **Do not deliver Mermaid** for CleantechHUB-facing artifacts; use this skill’s HTML+SVG output (or redraw imports per `import-*.md`).
- Co-branding with client palettes: run `onboarding.md` or save a separate profile — never mix client hues into CTH external deliverables without explicit co-brand approval.

## Project marker (optional)

To bind another repo to this skin without editing the installed working copy:

```text
profile: cleantechhub
```

in `<project-root>/.diagram-design`, after copying `references/profiles/cleantechhub.md` to `~/.diagram-design/profiles/cleantechhub.md`.
