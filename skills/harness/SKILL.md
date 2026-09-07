---
name: harness
description: >
  CTH Harness rulebook — Workbench, Tools, Tickets, Cloud Hands, Desks. Use when:
  harness, ticket, Cloud Hands, lane, Desk/Hands boundary. Read before any Cloud
  Hands ticket.
license: MIT
metadata:
  version: "3.2.0"
  category: infrastructure
  adopted: "2026-08-16"
---

# CTH Harness

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
- `model:` `gemini-3.7-flash` | `composer-2.5` (`fast=false`) — Cloud Hands only (Token lock 2026-08-26)
- `lane:` `github-pr` | `drive-folder` — store lane (Lane A vs Lane B)
- `hitl:` what must not go out
- `reviewer:` which Desk reviews

See `tickets/TEMPLATE.md`.

### iv) Cloud Hands
**Cloud Hands** writes files. Not a Desk. Not a Workbench. Gideon does not DM Hands for strategy.

Cloud Hands model lanes (Cursor cloud agents — **Token lock 2026-08-26**):
- `gemini-3.7-flash` — mechanical copy, file packs, inventories, research grind, unspecified mechanical
- `composer-2.5` (`fast=false`) — repo / code Hands

That is the whole Cloud Hands model list. Anything more advanced (Sonnet, Opus, Haiku as Hands, etc.) → HOLD and flag Gideon. Do not silently fill.

OpenCode Go (`opencode-go/kimi-k2.7-code`) is an OSS coding path named in OSS-first (2026-08-20). It is not a Cloud Hands model fill-in under the 26 Aug token lock. Never launch Kimi as a second cloud agent.

OpenCode is a Hands path, not a Workbench, not a Desk, not a chat.

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

### Operating protocol — Desk / Hands boundary (hard gate)

Desks ticket Cursor Cloud Hands workers. Desks review and escalate. They do not first-draft file packs, inventory-grind, or write code. Researcher/Scraper file writes are Hands tickets. Drive packs use Drive MCP/Tool, not a GitHub repo unless Gideon marked a repo row.

### Hands-shift lock — Gideon 2026-08-17 (hard gate)

**1. Any first-draft file pack (md, html, docx, png, csv, svg, xlsx) = a seven-field ticket to Cursor Cloud Hands.** No bc-id = miss. Desk reviews only. Desks do not write file packs themselves.

**2. Two stores, three lanes.**
- Lane A — GitHub PR: code, skills, harness, repo-tracked assets.
- Lane B — Drive folder: grant packs, client packs (official Drive MCP → Composio Drive → VPS `gws`, in that order; all via Hands, all must return a bc-id).
- Box: scratch only.
- Archive (`/opt/claude-files`): only via a VPS Cursor worker. mac-scan is not a jump host.
- All Drive writes (official MCP, Composio, VPS `gws`) go through Hands and must return a bc-id. Desks do not write Drive.

Drive MCP fallback order (Hands only):
1. **Official Google Drive MCP** — attempt first; still often needsAuth / cursor:// OAuth bug.
2. **Composio Drive** — only if connector available on the Hands worker.
3. **`gws` on the VPS** (`/home/debian/.local/bin/gws`, account `gideon.blaauw@cleantechhub.net`) — only if a Cursor worker exists on the VPS. mac-scan is not a jump host. Default cloud VM must not SSH-grind the VPS.

**3. Mechanical jobs** (session dump, 2am VPS push, Friday Mac hygiene, SECOP scrape) = Hands ticket or a Cloud Agent Automation. Not a Desk task.

**4. Researcher / Scraper / Infra inventories = Hands tickets (Haiku/Flash lane).** Desk tickets and reviews. Desk does not run the scrape or inventory itself.

**5. Stay on desks (never below ~30% of work):** Orchestrator routing, go/no-go, HITL send/post/pay, channel I/O, PR review, merge, credentials, two-draft cap, REIN HOLD. Desks own these; Hands does not touch them.

