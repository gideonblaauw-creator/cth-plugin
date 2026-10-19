# Deck audit index

Index for the HTML deck audit. The playbook those notes feed is `skills/cth-html-deck/SKILL.md`. That skill supersedes `cth-html-deck-visual`.

## Documents

| Path | Status on 2026-10-19 | What it is |
|---|---|---|
| `docs/deck-audit/README.md` | In this branch | This index |
| `docs/deck-audit/A2-vercel-decks.md` | Merged from `deck-skill-audit-a2` @ `16f5251` | Prose audit of Sep–Oct 2026 Vercel decks |
| `docs/deck-audit/A2.json` | Merged from the same commit | Machine-readable twin of that audit |
| Branch `deck-skill-audit-a1` | Not on `origin` | Expected further notes under `docs/deck-audit/` |

## Merge audit findings

A2 is merged. Cite `docs/deck-audit/A2-vercel-decks.md` and `docs/deck-audit/A2.json`. The deck skill's **Audit** section lists what it adopted (Manual de Marca blues and Open Sans, B4B chrome plus an APC sources slide, visible `[PENDIENTE]` chips, no revival of paused Vercel hosts).

TODO: merge audit findings from `deck-skill-audit-a1` when that ref exists. Checked `origin` on 19 Oct 2026 after A2 landed: `deck-skill-audit-a1` was absent.

## Reference implementation

| Item | Value |
|---|---|
| Branch | `meetings-2026-10-13-b4b` |
| Folder | `decks/meetings-2026-10-13/b4b/` |
| Shell | `shell/deck.css`, `shell/deck.js`, `shell/head.html` |
| Build | `build.sh`, `render-deck.py` |
| Sources | `SOURCES.md`, `PENDIENTES.md` |
| Live URL | `https://decks.cleantechhub.net/b4b-cth-2026-10-13/` |

`decks/` is not on `main`. Do not merge the meeting branch just to land the skill.

## Brand contexts the skill switches on

| Context | Where the tokens live |
|---|---|
| CleantechHUB | `skills/cleantechhub-brand/brand_dna.yaml` (Manual de Marca, Jan 2024) plus voice in `skills/cleantechhub-brand/SKILL.md` |
| REIN Hubs | Token table in `skills/cth-html-deck/SKILL.md`. HOLD and the dollar-amount ban: `skills/rein-hubs-comms/SKILL.md` |
| AIC | `skills/aic-brand/SKILL.md` (PROPOSAL, tokens `[PENDIENTE]`) |

## Host

`https://decks.cleantechhub.net/<slug>/` on the existing Appwrite project `cth-decks`. Publish is HITL. The skill does not deploy.
