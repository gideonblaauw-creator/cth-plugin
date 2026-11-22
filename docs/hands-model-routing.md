# Hands model routing

**Canonical playbook:** `skills/hands-model-routing/SKILL.md` (Gideon GO **22 Nov 2026**).

**Default:** every Cloud Hands launch uses `composer-2.5` with **Fast OFF** (`model_params: {fast: false}` or `model: composer-2.5 (fast=false)`).

**HOLD and flag Gideon:** Sonnet, Opus, Grok, Fable, Sol, GPT high tiers, Auto-as-a-spend, Max mode, **Fast ON** (`fast=true`), and silent upgrades.

Repo copy surfaces: `skills/harness/SKILL.md` § Token budget protocol (batching/scoping only), `tickets/TEMPLATE.md`, `skills/infrastructure-comms/SKILL.md` § Hands model.

## Token budget protocol (22 Oct 2026) — spend rules (still active)

**Locked:** Gideon **22 Oct 2026**
**Goal:** Cut Cloud Hands token spend.

Model launch is **`skills/hands-model-routing/SKILL.md`** (22 Nov 2026). The rules below govern waves, scoping, and checkers.

1. **One job per wave, not per item.** Batch content work into one job per wave. Put about 10 to 20 items in one wave. Content work means Nexus pages, wiki entries, and Datalab tasks. Code builds may still split.
2. **Checker by risk.** Launch a separate read-only checker job only for high-risk work. High-risk work is a merge, a deploy, a live change, a key, a credential, or a client-facing deliverable. A low-risk content job checks its own result. A low-risk file job checks its own result. Attach proof on that job. Use a hash, an HTTP status code, or test output. **Control Tower · Infra** checks every Cloud Hands result (maker ≠ checker).
3. **Scoped tickets.** Name the exact files to open on every ticket. Name the exact paths to open on every ticket. Name a read budget on every ticket. Do not crawl the VPS with an open-ended search. Do not crawl a whole repo.
4. **Big-file rule.** Do not read a file larger than 200 KB into the job. Decks, PDFs, transcripts, and dumps follow this rule. Verify a large file by its hash. Verify it by its size. Verify it with grep.
5. **No duplicate launches.** Check for a running job with the same title before you launch. Do not relaunch a failed job until you fix its blocker.
6. **Step cap.** Stop the job at about 60 steps. Report the result at that stop. Split long work into planned phases.
7. **Daily budget.** Launch at most 40 jobs a day across all desks. The Orchestrator counts each launch. Gideon sets the Cursor dashboard spend limit. Gideon sets the spend alert.

## HITL (unchanged)

Gideon yes before: merge, deploy, public change, DNS, send/post, spend, credential activation/deletion, restarts.

## Historical note

**22 Oct 2026** briefly set every Cloud Hands job to Composer 2.5 **Fast ON**. **22 Nov 2026** Infra reorg restores **Fast OFF** as the default (`skills/hands-model-routing/SKILL.md`).