**Do not:** launch a second Sustenttia instance; use mac-scan as a jump host; move HITL off desks; invent new nodes or repos; open Grant Graph or TNS packs until gates A–C clear (Drive MCP auth, VPS Archive worker, Cloud Agent healthy).

### Lane A repo lock — Gideon 2026-08-19 (hard gate)

Desks cannot ticket Cloud Hands on the wrong GitHub repo. Lane A = GitHub PR on the **owning** repo. Match `repo_url` to the subject before launch. Wrong repo = miss. Do not launch.

| Subject | Lane A `repo_url` |
|---|---|
| Teclogi / dataroom scanner **ONLY** | `https://github.com/gideonblaauw-creator/cth-data-room-scanner` |
| AIC / Bravo Bridge / Americas Innovation Council | `https://github.com/gideonblaauw-creator/americas-innovation-hub` (private, already exists) |
| Almendra / Run Up coffee / house of brands | `https://github.com/gideonblaauw-creator/almendra` (private, just created) |
| CTH harness / Grant Graph / plugin rulebook | `https://github.com/gideonblaauw-creator/cth-plugin` |

**`cth-data-room-scanner` is Teclogi-only.** Never launch AIC splash/Lovable work on it. Never launch Almendra QBO / file-pack work on it.

In-flight Teclogi remirror `bc-ddf632e2` stays on `cth-data-room-scanner`. Do not move it.

If AIC work needs Archive or VPS `gws`, also pass environment `{type: machine, name: vps}`.

Lane B Drive packs still Drive (Hands writes, bc-id required). Empty bc-id = miss. Box = scratch. Archive only via worker `vps`. mac-scan is not a jump host.

### Token lock — Gideon 2026-08-26 (hard gate; supersedes Sonnet-default, Haiku-default, review-auto-Sonnet for Cloud Hands)

**Grok Bot is coordination only.** No craft, first-draft, long research, or file grind in Grok chats. Route, HITL, go/no-go, browser judgment, channel I/O escalation.

**File / research / code / copy → Cloud Hands.** Desk tickets. Desk reviews (maker ≠ checker). Grok does not write the pack.

**Allowed Cloud Hands models (whole list):**
| Job | Model id | Notes |
|---|---|---|
| Mechanical copy, file packs, inventories, research grind, unspecified mechanical | `gemini-3.7-flash` | Empty mechanical model still fills here |
| Repo / code Hands | `composer-2.5` (`fast=false`) | Never Fast |

**Anything more advanced** (Sonnet, Opus, Haiku as Hands, Fable, Sol, Grok, Composer Fast, second cloud Kimi) → **HOLD and flag Gideon.** Do not silently fill Sonnet, Haiku, Auto, Grok, or Kimi-cloud.

**Forbidden on Cloud Hands** (remap or hold; miss if used on pack writes): Grok, Grok Fast, Composer Fast, Opus, Fable, Sol, second cloud Kimi, Muse Spark 1.2 Contributor.

**Review / eval / brand** with no model → **HOLD and flag Gideon.** Do not auto-fill Sonnet. (Supersedes review-auto-Sonnet from 19 Aug.)

**Repo / code** with no model → `composer-2.5` (`fast=false`). Do not silent-fill OpenCode or Sonnet.

**Private residency** (must not leave 127.0.0.1) → local Ollama `LFM2.5-VL-3B` only. If it does not fit 3B, hold for Gideon. Private overrides Flash.

Machine-readable skill inventory: `skills/harness/references/skill-toolkit.json` (canonical + Cursor stub paths, skip list).

Do not weaken Lane A repo lock, Hands-shift lock, Tools-session lock, media-generation routing, or tiny/private axes from 19–21 Aug. Do not expand OSS/OpenCode Go beyond what OSS-first (20 Aug) already names.

### Model routing — Gideon 2026-08-19 (hard gate; $ table and usage scrape — historical)

