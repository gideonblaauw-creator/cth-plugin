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
  version: "1.0.1"
  category: infrastructure
  compatibility: Requires tools/quarto (Quarto 1.6.40 pin, Python venv on builder host).
---

# Quarto site build

Hands playbook for **Presentations** (demos) and **Datalab** (reports / Living Lab dashboards) using `tools/quarto/`. Output is static `_site/` only — **no deploy**, no Caddy/gating changes in this repo, no secrets, no client data.

## Workflow

1. **Intake** — Confirm slug, template (`demo` | `datalab` | `living-lab`), language (`en` | `es`), audience, and **sourced data paths** (Drive/VPS — never paste PII into git).
2. **Scaffold** — `cd tools/quarto && ./new-site.sh <slug> <template> [en|es]`.
3. **Wire data** — Copy approved exports into `sites/<slug>/data/`; keep **EXAMPLE DATA** labels until production sources are approved.
4. **Commit source** — On `lane: github-pr`, commit `sites/<slug>/` (`.qmd`, `_quarto.yml`, `data/`). Do **not** commit `_site/`, `_freeze/`, or `.quarto/`.
5. **Render** — `./build.sh <slug>` must exit 0 (any cell error fails the build).
6. **Evidence** — Attach render log, cite every number to a file path, desktop + mobile screenshots of `_site/`.
7. **Access** — Until Gideon GO per slug: no public URL. **Gating** on the host is **Caddy + oauth2-proxy** (Infra). Template **`noindex`** meta only discourages search crawlers.

Done when: `build.sh` passes, data sources cited, no invented KPIs, source in PR, host access still unset until GO.

## Rules

- Do **not** modify the live Datalab `/app/`, demo decks, Caddy, or oauth2-proxy from this repo.
- Do **not** commit secrets, tokens, or client CSV exports without HITL.
- Do **not** add GitHub or internal repo links to client-facing site navbars.
- Use `skills/cleantechhub-brand/SKILL.md` for voice; visual tokens come from `tools/quarto/theme/`.
- Quarto theme is **self-contained** under `tools/quarto/theme/` (not shared with Reveal Tool).

## Do not use when

- Slide decks or presenter HTML → `tools/reveal/` and `skills/reveal-deck-build/SKILL.md`.
- Competitive grants → `cth-grant`.
- Client service proposals → `cth-proposal-build`.

## Related skills

| Skill | When instead |
|---|---|
| `reveal-deck-build` | reveal.js decks on decks.cleantechhub.net |
| `cleantechhub-brand` | Copy/tone and palette checks |
| `diagram-design` | Standalone HTML+SVG figures (not full Quarto sites) |
| `harness` | Ticket lanes, Cloud Hands contract |

## Hands ticket template (copy into `tickets/`)

```
desk: Presentations | Datalab
folder: gideonblaauw-creator/cth-plugin/tools/quarto/sites/<slug>/
done-when: sites/<slug>/ committed; new-site.sh + build.sh pass; data cited; screenshots; no public URL without GO
model: composer-2.5 (fast=true)
files: tools/quarto/**, skills/quarto-site-build/SKILL.md
read-budget: 40 files / 2MB
lane: github-pr
tier: 0
hitl: no public URL, no client data in git, no deploy, no Caddy edits
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
    - noindex meta present (search hint only)
    - Caddy/oauth2-proxy gating documented; Infra after Gideon GO
```

## References

- `tools/quarto/README.md` — install pins, when to use vs Reveal.
- `skills/reveal-deck-build/SKILL.md` — reveal.js deck Hands playbook.
- `tickets/TEMPLATE.md` — full harness fields.
