# Hands report — Zidi MEG deck (zidi-meg-2026-12-01)

**bc-id:** `bc-f6b2aec9-493c-56e0-9a87-ea28cd85b9f6`  
**Branch:** `cursor/zidi-meg-2026-12-01-fix4`  
**Fix:** Gideon review 27 Nov 2026 13:28 COT (Fix-4)  
**Preview (gated, post-merge + Infra route):** `https://decks.cleantechhub.net/zidi-meg-2026-12-01/` (Google SSO)  
**Lane:** A · `decks/zidi-meg-2026-12-01/`  
**Reviewer:** Presentations (`499a82bc`)

## Deliverables

| Item | Path |
|------|------|
| Deck source | `decks/zidi-meg-2026-12-01/index.html` |
| PDF v4 (1920×1080 decktape) | `decks/zidi-meg-2026-12-01/ZidiCircle-MEG-Gideon-Blaauw-MubOn-1Dec2026-v4-REVIEW.pdf` |
| PDF (slug alias) | `decks/zidi-meg-2026-12-01/zidi-meg-2026-12-01.pdf` |
| Contact sheet v4 | `decks/zidi-meg-2026-12-01/review/contact-sheet-v4.png` |
| Image credits | `decks/zidi-meg-2026-12-01/review/image-credits.md` |
| Numbers sources | `decks/zidi-meg-2026-12-01/review/numbers-sources.md` |
| Non-public figures | `decks/zidi-meg-2026-12-01/review/nonpublic-figures.md` |
| Sources | `decks/zidi-meg-2026-12-01/SOURCES.md` |

## QA

- `tools/reveal/build.sh zidi-meg-2026-12-01` — exit 0; 15 slides / 15 PDF pages (decktape 1920×1080)  
- `tools/reveal/lint.sh zidi-meg-2026-12-01` — exit 0 (overflow, fonts)  
- `review/capture.mjs` — contact sheet + 15 slide PNGs  
- Fix-1 (content): removed Pool #1 / IRR; expanded Q1–Q2–Q4–Q5 answers; programme ladder; closing tagline + booking link
- Fix-2 (interactive): Chart.js MubOn metrics; clickable programme ladder + MubOn journey; Q3 toggle; readiness/regulatory tick lists; investor ticket slider; expandable Q2 sectors; Q4 risk table; Q6 diaspora/institutional lens; `review/capture-interactions.mjs`
- Fix-3 (PDF + charts): `decktape=1` static export; final KPI values + print fallbacks; kWh hero on slide 6 / EV brand share on slide 8; risk table Fix-1 cell notes; contact sheet + 1280 before/after captures  
- Fix-4 (Gideon 27 Nov): full-bleed Pexels/Unsplash backgrounds + strong navy scrim; removed AIC; five programme cards with MubOn path badges; flip cards for readiness/unit economics and Q5 regulatory diligence; larger Q2/Q4 typography; per-KPI source lines; thematic `assets/bg/` pack; review markdowns; v4 PDF filename  
- Frame: FODESEP `fp-*` pattern + `assets/deck.css`; Titillium titles via `assets/cth-skin.css`; globe logo top right (incl. photo slide)  
- Exclusions honoured (no Axioma / projected IRR, named investors, EUR 2M roadshow, EBITDA, BDO narrative, live zero counters)

## HITL

- `deck-meta.json` `gated: true` — not public until Gideon GO + Caddy route. Do not share outside Presentations review without GO.