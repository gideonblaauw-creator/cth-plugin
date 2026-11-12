# Reveal deck toolkit (Presentations bench)

Pinned **reveal.js 5.x** scaffold for CleantechHUB narrative decks. Cloud Hands builds new slugs; the Presentations desk reviews. Heavy interactive decks (e.g. `decks/nexus-co2/`) may still use custom JS — this template allows raw HTML/JS slides.

## Prerequisites

- Node.js 18+
- `google-chrome-stable` (decktape uses Chromium for PDF export)

## Install (once per clone)

```bash
cd tools/reveal
npm ci
```

Compiles `theme/cleantechhub.css` from `skills/cleantechhub-brand` palette (Inter, CTH Green/Dark/Lime).

## Outline (YAML)

```bash
tools/reveal/outline.sh [--force] <deck.yaml>
```

Validates against `library/schema.json`, renders typed slides into `decks/<meta.slug>/`, then runs `build.sh`. Use `--validate-only` or `--skip-build` for CI subsets.

## Lint

```bash
tools/reveal/lint.sh <slug>
```

Brand palette, theme fonts, sourced stat/chart/table slides, PDF page count vs slide count, and Chromium overflow check.

## New deck (legacy scaffold)

```bash
tools/reveal/new-deck.sh <slug> [en|es] ["Optional title"]
```

- Copies `template/` → `decks/<slug>/`
- Sets `deck-meta.json` with **`gated: true`** (label only — see Gating below)
- Refuses to overwrite an existing folder

## Build

```bash
tools/reveal/build.sh <slug>
```

Produces:

- `decks/<slug>/dist/` — static tree for `decks.cleantechhub.net/<slug>/` (deploy is **not** Hands; Infra + Gideon GO)
- `decks/<slug>/<slug>.pdf` — decktape export (1920×1080)

## Starter template slides

Title, agenda, section, two-column, chart placeholder, quote, contact — each with speaker notes. Plugins: notes, search, zoom, highlight.

## Quarto

Merge `theme/_quarto-revealjs.yml` into a Quarto project to reuse `theme/cleantechhub.scss` (e.g. demo-promigas jobs).

## Hands routing

New reveal decks: ticket via `skills/reveal-deck-build/SKILL.md` → Cloud Hands on this repo.

## Gating (label vs enforcement)

`deck-meta.json` → `"gated": true` and the HTML meta tag `cth-deck-gated` are **labels only** for Hands and reviewers. They do **not** enforce access.

**Real gating** is **Caddy + oauth2-proxy** on the decks server (`decks.cleantechhub.net`). Making a deck **public** requires **Gideon’s own GO per slug** plus an **Infra Caddy route change** — never done by this toolkit or Cloud Hands in a deck ticket.

New scaffolds keep `gated: true` in metadata as documentation; do not treat that JSON field as security.

## Constraints (harness)

- No Caddy, gating server, or VPS deploy from this tool
- Do not edit or delete existing decks except the slug named in the ticket
- No secrets in repo
