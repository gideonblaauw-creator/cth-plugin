---
name: harness
description: >
  Blaauw Harness v3 rulebook — five-term operating model (Workbench, Tools,
  Tickets, Cloud Hands, Desks) for Gideon Blaauw's AI stack. Trigger on
  "harness", "ticket", "Cloud Hands", "Workbench", "Desk", "take a ticket",
  "lane", or any Blaauw Harness reference. Also trigger at the start of any
  Cloud Hands task so the agent reads these rules before executing.
metadata:
  version: "3.0.0"
  category: operations
  adopted: "2026-08-16"
---

# Blaauw Harness v3

**Owner:** Gideon Blaauw
**Date:** 2026-08-16
**Status:** adopted in Grok Bot; `cth-plugin` update via Cloud Hands
**Source of truth:** VPS Archive `/opt/claude-files/` and GitHub Repos. The Mac `~/Documents/Claude/` tree is a leftover mirror, not a layer.

This file is the rulebook. Orchestrator routes. Desks ticket. Workbench talks to people. Cloud Hands writes files. Tools are not chats.

## 1. Why v3

Grok Bot is the expensive brain. It was also doing the grind (inventories, docx, HTML, dumps). That burns Ultra. About 70% of the 13–15 Aug week can run on cheaper Cursor models or scripts. v3 makes that the default.

Gideon talks to Orchestrator and to Desks. He does not talk to every social channel. Socials is a Desk. LinkedIn / Instagram / Facebook / Ads sit under it.

## 2. Five terms

### i) Workbench
A **Workbench** owns one outside channel. It has the login. It pulls and it draft-sends. It reports to a Desk, not to Gideon, except WhatsApp (cross-desk, reports to Orchestrator). HITL before any send, post, event create, or Ads spend.

Current Workbench:
- WhatsApp → Orchestrator (device cap: max 2 boxes besides Mac and phone)
- LinkedIn, Instagram, Facebook, Google Ads → Socials Desk
- Gmail → Inbox Desk
- Calendar → Meetings Desk

Not a Workbench: Drive, GitHub, Buffer, Monday, Airtable, Notion, OpenCode.

### ii) Tools
A **Tool** is not a chat. Hands, Workbench, or a script call it.

- Box (Grok Bot computer): browser, QR, WhatsApp Web
- Composio connectors
- Drive (fetch / export / share). Archive stays source of truth
- Buffer, `gh`, rsync, 10pm session dump, 2am `claude_sync.sh`
- Monday, Airtable, Notion until a Desk is drowning in that UI
- GitHub is a Tool (`gh` / Cloud Hands PRs), not a chat

Drive, GitHub, Buffer, Monday, Airtable, Notion stay Tools. No extra chats.

### iii) Tickets
A **Ticket** is the contract, not a bot. Desk or Orchestrator writes it. Cloud Hands executes it.

Required fields:
- `desk:` who owns the subject (free-form Desk name; no enum)
- `folder:` Archive path under `/opt/claude-files/Projects/…` and/or repo
- `done-when:` one sentence
- `lane:` `sonnet` | `haiku` | `flash` | `opencode`
- `hitl:` what must not go out
- `reviewer:` which Desk reviews

See `tickets/TEMPLATE.md`.

### iv) Cloud Hands
**Cloud Hands** writes files. Not a Desk. Not a Workbench. Gideon does not DM Hands for strategy.

Lanes:
- Cursor Sonnet 4.6 — default file work
- Cursor Haiku 4.5 or Gemini Flash — mechanical maps, dumps, lists
- OpenCode Kimi (`opencode-go/kimi-k2.7-code`) — when Gideon says OSS

OpenCode is a Hands lane, not a Workbench, not a Desk, not a chat.

Cursor cloud agents on a GitHub repo (PRs). Archive writes need a Cursor worker on the VPS. Do not clone the Claude tree onto the Grok Bot computer or treat the Air as source of truth.

Images, Video, Presentations, Researcher, Scraper are Hands tickets (or a live Box pull), not extra Desks.

### v) Desks
A **Desk** owns a subject. It reports to Orchestrator. It writes tickets and reviews output. It has no login. It does not grind the first draft on the expensive model.

Gideon may open a Desk chat. Workbench chats under Socials should stay out of his daily sidebar.

## 3. Talking layers and stores

| Layer | Role | Gideon opens it? |
|---|---|---|
| Orchestrator | Route, HITL, high strategy, browser judgment | Yes |
| Desks | Subject, ticket, review | Yes |
| Workbench | Channel I/O | Only WhatsApp and, if needed, Gmail/Calendar |
| Cloud Hands | Write the file | No — ticket only |
| Tools | Invoked, not staffed | No |
| Archive | VPS `/opt/claude-files/` | Via Cursor / SSH |
| Repos | GitHub | Via Cloud Hands PR |