**Cloud Hands model fill-in** is governed by Token lock 2026-08-26 above. Table rows below that name Sonnet, Haiku, or Auto as Hands defaults are superseded for fill-in.

Cursor usage is not efficient unless the Desk names the model on the Hands ticket. Empty model on a mechanical job = `gemini-3.7-flash`. One complete Hands ticket, no second pass for the same artifact.

Historical note (19 Aug): Ultra pools and never-list context below. Do not spend Opus, Grok 4.6, or GPT 5.6 Sol on pack writes. Do not run a second Kimi as a cloud agent.

**Sourced — two Ultra pools** (`https://cursor.com/docs/models-and-pricing`, 19 Aug 2026):
- **Cursor Models** = Grok 4.6 / Grok 4.5 / Composer 2.5 (generous included)
- **Other Models** = $400/mo at API rate (Ultra included Other Models usage)

Official $ are per 1M tokens (input / output) from that same page, 19 Aug 2026. Do not invent prices. Empty model on a mechanical job = `gemini-3.7-flash`.

| Job type | Model id | $ in / $ out | Notes |
|---|---|---|---|
| Mechanical Drive/Docs/Sheets/HTML copy, MD→Doc sweep, indexes, trackers, receipts lists | `claude-haiku-4-5` | $1 / $5 | Other Models. Not Sonnet. Not Opus. |
| Mechanical (same jobs) | `gemini-3.7-flash` | $0.75 / $3.50 | Other Models |
| Cheapest Flash fallback | `gemini-2.5-flash` | $0.30 / $2.50 | Other Models |
| Cheapest Flash fallback | `gemini-3-flash` | $0.50 / $3 | Other Models |
| Tiny transforms | `gpt-5.6-luna` | $0.20 / $1.20 | Other Models |
| Tiny transforms | `gpt-5.4-nano` | $0.20 / $1.25 | Other Models |
| Repo / code Hands | `composer-2.5` (`fast=false`) | $0.50 / $2.50 | Cursor Models pool. Never Fast. Cursor Hands fallback when Go is blocked (VPS CF 1010), over quota, hung, or Gideon says Hands. |
| Review / eval / brand / Grant Graph spec | `claude-sonnet-4-6` | $3 / $15 | Other Models. Keep as review default. |
| Review note only | `claude-sonnet-5` | $2 / $10 | Cheaper. Do not lock unless Gideon says. |
| Mixed / unspecified | `default` (Auto) | — | Do not invent an Auto Cost $. Official models-and-pricing does not publish one. |
| OSS | `opencode-go/kimi-k2.7-code` | — | Coding default (20 Aug). Do not launch `kimi-k2.7-code` / `kimi-k3` as a cloud agent. Never a second Kimi cloud agent. |
| Tiny (not private) | `gemini-3.7-flash` or local 3B | $0.75 / $3.50 for Flash | Job-size axis. One artifact, mechanical, no architecture, no grant/eval/brand. Empty mechanical still Flash. |
| Private (residency) | local Ollama `LFM2.5-VL-3B` | — | Must stay on 127.0.0.1. Client raw, unsigned, QBO staging, credentials, unpublished packs. If it does not fit 3B, hold for Gideon. No Cursor $. |
| Tiny + private | local Ollama `LFM2.5-VL-3B` | — | Both axes. Local 3B only. |
| Forbidden | `muse-spark-1.2-contributor` | — | Trains on prompts. Official Go privacy: model training = Yes (`https://opencode.ai/docs/go/`). Miss if used. |
| Forbidden on pack writes | `grok-4.6` | $2 / $6 | Orchestrator chat only. Not pack Hands. |
| Forbidden on pack writes | `grok-4.6` Fast | $4 / $12 | Especially never Fast on packs. Miss if used. |
| Forbidden on pack writes | `grok-4.5` Fast | $4 / $12 | Official table $4/$12 (not the help-page $18 out). Miss if used. |
| Forbidden on pack writes | `composer-2.5` Fast | $3 / $15 | Product default is Fast — Hands must set `fast=false`. Miss if used. |
| Forbidden on pack writes | any Opus | $5 / $25 | Opus 5 official rate. Miss if used. |
| Forbidden on pack writes | `claude-fable-5` | $10 / $50 | Miss if used. |
| Forbidden on pack writes | `gpt-5.6-sol` | $5 / $30 | Miss if used. |
| Forbidden unless the ticket says so | thinking=high / 1M context | — | Miss unless the ticket says so. |
| Tools (Lovable, HeyGen, WhatsApp, Vercel) | session Tool (not a model slot) | — | Launch allowed when the session exists. No-access / NEED_LOGIN / blocked auth → escalate to the Desk (HITL login), then the same Hands run (same bc-id) continues. Not a Flash fill-in. |

