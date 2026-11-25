# Rollout — Fresh context per task (25 Nov 2026)

**Rule:** `skills/harness/SKILL.md` § Fresh context per task (usage fix A; Gideon approved 25 Nov 2026 08:56 COT).

**Baseline (25 Nov 2026 usage review):** Grok Bot cached-prompt re-reads ≈92.6% of Grok tokens on long desk chats. On a 1.54B-token slice, Grok 56% / Cursor 44%; target split ≈1/3 Grok, 2/3 Cursor. Evidence on VPS: `/opt/claude-files/Infra/usage-review/2026-11-25/` (`out/report.md`, `verify/verdict.md`).

## Rollout plan

1. After merge, Control Tower updates the shared desk skill from this repo.
2. Orchestrator broadcasts one message to every desk with the rule and this doc.
3. Each desk writes its first handover note within 24 hours of the broadcast.
4. Gideon clears the longest threads first (likely candidates — **guess, not measured:** Orchestrator, Infra, Datalab, Inbox, Socials, Teclogi).

## Per-desk checklist

1. Read `skills/harness/SKILL.md` § Fresh context per task.
2. List open work; write a ≤15-line handover (dates, ids, paths, waits-on).
3. Store the handover in tracked tasks or desk memory — not secrets, not chat-only.
4. Tell Gideon in one line when the thread is ready to clear or summarise.
5. Launch new work as fresh Hands (`composer-2.5`, `fast:false`) with a self-contained brief.

## How to measure (one week later)

Re-run the usage CSV review on the same methodology as 25 Nov. Compare:

- Cached-prompt share (baseline: **92.6%** on Grok).
- Grok vs Cursor split (baseline: **56% / 44%** on the 1.54B-token slice).

Target direction: lower cached-prompt share; move toward **~33% Grok / ~67% Cursor**.

## Rollback

Revert the docs PR that added the rule and this file. Desks resume prior thread habits until a replacement policy ships.
