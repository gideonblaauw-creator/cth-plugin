# Understanding Lab tiers (Gideon lock 2026-09-12)

**One-liner:** Push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.

Canonical lock for Lane A desks. Playbook surfaces: `skills/harness/SKILL.md` § View Understanding Lab, `skills/notion/SKILL.md`, `skills/infrastructure-comms/SKILL.md` §7. Delivery helper: `docs/view-understanding-lab-footer.md`.

`major: yes|no` from PR #24 is **superseded**. Do not infer a lab from “substantive scope” or `major: yes`. The ticket must name `tier:` or a one-line escalate reason. Omit `tier:` → **Tier 0**.

Notion page titles may still use legacy names (HITL Lab, Explainer, Microworld). Do not rewrite live Notion pages in this lock — Infra may update Notion separately.

## Tier 0 — Ship (DEFAULT)

- **When:** internal, familiar, low blast radius.
- **Bar:** normal PR + short what/why. No lab.
- **Anti-blackbox:** explainable in ~1 minute if asked.
- **CTA:** none. Do **not** add View Understanding Lab to the PR or Infra chat.

## Tier 1 — Light Understanding (most client / agent work)

- **When:** agent-heavy, client-facing, or “don’t fully feel this.”
- **Bar:**
  1. Context ≤½ page
  2. Playground light: one scenario, 2–3 options with tradeoffs, choose
  3. one Shared decision row / locks file with rationale + `locked_at`
- **Skip:** full Explanation essay, quiz, stable host requirement, event-store projector.
- **Escalate** with one-line reason on the ticket (`escalate:`).
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR.
- **PASS:** light bar above — **not** full five-beat PASS.

## Tier 2 — Full Lab + ledger (rare)

- **When:** donor/audit, unfamiliar domain, production agent permissions, or decision will be cited later.
- **Bar:** full five beats (`Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle`) + append `events.jsonl` (VPS Archive ledger path) + Notion promote + GH run artifact on close.
- **Ticket MUST name Tier 2.** Never default. Never infer.
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR.
- **PASS:** full five-beat PASS only. Event-store *implementation* is out of scope here — Hands appends the ledger file when Infra has planted the Archive path.

## Operating rules

1. **Default Tier 0.**
2. **Playground > paperwork** (if budget for one beat: options→choose).
3. **Ledger follows tier:** Tier 1 = disk/Notion row; Tier 2 = `events.jsonl`.
4. **Harness CTA “View Understanding Lab” only on Tier 1–2 PRs** — not every Lane A merge.
5. **Kill:** Tier 1 >30 min human time with no clearer decision → strip; Tier 0 ship you can’t re-explain in a week → next similar job Tier 1.

## Playground hard lock (Tier 1–2)

Keep Playground hard lock for Tier 1–2: `scenario → consequences → options → choose`.

- Tier 1: one scenario, 2–3 options with tradeoffs, then choose.
- Tier 2: full Playground hard gate (scenarios + consequences + 2–4 option paths with tradeoffs) before Shared decisions.
- Not scrub-only. Not a single-suggestion override.

## Ticket fields

```
tier: 0 | 1 | 2
escalate:
```

| Signal | Meaning |
|---|---|
| `tier:` omitted or `0` | Default Ship. No lab. No CTA. |
| `tier: 1` + `escalate:` one-liner | Light Understanding. CTA. Light PASS. |
| `tier: 2` (must be named) + `escalate:` one-liner | Full Lab + ledger. CTA. Full five-beat PASS. |
| `major: yes` without `tier:` | **Miss.** Do not treat as lab. Default Tier 0 and flag the Desk to name a tier or reason. |

## Delivery (CTA + PASS)

| Tier | View Understanding Lab CTA | Merge PASS |
|---|---|---|
| 0 | No | Short what/why. Infra reviews. Gideon merges. |
| 1 | Yes (PR footer + Infra chat) | Light PASS only |
| 2 | Yes (PR footer + Infra chat) | Full five-beat PASS only |

Full five-beat PASS is **not** the merge bar for every Lane A PR. CTA + full five-beat PASS apply only when the ticket names Tier 1–2 (Tier 2 for the full five beats; Tier 1 keeps the light bar).
