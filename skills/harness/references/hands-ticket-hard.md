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
- **Parallel-first** micro-Hands: one artifact + one acceptance; cap **3–5** live Hands per workstream

---

## Workbench / connector exception (narrow)

Channel I/O (Gmail, Calendar, LinkedIn, Instagram, Facebook, Ads, WhatsApp/Babo, Monday stamps) **only when Hands cannot** (no CLI/connector/API for that step). Never use the exception to run crawl, research, or file-pack grind locally.

---

## Anti-patterns

- Spawning a local executor to crawl, scrape, research, or draft packs
- Capability agents doing first-draft file trees in the Grok chat instead of Hands
- Blind-copying work that belongs on VPS Archive or a GitHub PR into chat-only artifacts
- Claiming “reviewed” without Hands evidence paths / bc-ids

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
