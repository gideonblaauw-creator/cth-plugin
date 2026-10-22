# Hands-ticket HARD — Desks + Workbenches → Cloud Hands

**Status:** reference under the harness SoT — not a second rulebook.  
**Canonical rulebook:** `skills/harness/SKILL.md` (§ Hands-ticket HARD)  
**Locked:** Gideon / Orchestrator **24 Sep 2026**  
**Related:** `skills/harness/references/harness-engineering.md` (verification loops, autonomy bands, maker≠checker)

---

## Core rule

**Every Desk and every Workbench tickets craft to Cursor Cloud Hands.** Local Grok `executor` / box grind for research, crawl, file packs, code, copy, HTML/PDF, or scrape is a **protocol miss** (Mail Finder was the incident that broke this once).

**Applies to:** subject Desks, isolated client/grant Desks, capability agents (Researcher, Scraper, Presentations, Images, Video), and Workbenches (Mail Finder, Voice, Fillout, Monday helpers, channel benches).

**Layers:** Orchestrator · Desks · Workbench · Cloud Hands. Tools and Tickets are not chats.

---

## What the agent keeps

- Own the subject / channel
- Write Hands tickets (outcome, sources, **exclusive write path**, acceptance, model from `docs/hands-model-routing.md`)
- Review high-risk Hands output with a separate read-only checker (**maker ≠ checker**). A low-risk content or file job checks its own result (**Token budget protocol, 22 Oct 2026**)
- **HITL** gates before send / post / pay / activate / cutover
- Ready-ping Orchestrator with PR / URL / **bc-id** / paths — not process notes

---

## What Hands does

- **Lane A** — allowlist repos (e.g. `cth-plugin`) for code/skills
- **Lane B** — `{type: machine, name: vps}` for Archive / Drive / HTML packs — no `repo_url` on Lane B when packs-only
- **Parallel-first** for code: one artifact + one acceptance. Content work uses one job per wave. See **Token budget protocol (22 Oct 2026)**. Above ~8 live per desk, ping Orchestrator.

---

## Plan first (MANDATORY, Gideon 12 Oct 2026)
Before any Hands launch the desk writes a plan and puts it in the ticket:
1. Precise restatement in Simplified Technical English (ASD-STE100): approved words with one meaning, sentences of at most about 20 words, one instruction per sentence, active voice, imperative verbs. Fields: Goal / Audience / Deliverable / Done when / Constraints / Out of scope / Open questions.
2. Context check: memory, Archive, prior work; no duplication or contradiction.
3. Job split: for code, split into the smallest units that each yield one artifact with one acceptance check. For content, batch about 10 to 20 items into one wave (**Token budget protocol, 22 Oct 2026**). List dependencies explicitly.
4. Risks + mandatory push back: state at least one challenge to the ask (weak assumption, better route, cost, scope, timing) or write 'no push back: <reason>'. Questions only Gideon can answer are asked once, up front.
5. Plan in ticket: the reviewer checks the output against the plan.
Big or costly jobs: show Gideon the plan before launch. Small jobs proceed.

## Parallel jobs (MANDATORY, Gideon 12 Oct 2026)
Code builds still use one Hands agent per independent job. Launch those jobs at the same time. Never work one code job and queue the rest.
Content work (Nexus pages, wiki entries, Datalab tasks) follows **Token budget protocol (22 Oct 2026)** below. Use one job per wave. Do not use one Hands job per item.
- Each code job gets its own bc-id in the turn it arrives; only true dependencies wait, and they are written down.
- Keep a job list (job, bc-id, state): live, blocked on a named HITL/blocker, or done. Nothing is 'queued' without a bc-id.
- Above ~8 live per desk, ping Orchestrator instead of serializing.
- Every Cloud Hands job runs on Composer 2.5 Fast (`composer-2.5`, `fast=true`). See the model rule below.

## Token budget protocol (22 Oct 2026)

**Locked:** Gideon **22 Oct 2026**
**Goal:** Cut Cloud Hands token spend.
**Canonical:** `skills/harness/SKILL.md` § Token budget protocol. This copy must match that section.

This section amends the 12 Oct 2026 parallel-jobs rule for content work. It amends maker ≠ checker for low-risk jobs. Desk comms §5 tables that still name Flash keep the 13 Sep record. This section is the launch rule.

**Model rule (Gideon, 22 Oct 2026).** Run every Cloud Hands job on Composer 2.5 Fast. Set `model:` to `composer-2.5` (`fast=true`). This replaces Flash on mechanical jobs. This replaces a HOLD when a review job has no model. Do not mark Composer 2.5 Fast on a content job as a miss. Private data that must stay on 127.0.0.1 still uses local Ollama `LFM2.5-VL-3B`.

