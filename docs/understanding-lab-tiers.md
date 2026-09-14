# Understanding Lab tiers (Gideon lock 2026-09-12)

**One-liner:** Push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.

Canonical lock for Lane A desks. Playbook surfaces: `skills/harness/SKILL.md` § View Understanding Lab, `skills/notion/SKILL.md`, `skills/infrastructure-comms/SKILL.md` §7. Delivery helper: `docs/view-understanding-lab-footer.md`.

**Per-build pages:** every build / product gets its own Understanding Lab Notion page(s). Do not reuse Scanner lab pages for LexiScan or other products.

**Playground format (Gideon lock t1268u):** Tier 1–2 playgrounds use the **LexiScan house-tour HTML standard** — interactive floor-plan navigation, per-room quests/quiz/decision doors, EN+ES, decision ledger export. Canonical template: `docs/understanding-lab-playground-standard.md`. Do not invent a new layout per product.

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
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR — **this build’s** Notion URLs from the ticket. Never Scanner defaults.
- **PASS:** light bar above — **not** full five-beat PASS.

## Tier 2 — Full Lab + ledger (rare)

- **When:** donor/audit, unfamiliar domain, production agent permissions, or decision will be cited later.
- **Bar:** full five beats (`Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle`) + append `events.jsonl` (VPS Archive ledger path) + Notion promote + GH run artifact on close.
- **Ticket MUST name Tier 2.** Never default. Never infer.
- **CTA:** View Understanding Lab on the draft PR + Infra chat link beside View PR — **this build’s** Notion URLs from the ticket. Never Scanner defaults.
- **PASS:** full five-beat PASS only. Event-store *implementation* is out of scope here — Hands appends the ledger file when Infra has planted the Archive path.

## Operating rules

1. **Default Tier 0.**
2. **Playground > paperwork** (if budget for one beat: options→choose).
3. **Ledger follows tier:** Tier 1 = disk/Notion row; Tier 2 = `events.jsonl`.
4. **Harness CTA “View Understanding Lab” only on Tier 1–2 PRs** — not every Lane A merge. CTA links are **per-build**; never default to Scanner / VertiGreen / Dataroom pages.
5. **Kill:** Tier 1 >30 min human time with no clearer decision → strip; Tier 0 ship you can’t re-explain in a week → next similar job Tier 1.

## Playground hard lock (Tier 1–2)

Keep Playground hard lock for Tier 1–2: `scenario → consequences → options → choose`.

- Tier 1: one scenario, 2–3 options with tradeoffs, then choose.
- Tier 2: full Playground hard gate (scenarios + consequences + 2–4 option paths with tradeoffs) before Shared decisions.
- Not scrub-only. Not a single-suggestion override.

**Artifact format (t1268u):** implement beat 3 as a **LexiScan-standard HTML house tour** at `understanding-lab/playground/` in the product repo (`index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh`). Scanner’s legacy tabbed microworld shell is not the template for new builds. Full checklist: `docs/understanding-lab-playground-standard.md`. **Stable host (LexiScan reference):** https://fabfloow-ul-playground.vercel.app — not the LexiScan product demos (`fabfloow-lexiscan.vercel.app` DEMO, `fabfloow-lexiscan-app.vercel.app` PROD).

## Ticket fields

```
tier: 0 | 1 | 2
escalate:
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
```

Flat aliases also work: `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url` on the ticket root.

| Signal | Meaning |
|---|---|
| `tier:` omitted or `0` | Default Ship. No lab. No CTA. Lab URL fields unused. |
| `tier: 1` + `escalate:` one-liner | Light Understanding. CTA. Light PASS. **Must** supply this build’s Notion lab URLs. |
| `tier: 2` (must be named) + `escalate:` one-liner | Full Lab + ledger. CTA. Full five-beat PASS. **Must** supply this build’s Notion lab URLs. |
| `major: yes` without `tier:` | **Miss.** Do not treat as lab. Default Tier 0 and flag the Desk to name a tier or reason. |
| Tier 1–2 without lab URLs | **Miss on the lab CTA only.** Infra posts Tier label + View PR, flags missing lab pages, and does **not** paste Scanner / VertiGreen / Dataroom links. |

## Per-build Notion lab pages (Gideon 2026-09-12 via FabFloow)

**Every build / product gets its own Understanding Lab Notion page(s).** Do not reuse Scanner (Dataroom / VertiGreen) lab pages for LexiScan, Sustenttia, or any other product.

- Every **Tier 1–2** ticket **must** supply that build’s Notion lab URLs (`lab_notion:` or the three flat `lab_*_url` fields).
- Hands copies **only** those ticket URLs into the PR footer. Hands never invents a URL and never falls back to Scanner pages.
- Footer templates use placeholders (`<lab_context_url>`, `<lab_playground_url>`, `<lab_shared_decisions_url>`). Scanner page IDs are **not** a default for all products.
- If a Tier 1–2 ticket omits lab URLs: Infra posts the Tier label + View PR only and flags missing lab pages. Infra **does not** paste Scanner VertiGreen / Dataroom links and **does not** post View Understanding Lab until the Desk supplies this build’s pages.
- Scanner / Teclogi: the Desk may supply the existing Scanner lab pages **on that Scanner ticket only**. Those URLs stay Scanner-only.
- Creating LexiScan (or other product) Notion pages is **not** a Hands default — FabFloow owns LexiScan lab pages. Flag the gap; do not invent pages or borrow Scanner URLs.

## Delivery (CTA + PASS)

**Infra chat first line** (Gideon lock 2026-09-12): every Hands completion leads with the Tier label **before** View PR / View Understanding Lab.

| Tier | Infra first line (Gideon chat) | View Understanding Lab CTA | Merge PASS |
|---|---|---|---|
| 0 | `**Tier 0** — Ship` then View PR. **No** lab CTA. | No | Short what/why. Infra reviews. Gideon merges. |
| 1 | `**Tier 1** — Light Understanding` then View PR then **this build’s** lab links | Yes (PR footer + Infra chat) — **only** with ticket `lab_notion:` URLs | Light PASS only |
| 2 | `**Tier 2** — Full Lab + ledger` then View PR then **this build’s** lab links | Yes (PR footer + Infra chat) — **only** with ticket `lab_notion:` URLs | Full five-beat PASS only |
| 1–2, lab URLs omitted | Tier label then View PR. Flag missing lab pages. **No** Scanner / VertiGreen / Dataroom paste. | No until the Desk supplies this build’s pages | Do not treat Scanner pages as the lab |

Full five-beat PASS is **not** the merge bar for every Lane A PR. CTA + full five-beat PASS apply only when the ticket names Tier 1–2 (Tier 2 for the full five beats; Tier 1 keeps the light bar) **and** supplies this build’s Notion lab URLs. Infra never leads Gideon chat with the lab CTA. Infra never defaults to Scanner lab pages.
