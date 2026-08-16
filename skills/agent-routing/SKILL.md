---
name: agent-routing
description: >
  Decide whether a task stays with the Grok Bot fleet (SpaceXAI's always-on
  teammate product — a Chief-of-Staff Bot on top routing to specialist
  Bots on a shared persistent cloud computer) or gets mirrored to a Cursor
  IDE background agent running Sonnet for cheap, high-volume daily
  execution. Trigger on "which bot should handle this", "route this task",
  "save Grok Bot quota/usage", "run this in Cursor instead", "mirror this
  bot to Cursor", "daily tasks vs high thinking", "efficient model for
  routine work", or whenever Grok Bot's weekly usage is running low.
metadata:
  version: "2.0.0"
  category: orchestration
---

# Agent Routing: Grok Bot fleet ⇄ Cursor/Sonnet

## What Grok Bot actually is (don't confuse this with Claude Cowork)

Grok Bot is SpaceXAI's product for persistent, named "teammate" agents,
sold through Cursor Ultra / Cursor Teams Premium / SuperGrok Heavy and tied
to the same Cursor account used to open this repo. Key mechanics that drive
this routing policy:

- **All Bots on an account share one persistent cloud computer** (browser,
  filesystem, terminal). That's what lets a Bot sign into apps and
  websites with no clean API — but every Bot on that computer draws from
  the same account's weekly AI token allowance.
- **A Bot is just a name + job + description**, not a different model.
  Grok Bot does not expose per-Bot model choice — every Bot on the roster
  runs on the same underlying (Grok) capacity, so a trivial "check Buffer
  for failed posts" Bot costs the same pool of tokens as a "decide our
  grant go/no-go" Bot.
- **Bots route to each other by description-matching**, typically through
  one Bot whose job is explicitly to triage and hand off (the "Chief of
  Staff sits on top, with a specialist for each lane" pattern SpaceXAI
  itself uses internally). That triage/routing Bot is the "Grok Bot
  orchestrator" this skill refers to.
- **Skills and routines are native Grok Bot concepts too** — a skill is a
  reusable instruction set (installed via Settings → Plugins, or pasted
  in), a routine is a schedule/event trigger for a skill. This is why the
  21 `SKILL.md` files in this repo map cleanly onto a Grok Bot roster: the
  user mirrored this repo's skill catalog into named Bots (Buffer, Canva,
  Doctor_Bot, Grant, Proposal, SEO, Campaign, etc.) roughly a week ago.

## Why the quota drains fast

Every Bot in the fleet — no matter how mechanical its job — spends from the
**same shared, capped weekly allowance**. There is no cheap tier inside
Grok Bot itself. The only way to stop burning quota on routine work is to
move that work to a *different* execution surface that has its own,
separate model choice: **Cursor's IDE background/cloud agents**, where the
model is explicitly selectable (e.g. Sonnet) per agent and isn't drawn from
Grok Bot's allowance at all.

## The two-axis routing rule

Classify every task on **two axes** before deciding where it runs:

**Axis 1 — Judgment.** Is this ambiguous, high-stakes, or a genuine
decision, or is it well-scoped and repeatable?

**Axis 2 — Tool access.** Can the task be done through an MCP connector or
API this repo already has wired up (`.mcp.json`: Slack, Google Drive,
Gmail, Google Calendar, Canva, Buffer, Monday, Miro, Notion — plus
Shell/API access to BookStack, and local Playwright for HTML→PDF), or does
it need Grok Bot's unique **persistent-computer / browser computer-use**
because the target has no API (e.g. a dashboard UI, Google Search
Console/Ads UI, an internal tool)?

| | MCP/API available (Cursor can do it) | No API — needs computer-use |
|---|---|---|
| **Routine, well-scoped** | **Move to Cursor + Sonnet.** This is the whole point of the migration. | Stays on Grok Bot (no substitute exists), but keep it narrow and routine-scheduled, not ad hoc, to limit token burn. |
| **Judgment / ambiguous / high-stakes** | Stays on the Grok Bot orchestrator for the decision; only the resulting execution moves to Cursor. | Stays on Grok Bot end-to-end. |

### Hard boundary — never move this

`skills/secrets` never moves to Cursor and is never mirrored into
`.cursor/skills/`, regardless of either axis — per `AGENTS.md` and
`.cursor/rules/cleantechhub.mdc`. Keep it exclusively on the Grok Bot
fleet / VPS side.

