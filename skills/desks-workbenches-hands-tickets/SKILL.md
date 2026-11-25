---
name: desks-workbenches-hands-tickets
description: >-
  Use whenever a Desk, Workbench, or capability agent has file, research, code,
  copy, crawl, HTML/PDF, letter or pack craft — ticket Cursor Cloud Hands; never
  local executor grind. CTH letters, agreements and MOUs start from the official
  letterhead.
---
# Desks + Workbenches → Cursor Hands (HARD)

Gideon lock **24 Sep 2026**: **every Desk and every Workbench tickets craft to Cursor Cloud Hands**. Local Grok `executor` / box grind for research, crawl, file packs, code, copy, HTML/PDF, or scrape is a **protocol miss** (Mail Finder was the example that broke it).

Applies to subject desks, isolated client/grant desks, capability agents (Researcher, Scraper, Presentations, Images, Video), and workbenches (Mail Finder, Voice, Fillout, Monday helpers, channel benches).

## Layers
Orchestrator · Desks · Workbench · Cloud Hands. Tools and Tickets are not chats.

## Fresh context per task (25 Nov 2026)
Follow **`skills/harness/SKILL.md`** § Fresh context per task: one task per fresh agent, desk thread cap with handover notes, no polling on running Hands, craft still tickets to Hands. Rollout: `docs/rollout/2026-11-25-fresh-context-per-task.md`.

## What the agent keeps
- Own the subject / channel
- Write Hands tickets (outcome, sources, exclusive write path, acceptance, model from [hands-model-routing](sand-workflow:hands-model-routing))
- Review Hands output (maker ≠ checker)
- HITL gates before send / post / pay / activate / cutover; GO / NO GO asks to Gideon use inline widget buttons (`HARNESS.md`, 22 Nov 2026)
- Ready-ping Orchestrator with PR/URL/bc-id/paths — not process notes

## What Hands does
- Lane A allowlist repos (e.g. `cth-plugin`) for code/skills
- Lane B `{type: machine, name: vps}` for Archive / Drive / HTML packs — no `repo_url` on Lane B
- Parallel-first micro-Hands (one artifact + one acceptance); see Parallel jobs (above ~8 live per desk, ping Orchestrator)

## Plan first (MANDATORY, Gideon 12 Oct 2026)
Before any Hands launch the desk writes a plan and puts it in the ticket:
1. Precise restatement in Simplified Technical English (ASD-STE100): approved words with one meaning, sentences of at most about 20 words, one instruction per sentence, active voice, imperative verbs. Fields: Goal / Audience / Deliverable / Done when / Constraints / Out of scope / Open questions.
2. Context check: memory, Archive, prior work; no duplication or contradiction.
3. Smallest independent jobs: split into the smallest units that each yield one artifact with one acceptance check; list dependencies explicitly.
4. Risks + mandatory push back: state at least one challenge to the ask (weak assumption, better route, cost, scope, timing) or write 'no push back: <reason>'. Questions only Gideon can answer are asked once, up front.
5. Plan in ticket: the reviewer checks the output against the plan.
Big or costly jobs: show Gideon the plan before launch. Small jobs proceed.

## Parallel jobs (MANDATORY, Gideon 12 Oct 2026)
More than one job means one Hands agent per independent job, all launched at the same time. Never work one and queue the rest.
- Each job gets its own bc-id in the turn it arrives; only true dependencies wait, and they are written down.
- Keep a job list (job, bc-id, state): live, blocked on a named HITL/blocker, or done. Nothing is 'queued' without a bc-id.
- Above ~8 live per desk, ping Orchestrator instead of serializing.
- Models still follow hands-model-routing (low-end by default).
- Exception: browser and channel jobs that share one account or session (for example LinkedIn, Instagram, WhatsApp/Babo) run one at a time, to avoid account restrictions. All non-browser work for those desks still runs in parallel.