**MISS node — Gideon 2026-08-19 (fill-in, not a stop).** The MISS node must have a model. Desk should still name the model; Flash is the safety net, not an excuse to omit it.

- Empty model on a mechanical / unspecified Hands ticket → launch `gemini-3.7-flash` ($0.75 / $3.50). Do not refuse. Do not fall through to Sonnet or Grok.
- Ticket names a forbidden pack model (`grok-4.6` / Fast, `composer-2.5` Fast, any Opus, `claude-fable-5`, `gpt-5.6-sol`, `muse-spark-1.2-contributor`) → remap to the job’s allowed model. If job type is missing, remap to `gemini-3.7-flash`.
- Review / eval / brand with no model → HOLD and flag Gideon. Do not auto-fill Sonnet. (Token lock 2026-08-26 supersedes review-auto-Sonnet.)
- Repo / code with no model → `composer-2.5` (`fast=false`). Never Fast. Never a second Kimi cloud agent. Do not silent-fill OpenCode or Sonnet. (Token lock 2026-08-26.)
- Private residency (must not leave 127.0.0.1) → local Ollama `LFM2.5-VL-3B` only. Do not fill Flash. If it does not fit 3B, hold for Gideon.

**Tools session — Gideon 2026-08-19 (launch allowed).** Lovable, HeyGen, WhatsApp, and Vercel are Tools Hands uses. They are not a do-not-launch dead end.

- Hands may use Lovable, HeyGen, WhatsApp, Vercel when the session exists.
- If no access / NEED_LOGIN / blocked auth: do not retry in a loop. Escalate back to the Desk that wrote the ticket. Desk owns getting the session (HITL login). Then the same Hands run (same bc-id) continues.
- Do not rewrite this as “do not launch.” Launch is allowed. No-access is an escalate-to-Desk, not a miss-and-stop and not a second Hands.
- Still not a model slot. Do not fill `gemini-3.7-flash` for a missing session.

One complete Hands ticket per artifact. Two Teclogi Hands for one job (eval then remirror) is a miss unless Gideon asked for a second. Desk ping-pong / second Sketch-fix passes = miss.

**Sourced fact — billed headline.** Source: `cursor.com/dashboard/usage`, Gideon Blaauw / Ultra, 13–19 Aug 2026. Do not mix billed headline with raw event tokens.

- Total 221.2M
- Included 221.2M
- On-demand 0
- 221.2M is the dashboard weighted figure, not the sum of the log.

**Sourced fact — raw event tokens (export, different scale).** Same source. Do not add billed 221.2M to these totals. Do not invent extra numbers.

- Raw event tokens: 1,643,210,180
- Kind=Included 1,299,295,852 + Kind=Free 343,914,328

Per-model raw (7d):

| Model | Raw tokens | Share (sourced) |
|---|---|---|
| `grok-4.6-high-fast` | 1,519,836,465 | 92.5% |
| `grok-4.6-high` | 35,470,135 | 2.16% |
| `opus-5-low` | 35,085,697 | 2.14% |
| `gemini-2.5-flash` | 24,431,762 | 1.49% |
| `sonnet-4.6-medium-thinking` | 11,906,809 | 0.72% |
| `opus-5-thinking-low` | 7,250,763 | — |
| `opus-4-8-thinking-high` | 6,764,598 | — |
| `sonnet-5-thinking-high` | 993,195 | — |
| `grok-4.5-high` | 824,720 | — |
| `gpt-5.6-sol-medium` | 471,672 | — |
| `auto` | 174,364 | — |

