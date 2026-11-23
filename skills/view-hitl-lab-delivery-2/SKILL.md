---
name: view-hitl-lab-delivery-2
description: >-
  DEPRECATED duplicate of view-hitl-lab-delivery. Do not use; pending Gideon GO to delete.
---
# View Understanding Lab delivery (duplicate — deprecated)

> **Superseded by `skills/view-hitl-lab-delivery/SKILL.md` (pending Gideon GO to delete).**

## When
Every **major** Lane A Hands completion (allowlist repo, substantive PR). Skip for tiny/mechanical PRs.

## Locked naming (Gideon 2026-09-12)
**Lab name:** Understanding Lab

**Steps (always this order):**
1. Context
2. Explanation (+ quiz)
3. Playground *(key understanding step)*
4. Shared decisions
5. Next cycle

Legacy synonyms (docs may still mention once): HITL Lab→Understanding Lab; Home→Context; Explainer→Explanation; Microworld→Playground; Decisions DB→Shared decisions; Next loop→Next cycle.

## Do in Gideon chat (Infrastructure)
1. Send the cloud-agent card (View PR).
2. Immediately send a text message that **leads with View Understanding Lab**:
   - Notion lab Home (Context): https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
   - Stable interactive HTML URL (Playground host — from harness once planted)
   - Local fallback: `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>`
   - Shared decisions: https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b
3. Remind: draft only; merge after Gideon PASS on Understanding Lab (≤10 min: Explanation → Playground → Shared decisions).

## Do not
- Do not say View HITL Lab in new chat/PR copy (use View Understanding Lab).
- Do not rely only on the PR body.
- Do not claim a native button inside Cursor’s View PR chrome.
- Do not put live client findings on a public HTML host — synthetic Playground only on public Vercel; production review stays local/Tailscale.

## Hands obligation
Major Lane A PR bodies must include the **View Understanding Lab** footer block (cth-plugin notion + harness skills).