## Blocker escalation (MANDATORY, Gideon 12 Oct 2026)
Any blocker or slowdown that delays a deliverable (site/LinkedIn stall, tab crash, rate limit, warning banner, box freeze, Tailscale exit offline, failed or skipped routine, target/quota at risk) is escalated up the chain to Gideon as a HITL alert immediately, even if a retry is planned. Never log it silently. Automated ops surfacing for routines and infra failures uses **CTH_OPS** on the CTH Slack workspace via n8n **`CTH-OPS · Core · notify-ops`** (Gideon **18 Nov 2026**; **Telegram CTH_OPS on hold**). Canonical: `skills/hands-model-routing/SKILL.md` § Routines.

## Official CTH letterhead (HARD, Gideon 17 Nov 2026)
Every CTH letter, agreement, MOU or other formal document starts from the official blank Word letterhead. This applies to desks, workbenches and every Hands ticket.
- Source: opencode-vps `/opt/claude-files/Projects/CTH-Brand/letterhead/` (`CTH_Letterhead_Official.docx` and `.pdf`, `CTH_header.png`, `CTH_footer.png`). Attach the `.docx` to the Hands ticket and build on it.
- Reuse its header and footer parts and images as they are. Do not redraw, retrace or re-encode the wave or the colour bar.
- Header: a flowing wave, page-anchored at top 0 and left 0, flush with the top and left edges, with the white logo. Footer: a colour bar on the bottom edge. Above the bar is the address in Open Sans 8 pt #0C498A: "Fundación CleantechHUB · NIT 901.523.941-9 · Cl 90 No. 19-41 Of 801, Bogotá, Colombia" / "www.cleantechhub.net · +57 313 715 5965". Never 7 pt and never compressed.
- Body in Open Sans, A4.
- Checker QA: render to PDF and PNG and inspect the header and footer crops. The wave touches the top and left edges, the bar touches the bottom, the text clears the bar and nothing is clipped. `pdffonts` shows only Open Sans and the media sha256 matches the source.
- Details are in the [cleantechhub-brand](sand-workflow:cleantechhub-brand) skill's "Official letterhead" section.

## Protocol changes
Every change to this protocol ships as a PR to main in cth-plugin (HITL merge by Gideon).

## Workbench / connector exception (narrow)
Channel I/O (Gmail, Calendar, LinkedIn, Instagram, Facebook, Ads, WhatsApp/Babo, Monday stamps) **only when Hands cannot** (no CLI/connector/API for that step). Never use the exception to run crawl, research, or file-pack grind locally.

## WhatsApp channel (HARD, Gideon 7 Oct 2026)
1. **babo-wa ("wabo") on the VPS, channel 573137155965 (Gideon's personal number), is the ONLY WhatsApp channel** for pull and send. No WhatsApp Web, no QR session on the box, no Twilio WhatsApp, no Composio or other WhatsApp tools, no second linked device. The Twilio account is not a WhatsApp channel unless Gideon reverses this.
2. **All WhatsApp I/O goes through the WhatsApp agent (d280b734).** Desks and Hands request via the WhatsApp agent or the Orchestrator; they never read or send WhatsApp directly. Read-only pulls of the babo-wa store for briefs (e.g. Daily Note) are routed through or cleared with the WhatsApp agent.
3. **Send is unlocked** (sendEnabled stays true; it resets to false if babo restarts). Sends Gideon asks for himself go out without a confirm step. Messages another agent wants sent still need Gideon's own request in the WhatsApp chat first.

## Anti-patterns
- Spawning a local executor to crawl, scrape, research, or draft packs
- Capability agents doing first-draft file trees in the Grok chat instead of Hands
- Blind-copying work that belongs on VPS Archive or a GitHub PR into chat-only artifacts
- Claiming “reviewed” without Hands evidence paths / bc-ids
- Touching WhatsApp from any desk other than the WhatsApp agent, or via any channel other than babo-wa
- Launching Hands without a written plan or push back
- Working one job and queuing the rest
- Logging blockers quietly instead of alerting Gideon
- Redrawing or regenerating the CTH letterhead instead of building on the archived template

## Mail Finder
Also follow [Mail Finder Hands tickets](sand-workflow:mail-finder-hands-tickets).

## Orchestrator verify
Orchestrator checks desks/workbenches are ticketing Hands, not grinding. On miss: stop the local grind, re-ticket Hands, patch profile + this skill if needed, ready-ping Gideon only if HITL or blocker.