By day UTC raw: 13=457.3M, 14=382.0M, 15=27.8M, 16=162.0M, 17=252.1M, 18=59.0M, 19=303.0M (partial, latest 20:15 UTC).

Feature: no UI group. Cloud Agent column = 228,601,182 raw; rest 1,414,608,998 undifferentiated. Chat/Tab/Composer split [PENDIENTE].

Never-list already burning: Opus 5, Opus 4.8 thinking-high, GPT-5.6 Sol. `composer-2.5-fast` and `default` appear in the chart legend but have zero export rows.

**Lock from that fact (usage context; Cloud Hands fill-in governed by Token lock 2026-08-26):**
- `grok-4.6-high-fast` is Orchestrator coordination chat, not pack Hands. Empty model on a mechanical job = `gemini-3.7-flash`. NEVER Opus / Grok 4.6 Fast / GPT-5.6 Sol on pack writes (remap; do not refuse).
- Mechanical Cloud Hands = `gemini-3.7-flash` only (Haiku/Luna/Nano in the table are historical $ context, not fill-in).
- Review/eval/brand with no model → HOLD and flag Gideon. Do not auto-fill Sonnet.
- Repo / code Cloud Hands = `composer-2.5` (`fast=false`). No second Kimi cloud agent. Never Muse Spark 1.2 Contributor.
- One Hands ticket per artifact.
- Lovable, HeyGen, WhatsApp, Vercel: Tools Hands uses when the session exists. No-access → escalate to Desk (HITL login), same bc-id continues. Not a model slot. Presenter video stays HeyGen primary. Do not invert HeyGen to fallback.

Live docs check (19 Aug 2026): ticket $ match official `models-and-pricing` for every named model. Two disagreements, live docs win where they publish $: (1) official page does **not** publish an Auto Cost dollar rate — do not invent one (a help page lists $1.25/$6; not planted). (2) official Grok 4.5 Fast is $4/$12; a help page listed $18 out — table uses official $4/$12. Composer 2.5 docs: Fast is the product default ($3/$15); Hands must set `fast=false`. Cloud Agent API List Models example uses `composer-2` + `fast` and `claude-4.6-sonnet-thinking`. This run's launch catalog includes `composer-2.5`, `composer-2.5-fast`, `cursor-grok-4.6-high-fast`, `gemini-3.7-flash-high`, `gpt-5.6-luna-high`, `default`. Ticket model ids in the table are the Hands `model` field.

### Secrets SoT — Gideon 2026-09-07 (hard gate)

**Infisical = sole durable secrets SoT** for service credentials (API keys, tokens, OAuth client secrets used by automation).

- **No durable secret storage** on VPS disk (`.env` as SoT), Mac plaintext, Grok Bot box-secrets, chat, Drive Docs, Notion, or git.
- **Hands tickets:** fetch from Infisical by **project / environment / key name** — never paste token values into prompts, PRs, tickets, or chat.
- **Prefer Infisical machine identity** for Hands/VPS workers. Do not rely on user JWTs pasted in chat.
- **Runtime injection only** (process env from Infisical sync / agent identity). Short-lived runtime env is OK; durable SoT is Infisical.
- VPS `.env` files may exist as **regenerable runtime cache** (`chmod 600`, gitignored) — never as authoritative SoT. If disk disagrees with Infisical, Infisical wins.

Full protocol: `skills/secrets/SKILL.md`. Desk pointer: `skills/infisical/SKILL.md`.

**Supersedes** any prior wording that treats VPS `.env`, Beehiiv-in-Lovable, connector-secrets boxes, or Grok box-secrets as durable SoT.

