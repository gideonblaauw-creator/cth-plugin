# Human-in-the-loop — Understanding Lab

**Source:** Geoffrey Litt (Notion design engineer), *Understanding is the new bottleneck* — [AI Engineer talk (~19:33)](https://www.youtube.com/watch?v=WkBPX-oDMnA)

**Synonym map (legacy → locked):** Home → Context · Explainer → Explanation (+ quiz) · Micro world / Microworld → Playground · Decisions DB (beat) → Shared decisions · Next loop → Next cycle · HITL Lab → Understanding Lab · View HITL Lab → View Understanding Lab. Existing Notion page titles may still use legacy names.

## Thesis

Agents increasingly handle correctness verification. Humans stay in the loop to **understand to participate** across successive loops (creative leaps), not only thumbs-up verify. Unexplained agent velocity = cognitive debt.

## Understanding Lab — 5-beat flow

For **major Lane A builds**, plant a collaborative **Understanding Lab** in Notion. Walk reviewers through five beats in this order only:

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

## Gate policy — major builds only

| Applies | Does not apply |
|---|---|
| CTH Apps, client products, Tools, FabFloow products | Tiny/mechanical PRs (copy, inventories, stub-only edits) |
| Substantive Lane A PRs on allowlist repos | Wrong-repo or out-of-scope work |

**Trigger:** major PRs only on **Lane A allowlist repos** (`skills/harness/SKILL.md` § Lane A repo lock).

**Maker ≠ checker:** Hands plants the lab and opens a **draft** PR. Infrastructure Desk reviews. Gideon merges.

## Timebox

Total human gate ≤ **10 minutes** (suggested):

| Segment | Target |
|---|---|
| Explanation + quiz | ~4 min |
| Playground | ~3 min |
| Shared decisions | ~3 min |

Quiz = speed regulator. Do not mark **Approved** until quiz passed or waived with a one-line reason on the page.

## Collaborative

Understanding Lab is a **shared space**. Team members participate via page comments and Shared decisions rows. Do not assume Gideon reviews alone.

## EN / ES

Lab pages support a **language toggle** — dual pages (EN + ES) or in-page switch. Default EN; mirror key beats for Spanish-speaking reviewers when the build touches ES audiences.

## Running demo (reference implementations)

| Demo | Subject | Use as template for |
|---|---|---|
| Dataroom Reviewer | `gideonblaauw-creator/cth-data-room-scanner` | Teclogi Lane A major PR |
| Synthetic VertiGreen | FabFloow / client product | Playground + Shared decisions pattern |
| CleantechHUB Notion lab URLs | CTH Apps on allowlist repos | Full 5-beat flow |

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

### iii) Shared spaces (beat 4)

Plans, explanations, and decisions live in Notion multiplayer — not only in solo agent chat.

- Shared threads (humans + agents).
- Commentable plan docs.
- Shared decisions databases with human rationale recorded (Notion page title may still read Decisions DB).

Collective understanding beats private laptop artifacts. **Shared decisions** = beat 4 in the Understanding Lab flow.

## View Understanding Lab delivery (major Lane A)

When Hands opens a **major** Lane A draft PR on an allowlist repo, the PR body **MUST** end with this block (fill real URLs):

```markdown
## View Understanding Lab
- **Context (Notion):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (stable HTML):** HITL_HTML_STABLE_URL
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after ≤10 min Understanding Lab pass (Explanation → Playground → Shared decisions).
```

**Cursor product limit:** The cloud-agent **View PR** card cannot host a native second button. Infra chat **must** post **View Understanding Lab** as its own prominent link beside the agent card whenever a major Hands run finishes — not only links buried in the PR body.

**Stable HTML host:** `HITL_HTML_STABLE_URL` in `skills/harness/SKILL.md` until Infra plants Vercel/Tailscale. Paste helper: `docs/view-understanding-lab-footer.md`. Notion URLs: this file and `skills/notion/SKILL.md`.

## Operating rules

| Rule | Action |
|---|---|
| Understand to participate | HITL is for comprehension across loops, not rubber-stamp approval. |
| Major builds only | Full Understanding Lab for substantive Lane A PRs; skip for tiny/mechanical work. |
| Cognitive debt pause | If velocity outpaces explanation, pause new work and write the Explanation first. |
| Collaborative | Shared space; team comments and Shared decisions rows; not solo Gideon. |
| Timebox | ≤ 10 min total human gate (Explanation ~4 · Playground ~3 · Shared decisions ~3). |
| Playground hard gate | Beat 3: `scenario → consequences → options → choose`; not scrub-only or single-suggestion override. |
| Secrets | Use Infisical (`skills/infisical/SKILL.md`); never paste tokens in Notion or chat. |
| Notion is not secrets SoT | Notion holds plans and rationale; credentials stay in Infisical. |
