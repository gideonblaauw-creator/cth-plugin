---
name: teclogi-comms
description: >
  Communications protocol for the Teclogi Desk. Trigger on Teclogi comms, dataroom client messages, or Teclogi Desk coordination.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "Teclogi"
  owner: Infrastructure desk c656afb9
---

# Teclogi — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End client:** Teclogi (logistics / dataroom client). Primary external contacts: **[PENDIENTE]**.
- **Who hears what:** Client-facing → **Spanish** unless the live thread is English. Gideon ↔ Desk chat → **English** unless the live thread is Spanish.
- **Internal:** Gideon Blaauw (HITL, Orchestrator escalation).

## 2. Brand skill to follow

`[PENDIENTE]` — Teclogi client brand (not `cleantechhub-brand`). No CTH lime leak.

No brand leak across clients. Co-brand only when Gideon explicitly approves.

## 3. Coordination only

Grok Bot on this Desk is **coordination only** (Token lock 2026-08-26). Route, HITL, go/no-go, and channel I/O escalation.

- Desk **tickets** Cursor Cloud Hands.
- Desk **reviews** output (maker ≠ checker).
- No first-draft packs, research grind, inventory, or code in the Grok chat.
- Do not write Grok Bot box workflows in this skill.

## 4. Everything file/research/code/copy is ticketed to Cursor Cloud Hands

All file packs, research grind, copy drafts, inventories, HTML/docx/xlsx, and repo/code work → **seven-field ticket** to Cursor Cloud Hands. No bc-id = miss.

- Lane A (this repo and other owning repos): `lane: github-pr`
- Lane B (grant/client packs on Drive): `lane: drive-folder`
- **Lane A repo / store for this Desk:** `https://github.com/gideonblaauw-creator/cth-data-room-scanner` (Teclogi-only per Lane A repo lock).
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.

## 5. Lowest-tier model

| Job | Model | Notes |
|-----|-------|-------|
| Mechanical copy, file packs, inventories, research grind | `gemini-3.7-flash` | Empty mechanical model → Flash |
| Repo / code / build Hands | `composer-2.5` (`fast=true`) | Fast ON for builds (t1242u) |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |

Never silently use Sonnet, Haiku, Opus, or Grok on Cloud Hands. Repo/code builds use Composer 2.5 Fast ON (t1242u); mechanical/tiny stay Flash.

## 6. Workbench exception

This Desk has **no standing Workbench**. WhatsApp only via Orchestrator when Hands cannot reach the contact.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.


Lane A repo lock: never launch non-Teclogi work on `cth-data-room-scanner`.
## 8. Secrets (Infisical SoT — Gideon 2026-09-07)

Service secrets → **Infisical** (`skills/secrets/SKILL.md`). Never paste token values in tickets, PRs, or chat. Hands fetch by project / environment / key name only.
