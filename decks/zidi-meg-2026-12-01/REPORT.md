# Hands report — Zidi MEG deck (zidi-meg-2026-12-01)

**bc-id:** `bc-555afe81-668f-5248-a440-7cba12fb49b4`  
**Branch:** `cursor/zidi-meg-2026-12-01`  
**Preview (gated, post-merge + Infra route):** `https://decks.cleantechhub.net/zidi-meg-2026-12-01/` (Google SSO)  
**Lane:** A · `decks/zidi-meg-2026-12-01/`  
**Reviewer:** Presentations (`499a82bc`)

## Deliverables

| Item | Path |
|------|------|
| Deck source | `decks/zidi-meg-2026-12-01/index.html` |
| PDF (1920×1080 decktape) | `decks/zidi-meg-2026-12-01/zidi-meg-2026-12-01.pdf` |
| Contact sheet | `decks/zidi-meg-2026-12-01/review/contact-sheet.png` |
| Sources | `decks/zidi-meg-2026-12-01/SOURCES.md` |

## QA

- `tools/reveal/build.sh zidi-meg-2026-12-01` — exit 0; 15 slides / 15 PDF pages (decktape 1920×1080)  
- `tools/reveal/lint.sh zidi-meg-2026-12-01` — exit 0 (overflow, fonts)  
- `review/capture.mjs` — contact sheet + 15 slide PNGs  
- Fix-1 (content): removed Pool #1 / IRR; expanded Q1–Q2–Q4–Q5 answers; programme ladder; closing tagline + booking link  
- Frame: FODESEP `fp-*` pattern + `assets/deck.css`; Titillium titles via `assets/cth-skin.css`; globe logo top right (incl. photo slide)  
- Exclusions honoured (no Axioma / projected IRR, named investors, EUR 2M roadshow, EBITDA, BDO narrative, live zero counters)

## HITL

- `deck-meta.json` `gated: true` — not public until Gideon GO + Caddy route. Do not share outside Presentations review without GO.