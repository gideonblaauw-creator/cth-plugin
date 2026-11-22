# Control Tower · Infra (Gideon GO 22 Nov 2026)

**Supersedes** the monolithic **Infrastructure · Desks** / Infra desk model for routing and standards. Harness playbook: `skills/harness/SKILL.md` § Control Tower · Infra. Desk comms: `skills/infrastructure-comms/SKILL.md`.

## Desk — Control Tower · Infra

| Field | Value |
|---|---|
| **Name** | Control Tower · Infra |
| **Agent id** | `c656afb9-5323-440c-b90a-e3abf72135c4` |
| **Cursor Project** | `CTH-Infrastructure` (sidebar label may read Control Tower · Infra) |
| **Lane A workspace** | `cth-plugin` |

**Role (thin desk):**

- Set standards: diagram standard (Mermaid + Graphviz), Hands model routing, ticket rules.
- Keep the Infra backlog.
- **Checker** on every Cloud Hands result (maker ≠ checker; Desk does not skip review).
- **Single queue** for Infra items awaiting Gideon's yes (no parallel hidden queues).

Orchestrator routes stack/harness questions here. Control Tower tickets Hands; it does not SSH-inventory or grind maps on the expensive model.

## Workbenches (report to Control Tower · Infra)

| Workbench | Agent id | Scope |
|---|---|---|
| **Engine Room · Workbench** | `85949e8a-e9c8-44ff-9396-5b03e29be062` | Server/box, disk, backups, containers, DNS/vhosts, uptime |
| **Autopilot · Workbench** | `f8b4b4c2-28a1-45c1-849f-bbb6b5776819` | n8n-li workflows, Slack ops/HITL channel, Telegram→Slack swap, routines, workflow failure forensics |
| **Vault · Workbench** | `c0a4443d-afff-4949-8b3e-21a4cb4e3c98` | Meetings DB + adapters, Cognee, Docmost, BookStack, Infisical secret **names** only (never values) |

**Health:** Doctor_Bot / health checks are owned under **Engine Room · Workbench** (not a separate Desk). Canonical skill: `skills/doctor-bot/SKILL.md`.

Channel workbenches (WhatsApp, Gmail, socials, etc.) are unchanged — see `skills/harness/SKILL.md` § Workbench map.

## Toolbox (shared tools — not an agent)

| Tool | Use |
|---|---|
| Diagram standard | Mermaid + Graphviz (`skills/diagram-design/SKILL.md`) |
| IOPaint | Image cleaner |
| GINA | App builder (Bubblewrap/TWA) |

**Flow:** Desks request via **Control Tower · Infra** → Hands runs → **Control Tower** reviews.

**Client-specific** Toolbox jobs: route to the **client desk first**; that desk requests the job through Control Tower.

## Routing (not Infra)

| Topic | Owner |
|---|---|
| Deck builds, deck catalog, `tools/reveal/` library reviews | **Presentations** desk (+ Images for stills) |
| Image library / brand stills QA | **Images** desk |
| VPS cutover, DNS records, Caddy, deploy | Engine Room · Workbench → Control Tower checker → Gideon HITL |

## Hands model (22 Nov 2026)

Every Cloud Hands launch: **`composer-2.5` with Fast OFF** (`model_params: {fast: false}`). Canonical: `skills/hands-model-routing/SKILL.md`.

## HITL (unchanged)

Gideon yes required before:

- merge
- deploy
- public change
- DNS
- send / post
- spend
- credential activation / deletion
- restarts

## Orchestrator

Orchestrator picks Desk, Workbench, or Hands lane. For Infra standards, backlog, and checker queue → **Control Tower · Infra**. For deck/image library craft review → **Presentations** / **Images**, not Control Tower.