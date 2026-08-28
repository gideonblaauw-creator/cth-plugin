---
name: skill-template
description: >
  Author, review, and normalize CTH Agent Skills in cth-plugin. Defines the
  canonical SKILL.md template, frontmatter spec, Cursor stub pattern, and
  progressive-disclosure rules. Use when: creating a new skill, rewriting a
  skill description, reviewing skill quality, aligning frontmatter with the
  Agent Skills spec, or adding a Cursor stub. Do not use when: executing a
  domain workflow (use that domain's skill instead).
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
---

# CTH Skill Template

One-liner: the description field is the agent's routing signal — get it right first, then write the body.

Sources synthesized for this template: [anthropics/skills](https://github.com/anthropics/skills) (Agent Skills spec), [theneoai/awesome-skills write-skill](https://github.com/theneoai/awesome-skills), [mattpocock/skills writing-for-agents](https://github.com/mattpocock/skills), [agentskills.io/specification](https://agentskills.io/specification).

## Workflow

1. **Gather requirements** — Capability, triggers, output, scripts vs text-only, overlapping skills. Done when: one-sentence capability and 3–8 trigger intents are written.
2. **Write the description first** — Use the template in [references/SKILL-TEMPLATE.md](references/SKILL-TEMPLATE.md). Done when: description has capability + `Use when:` + optional `Do not use when:`.
3. **Draft the body** — Workflow steps with **done when** criteria; rules; related-skills table. Done when: an agent can execute without guessing.
4. **Disclose reference** — Move occasional or branch-specific content to `references/`. Done when: main `SKILL.md` stays under 500 lines.
5. **Add Cursor stub** — Copy stub skeleton from [references/SKILL-TEMPLATE.md](references/SKILL-TEMPLATE.md) to `.cursor/skills/<name>/SKILL.md`. Done when: stub points at canonical only (no playbook fork).
6. **Validate** — Name matches directory; stub parity (except `secrets`); `jq` on manifests. Done when: AGENTS.md validation passes.

## Description rules (routing signal)

| Requirement | Pass | Fail |
|---|---|---|
| Capability | "Builds bilingual Nexus one-pagers" | "Helps with startups" |
| Triggers | Contains `Use when:` | No trigger language |
| Length | ≤ 1024 chars (target ≤ 500) | Wall of keywords |
| Voice | Third-person capability | "You should…" in description |
| Overlap | `Do not use when:` names sibling skill | Identical to another skill |
| CTH routing | Grant vs proposal vs brand separated | Mixed playbooks |

CTH-specific routing (never mix):

| Work type | Skill |
|---|---|
| Grant, donor, competitive bid | `cth-grant` |
| Commercial client service proposal | `cth-proposal-build` |
| CleantechHUB visual/copy brand | `cleantechhub-brand` |
| CLP26 campaign brand | `clp26-brand` |
| Cloud Hands / tickets / lanes | `harness` |
| New GitHub repo / promote tree | `app-build` |

## Body rules (writing-for-agents)

- **Steps** end with checkable **done when** criteria — not "understanding reached."
- **Progressive disclosure**: inline what every branch needs; push branch-only material to `references/`.
- **Single source of truth**: do not duplicate `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` inside skills — pointer only.
- **No secrets**: never embed tokens, API keys, or MCP credentials in skills.
- **Imperative voice** in steps; positive instructions over negation-only guards.

## Directory layout (Agent Skills spec)

```
skills/<name>/
├── SKILL.md              # required
├── references/           # optional — on-demand docs
├── scripts/              # optional — deterministic automation
└── assets/               # optional — templates, static files
```

## Do not use when

- Running a grant pack → `cth-grant`
- Building a client proposal → `cth-proposal-build`
- Executing Harness tickets → `harness`
- Loading credentials → `secrets` (Claude Desktop only; no Cursor stub)

## Related skills

| Skill | Relationship |
|---|---|
| `harness` | Operating model; token lock; Desk/Hands boundary |
| `app-build` | When a skill backs a new repo or promoted app tree |

## References

- [SKILL-TEMPLATE.md](references/SKILL-TEMPLATE.md) — copy-paste skeleton + Cursor stub
- [skill-toolkit.json](../harness/references/skill-toolkit.json) — machine-readable inventory of all CTH skills