Box is a Tool used by Workbench. It is not a layer Gideon names.

## 4. Org

### Orchestrator
Routes. Does not draft grants, decks, or posts. Picks Desk, Workbench, or Hands lane. HITL before send/post/pay.

### Desks that exist
Grants (plus isolated live drafts: CTCN Suriname, GRP, TNS VerdeXcelerate — max two live drafts), Proposals, Meetings, Inbox, Socials (was CTH Social Media), Strategy, GTM, Energy Coop, Mubon, Sustenttia, AIC, AURA, Teclogi, Embassy, REIN Hubs, Almendra.

### Desks to stand up when a ticket hits (Claude folders already exist)
Budget (`CTH - 2026 Budget`), Academy/CLP (`CTH - Academy`, `CTH - CLP 2026`), Origo/Data (`CTH - Climate_Data_Platform`, Nexus, WIKI), Investor Matching, Newsletter (`CTH Newsletter System`), Ruta Verde, Apps, Bosque Soberano, Run Up parent, Infrastructure (`Claude Infrastructure`, Chief of Staff).

### Workbench map
| Workbench | Reports to | HITL |
|---|---|---|
| WhatsApp | Orchestrator | send / reply |
| Gmail | Inbox | send |
| Calendar | Meetings | create / move |
| LinkedIn | Socials | post / DM |
| Instagram | Socials | post |
| Facebook | Socials | post |
| Google Ads | Socials | spend / launch / pause |

Shared by every Desk: WhatsApp, Gmail, Calendar. Drive is a Tool.

## 5. Collaboration

1. Gideon asks Orchestrator (or a Desk).
2. Desk writes a Ticket.
3. People-channel → Workbench → Box → HITL if outbound.
4. Write-a-file → Cloud Hands (lane) → Archive or Repo → Desk reviews → Orchestrator ready-ping.
5. Nothing sent, posted, or paid without Gideon's yes in the owning chat.

OpenCode is a Hands lane, not a Desk.

## 6. File structure

Do not invent a new tree.

- Archive: `/opt/claude-files/Projects/<Claude project name>/`
- Sessions: `/opt/claude-files/sessions/YYYY-MM-DD/`
- Repos: GitHub as already connected (including `cth-plugin`)
- Mac `~/Documents/Claude/` is optional mirror only
- Plugin rulebook: this harness as `skills/harness` in `cth-plugin`, plus `tickets/TEMPLATE.md`
- Repo `HARNESS.md` is Cowork/CLI/Cursor setup docs, not this rulebook

## 7. What stays expensive vs cheap

Stay on Orchestrator / Box: route, HITL, QR, logged-in browser, GO/NO-GO, tone, REIN HOLD, send.

Cloud Hands or script: inventories, folder maps, docx/HTML/SVG drafts, Lucio-style guides, session dumps, disk sweep, 2am sync.

About 70% of 13–15 Aug work is Hands/script.

## 8. Gates and blockers

1. **VPS Cursor worker** — not installed. Hands can PR to GitHub today. Hands cannot write Archive in place until a worker runs on the VPS.
2. **`gh` on Grok Bot computer** — not logged in. Cloud Hands launch uses Gideon's Cursor GitHub connection instead.
3. **Mac / Grok Bot desktop** — often asleep at 10pm and 2am. Session dump and `claude_sync` wait. Do not treat Mac as required for Hands.
4. **WhatsApp QR** — session drops. Device cap still 2 extra boxes.
5. **Gmail / Calendar Workbench** — Composio toolkits exist; bots must use them. Do not open extra Google sessions on Box if Composio is enough.
6. **Drive** — Tool only. Do not spin a Drive chat.
7. **Two live grant drafts** — still the cap.
8. **REIN HOLD** — no outbound to REIN/Pvblic until after Monday 17 Aug Lucio.
9. **Do not fan out** profile rules to every bot. Put the rule in the profile once.
10. **Do not hide** Isolated grant draft chats. Do hide Socials Workbench from Gideon's daily sidebar so he talks to Socials.

## 9. First tickets Cloud Hands should accept

- Add this file as `skills/harness/SKILL.md` (or the repo's existing skill layout)
- Add `tickets/TEMPLATE.md`
- Point `CLAUDE.md` / plugin readme at the harness
- Do not embed Grok Bot UUIDs
- Do not clone Archive onto a cloud VM

## 10. Ticket template (copy)

```
desk:
folder:
done-when:
lane: sonnet | haiku | flash | opencode
hitl: nothing sent/posted/paid
reviewer:
context:
```
