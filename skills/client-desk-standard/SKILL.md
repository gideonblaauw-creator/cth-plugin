---
name: client-desk-standard
description: >
  Parameterized playbook for low-volume client desks without a bespoke *-comms skill.
  Use when a client desk needs stakeholder lookup, HITL gates, Hands tickets, logging,
  and Archive paths under /opt/claude-files/Clients/.
metadata:
  version: "1.0.0"
  category: operations
  desk: client desk (parameterized)
---

# Client desk standard

Use for active client desks that lack a dedicated `<client>-comms` skill. Bind this skill plus `desks-workbenches-hands-tickets`. High-volume retainers keep bespoke comms (`teclogi-comms`, `sustenttia-comms`, `rein-hubs-comms`, etc.).

Set parameters at session start:

- `{Client}` — display name (example: GIZ, PASO Colombia)  
- `{client_slug}` — Archive folder slug (example: `GIZ`, `PASO-Colombia`)  
- `{language}` — client thread language (often Spanish)  
- `{reports_to}` — owning internal desk if not Orchestrator

## Stakeholder context lookup

Before drafting or ticketing, gather context from Tools (not parallel chats):

| Tool | Use |
| --- | --- |
| Gmail | Thread history via Gmail · Workbench or Inbox desk ticket |
| Google Drive | Client packs and shared decks |
| Monday | Board items and status columns when client uses Monday |
| Granola | Meeting decisions and action items |
| Memory / Notion | Prior commitments; cite links |

Do not copy secrets into tickets. Ticket Hands with file paths and connector scopes only.

## HITL gates

- Draft cards only for email, social, invoices, and contracts.  
- Never **send**, **post**, **pay**, or **sign** without Gideon yes.  
- Never merge PRs or deploy client apps from the desk chat.

**GO / NO GO:** Use inline widget buttons per `HARNESS.md` § GO / NO GO decisions (PR #169). One decision per widget. Prose-only approval is a protocol miss.

## Hands ticketing

Follow `skills/desks-workbenches-hands-tickets/SKILL.md`:

- Plan first with ASD-STE100 fields.  
- Ticket all file, research, code, copy, HTML/PDF craft to Cursor Cloud Hands.  
- Model: `composer-2.5`, `model_params`: `fast: false` (Gideon lock 17 Nov 2026).  
- Lane A for `cth-plugin` and owning repos; Lane B `{type: machine, name: vps}` for Archive packs.  
- Report bc-ids and paths to Orchestrator. Maker ≠ checker.

## Logging conventions

| Channel | Log |
| --- | --- |
| Email | Gmail labels + Archive export under client folder |
| Monday | Item updates with `CTH-` prefix in update body |
| Slack CTH_OPS | Failures and HITL via `CTH-OPS · Core · notify-ops` when wired |
| Vault / Drive | `{Client}` shared folder; versioned filenames `YYYY-MM-DD-<topic>` |

## Archive path

Source of truth on VPS:

`/opt/claude-files/Clients/<Client>/`

Structure (create as needed):

- `comms/` — drafts and sent exports (HITL before send)  
- `meetings/` — Granola exports and notes  
- `deliverables/` — Hands output paths  
- `admin/` — contracts and invoices **no secrets in git**

Never keep client payloads only in chat.

## Tone

Match `{language}` of the live client thread. Gideon ↔ desk stays English unless the desk is Spanish-only. Lead with benefit and impact. Metric units. Oxford comma.

## Escalation

Escalate blockers that delay client deliverables to Gideon immediately (12 Oct rule). Ping Orchestrator when more than ~8 live Hands jobs queue on one desk.