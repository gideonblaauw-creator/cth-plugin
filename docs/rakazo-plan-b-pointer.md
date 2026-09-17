# Rakazo Plan B — coordination pointer (Infra lock)

**Owner:** Infrastructure. **SoT for Phases 0–4:** private repo [`gideonblaauw-creator/rakazo-plan-b`](https://github.com/gideonblaauw-creator/rakazo-plan-b).

This doc is a **pointer only**. Do not install, deploy, or paste secrets from here. Live runbooks and channel layers live in `rakazo-plan-b`.

## Plan A vs Plan B

| Plan | Role | When |
|---|---|---|
| **Plan A** | Grok Bot Orchestrator + Cursor Cloud Hands | Default — all normal desk work |
| **Plan B** | Rakazo Orchestrator + Desks (emergency failover) | **Gideon declare only** — not a standing mode |

**Cursor Cloud Hands always craft** (Lane A and Lane B). Craft does **not** move to Rakazo computers.

Plan B is **emergency-only**. Desks do not pre-switch, dual-primary, or warm-failover without explicit Gideon go.

## Phase map (detail in `rakazo-plan-b`)

| Phase | Scope | Notes |
|---|---|---|
| **0** | Docs plant | Coordination pointers + skills in `cth-plugin`; no VPS install |
| **1** | VPS-4 Tailscale Docker twins | Orch + Infra containers — live steps in `rakazo-plan-b` |
| **2–4** | Orchestration + channels | See `rakazo-plan-b` runbooks |

## Emergency coordination rule

When Gideon declares Plan B:

- **Orchestration → Rakazo** (Orchestrator + Desks only).
- **Craft → Cursor Cloud Hands** (always — ticket Hands on Lane A or Lane B).
- **Channels → Babo HITL** (human-in-the-loop before send/post/pay).
- **LinkedIn:** **[PENDIENTE]** — no standing Workbench assumption under Plan B.

## Where to read next

| Artifact | Location |
|---|---|
| Failover runbook | `rakazo-plan-b` → `failover-runbook` (repo root or `docs/`) |
| Babo channel layer | `rakazo-plan-b` → `babo-channel-layer` |
| Desk comms playbook | `skills/rakazo-failover-comms/SKILL.md` |
| Harness rulebook | `skills/harness/SKILL.md` |

## Non-goals (this pointer)

- No VPS install from `cth-plugin`
- No secrets, tokens, or Eve trees
- No dual-primary wording — Plan A stays default until Gideon declares Plan B
- No wording that craft moves to Rakazo computers
