---
name: quarto-site-build
description: >
  Scaffolds and renders CleantechHUB Quarto data sites via tools/quarto.
  Use when: demo, datalab, or living-lab Quarto build, data-heavy report site,
  Living Lab dashboard, Presentations or Datalab bench Quarto ticket. Do not
  use when: HTML slide decks (Reveal Tool), grant/proposal playbooks, or edits
  to the existing Datalab JS app.
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
  compatibility: Requires tools/quarto (Quarto 1.6.40 pin, Python venv on builder host).
---

# Quarto site build

Hands playbook for **Presentations** (demos) and **Datalab** (reports / Living Lab dashboards) using `tools/quarto/`. Output is static `_site/` only — **no deploy**, no Caddy/gating changes, no secrets, no client data in repo.

## Workflow

1. **Intake** — Confirm slug, template (`demo` | `datalab` | `living-lab`), language (`en` | `es`), audience, and **sourced data paths** (Drive/VPS — never paste PII into git).
2. **Scaffold** — `cd tools/quarto && ./new-site.sh <slug> <template> [en|es]`.
3. **Wire data** — Copy approved exports into `sites/<slug>/data/`; keep **EXAMPLE DATA** labels until production sources are approved.
4. **Render** — `./build.sh <slug>` must exit 0 (any cell error fails the build).
5. **Evidence** — Attach render log, cite every number to a file path, desktop + mobile screenshots of `_site/`.
6. **Gate** — New slugs stay **noindex** until Gideon GO for public hosting (per slug).

Done when: `build.sh` passes, data sources cited in the QMD or ticket, no invented KPIs, site remains gated by default.

## Rules

- Do **not** modify the live Datalab `/app/`, demo decks, Caddy, or auth gating in this repo.
- Do **not** commit secrets, tokens, or client CSV exports without HITL.
- Use `skills/cleantechhub-brand/SKILL.md` for voice; visual tokens come from `tools/quarto/theme/`.
- Quarto theme is **self-contained** under `tools/quarto/theme/` (not shared with Reveal Tool).

## Do not use when

- Slide decks or presenter HTML → `tools/reveal/` (Reveal Tool skill when landed).
- Competitive grants → `cth-grant`.
- Client service proposals → `cth-proposal-build`.

## Related skills

| Skill | When instead |
|---|---|
| `cleantechhub-brand` | Copy/tone and palette checks |
| `diagram-design` | Standalone HTML+SVG figures (not full Quarto sites) |
| `harness` | Ticket lanes, Cloud Hands contract |

## Hands ticket template (copy into `tickets/`)

```
desk: Presentations | Datalab
folder: gideonblaauw-creator/cth-plugin/tools/quarto/sites/<slug>/
done-when: new-site.sh + build.sh pass; data cited; screenshots in PR; slug gated
model: composer-2.5 (fast=true)
files: tools/quarto/**, skills/quarto-site-build/SKILL.md
read-budget: 40 files / 2MB
lane: github-pr
tier: 0
hitl: no public URL, no client data in git, no deploy
reviewer: Infrastructure

context:
  slug: <kebab-slug>
  template: demo | datalab | living-lab
  language: en | es
  audience: <bench / donor / internal>
  data_paths: <Archive or Drive paths for sourced files>
  acceptance:
    - build.sh exits 0
    - every metric traces to a cited file (no invented numbers)
    - EXAMPLE DATA banner until production sources approved
    - robots noindex until Gideon GO for this slug
```

## References

- `tools/quarto/README.md` — install pins, when to use vs Reveal.
- `tickets/TEMPLATE.md` — full harness fields.
