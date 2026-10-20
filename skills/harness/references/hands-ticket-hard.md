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
- Review Hands output (**maker ≠ checker**)
- **HITL** gates before send / post / pay / activate / cutover
- Ready-ping Orchestrator with PR / URL / **bc-id** / paths — not process notes

---

## What Hands does

- **Lane A** — allowlist repos (e.g. `cth-plugin`) for code/skills
- **Lane B** — `{type: machine, name: vps}` for Archive / Drive / HTML packs — no `repo_url` on Lane B when packs-only
- **Parallel-first** micro-Hands: one artifact + one acceptance; see § Parallel jobs (above ~8 live per desk, ping Orchestrator)

---

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

## Protocol changes
Every change to this protocol ships as a PR to main in cth-plugin (HITL merge by Gideon).

## GitHub-before-live HARD (Gideon 20 Oct 2026)

**Scope:** every Desk and every Hands job. Every build, including every deploy.

Put each change on GitHub before that change goes live.
Use a pushed branch or a pull request.
Do not deploy a local-only commit.
Do not deploy an unpushed commit.

1. Name the full commit SHA on the deploy ticket.
2. Confirm that this SHA exists on origin before you deploy.
3. Use `git ls-remote` or the GitHub API for that check.
4. Record the pushed branch or the pull request on the receipt.
5. Record the same SHA on the receipt.
6. Stop when the push fails.
7. Escalate the failure to the Desk.
8. Do not deploy.
9. Do not use a workaround.
10. Confirm that the live SHA is present on GitHub.

Mandatory ticket line: Commit to a pushed branch or PR first. Deploy only from what is on GitHub. Never deploy unpushed commits live.

Canonical: `skills/harness/SKILL.md` § GitHub-before-live HARD.

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
- Working one job and queuing the rest
- Deploying a commit that is not on GitHub
- Continuing a deploy after a failed push

---

## Mail Finder (incident + pattern)

**All Mail Finder craft is Hands.** Workbench tickets; Hands does domain resolve, page-source parse, Photon/Wayback/theHarvester/pdfgrep cohorts, attribution gate, FOUND/EMPTY/UNCERTAIN CSV+MD, evidence packs. Local executors for research/crawl are a miss.

**Launch shape (Lane B):** environment `{type: machine, name: vps}`. Mechanical extract → `gemini-3.7-flash`; judgment/pack craft → `composer-2.5` Fast ON. Parallel-first: one Hands = one firm domain or small seat batch (≤10–15 seats) + one acceptance; cap 3–5 live per wave.

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
| `model:` | From `docs/hands-model-routing.md` |
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