### The Approval Gate still applies

Public-voice content (social posts, newsletter copy, website text,
external comms) is marked "Awaiting Gideon's approval" before publishing —
regardless of whether the Grok Bot fleet or a Cursor/Sonnet agent produced
the draft.

## Per-skill verdict

See `references/wire-diagram.md` for the full 21-skill table with both
axes scored. Summary:

- **Full mirror to Cursor + Sonnet** (routine + MCP/API-covered):
  `doctor-bot`, `buffer`, `canva`, `notion`, `monday`, `google-drive`,
  `slack`, `miro`, `bookstack`, `html-to-pdf`, `nexus-onepager` (build
  step), `composio` (once target is decided), `live-artifact-build`
  (rebuilt as a repo-hosted dashboard file instead of a Cowork-sidebar
  artifact).
- **Hybrid — decision on Grok Bot, execution on Cursor**: `cth-grant`,
  `cth-proposal-build`, `social-media-campaign`, `cleantechhub-brand`,
  `clp26-brand`.
- **Stays on Grok Bot** (needs computer-use with no API, e.g. Google
  Search Console/Ads dashboards): the UI-dependent parts of `cth-seo`.
- **Never mirrored**: `secrets`.

## Handoff protocol (no new infrastructure, no new host)

1. **Phase 1 — manual (ship today).** The Grok Bot orchestrator's reply
   ends with an explicit routing line, e.g. `→ Cursor/Sonnet: run buffer
   with <context>`. Gideon opens this repo in Cursor and starts a
   background agent with that line as the task — it inherits the matching
   skill automatically via `.cursor/skills/<name>/SKILL.md` →
   `skills/<name>/SKILL.md`.
2. **Phase 2 — GitHub as the shared queue.** Both products already
   integrate with GitHub natively, so use that instead of standing up new
   infrastructure: the Grok Bot orchestrator opens a GitHub issue on this
   repo (`skill: buffer`, context, priority). A Cursor background agent
   picks up the issue, executes with Sonnet, comments the result, and
   closes it. Grok Bot's own docs confirm routines can be triggered "from
   an event, such as a Slack message or a GitHub notification" — the same
   channel works in reverse as a handoff target.
3. **Phase 3 — optional tightening.** Only after Phase 2 has run cleanly
   for a week: add a routine on the Grok Bot orchestrator that
   auto-drafts the GitHub issue the moment it classifies a task as
   "routine + MCP-covered," instead of waiting for the reply-line prompt
   in Phase 1.

## Model settings in Cursor

- Default every mirrored bot's Cursor agent to **Sonnet**. Don't reach for
  a high-reasoning/"thinking" tier for routine execution — that just
  relocates the cost problem.
- If a Cursor/Sonnet agent hits genuine ambiguity mid-task, stop and hand
  it back to the Grok Bot orchestrator rather than escalating Cursor's own
  model tier.

## Monitoring

Extend Doctor_Bot (see `skills/doctor-bot/SKILL.md` → "Extending
Doctor_Bot") with a usage-tracking check:

- New check: `check_grok_bot_quota.py` — logs the Grok Bot fleet's weekly
  token usage (pull from account settings if exposed; log manually each
  day if not).
- Thresholds: **AMBER** at 70% of weekly quota used with 3+ days left in
  the week; **RED** at 90% used at any point.
- On AMBER/RED, audit the last day of Grok Bot activity for any Bot that
  ran a task matching the "routine + MCP/API available" cell above — that
  task should have been routed to Cursor instead.

## Rollout order

Start with the lowest-risk, highest-frequency, fully-MCP-covered bots so
you can validate the GitHub handoff before trusting it with anything
client-facing:

1. `doctor-bot` — already read-only and non-destructive by design.
2. `buffer` + `canva` — mechanical, template-driven.
3. `notion` + `monday` — CRUD, low blast radius.
4. `bookstack`, `gmail`, `google-drive`, `slack`, `miro`, `html-to-pdf`,
   `live-artifact-build`, `composio`.
5. The execution half of hybrid programs (`social-media-campaign`,
   `cth-grant`, `cth-proposal-build`, `cleantechhub-brand`, `clp26-brand`)
   — only after the Grok Bot orchestrator has made the strategic call for
   that specific task.
