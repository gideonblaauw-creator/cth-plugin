# CTH Skill Template (copy-paste skeleton)

Copy this file to `skills/<name>/SKILL.md`, replace placeholders, delete unused sections, and add a matching `.cursor/skills/<name>/SKILL.md` stub.

## Frontmatter (required)

```yaml
---
name: skill-name
description: >
  <One clause: what the skill does and what it produces>. Use when: <intent 1>,
  <intent 2>, <intent 3>. Do not use when: <overlap skill or wrong context>.
license: MIT
metadata:
  version: "1.0.0"
  category: brand | programs | operations | infrastructure
---
```

### Frontmatter rules (CTH + Agent Skills spec)

| Field | Rule |
|---|---|
| `name` | kebab-case; must match directory name; max 64 chars |
| `description` | Non-empty; max 1024 chars; **the routing signal** — capability + `Use when:` triggers |
| `license` | `MIT` (matches `cth-plugin`) |
| `metadata.version` | Semver string |
| `metadata.category` | One of: `brand`, `programs`, `operations`, `infrastructure` |
| `compatibility` | Optional; only if env requirements (e.g. Playwright, VPS SSH) |

**Description template (write-skill + agentskills.io):**

```
<Capability in one clause>. <Output or behavior>. Use when: <3–8 concrete intents>. Do not use when: <wrong playbook>.
```

**Good:** third-person capability + explicit triggers. **Bad:** "Helps with X", vague verbs, no triggers.

## Body skeleton

```markdown
# Skill Title

<One sentence — what this playbook guarantees.>

## Workflow

1. **Step name** — Action. Done when: <checkable criterion>.
2. **Step name** — Action. Done when: <checkable criterion>.

## Rules

- Hard constraints the agent must not violate.

## Do not use when

- <Wrong context> → use `other-skill` instead.

## Related skills

| Skill | When instead |
|---|---|
| `other-skill` | <condition> |

## References

- `references/<file>.md` — load when <condition>.
```

## Cursor stub skeleton

Path: `.cursor/skills/<name>/SKILL.md`

```yaml
---
name: skill-name
description: >
  <Same trigger branches as canonical — shortened if needed for stub discovery.>
---
```

```markdown
# skill-name

This file is a Cursor discovery stub. The playbook source of truth is `skills/<name>/SKILL.md`.

1. Read `skills/<name>/SKILL.md` and any `skills/<name>/references/` files it points to before doing the work.
2. Follow that playbook. Do not invent parallel rules in this stub.
```

## Progressive disclosure

| Body size | Action |
|---|---|
| ≤ 200 lines | Keep in `SKILL.md` |
| 200–500 lines | Move occasional sections to `references/` |
| > 500 lines | Split by branch or domain into `references/` |

Keep file references **one level deep** from `SKILL.md`.

## Validation (cth-plugin)

```bash
jq empty .claude-plugin/plugin.json .mcp.json
python3 -c "
import yaml, json
from pathlib import Path
# See AGENTS.md — frontmatter name parity + stub parity (exclude secrets)
"
```