1. **One job per wave, not per item.** Batch content work into one job per wave. Put about 10 to 20 items in one wave. Content work means Nexus pages, wiki entries, and Datalab tasks. This replaces "one Hands per smallest independent job" for content work. Code builds may still split.
2. **Checker by risk.** Launch a separate read-only checker job only for high-risk work. High-risk work is a merge, a deploy, a live change, a key, a credential, or a client-facing deliverable. A low-risk content job checks its own result. A low-risk file job checks its own result. Attach proof on that job. Use a hash, an HTTP status code, or test output.
3. **Scoped tickets.** Name the exact files to open on every ticket. Name the exact paths to open on every ticket. Name a read budget on every ticket. Do not crawl the VPS with an open-ended search. Do not crawl a whole repo.
4. **Big-file rule.** Do not read a file larger than 200 KB into the job. Decks, PDFs, transcripts, and dumps follow this rule. Verify a large file by its hash. Verify it by its size. Verify it with grep.
5. **No duplicate launches.** Check for a running job with the same title before you launch. Do not relaunch a failed job until you fix its blocker.
6. **Step cap.** Stop the job at about 60 steps. Report the result at that stop. Split long work into planned phases.
7. **Daily budget.** Launch at most 40 jobs a day across all desks. The Orchestrator counts each launch. Gideon sets the Cursor dashboard spend limit. Gideon sets the spend alert.

## Protocol changes
Every change to this protocol ships as a PR to main in cth-plugin (HITL merge by Gideon).

---

## Workbench / connector exception (narrow)

Channel I/O (Gmail, Calendar, LinkedIn, Instagram, Facebook, Ads, WhatsApp/Babo, Monday stamps) **only when Hands cannot** (no CLI/connector/API for that step). Never use the exception to run crawl, research, or file-pack grind locally.

---

## Anti-patterns

- Spawning a local executor to crawl, scrape, research, or draft packs
- Capability agents doing first-draft file trees in the Grok chat instead of Hands
- Blind-copying work that belongs on VPS Archive or a GitHub PR into chat-only artifacts
- Claiming “reviewed” without Hands evidence paths / bc-ids
- Launching Hands without a written plan or push back
- Working one code job and queuing the rest
- One Hands job per Nexus page, wiki entry, or Datalab task
- A second checker job on a low-risk content or file task
- An open-ended crawl of the VPS or a whole repo
- Reading a file larger than 200 KB into the job
- A second launch of a running title, or a relaunch before the blocker is fixed

---

## Mail Finder (incident + pattern)

**All Mail Finder craft is Hands.** Workbench tickets; Hands does domain resolve, page-source parse, Photon/Wayback/theHarvester/pdfgrep cohorts, attribution gate, FOUND/EMPTY/UNCERTAIN CSV+MD, evidence packs. Local executors for research/crawl are a miss.

**Launch shape (Lane B):** environment `{type: machine, name: vps}`. Every Mail Finder Hands job runs on `composer-2.5` Fast ON (**Token budget protocol, 22 Oct 2026**). Parallel-first: one Hands = one firm domain or small seat batch (≤10–15 seats) + one acceptance; cap 3–5 live per wave.

**Ticket must name:** input CSV path on VPS / attachments; locked method; exclusive write paths; acceptance counts; Monday column ids if stamping authorized; attribution gate wording.

**After Hands:** read artifacts; ping Teclogi with counts + paths + bc-id; stamp Monday only after attribution review (HITL).

---

## Orchestrator verify

Orchestrator checks Desks and Workbenches are ticketing Hands, not grinding. On miss: **stop the local grind**, re-ticket Hands, patch profile/skill if needed, ready-ping Gideon only if HITL or blocker.

---

## Ticket fields (Hands evidence)

Every craft ticket should make review mechanical:

| Field | Purpose |
|---|---|
| `done-when` | One-sentence acceptance |
| `folder:` / repo + branch | Where artifacts land |
| **Exclusive write path** | Named in `context:` — no shared grind paths |
| `model:` | `composer-2.5` (`fast=true`) on every Cloud Hands job (Token budget protocol 22 Oct 2026) |
| `files:` | Exact files and paths the job may open |
| `read-budget:` | File count or byte cap. Stop at the cap |
| **bc-id** | Cloud agent run id in ready-ping when Hands finishes |

See `tickets/TEMPLATE.md` for the seven-field block.

---

## Related paths

| Path | Role |
|---|---|
| `skills/harness/SKILL.md` | Harness SoT |
| `skills/harness/references/harness-engineering.md` | Verification, autonomy bands |
| `tickets/TEMPLATE.md` | Ticket contract |
| `docs/hands-model-routing.md` | Model fill-in |
