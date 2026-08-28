---
name: embassy-albert-kobus-comms
description: >
  Communications protocol for the Embassy · Albert Kobus Desk. Trigger on Embassy Desk comms with Albert Kobus.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "Embassy · Albert Kobus"
  owner: Infrastructure desk c656afb9
---

# Embassy · Albert Kobus — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End client:** **Albert Kobus** (Embassy Desk named contact). Institution: **[PENDIENTE]** (embassy / mission name not planted in repo).
- **Who hears what:** Diplomatic-facing → language of live thread (**English** / **Dutch** / **Spanish** as used). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).

## 2. Brand skill to follow

`cleantechhub-brand` for CTH institutional voice unless embassy co-branding is explicit.

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
- **Lane A repo / store for this Desk:** Archive per ticket.
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

No standing Workbench. WhatsApp via Orchestrator when needed.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.



