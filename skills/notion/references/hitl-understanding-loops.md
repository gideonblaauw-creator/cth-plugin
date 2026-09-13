# Human-in-the-loop — Understanding Lab

**Source:** Geoffrey Litt (Notion design engineer), *Understanding is the new bottleneck* — [AI Engineer talk (~19:33)](https://www.youtube.com/watch?v=WkBPX-oDMnA)

**Synonym map (legacy → locked):** Home → Context · Explainer → Explanation (+ quiz) · Micro world / Microworld → Playground · Decisions DB (beat) → Shared decisions · Next loop → Next cycle · HITL Lab → Understanding Lab · View HITL Lab → View Understanding Lab. Existing Notion page titles may still use legacy names.

## Thesis

Agents increasingly handle correctness verification. Humans stay in the loop to **understand to participate** across successive loops (creative leaps), not only thumbs-up verify. Unexplained agent velocity = cognitive debt.

## Understanding Lab — 5-beat flow

For **Tier 2** tickets only, plant a collaborative **Understanding Lab** in Notion and walk reviewers through five beats in this order only. Tier 1 is a light subset. Tier 0 plants no lab. Canonical lock: `docs/understanding-lab-tiers.md`.

```
Context → Explanation (quiz) → Playground → Shared decisions → Next cycle
```

| Beat | Artifact | Notes |
|---|---|---|
| 1. Context | Lab landing page | Context, links, language toggle, reviewer roster |
| 2. Explanation (+ quiz) | ExplainDiff-style page + quiz | Background → Intuition → Walkthrough → 5 medium questions |
| 3. Playground | Scenario-based interactive surface | **Key understanding step** — see Playground definition below |
| 4. Shared decisions | Shared database (Notion page may still be titled Decisions DB) | Rationale, blockers, go/no-go rows; team participates **after** Playground choice |
| 5. Next cycle | Handoff page | What ships, what returns, next cycle needs |

Playground is beat 3 — after comprehension (Explanation + quiz), before Shared decisions. Playground is the **key understanding step** (Explanation orients; Shared decisions records locked intent).

### Playground definition (Gideon 2026-09-12 — hard)

Playground is **not** only scrubbing agent findings or agree/override/defer on one suggestion.

Playground **must**:

1. Give **scenarios** — concrete situations tied to the build.
2. Surface **consequences** of each path (what happens if…).
3. Give **optionality** — especially when the reviewer is less familiar with the topic: the agent proposes **2–4 clear alternative options** with tradeoffs, not a single forced recommendation.
4. Let the human pick / combine / defer **before** Shared decisions records the lock.

**Flow inside beat 3:** `scenario → consequences → options → choose` — then proceed to Shared decisions.

## Gate policy — Understanding Lab tiers (Gideon 2026-09-12)

Desks **default Tier 0**. Ticket must name `tier: 1` or `tier: 2` (or `escalate:` one-liner). Do not infer a lab from “major” scope. `major: yes` without `tier:` is a miss.

| Tier | Applies when | Does not apply | PASS |
|---|---|---|---|
| **0 — Ship (DEFAULT)** | Internal, familiar, low blast radius | — | No lab. Short what/why. |
| **1 — Light Understanding** | Agent-heavy, client-facing, or “don’t fully feel this” + named escalate reason | Ticket omitted the reason | Light PASS (Context ≤½ page + Playground light + one Shared decision row). Skip essay, quiz, stable host, event-store. |
| **2 — Full Lab + ledger** | Donor/audit, unfamiliar domain, production agent permissions, or cited-later decision. **Ticket MUST name Tier 2.** | Inferred / defaulted Tier 2 | Full five-beat PASS + `events.jsonl` + Notion promote + GH run artifact. |

**Trigger:** Tier 1–2 only on **Lane A allowlist repos** (`skills/harness/SKILL.md` § Lane A repo lock).

**Maker ≠ checker:** Hands plants the lab when the ticket names Tier 1–2 and opens a **draft** PR. Infrastructure Desk reviews. Gideon merges.

**One-liner:** Push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.

## Timebox

| Tier | Target |
|---|---|
| 0 | No lab timebox — short what/why |
| 1 | Light bar only. Kill if >30 min human time with no clearer decision → strip |
| 2 | ≤ **10 minutes** total (Explanation + quiz ~4 · Playground ~3 · Shared decisions ~3) |

Quiz (Tier 2) = speed regulator. Do not mark **Approved** until quiz passed or waived with a one-line reason on the page.

## Collaborative

Understanding Lab is a **shared space**. Team members participate via page comments and Shared decisions rows. Do not assume Gideon reviews alone.

## EN / ES

Lab pages support a **language toggle** — dual pages (EN + ES) or in-page switch. Default EN; mirror key beats for Spanish-speaking reviewers when the build touches ES audiences.

## Running demo (reference implementations)

These are **pattern templates**, not default CTA URLs. Every build / product gets its own Understanding Lab Notion page(s) (Gideon 2026-09-12 via FabFloow). Do not reuse Scanner / VertiGreen pages for LexiScan, Sustenttia, or other products.

| Demo | Subject | Use as template for |
|---|---|---|
| Dataroom Reviewer | `gideonblaauw-creator/cth-data-room-scanner` | Teclogi Lane A **Tier 1–2** PR (ticket must name the tier **and** Scanner lab URLs) |
| Synthetic VertiGreen | FabFloow / client product | Playground + Shared decisions pattern — **not** a fallback URL |
| CleantechHUB Notion lab URLs | CTH Apps on allowlist repos | Full 5-beat flow — **per build** |

## Three techniques (Geoffrey Litt pillars — Notion as HITL surface)

### i) Explanations (beat 2)

After meaningful agent work, write an **Explanation** page (ExplainDiff-style):

1. **Background** — What problem or change are we looking at?
2. **Intuition / essence** — The one-paragraph mental model.
3. **Literate walkthrough** — Step through the diff or decision with context, not a raw dump.
4. **Quiz** — Five medium-difficulty questions that test understanding, not trivia.

**Notion over local-only HTML** so teammates can comment and async review.

- Quiz = speed regulator. Do not mark **Approved** until the quiz is passed or waived with a one-line reason on the page.
- Use tasteful HTML blocks only (Notion HTML blocks for interactive figures). Avoid interactive slop.

### ii) Playground (beat 3)

When behavior is hard to feel from prose alone — see **Playground definition** above (hard gate):

- Scenarios tied to the build, with consequences per path.
- **2–4 alternative options** with tradeoffs (not a single forced recommendation).
- Host via Notion HTML block, stable HTML, or local fallback.
- Flow: `scenario → consequences → options → choose`.
- Human picks / combines / defers **before** Shared decisions. Archive Playground when the mental model lands; keep the Explanation.

**HTML artifact standard (Gideon t1268u):** Tier 1–2 repo playgrounds use the **LexiScan house-tour format** — canonical path `understanding-lab/playground/` in https://github.com/gideonblaauw-creator/fabfloow-lexiscan (PR #16). Interactive floor-plan navigation; per-room quests, quiz, and decision doors; EN+ES; decision ledger export. Notion example: Playground — LexiScan L1 laboral (https://app.notion.com/p/3d9dfee50be981e08a7bfffe2cc2f33f). Full checklist and anti-patterns: `docs/understanding-lab-playground-standard.md`. Scanner’s legacy tabbed microworld (Context / Explainer / Decision Tree / …) is a **legacy shell** — remediate toward LexiScan standard; do not copy that shell for new products.

### iii) Shared spaces (beat 4)

Plans, explanations, and decisions live in Notion multiplayer — not only in solo agent chat.

- Shared threads (humans + agents).
- Commentable plan docs.
- Shared decisions databases with human rationale recorded (Notion page title may still read Decisions DB).

Collective understanding beats private laptop artifacts. **Shared decisions** = beat 4 in the Understanding Lab flow.

## View Understanding Lab delivery (Tier 1–2 only)

CTA **View Understanding Lab** and full five-beat PASS apply **only** when the ticket names Tier 1 or Tier 2. **Not** every Lane A merge. Tier 0: omit this block.

When Hands opens a **Tier 1 or Tier 2** Lane A draft PR on an allowlist repo **and the ticket supplied this build’s lab URLs**, the PR body **MUST** end with the matching footer in `docs/view-understanding-lab-footer.md`. Fill placeholders from the ticket (`lab_notion:` or `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`). Never default to Scanner page IDs. Tier 2 full five-beat block:

```markdown
## View Understanding Lab
- **Tier:** 2
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion):** <lab_context_url>
- **Playground (stable HTML):** <lab_playground_url or HITL_HTML_STABLE_URL>
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** <lab_shared_decisions_url>

**Gate:** Draft only. Infra reviews. Gideon merges after full five-beat PASS (Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle).
```

Tier 1 uses the **light** footer in the same helper. Gate line must say light PASS, not full five-beat PASS.

If the ticket omitted lab URLs: omit the filled footer. Infra posts Tier label + View PR only and flags missing lab pages. Do **not** paste Scanner / VertiGreen / Dataroom links.

**Cursor product limit:** The cloud-agent **View PR** card cannot host a native second button. Infra chat **must** post **View Understanding Lab** as its own prominent link beside the agent card on **Tier 1–2** Hands completion **only when this build’s lab URLs are on the ticket** — not only links buried in the PR body, and **not** on Tier 0.

**Stable HTML host:** `HITL_HTML_STABLE_URL` in `skills/harness/SKILL.md` until Infra plants Vercel/Tailscale. Required for Tier 2; skip as a requirement on Tier 1. Paste helper: `docs/view-understanding-lab-footer.md`. Notion URLs come from the **ticket**, not from this file. Do not rewrite live Notion page content in this lock.

## Operating rules

| Rule | Action |
|---|---|
| Understand to participate | HITL is for comprehension across loops, not rubber-stamp approval. |
| Default Tier 0 | No lab and no CTA unless the ticket names Tier 1–2 or an escalate reason. |
| CTA + full five-beat PASS only for Tier 1–2 | CTA on both; full five-beat PASS is Tier 2 only (Tier 1 = light PASS). Not every Lane A merge. |
| Playground > paperwork | If budget for one beat: options→choose. |
| Ledger follows tier | Tier 1 = disk/Notion row; Tier 2 = `events.jsonl`. |
| Playground hard lock (Tier 1–2) | `scenario → consequences → options → choose`; not scrub-only or single-suggestion override. |
| Kill | Tier 1 >30 min human with no clearer decision → strip; Tier 0 you can’t re-explain in a week → next similar job Tier 1. |
| Cognitive debt pause | If velocity outpaces explanation, escalate the next similar job to Tier 1. |
| Collaborative | Shared space; team comments and Shared decisions rows; not solo Gideon. |
| Secrets | Use Infisical (`skills/infisical/SKILL.md`); never paste tokens in Notion or chat. |
| Notion is not secrets SoT | Notion holds plans and rationale; credentials stay in Infisical. |
