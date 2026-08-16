---
name: harness
description: >
  Blaauw Harness v3 rulebook — five-term operating model for Gideon Blaauw's
  AI stack. Trigger on "harness", "ticket", "Cloud Hands", "Orchestrator",
  "Workbench", "Desk", "take a ticket", "lane", or references to the
  Blaauw Harness. Also trigger when a Cloud Hands agent starts any task so it
  reads these rules before executing.
metadata:
  version: "3.0.0"
  category: operations
  adopted: "2026-08-16"
---

# Blaauw Harness v3

**Owner:** Gideon Blaauw
**Date:** 2026-08-16
**Status:** adopted; cth-plugin source of truth

This file is the rulebook. Orchestrator routes. Desks ticket. Workbench talks to people. Cloud Hands writes files. Tools are not chats.

---

## 1. Why v3

Grok Bot is the expensive brain. About 70 % of work can run on cheaper Cursor models or scripts. Gideon talks to Orchestrator and Desks, not every social channel. Socials is a Desk. LinkedIn / Instagram / Facebook / Ads sit under it.

---

## 2. Five terms

### i) Workbench

Owns one outside channel. Reports to a Desk except WhatsApp (reports to Orchestrator). HITL before send / post / event / Ads spend.

Current assignments:

| Workbench | Channel | Reports to |
|-----------|---------|------------|
| WhatsApp | WhatsApp | Orchestrator |
| LinkedIn | LinkedIn | Socials Desk |
| Instagram | Instagram | Socials Desk |
| Facebook | Facebook | Socials Desk |
| Google Ads | Google Ads | Socials Desk |
| Gmail | Gmail | Inbox Desk |
| Calendar | Calendar | Meetings Desk |

Not a Workbench: Drive, GitHub, Buffer, Monday, Airtable, Notion, OpenCode.

### ii) Tools

Not a chat. Box (browser/QR), Composio, Drive (share only; Archive is source of truth), Buffer, gh, rsync, 10 pm dump, 2 am claude_sync.sh.

### iii) Tickets

The contract, not a bot. See `tickets/TEMPLATE.md` for fields. Required fields: `desk`, `folder`, `done-when`, `lane`, `hitl`, `reviewer`, `context`.

Lanes:

| Lane | When to use |
|------|-------------|
| `sonnet` | Default Cloud Hands work (Cursor Sonnet 4.6) |
| `haiku` | Mechanical / high-volume tasks |
| `flash` | Fast cheap tasks (Gemini Flash) |
| `opencode` | When Gideon explicitly says OSS (Kimi via OpenCode) |

### iv) Cloud Hands

Writes files. GitHub PRs on connected repos. Archive writes need a Cursor worker on the VPS.

Rules for Cloud Hands:

- Read this skill before executing any ticket.
- Use `sonnet` lane by default unless the ticket specifies otherwise.
- Open a GitHub PR; never merge without HITL approval.
- Do not clone `/opt/claude-files` onto the VM.
- Do not require the Mac (`~/Documents/Claude/` is an optional mirror, not a layer).
- Do not embed bot UUIDs or internal orchestrator identifiers in the repo.
- Images / Video / Presentations / Researcher / Scraper tasks are Hands tickets.
- Max two live grant drafts at a time.

### v) Desks

Own a subject. Ticket + review. No login. No first-draft grind on the expensive model.

Current Desks: Socials, Inbox, Meetings, Grant, Proposal, SEO, Infra.

---

## 3. Stores

| Store | Path | Role |
|-------|------|------|
| Archive | `/opt/claude-files/` on OVH VPS | Source of truth |
| Repos | GitHub | Code and skills source of truth |
| Mac Claude tree | `~/Documents/Claude/` | Optional mirror — not a layer |

---

## 4. Collaboration flow

```
Gideon → Orchestrator/Desk → ticket → Workbench (people) or Hands (files)
                                     → Desk reviews → HITL if outbound
```

---

## 5. Gates

- No VPS Cursor worker yet — do not attempt direct Archive writes from this repo.
- Do not require the Mac.
- Do not fan out — sequential over parallel.
- Max two live grant drafts.
- REIN HOLD until after 17 Aug Lucio call — do not cite REIN Hubs dollar amounts.
