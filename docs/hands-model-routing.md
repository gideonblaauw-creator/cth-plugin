# Hands model routing (Gideon lock — Token budget protocol 22 Oct 2026)

**Every Cloud Hands job = Composer 2.5 Fast ON.**

Canonical lock for Cloud Hands model fill-in. Playbook surfaces: `skills/harness/SKILL.md` § Token budget protocol, `tickets/TEMPLATE.md`. Desk comms §5 tables that still name Flash keep the 13 Sep record. This file is the launch rule.

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

**Fast ON stays.** Never silently launch a Cloud Hands job with Fast off. `composer-2.5 (fast=false)` is a miss. Remap it to `fast=true` and flag.

## Historical — BUILDING lock t1263u (2026-09-13)

**BUILDING = Composer 2.5 Fast ON.**

This block is the 13 Sep record. It is not the launch fill-in after 22 Oct 2026.

**Supersedes** t1242u (2026-09-12) and the 2026-08-26 default that repo/code Hands must use `composer-2.5` with `fast=false`. Repo/code **builds** launched **Fast ON** only. No silent swap back to Fast off. The 22 Oct protocol extends Fast ON to every Cloud Hands job.

## Explicit build surfaces

These surfaces still use Fast ON. After 22 Oct 2026, every other Cloud Hands job does too.

Includes but is not limited to:

- Repo / code on Lane A (`lane: github-pr`)
- LangGraph lane (`langgraph: yes`) and Lane A product apps
- **Signal Radar**, **LexiScan**, **scanner** (e.g. `cth-data-room-scanner`)
- Harness code (`skills/harness/`, `tickets/`, desk routing in `*-comms` skills)
- Skill plant, app graph, infrastructure playbook edits on owning repos

## Fill-in table (22 Oct 2026)

| Job class | Ticket signal | Model | Empty `model:` fill-in |
|---|---|---|---|
| Every Cloud Hands job | Mechanical, content, review, repo/code/build, skill plant, harness | `composer-2.5` (`fast=true`) | Yes — **Fast ON**. Do not fill Flash. Do not HOLD for a missing model |
| Private residency | Must stay on 127.0.0.1 | local Ollama `LFM2.5-VL-3B` | Private overrides Composer |

### Historical fill-in (through 21 Oct 2026)

| Job class | Ticket signal | Model | Empty `model:` fill-in |
|---|---|---|---|
| Mechanical / tiny | Pack writes, inventories, copy grind, research grind, unspecified mechanical | `gemini-3.7-flash` | Was the empty **mechanical** fill-in. Retired 22 Oct 2026 |
| Repo / code / build | Lane A PR, app, graph, skill plant, `langgraph: yes`, Signal Radar, LexiScan, scanner, harness | `composer-2.5` (`fast=true`) | Still Fast ON. Now covers every Cloud Hands job |
| Review / eval / brand | No model named | — | Was **HOLD**. Retired 22 Oct 2026. Launch Composer 2.5 Fast |

## Rules

1. **Every Cloud Hands job uses Composer 2.5 Fast** (Token budget protocol, 22 Oct 2026). Mechanical work does not fill Flash. An empty `model:` fills `composer-2.5` (`fast=true`).
2. **Fast ON** — ticket `model: composer-2.5 (fast=true)`, or omit `model:` → launch Fast ON.
3. **Do not fill Flash** on a Cloud Hands job. The 13 Sep Flash row is history.
4. **Never silently launch with Fast off** — do not default to `fast=false`, omit Fast, or swap Fast ON → Fast off. HITL: no silent model swap to Fast off. `fast=false` is a miss. Remap to `fast=true` and flag.
5. **Composer 2.5 Fast on content jobs is allowed** (22 Oct 2026). Do not remap it to Flash. The old pack-write miss is retired.
6. **High-tier HOLD** — Sonnet, Opus, Haiku, Fable, Sol, Grok, second cloud Kimi, Muse Spark 1.2 Contributor → HOLD and flag Gideon. Do not HOLD a review job that simply omitted `model:`.
7. **Infisical unchanged** — secrets SoT stays Infisical; model routing does not change credential rules.
8. **Private residency unchanged** — data that must stay on 127.0.0.1 uses local Ollama `LFM2.5-VL-3B`. Private overrides Composer.

## Ticket `model` field

```
model: composer-2.5 (fast=true)
```

| Written on ticket | Launch |
|---|---|
| `composer-2.5 (fast=true)` or empty `model:` | Composer 2.5 **Fast ON** |
| `gemini-3.7-flash` | **Miss** — remap to `composer-2.5` (`fast=true`) and flag (22 Oct 2026) |
| `composer-2.5 (fast=false)` | **Miss** — remap to `fast=true` and flag |
| Silent Fast off | **Miss** — remap to `fast=true` and flag |
| Review/eval/brand, no model | Composer 2.5 **Fast ON** (22 Oct 2026). Do not HOLD |
| Private residency | local Ollama `LFM2.5-VL-3B` |

## Historical note

Token lock **2026-08-26** remains in `skills/harness/SKILL.md` for Grok coordination-only and forbidden high-tier fill-in. Mechanical Flash was the fill-in until 21 Oct 2026. **t1242u** (2026-09-12) first planted BUILDING = Fast ON. **t1263u** (2026-09-13) hardened Fast ON for builds. **Token budget protocol (22 Oct 2026)** sets Composer 2.5 Fast ON for every Cloud Hands job.
