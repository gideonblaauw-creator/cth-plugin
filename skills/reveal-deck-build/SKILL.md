---
name: reveal-deck-build
description: >
  Cloud Hands playbook for new CleantechHUB reveal.js decks via tools/reveal. Use
  when: new presentation slug, reveal deck scaffold, Presentations bench Hands
  ticket, decks.cleantechhub.net narrative deck. Do not use when: 1920×1080 HTML
  stage shell (cth-html-deck), scroll REIN long-page (cth-html-deck-visual), or
  heavy interactive deck without reveal scaffold.
license: MIT
metadata:
  version: "1.0.0"
  category: operations
---

# Reveal deck build (Cloud Hands)

Hands scaffolds and builds **new** reveal.js decks using `tools/reveal/`. Presentations desk reviews; merge and deploy are Gideon HITL.

## Ticket template (paste into `tickets/`)

```
desk: Presentations
folder: decks/<slug>/ and tools/reveal/
cursor_project: CTH-Presentations
cursor_workspace: cth-plugin
done-when: tools/reveal/new-deck.sh and build.sh pass for <slug>; PDF exists; no invented numbers; deck-meta gated label stays true unless ticket documents Gideon public GO (Caddy still separate)
model: composer-2.5 (fast=true)
files:
  - tools/reveal/**
  - decks/<slug>/**
  - skills/reveal-deck-build/SKILL.md
read-budget: 40 files / 400 KB
lane: github-pr
tier: 0
hitl: no public slug without Gideon GO + Infra Caddy; Hands do not change Caddy/oauth2-proxy or VPS deploy; no changing other decks
reviewer: Presentations
context:
  slug: <kebab-case>
  language: en | es
  title: "<human title>"
  audience: <one line>
  brief: <Drive path or pasted STE — sourced metrics only>
  gated: true
```

## Workflow

1. **Read brief** — Load `skills/cleantechhub-brand/SKILL.md` for colours/tone. Load sourced metrics only; use `SOURCES.md` in the deck folder.
2. **Outline (preferred)** — Tickets supply `deck.yaml` (`meta` + typed `slides[]`). Run `tools/reveal/outline.sh deck.yaml` (add `--force` to refresh an existing slug). Validates against `tools/reveal/library/schema.json`, renders slide types, then runs `build.sh`.
3. **Scaffold (legacy)** — `tools/reveal/new-deck.sh <slug> <lang> "<title>"` when no outline exists. Never overwrite an existing `decks/<slug>/` without `--force` on outline.
4. **Author** — For outline-driven decks, edit `deck.yaml` and re-run outline; for hand-built decks, edit `decks/<slug>/index.html`. Keep speaker notes.
5. **Lint** — `tools/reveal/lint.sh <slug>` after build (brand colours, theme fonts, overflow, sourced stat/chart/table slides, PDF page count vs slides).
6. **Gate label** — Leave `deck-meta.json` `gated: true` unless the ticket documents Gideon public GO for this slug. **`gated` in JSON is a label only** — it does not enforce access. **Real gating** is **Caddy + oauth2-proxy** on the decks server. Making a deck public requires **Gideon GO per slug** plus an **Infra Caddy change** (out of scope for Hands deck tickets).

## Acceptance

- **Outline tickets:** `tools/reveal/outline.sh <deck.yaml>` and `tools/reveal/lint.sh <slug>` both exit 0.
- **Hand-built tickets:** `build.sh` exits 0; `lint.sh <slug>` exits 0 when the ticket requires brand checks.
- `decks/<slug>/dist/index.html` opens in browser; `decks/<slug>/<slug>.pdf` page count matches slide count.
- Unknown slide `type` or missing required fields fail at outline validation (before render).
- No invented financial or impact numbers; `stat-band`, `chart-proof`, and `data-table` include `source`.
- No edits to Caddy, oauth2-proxy, decks server, or unrelated deck folders.

## Gating (do not confuse label with enforcement)

| Layer | Role |
|-------|------|
| `deck-meta.json` `gated`, HTML `cth-deck-gated` | Documentation label for Hands/reviewers |
| Caddy + oauth2-proxy on VPS | **Actual** access control for `decks.cleantechhub.net` |

Cloud Hands **must not** claim a deck is public because metadata says `gated: false`. Public publish is Gideon GO + Infra Caddy only.

## Do not use when

| Instead | Skill / path |
|---------|----------------|
| Pixel-perfect 1920×1080 stage shell | `skills/cth-html-deck/SKILL.md` |
| Long scroll REIN partner deck | `skills/cth-html-deck-visual/SKILL.md` |
| Diagram-only deliverable | `skills/diagram-design/SKILL.md` |

## Related skills

| Skill | When |
|-------|------|
| `cleantechhub-brand` | Colours, Inter, wordmark |
| `harness` | Ticket lanes, Hands boundary |
| `cth-html-deck` | Non-reveal stage decks |

## References

- `tools/reveal/README.md` — install, outline, lint, new-deck, build
- `tools/reveal/library/schema.json` — `deck.yaml` contract
- `tools/reveal/theme/_quarto-revealjs.yml` — Quarto revealjs variant
- `docs/html-deck-protocol.md` — PDF/download standard for **HTML** stage decks (separate from reveal toolkit)
