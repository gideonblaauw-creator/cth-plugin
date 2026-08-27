---
name: cth-grants-comms
description: >
  Communications protocol for the CTH Grants Desk. Trigger on CTH Grants Desk comms, donor messages, or grant coordination.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "CTH Grants"
  owner: Infrastructure desk c656afb9
---

# CTH Grants — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End clients / funders:** UNDP, P4G, GIZ, Climate KIC, Expertise France, BID/IDB, and other funders in `skills/cth-grant/SKILL.md`. Named funder contacts: **[PENDIENTE]** per live grant.
- **Who hears what:** Donor-facing follows funder thread language. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Isolated live drafts (CTCN Suriname, GRP, TNS VerdeXcelerate) have their own comms skills.

## 2. Brand skill to follow

`cleantechhub-brand` for CTH institutional voice. Read `skills/cth-grant/SKILL.md` for grant copy rules.

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
- **Lane A repo / store for this Desk:** Grant packs → Lane B Drive (not `cth-plugin`). Specs/harness → `cth-plugin`.
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.

## 5. Lowest-tier model

| Job | Model | Notes |
|-----|-------|-------|
| Mechanical copy, file packs, inventories, research grind | `gemini-3.7-flash` | Empty mechanical model → Flash |
| Repo / code Hands | `composer-2.5` (`fast=false`) | Never Fast |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |

Never silently use Sonnet, Haiku, Opus, Grok, or Composer Fast on Cloud Hands.

## 6. Workbench exception

Gmail/Calendar via **Inbox** and **Meetings** Desks; this Desk coordinates only.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.


Two live grant drafts max. Nothing submitted without Gideon yes (N8).

