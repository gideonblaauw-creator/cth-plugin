# Eve file convention (Gideon lock t1423u)

**One-liner:** **Eve** is a **file convention only** for Lane A **product-agent** repos. It defines where agent runtime files live in GitHub — not a deploy target, not a Desk, not a Drive pack.

**Owner:** Infrastructure (same ownership model as Software Factory and Understanding Lab format locks).

**Harness pointer:** `skills/harness/SKILL.md` § Eve · **Skill cross-ref:** `skills/software-factory/SKILL.md` (product-agent builds may also set `factory: yes`).

**Related (do not conflate):** Understanding Lab playground UI = LexiScan house-tour HTML — `docs/understanding-lab-playground-standard.md`. Eve is for **agent runtime files**, not the playground UI.

---

## What Eve is / is not

| Eve **is** | Eve **is not** |
|---|---|
| A locked **file tree** under `agent/` on Lane A product-agent repos | **Vercel Agent Runs** or any hosted agent runtime |
| Auto-discovery of tools and skills from repo paths | A **Desk** (Legal, Grants, Inbox, Socials, Workbench, etc.) |
| SSOT on **GitHub Lane A** for product-agent loops | **Archive** (`/opt/claude-files/`), Drive packs, Lane B, or session dumps |
| Optional TypeScript agent entry + Zod tool schemas | A central tool registry or global config server |

**Source of truth:** GitHub Lane A repo = SSOT for Eve trees. **Never** plant Eve under `/opt/claude-files/` or box scratch as SoT. Archive and VPS paths may mirror for ops — they do not own the convention.

---

## Locked paths

All paths are relative to the **owning Lane A product repo** root.

| Path | Required | Role |
|---|---|---|
| `agent/instructions.md` | **Yes** | System / role instructions for the product agent loop |
| `agent/agent.ts` | Optional | Agent entry (runner wiring, graph bootstrap) |
| `agent/tools/*.ts` | As needed | Tool definitions with **Zod** schemas; one file per tool or small group |
| `agent/skills/*.md` | As needed | Product-scoped skill playbooks (not `cth-plugin` desk skills) |
| `agent/tasks/` | Optional | Task specs, prompts, or job definitions for the loop |

**Discovery:** Runners load tools and skills from these paths. **No** central tool registry in `cth-plugin` or Archive. Product repos own their tool files.

**Do not invent** parallel trees (`agents/`, `.eve/`, `src/agent-registry.ts`, etc.) unless a dedicated remediation ticket renames an existing product.

---

## Apply to (Lane A product-agent repos)

Eve applies to repos where the product **is** an agent loop:

| Product / loop | Notes |
|---|---|
| **Signal Radar** | Product-agent repo; Eve paths apply on remap tickets (not in t1423u) |
| **dataroom-scanner** agent loops | Scanner agent surfaces under `agent/` |
| **LexiScan** runner | FabFloow product; agent runtime files use Eve |
| **Origo** agent loops | Climate data / Nexus agent work on owning Lane A repo |
| **New “app is an agent” Lane A products** | Adopt Eve from first agent ticket |

Factory conveyor (`factory: yes`) and Eve (`eve: yes`) may both appear on the same ticket when the build is Apps+Software **and** product-agent-loop scoped.

---

## Forbid — do not invent Eve trees

Hands **must not** create `agent/` trees for:

| Context | Lane | Use instead |
|---|---|---|
| Legal, Grants, Inbox, Socials, Workbench desks | Desk / comms | Desk skills in `cth-plugin`; tickets to Hands without Eve |
| Drive packs, client deliverables | Lane B | Archive / Drive folder paths on ticket |
| Session dumps, box scratch, Archive-only packs | Non-repo | `/opt/claude-files/…` on ticket; no Eve |
| Harness-only skill edits (`cth-plugin`) | Harness repo | Normal `skills/` paths — **no** `agent/` in this repo for desk playbooks |

Inventing Eve on a desk job is a **miss**. Remap to the correct store (Drive folder, desk skill, or product repo).

---

## Ticket gate

| Ticket type | Eve rule |
|---|---|
| **product-agent-loop** on a Lane A product repo | **Must** use Eve paths. Set optional field `eve: yes` on the ticket. |
| Desk / pack / channel jobs | **Must not** invent Eve trees. Omit `eve: yes`. |
| Harness / skill-only (`cth-plugin`) | No Eve. Document only (this file). |

**Optional ticket field:** `eve: yes` — product-agent-loop build; Hands plants or edits under `agent/` per this doc.

Canonical ticket template: `tickets/TEMPLATE.md`.

---

## Understanding Lab cross-link

Eve and the Understanding Lab solve different layers:

| Layer | Convention | Canonical doc |
|---|---|---|
| **Agent runtime files** | Eve (`agent/instructions.md`, tools, skills) | This file |
| **HITL playground UI** (Tier 1–2) | LexiScan house-tour HTML | `docs/understanding-lab-playground-standard.md` |

Playground stays the **LexiScan HTML house tour** — interactive rooms, quests, decision ledger. **Eve is not the playground UI.** Do not put house-tour HTML under `agent/` as a substitute for `understanding-lab/playground/`.

Tier rules: `docs/understanding-lab-tiers.md`. PR footer: `docs/view-understanding-lab-footer.md`.

---

## Non-goals (t1423u)

- No Vercel Agent / Eve deploy in this lock
- No Signal Radar path remap in t1423u (separate ticket)
- No secrets, tokens, or Infisical key values in Eve files

---

## Changelog

Planted in **t1423u** (`docs/eve-convention.md`). Register updates in root `CHANGELOG.md` when the convention changes.