**Carve-out:** Obsidian vault (Air + Tailscale daily copy to VPS) is allowed for **personal/work narrative notes** and non-API sensitive docs — **not** for API keys/tokens (those go Infisical).

**Migration gaps (HITL — document in tickets; do not delete live secrets without Gideon):** Grok box-secrets → Infisical; Orch connector-secrets (e.g. OpenRouter); Lovable env (e.g. Beehiiv); VPS leftover `infisical-creds` / OPENROUTER env files. See `skills/secrets/SKILL.md` § Migration gaps.

### OSS-first + tiny/private — Gideon 2026-08-20 (Orchestrator) (hard gate)

Do not weaken Lane A, the official $ table, the billed-vs-raw scrape, the Flash fill-in (empty mechanical = `gemini-3.7-flash`), or the Tools-session lock (Lovable / HeyGen / WhatsApp / Vercel escalate to Desk, same bc-id). Official prices stay `https://cursor.com/docs/models-and-pricing`. Do not invent prices.

**1. Coding is OSS-first.** OpenCode Go default is `opencode-go/kimi-k2.7-code`. `composer-2.5` (`fast=false`) is the Cursor Hands fallback when Go is blocked (current VPS CF 1010), over quota, hung, or Gideon says Hands. Never Composer Fast. Never a second Kimi cloud agent. Never Muse Spark 1.2 Contributor (trains on prompts — official Go privacy table, `https://opencode.ai/docs/go/`).

**2. Go has no image/video/voice generation weights.** Official list is coding-only (verified 20 Aug 2026, `https://opencode.ai/docs/go/`). Do not invent models. Current official list: Grok 4.5, GLM-5.3, GLM-5.2, GLM-5.1, GPT 5.6 Luna, Kimi K3, Kimi K2.7 Code, Kimi K2.6, MiMo-V2.5, MiMo-V2.5-Pro, MiniMax M3, MiniMax M2.7, Muse Spark 1.2 Contributor (limited regions — forbidden), Qwen3.8 Max, Qwen3.7 Max, Qwen3.7 Plus, Qwen3.6 Plus, DeepSeek V4 Pro, DeepSeek V4 Flash, Hy3. MiniMax M3 / MiMo / Kimi may read image/video (text out). Presenter video stays HeyGen primary. Image generate stays Images desk. Do not invert HeyGen to fallback.

**3. tiny vs private are two axes.** They are not the same gate.
- **Tiny** = job size: one artifact, mechanical, no architecture, no grant/eval/brand → `gemini-3.7-flash` or local 3B.
- **Private** = residency: must not leave 127.0.0.1 (client raw, unsigned, QBO staging, credentials, unpublished packs) → local Ollama `LFM2.5-VL-3B` only. If private does not fit 3B, hold for Gideon.
- **Tiny + private** = local 3B.

Empty model on a mechanical job still = `gemini-3.7-flash` (19 Aug fill-in). Private residency overrides Flash — private does not leave 127.0.0.1.

### Media generation routing — Gideon 2026-08-21 (HITL lock)

Do not connect fal.ai, `FAL_KEY`, or ElevenLabs. Official prices still `https://cursor.com/docs/models-and-pricing`. Do not invent prices.

