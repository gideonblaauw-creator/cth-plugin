# Observatorio de la Tierra — brand pack v1

Co-brand **Universidad Externado de Colombia × CleantechHUB**. Tokens inherit the five-colour CleantechHUB Manual (2024) and Open Sans stack used on `decks/earth-observatory-externado-2026-10` (`eo-extra.css` when present on `main`).

## Layout

| Path | Purpose |
|------|---------|
| `brand_dna.yaml` | Machine-readable DNA |
| `final/` | Approved lockups (from EO logo pack) |
| `brand-book/` | Manual de marca HTML + PDF |
| `templates/social/` | Sized social HTML templates |
| `applications/` | Agenda, one-pager, slide master, email header |
| `scripts/export-eo-assets.py` | Playwright PDF/PNG export → `out/` |
| `options/` | Five visual directions (no full-bleed gradients) — IG + banner mock-ups |

Regenerate exports:

```bash
python3 brand/earth-observatory/scripts/export-eo-assets.py
python3 brand/earth-observatory/options/export-five-directions.py
```

**Options deliverables:** `options/eo-dir-1.png` … `eo-dir-5.png`, `options/eo-5-directions.pdf`, `options/contact-sheet.png`.

Draft only — no deploy from this folder without Infra ticket.
