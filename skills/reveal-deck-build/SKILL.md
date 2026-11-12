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
done-when: tools/reveal/new-deck.sh and build.sh pass for <slug>; PDF exists; no invented numbers; gated stays true unless Gideon names public GO in ticket
model: composer-2.5 (fast=true)
files:
  - tools/reveal/**
  - decks/<slug>/**
  - skills/reveal-deck-build/SKILL.md
read-budget: 40 files / 400 KB
lane: github-pr
tier: 0
hitl: no public slug, no Caddy/VPS deploy, no changing other decks
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
2. **Scaffold** — `tools/reveal/new-deck.sh <slug> <lang> "<title>"`. Never overwrite an existing `decks/<slug>/`.
3. **Author** — Edit `decks/<slug>/index.html` (and optional `assets/`). Keep speaker notes. Custom HTML/JS slides allowed when the brief requires interactivity.
4. **Build** — `tools/reveal/build.sh <slug>`. Attach dist + PDF proof in the PR.
5. **Gate** — Leave `deck-meta.json` `gated: true` unless the ticket includes Gideon public GO for this slug.

## Acceptance

- `build.sh` exits 0; `decks/<slug>/dist/index.html` opens in browser.
- `decks/<slug>/<slug>.pdf` page count matches slide count (approximately one slide per page).
- No invented financial or impact numbers; quotes attributed in `SOURCES.md`.
- No edits to Caddy, decks server, or unrelated deck folders.

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

- `tools/reveal/README.md` — install, new-deck, build
- `tools/reveal/theme/_quarto-revealjs.yml` — Quarto revealjs variant
- `docs/html-deck-protocol.md` — PDF/download standard for **HTML** stage decks (separate from reveal toolkit)
