# Human-in-the-loop — understanding loops

**Source:** Geoffrey Litt (Notion design engineer), *Understanding is the new bottleneck* — [AI Engineer talk (~19:33)](https://www.youtube.com/watch?v=WkBPX-oDMnA)

## Thesis

Agents increasingly handle correctness verification. Humans stay in the loop to **understand to participate** across successive loops (creative leaps), not only thumbs-up verify. Unexplained agent velocity = cognitive debt.

## Three techniques (Notion as HITL surface)

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

### iii) Shared spaces

Plans, explainers, and decisions live in Notion multiplayer — not only in solo agent chat.

- Shared threads (humans + agents).
- Commentable plan docs.
- Decisions databases with human rationale recorded.

Collective understanding beats private laptop artifacts.

## Operating rules

| Rule | Action |
|---|---|
| Understand to participate | HITL is for comprehension across loops, not rubber-stamp approval. |
| Cognitive debt pause | If velocity outpaces explanation, pause new work and write the Explainer first. |
| Secrets | Use Infisical (`skills/infisical/SKILL.md`); never paste tokens in Notion or chat. |
| Notion is not secrets SoT | Notion holds plans and rationale; credentials stay in Infisical. |