- **IMAGE primary:** Images desk (no real people). Fallback: Canva brand layouts (not diffusion). **OSS self-host stills (when GPU host live):** ComfyUI + Flux.1-Dev + CTH LoRA per `skills/oss-stills/SKILL.md` — brand DNA in `skills/cleantechhub-brand/brand_dna.yaml`; `host: HOLD` until Gideon stands up a dedicated GPU box or confirms Air GPU. Never Flux weights on VPS-4. Later HITL only: fal.ai via Composio + `FAL_KEY`. fal generate tools are currently restricted/not Active — do not connect now.
- **VIDEO primary:** HeyGen presenter (avatar + ES translate). Auth the existing plugin first (needsAuth). Prefer Composio HeyGen only if plugin session fails. Do not add a second HeyGen plugin. B-roll: OpenRouter `POST /api/v1/videos` (`minimax/hailuo-3`, `hailuo-2.3`, `alibaba/wan-2.7`, `google/veo-3.1-lite`; not ZDR). Later HITL: MiniMax hosted Hailuo 2.3 / H3 API (NOT Go M3, NOT local H3 weights). GPU later (not on VPS-4): Wan-Animate-2 Apache or LTX-2.5 (community license under $10M ARR, official min 16GB VRAM). Never download video weights onto VPS-4. Never local H3 for US-facing AIC/Frank (US/EU/UK/KR excluded).
- **VOICE primary:** HeyGen Starfish inside presenter. Standalone TTS/clone/STT: hold. ElevenLabs Composio exists, not Active — do not connect until Gideon says. No Voice desk.

**OpenRouter media generate bus — Gideon GO 2026-08-20 7:10pm COT (one-key bus):**
- OpenRouter is the media-generate bus (Hands HTTP). Do not add a Cursor OpenRouter plugin (none in catalog). Prefer Composio later only if a toolkit exists. Do not connect fal.ai, `FAL_KEY`, or ElevenLabs.
- **IMAGE generate (cloud bus):** OpenRouter `POST /api/v1/images` (`FLUX` / `Qwen-Image`). Images desk stays throwaway mocks. Canva stays brand layouts. **OSS self-host track (parallel, not replacement):** `skills/oss-stills/SKILL.md` — ComfyUI + Flux.1-Dev + CTH LoRA on named GPU host; OpenRouter rows stay.
- **VIDEO B-roll:** OpenRouter `POST /api/v1/videos` (`minimax/hailuo-3`, `hailuo-2.3`, `alibaba/wan-2.7`, `google/veo-3.1-lite`). Not ZDR.
- **VIDEO presenter:** HeyGen stays presenter (`avatar` + `ES translate` + `Starfish`). Auth existing plugin first (`needsAuth`).
- **VOICE / STT:** OpenRouter `POST /api/v1/audio/speech` and `/audio/transcriptions` (`minimax/speech-2.8-hd` ES, `fish-audio/s2.1-pro` clone, `hexgrad/kokoro-82m` cheap EN).
- **Coding default UNCHANGED:** OpenCode Go `opencode-go/kimi-k2.7-code`. Do not point OpenCode coding at OpenRouter.
- **Private payloads:** Still `127.0.0.1` only (`LFM2.5-VL-3B` local Ollama). Never video weights on VPS-4. Never local H3 for US-facing AIC/Frank.

## 6. Skill toolkit (machine-readable inventory)

**Source:** repo evidence on `main`, 2026-08-26. Do not invent skills.

| Path | Role |
|---|---|
| `skills/<name>/SKILL.md` | Canonical playbook (Claude Desktop + read-through for Cursor) |
| `.cursor/skills/<name>/SKILL.md` | Cursor discovery stub → canonical |
| `skills/harness/references/skill-toolkit.json` | Full inventory: names, categories, canonical paths, Cursor stub parity, skip list |
| `skills/skill-template/SKILL.md` | Skill authoring template and quality rules |
| `skills/skill-template/references/SKILL-TEMPLATE.md` | Copy-paste skeleton for new skills |
| `HARNESS.md` | Cowork/CLI/Cursor **setup** docs (not this rulebook) |
| `AGENTS.md` | Cursor pointer + Skip list |
| `CLAUDE.md` | Claude Desktop plugin pointer |

**Planted on main (54 canonical skills):** 27 core/plugin skills (brand, programs, operations, infrastructure — includes `skill-template`, `socials-loop`, `oss-stills`, `infisical`) + 27 desk comms skills (`*-comms`) — see `skill-toolkit.json`.

**Cursor stubs (53):** all canonical except `secrets`.

**Authoring:** new or updated skills follow `skills/skill-template/SKILL.md` and `skills/skill-template/references/SKILL-TEMPLATE.md`.

