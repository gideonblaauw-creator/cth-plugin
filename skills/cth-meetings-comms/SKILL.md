---
name: cth-meetings-comms
description: >
  Communications protocol for the CTH Meetings Desk. Trigger on CTH Meetings Desk comms, calendar invites, or meeting coordination.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "CTH Meetings"
  owner: Infrastructure desk c656afb9
---

# CTH Meetings — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End clients:** Meeting attendees across CTH programs and clients. Named attendees: **[PENDIENTE]** per meeting.
- **Who hears what:** Invite/body language follows attendee locale. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).

## 2. Brand skill to follow

`cleantechhub-brand` for CTH-hosted meetings.

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
- **Lane A repo / store for this Desk:** Calendar is Tool/Workbench — not a GitHub pack by default.
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.

## 5. Cloud Hands model routing

Token lock **2026-08-28** (supersedes 2026-08-26 Flash-default for fill-in). See `skills/harness/SKILL.md` and `skills/hands-model-routing/SKILL.md`.

| Job | Model | Notes |
|-----|-------|-------|
| Empty / unspecified / file / Drive / inventory / copy / research compile / repo | `composer-2.5` (`fast=false`) | Hands default. Never Fast |
| Tiny only (one artifact, mechanical transform: rename, format, JSON fix, short classify) | `gemini-3.7-flash` | Ticket must **name** Flash. Empty ticket must NOT fill Flash |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |
| Private residency (must not leave 127.0.0.1) | local Ollama `LFM2.5-VL-3B` | If it does not fit 3B, HOLD Gideon. Do not fill Flash |

Never silently use Sonnet, Haiku, Opus, Grok, Composer Fast, or second cloud Kimi on Cloud Hands.

## 6. Workbench exception

**Calendar** Workbench (this Desk only): create/move events when Hands cannot. HITL before create/move.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.


HITL before any Calendar create, move, or external invite send.

