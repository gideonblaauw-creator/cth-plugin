---
name: rakazo-failover-comms
description: >
  Coordination playbook for Rakazo Plan B emergency failover. Use when: Plan B,
  Rakazo failover, Gideon declares emergency, Babo channel layer, or failover
  runbook routing. Do not use when: normal Plan A desk work (use the owning desk
  comms skill), VPS install from cth-plugin, or secrets handling.
license: MIT
metadata:
  version: "1.1.0"
  category: comms
  desk: "Infrastructure"
  owner: Infrastructure desk c656afb9
---

# Rakazo Plan B — Failover Comms

Coordination-only playbook for **Plan B emergency failover**. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

**Pointer doc:** `docs/rakazo-plan-b-pointer.md`. **Live Phases 0–4:** private repo [`gideonblaauw-creator/rakazo-plan-b`](https://github.com/gideonblaauw-creator/rakazo-plan-b).

## 1. Plan A vs Plan B

| Plan | Default? | Rakazo role | Who crafts | Who coordinates channels |
|---|---|---|---|---|
| **Plan A** | Yes | — (Grok Bot Orchestrator) | Cursor Cloud Hands (ticketed) | Desk Workbenches + Grok Bot |
| **Plan B** | No — Gideon declare only | **Orchestrator + Desks only** | **Cursor Cloud Hands** (always, Lane A/B) | **Babo HITL** |

Craft **never** moves to Rakazo computers. Plan B is **not** a standing mode. Do not pre-switch, warm-failover, or use dual-primary wording.

## 2. When to escalate Plan B

Escalate **only** when **Gideon Blaauw** explicitly declares Plan B emergency in the owning chat.

| Signal | Action |
|---|---|
| Gideon declares Plan B | Read `rakazo-plan-b` failover-runbook; Rakazo takes Orchestrator + Desks; **ticket Cursor Cloud Hands for all craft**; channels via Babo HITL |
| Grok Bot / VPS degraded but no declare | Stay on Plan A; ticket Infrastructure Hands for diagnosis — **do not** invoke Rakazo |
| Desk asks "should we switch?" | HOLD — flag Gideon; no self-serve failover |

## 3. Coordination only

Grok Bot on this stream is **coordination only**.

- **Ticket Cursor Cloud Hands** for all file/research/code/copy — Plan A and Plan B.
- **Never** send, post, or pay from Grok chat on this stream.
- **Never** install VPS services or paste secrets from Grok chat.
- In Plan B emergency: Rakazo holds Orchestrator + Desk coordination; Grok Bot/Rakazo routes and holds HITL gates only — **never** craft on Rakazo computers.

## 4. Runbook pointers (`rakazo-plan-b`)

When Plan B is declared, open the private repo (access via Gideon / Infrastructure):

| Artifact | Purpose |
|---|---|
| **failover-runbook** | Step order, roles, and emergency orchestration handoff |
| **babo-channel-layer** | Channel routing and Babo HITL before send/post/pay |

Do not duplicate runbook steps in this skill. `cth-plugin` holds coordination pointers only.

## 5. Model and Hands finish (this stream)

| Job | Model | Notes |
|---|---|---|
| Mechanical copy, file packs, inventories | `gemini-3.7-flash` | Empty mechanical → Flash |
| Repo / code / build on this stream | `composer-2.5` (`fast=true`) | **Composer Fast ON** (t1263u) |
| Review / eval / brand with no model | **HOLD** | Flag Gideon |

**Every Hands finish** on this stream **must name Understanding Lab tier** in Gideon chat — first line:

- `**Tier 0** — Ship` (default for pointer/doc plants)
- `**Tier 1** — Light Understanding`
- `**Tier 2** — Full Lab + ledger`

Canonical tier rules: `docs/understanding-lab-tiers.md`, `skills/infrastructure-comms/SKILL.md` §7.

## 6. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes.

Under Plan B, outbound channels go through **Babo HITL** per `babo-channel-layer` in `rakazo-plan-b`. **LinkedIn:** **[PENDIENTE]**.

## 7. Non-goals

- No VPS install from `cth-plugin` tickets on this skill
- No secrets, Eve trees, or dual-primary wording
- No wording that craft moves to Rakazo computers — **always ticket Cursor Cloud Hands for craft**

## Related skills

| Skill | When |
|---|---|
| `infrastructure-comms` | Normal Infra desk routing and peer doc pointers |
| `harness` | Tickets, Cloud Hands boundary, tier lock |
| `infisical` | Secrets SoT pointer (names only in tickets) |
