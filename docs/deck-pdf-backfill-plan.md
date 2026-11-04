# Deck PDF backfill plan

**HARD standard (Gideon 4 Nov 2026):** every HTML deck has co-located print-ready PDF plus footer and fixed **Download PDF** controls (hidden in print). Protocol: `docs/html-deck-protocol.md`. Templates: `decks/_templates/`.

**Scope of this document:** inventory and steps only. **Do not** change deck HTML in this phase. **Do not** deploy, Caddy, Appwrite, or VPS changes — Infra tickets need Gideon GO.

## Inventory (`decks/` on `main`)

| Folder | `index.html` | Download PDF UI | Co-located deck PDF (same folder as HTML) | Notes |
|---|---|---|---|---|
| `decks/_templates/` | No (templates only) | N/A | N/A | Ships `pdf-download.*` + `export-deck-pdf.py`; not a published deck. |
| `decks/_templates/clp26-rein-shell/` | Yes (sanitized shell) | **No** | **No** | Placeholder shell; add snippet + export when promoted to a live slug. |
| `decks/nexus-co2/` | Yes (via `build.sh`) | **No** | **No** | 1920×1080 stage deck; uses `render-deck.py` / PNG path in sibling patterns — backfill with `export-deck-pdf.py --mode slides` + HARD buttons. |
| `decks/rein-academic-city-ghana/` | Yes (via `build.sh`) | **No** | **Partial** — `render-deck.py` targets `REIN-Academic-City-Ghana-2026-10-21.pdf` at deck root (may be gitignored / generated locally); not wired to Download PDF links. Source copy only under `sources/REIN_AcademicCityGhana_Deck_v1.pdf`. |

**Live reference (not in repo):** `https://decks.cleantechhub.net/rein/externado-ncuk/` — has footer + fixed buttons and `rein-ncuk-externado.pdf` (pattern copied into templates).

**VPS-only decks** (Caddy map in `docs/infra/caddy/decks.cleantechhub.net.caddy`) are out of repo scope; Infra runs the same backfill checklist per slug after Gideon GO.

## Backfill steps (per deck folder)

1. **Ticket Presentations desk** — brief, slug, PDF basename, brand context (`cleantechhub-brand` | `rein-hubs-brand`), exclusive write path `decks/<name>/`.
2. **Copy templates** — `pdf-download.css` (or merge rules into `shell/deck.css` / `styles.css`), paste `pdf-download.html` fragment; set `DECK_BASENAME.pdf`.
3. **Build HTML** — run existing `build.sh` if the deck uses slide assembly; ensure footer region exists for `.pdf-dl-footer`.
4. **Generate PDF** — from deck root:
   - `python3 export-deck-pdf.py --pdf <basename>.pdf`
   - Stage decks: confirm `?print` / `.print-all` exposes all slides before export.
   - Scroll decks: confirm `.reveal.visible` and `[data-count]` finals in exported PDF.
5. **Verifier** — extend `CHECK.md`: links 200 locally; print preview hides buttons; A4 landscape spot-check; no confidential REIN content in git.
6. **PR** — commit `index.html`, stylesheet changes, PDF, and `CHECK.md` row. No deploy in the same Hands job.
7. **Infra (Gideon GO only)** — rsync/Appwrite upload for slug; `curl -sI` HTML + PDF + assets; Caddy unchanged unless Infra ticket says otherwise.

## Suggested wave order

| Priority | Folder | Rationale |
|---|---|---|
| 1 | `decks/rein-academic-city-ghana/` | Public REIN slug on host; PDF script already present — wire UI + align export to A4 HARD. |
| 2 | `decks/nexus-co2/` | CTH stage deck in repo; good template for slide-mode export. |
| 3 | Forks of `decks/_templates/clp26-rein-shell/` | When a shell becomes a named slug. |

## Out of scope (explicit)

- Editing production trees on `/opt/cth-decks/` without Infra ticket.
- Adding Caddy routes or TLS changes (`docs/infra/caddy/decks.cleantechhub.net.caddy`).
- Merging branch `cursor/cth-html-deck-skill-3ac4` (separate PR for `skills/cth-html-deck/SKILL.md`).
