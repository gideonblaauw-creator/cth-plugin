---
name: infrastructure-comms
description: >
  Communications protocol for the Infrastructure Desk. Trigger on Infrastructure Desk comms, harness tickets, or stack coordination.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "Infrastructure"
  owner: Infrastructure desk c656afb9
---

# Infrastructure — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End clients:** Internal CTH stack operators and vendors. Named vendor contacts: **[PENDIENTE]** per ticket.
- **Who hears what:** Internal ops → **English**. Gideon ↔ Desk → **English**.
- **Internal:** Gideon Blaauw (HITL). Owner profile: Infrastructure desk **c656afb9**. Read `skills/app-build/SKILL.md` and `skills/doctor-bot/SKILL.md`.

## 2. Brand skill to follow

`cleantechhub-brand` only for outward-facing infra comms; internal runbooks need no brand skill.

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
- **Lane A repo / store for this Desk:** `https://github.com/gideonblaauw-creator/cth-plugin` for harness/skills.
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

No standing Workbench. Infrastructure tickets Hands — does not SSH-inventory itself.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.


Gideon merges and deploys. Hands does not deploy.

## 8. Secrets (Infisical SoT — Gideon 2026-09-07)

Service API keys and tokens → **Infisical** only (`skills/secrets/SKILL.md`, `skills/infisical/SKILL.md`). Harness hard gate: `skills/harness/SKILL.md` §5 **Secrets SoT**.

- Ticket Hands with **project / environment / key name** — never paste token values in tickets, PRs, or chat.
- Prefer **machine identity** for VPS/Hands workers.
- VPS `.env` = runtime cache regenerable from Infisical — not SoT.

**Migration gaps (HITL — document; do not delete live secrets without Gideon):** Grok box-secrets; Orch connector-secrets (e.g. OpenRouter); Lovable env (e.g. Beehiiv); VPS leftover `infisical-creds` / OPENROUTER env files. See `skills/secrets/SKILL.md` § Migration gaps.

**Carve-out:** Obsidian vault = narrative notes only — no API keys/tokens in Obsidian.
