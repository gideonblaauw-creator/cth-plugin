# Deck audit index

Index for the HTML deck audit. The playbook those notes feed is `skills/cth-html-deck/SKILL.md`. That skill supersedes `cth-html-deck-visual`.

## Documents

| Path | Status on 2026-10-19 | What it is |
|---|---|---|
| `docs/deck-audit/README.md` | In this branch | This index |
| `docs/deck-audit/A1-decks-cleantechhub.md` | Merged from `deck-skill-audit-a1` @ `0c39db1` | Curl audit of the thirteen live slugs |
| `docs/deck-audit/A1.json` | Merged from the same commit | Machine-readable twin of that audit |
| `docs/deck-audit/A2-vercel-decks.md` | Merged from `deck-skill-audit-a2` @ `16f5251` | Prose audit of Sep–Oct 2026 Vercel decks |
| `docs/deck-audit/A2.json` | Merged from the same commit | Machine-readable twin of that audit |

## Findings from A1 and A2

- **Only APC has a sources slide.** A1 checked all thirteen live slugs on 19 Oct 2026. `apc-cth-2026-10-07` is the only one with a sources slide (`Fuentes públicas`). The other twelve do not. Bridge for Billions mentions `SOURCES.md`, and that file is not served.
- EN/ES exists on four live slugs (A1 rows): `cth-clp26`, `cth-clp26-rein`, `cpi-lab-backbone-cth`, and `aic-q1-2027-packages`. The other nine are one language. The two ClimateLaunchpad slugs share `localStorage` key `clp26lang`. The CPI backbone uses `data-en` / `data-es` and key `cpi-backbone-lang`. AIC uses `data-i18n` and does not store the choice.
- On 19 Oct 2026 at 21:02 UTC, A2's nine known hosts plus `teclogi-financial-model.vercel.app` returned HTTP 402 `DEPLOYMENT_DISABLED`. Guessed names in that audit returned 404 `DEPLOYMENT_NOT_FOUND`. New decks use `decks.cleantechhub.net`.

A1 and A2 are both merged. The deck skill cites them in **Outliers** and **Audit**.

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
| AIC | `skills/aic-brand/SKILL.md` (PROPOSAL, not adopted). OBSERVED: favicon, seven-section shape, type-only mark, and second-table `--ink`, `--gold`, `--serif`, `--sans` (ink `#070c18`, gold `#c9a45c`, Cormorant Garamond, Inter). Pending: `--navy`, `--navy2`, `--ivory`, `--muted`, `--dim`, `--champ`, `--gold-d`, `--plat`, `--line`, `--r`. |

## Host

`https://decks.cleantechhub.net/<slug>/` on the existing Appwrite project `cth-decks`. Publish is HITL. The skill does not deploy.
