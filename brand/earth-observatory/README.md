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

Regenerate exports:

```bash
python3 brand/earth-observatory/scripts/export-eo-assets.py
```

Draft only — no deploy from this folder without Infra ticket.
