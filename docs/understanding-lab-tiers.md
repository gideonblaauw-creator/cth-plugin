# Understanding Lab tiers (Gideon lock 2026-09-12)

**One-liner:** Push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.

Canonical lock for Lane A desks. Playbook surfaces: `skills/harness/SKILL.md` § View Understanding Lab, `skills/notion/SKILL.md`, `skills/infrastructure-comms/SKILL.md` §7. Delivery helper: `docs/view-understanding-lab-footer.md`.

`major: yes|no` from PR #24 is **superseded**. Do not infer a lab from “substantive scope” or `major: yes`. The ticket must name `tier:` or a one-line escalate reason. Omit `tier:` → treat as **Tier 0** and **say so**.

Notion page titles may still use legacy names (HITL Lab, Explainer, Microworld). Do not rewrite live Notion pages in this lock — Infra may update Notion separately.

## Tier 0 — Ship (DEFAULT)

- **When:** internal, familiar, low blast radius.
- **Bar:** normal PR + short what/why. No lab.
- **Anti-blackbox:** explainable in ~1 minute if asked.
- **CTA:** none. Tier 0 **never** gets the lab popup.
- **Say so:** Infra and any harness footer copy **lead with** `**Tier 0** — ship (no Understanding Lab)`. If the ticket omitted `tier:`, say that in the same message.

## Tier 1 — Light Understanding (most client / agent work)

- **When:** agent-heavy, client-facing, or “don’t fully feel this.”
- **Bar:**
  1. Context ≤½ page
  2. Playground light: one scenario, 2–3 options with tradeoffs, choose
  3. one Shared decision row / locks file with rationale + `locked_at`
- **Skip:** full Explanation essay, quiz, stable host requirement, event-store projector.
- **Escalate** with one-line reason on the ticket (`escalate:`).
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR. **Lead with** `**Tier 1** — Light Understanding` in the same message, then lab links. Never surface the lab box/CTA without naming Tier 1.
- **PASS:** light bar above — **not** full five-beat PASS.

## Tier 2 — Full Lab + ledger (rare)

- **When:** donor/audit, unfamiliar domain, production agent permissions, or decision will be cited later.
- **Bar:** full five beats (`Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle`) + append `events.jsonl` (VPS Archive ledger path) + Notion promote + GH run artifact on close.
- **Ticket MUST name Tier 2.** Never default. Never infer.
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR. **Lead with** `**Tier 2** — Full Lab + ledger` in the same message, then full lab links. Never surface the lab box/CTA without naming Tier 2.
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

## Delivery — lead with the tier label (HARD)

Every View Understanding Lab / Hands completion instruction (Infra chat **and** harness footer copy) **must lead with** the tier label. First line, before any lab heading or links:

- `**Tier 0** — ship (no Understanding Lab)`
- `**Tier 1** — Light Understanding` + lab links
- `**Tier 2** — Full Lab + ledger` + full lab links

**Never** surface the Understanding Lab box/CTA without naming Tier 1 or Tier 2 in the **same** message. Tier 0 never gets the lab popup.

If the ticket omits `tier:` → treat as Tier 0 and **say so** (`**Tier 0** — ship (no Understanding Lab)` plus “ticket omitted `tier:`”).

| Tier | First line (required) | Lab box / CTA | Merge PASS |
|---|---|---|---|
| 0 | `**Tier 0** — ship (no Understanding Lab)` | No | Short what/why. Infra reviews. Gideon merges. |
| 1 | `**Tier 1** — Light Understanding` | Yes, after the label | Light PASS only |
| 2 | `**Tier 2** — Full Lab + ledger` | Yes, after the label | Full five-beat PASS only |

Full five-beat PASS is **not** the merge bar for every Lane A PR. CTA + full five-beat PASS apply only when the ticket names Tier 1–2 (Tier 2 for the full five beats; Tier 1 keeps the light bar).