**Skipped (intentional):**
- `secrets` — playbook at `skills/secrets/SKILL.md`; Claude Desktop only; no Cursor stub (`AGENTS.md` Skip list).
- `dual-desktop-macos` — Claude Desktop only; not on `main`; do not invent.

Human-readable category tables also live in `README.md` § Skill Inventory (may lag `skill-toolkit.json`).

## 7. File structure

Do not invent a new tree.

- Archive: `/opt/claude-files/Projects/<Claude project name>/`
- Sessions: `/opt/claude-files/sessions/YYYY-MM-DD/`
- Repos: GitHub as already connected (including `cth-plugin`)
- Mac `~/Documents/Claude/` is optional mirror only
- Plugin rulebook: this harness as `skills/harness` in `cth-plugin`, plus `tickets/TEMPLATE.md`
- Repo `HARNESS.md` is Cowork/CLI/Cursor setup docs, not this rulebook

## 8. What stays expensive vs cheap

Stay on Orchestrator / Box: route, HITL, QR, logged-in browser, GO/NO-GO, tone, REIN HOLD, send.

Cloud Hands or script: inventories, folder maps, docx/HTML/SVG drafts, Lucio-style guides, session dumps, disk sweep, 2am sync.

About 70% of 13–15 Aug work is Hands/script.

## 9. Gates and blockers

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
11. **Desks send tickets to Hands. They do not first-draft, inventory-grind, or write files.** Isolated grant agents review; Hands writes. Infrastructure tickets Hands; it does not SSH-inventory or grind maps itself.

## 10. War stories

Facts from the first week. Do not repeat these mistakes.

1. **Desks ticket; Desks do not grind file packs.** Grant Desks were writing docx and xlsx themselves instead of writing a Ticket for Hands. Infrastructure was SSH-inventorying and grinding maps instead of ticketing Hands. Isolated grant agents review; Hands writes. First-draft grind on the expensive model was the miss.

2. **Grant outputs may be Drive-only. Drive is a Tool.** A donor pack that lives in Google Drive is not a reason to open a GitHub repo. Do not create a repo for a grant output unless Gideon marks a repo row. Drive packs (docx/xlsx on Google Drive) are a Tool job — Composio or GDrive connector — not a Cloud Hands run. Hands writes GitHub PRs. A Desk that needs a donor pack on Drive does not ask for a repo and does not launch Hands.

3. **Mac Hands: worker must be running AND visible in Cursor Agents (My Machines) before ticketing.** `agent login` is not `agent worker start`. Do not paste both commands on one line. Leave the worker window open. If Gideon cannot see the machine in My Machines, the ticket will fail silently.

4. **In Orchestrator chat, Desk names are tap-links, not bare names.** Bare names do not route. Link the Desk.

5. **Tools are not Workbenches or chats.** Drive, GitHub, Buffer, Monday, Airtable, Notion stay Tools. OpenCode is a Hands lane, not a Desk or Workbench. No extra chats for any of them.

6. **The default Cursor cloud VM cannot see the Air or write Archive.** Archive writes need a VPS Cursor worker. Do not clone `/opt/claude-files`. Cloud Hands can only PR to GitHub until that worker exists.

7. **When planting this rulebook: do not invent Desk enums, do not rewrite gates.** Fan-out, REIN HOLD, and the five terms must stay verbatim. If a Hands agent is updating this skill, plant the text — do not compress it.

## 11. First tickets Cloud Hands should accept

- Add this file as `skills/harness/SKILL.md` (or the repo's existing skill layout)
- Add `tickets/TEMPLATE.md`
- Point `CLAUDE.md` / plugin readme at the harness
- Do not embed Grok Bot UUIDs
- Do not clone Archive onto a cloud VM

## 12. Ticket template (copy)

```
desk:
folder:
done-when:
model: gemini-3.7-flash | composer-2.5 (fast=false)
lane: github-pr | drive-folder
hitl: nothing sent/posted/paid
reviewer:
context:
```
