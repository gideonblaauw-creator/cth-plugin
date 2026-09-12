# Human-in-the-loop — HITL Lab (understanding loops)

**Source:** Geoffrey Litt (Notion design engineer), *Understanding is the new bottleneck* — [AI Engineer talk (~19:33)](https://www.youtube.com/watch?v=WkBPX-oDMnA)

## Thesis

Agents increasingly handle correctness verification. Humans stay in the loop to **understand to participate** across successive loops (creative leaps), not only thumbs-up verify. Unexplained agent velocity = cognitive debt.

## HITL Lab — 5-beat flow

For **major Lane A builds**, plant a collaborative HITL Lab in Notion. Walk reviewers through five beats in order:

```
Home → Explainer (quiz) → Micro world (sim) → Decisions DB → Next loop
```

| Beat | Artifact | Notes |
|---|---|---|
| 1. Home | Lab landing page | Context, links, language toggle, reviewer roster |
| 2. Explainer | ExplainDiff-style page + quiz | Background → Intuition → Walkthrough → 5 medium questions |
| 3. Micro world | Sim / scrubber / playground | **Between Explainer and Decisions** — feel the behavior |
| 4. Decisions DB | Shared database | Rationale, blockers, go/no-go rows; team participates |
| 5. Next loop | Handoff page | What ships, what returns, next cycle needs |

Microworld is beat 3 — after comprehension (Explainer + quiz), before team decisions. Micro world is the **key understanding step** (Explainer orients; Decisions records locked intent).

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
| Explainer + quiz | ~4 min |
| Micro world | ~3 min |
| Decisions DB | ~3 min |

Quiz = speed regulator. Do not mark **Approved** until quiz passed or waived with a one-line reason on the page.

## Collaborative

HITL Lab is a **shared space**. Team members participate via page comments and Decisions DB rows. Do not assume Gideon reviews alone.

## EN / ES

Lab pages support a **language toggle** — dual pages (EN + ES) or in-page switch. Default EN; mirror key beats for Spanish-speaking reviewers when the build touches ES audiences.

## Running demo (reference implementations)

| Demo | Subject | Use as template for |
|---|---|---|
| Dataroom Reviewer | `gideonblaauw-creator/cth-data-room-scanner` | Teclogi Lane A major PR |
| Synthetic VertiGreen | FabFloow / client product | Sim + decisions pattern |
| CleantechHUB Notion lab URLs | CTH Apps on allowlist repos | Full 5-beat flow |

## Three techniques (Geoffrey Litt pillars — Notion as HITL surface)

### i) Explanations

After meaningful agent work, write an **Explainer** page (ExplainDiff-style):

1. **Background** — What problem or change are we looking at?
2. **Intuition / essence** — The one-paragraph mental model.
3. **Literate walkthrough** — Step through the diff or decision with context, not a raw dump.
4. **Quiz** — Five medium-difficulty questions that test understanding, not trivia.

**Notion over local-only HTML** so teammates can comment and async review.

- Quiz = speed regulator. Do not mark **Approved** until the quiz is passed or waived with a one-line reason on the page.
- Use tasteful HTML blocks only (Notion HTML blocks for interactive figures). Avoid interactive slop.

### ii) Micro worlds

When behavior is hard to feel from prose alone, the agent builds an ephemeral UI, sim, or debugger:

- Scrubber, side-by-side migration view, playground, or similar.
- Host via a Notion HTML block or link to a throwaway demo.
- This is a **learning artifact**, not product scope.
- Archive the micro world when the mental model lands; keep the Explainer.
- In the 5-beat flow: beat 3, **after** Explainer, **before** Decisions DB.

### iii) Shared spaces

Plans, explainers, and decisions live in Notion multiplayer — not only in solo agent chat.

- Shared threads (humans + agents).
- Commentable plan docs.
- Decisions databases with human rationale recorded.

Collective understanding beats private laptop artifacts. Decisions DB = beat 4 in the HITL Lab flow.

## View HITL Lab delivery (major Lane A)

When Hands opens a **major** Lane A draft PR on an allowlist repo, the PR body **MUST** end with this block (fill real URLs):

```markdown
## View HITL Lab
- **Notion lab Home:** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Interactive HTML (stable host):** <URL from HITL static host — see harness § View HITL Lab>
- **Interactive HTML (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Decisions DB:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after ≤10 min HITL pass (Explainer → Microworld → Decisions).
```

**Cursor product limit:** The cloud-agent **View PR** card cannot host a native second button. Infra chat **must** post **View HITL Lab** as its own prominent link beside the agent card whenever a major Hands run finishes — not only links buried in the PR body.

**Stable HTML host:** `HITL_HTML_STABLE_URL` in `skills/harness/SKILL.md` until Infra plants Vercel/Tailscale. Paste helper: `docs/hitl-view-lab-footer.md`. Notion URLs: this file and `skills/notion/SKILL.md`.

## Operating rules

| Rule | Action |
|---|---|
| Understand to participate | HITL is for comprehension across loops, not rubber-stamp approval. |
| Major builds only | Full HITL Lab for substantive Lane A PRs; skip for tiny/mechanical work. |
| Cognitive debt pause | If velocity outpaces explanation, pause new work and write the Explainer first. |
| Collaborative | Shared space; team comments and Decisions rows; not solo Gideon. |
| Timebox | ≤ 10 min total human gate (Explainer ~4 · Microworld ~3 · Decisions ~3). |
| Secrets | Use Infisical (`skills/infisical/SKILL.md`); never paste tokens in Notion or chat. |
| Notion is not secrets SoT | Notion holds plans and rationale; credentials stay in Infisical. |
