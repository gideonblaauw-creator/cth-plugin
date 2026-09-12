---
name: langgraph-production
description: >
  Builds production LangGraph agent graphs with HITL interrupt, Notion
  Understanding Lab, checkpoint memory, and LangSmith evals. Use when:
  langgraph: yes on a ticket, production agent graph, client agent graph,
  HITL interrupt, LangGraph checkpoint, LangSmith eval. Do not use when:
  OpenCode OSS experiments, grant packs, or skill-only harness edits.
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
  adopted: "2026-09-12"
---

# LangGraph Production — Hands lane

Hands builds **client and production** agent graphs on this lane only: LangGraph + HITL `interrupt` ↔ Notion Understanding Lab + LangSmith. OpenCode is OSS experiments only.

**Owner:** Infrastructure Desk
**Model:** `composer-2.5` (`fast=false`) — never Fast, never Flash
**HITL:** draft PR; Infrastructure PASS; Gideon merges. HITL before any client deploy.

## When to use

Use this playbook when the ticket sets `langgraph: yes`.

| Ticket signal | Meaning |
|---|---|
| `langgraph: yes` | Production / client agent graph. Follow this skill. Lane A on the **owning product repo**. |
| `langgraph:` omitted | Not this lane. Do not open a production graph. |
| OpenCode / OSS scratch | Experiments and Academy notebook forks only. Never a client deploy path. |

Pair with existing Lane A fields. `tier:` and `lab_notion:` keep the Understanding Lab lock from `docs/understanding-lab-tiers.md`.

```
desk: <owning Desk>
folder: <owning repo path>
done-when: graph compiles; HITL interrupt resumes from this build’s lab; eval fixtures pass
model: composer-2.5 (fast=false)
lane: github-pr
langgraph: yes
tier: 0 | 1 | 2
escalate:
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
hitl: draft PR; no client deploy; no secrets in repo
reviewer: Infrastructure
```

**Done when:** ticket has `langgraph: yes`, names the owning repo, and Hands has read this file before writing graph code.

## Desk routing

- **Client agent graphs and production agents** — this Hands lane only (`composer-2.5`, `fast=false`, Lane A on the owning repo).
- **OpenCode** — OSS experiments and public-notebook mirrors only. Never a client or production deploy path.
- **This repo (`cth-plugin`)** — playbook and ticket fields only. Graph code lives on the owning product repo (Lane A lock in `skills/harness/SKILL.md` §5).
- Wrong repo = miss. Do not plant a Teclogi graph on `cth-plugin`. Do not plant LexiScan on `cth-data-room-scanner`.

## Version pins (plant 2026-09-12)

Pin these exact versions in the owning repo. Do not write `latest` or unbounded `>=`.

| Package | Pin | Source (PyPI, 2026-09-12) |
|---|---|---|
| `langgraph` | `1.2.11` | https://pypi.org/project/langgraph/1.2.11/ (stable, released 2026-08-11) |
| `langgraph-checkpoint` | `4.2.0` | https://pypi.org/project/langgraph-checkpoint/4.2.0/ |
| `langsmith` | `0.12.4` | https://pypi.org/project/langsmith/0.12.4/ |

```
langgraph==1.2.11
langgraph-checkpoint==4.2.0
langsmith==0.12.4
```

Bump pins only on a later ticket that names new versions. Optional extras (`langgraph-checkpoint-postgres`, `langgraph-checkpoint-sqlite`) get their own explicit pins on that ticket — do not float them.

**Done when:** the owning repo lockfile or requirements list these three pins verbatim.

## Workflow

1. **Confirm the ticket** — Require `langgraph: yes`, owning `repo_url`, `composer-2.5` (`fast=false`), and HITL “no client deploy.” Read `tier:` and `lab_notion:`. Done when: fields present or Desk flagged; no graph work on a missing `langgraph: yes`.
2. **Design graph and state** — Write typed state, nodes, and edges before code. Done when: a short state map lists keys, reducers, and which node may `interrupt()`.
3. **Wire HITL** — Call `interrupt()` at the human gate. Map the payload to this build’s Notion lab URLs. Done when: resume uses `Command(resume=…)` on the same `thread_id`.
4. **Checkpoint memory** — Compile with a durable checkpointer in production. Done when: `MemorySaver` is local-only and production uses a pinned durable store.
5. **Eval fixtures** — Add golden cases in-repo (no secrets) and a LangSmith dataset name. Done when: one offline eval command is documented and passes on the fixture set.
6. **Draft PR** — Open a draft PR on the owning repo. Infra reviews. Gideon merges and deploys. Done when: draft URL returned; no merge; no client deploy.

## Graph / state design basics

Keep the first production graph small. Prefer one compiled graph over a nest of implicit agents.

1. **State** — Use a typed schema (`TypedDict` or dataclass). Every key must be JSON-serializable. List fields need an explicit reducer. Do not store API keys, tokens, or raw credentials in state.
2. **Nodes** — One job per node. Return a partial state update. Side effects (email, write, spend) sit **after** an `interrupt()` approval node.
3. **Edges** — Static edges for the happy path. Conditional edges only when the branch is testable with a fixture.
4. **Compile** — `graph = builder.compile(checkpointer=…)` with a `thread_id` in `config={"configurable": {"thread_id": …}}`. The thread id is the persistent cursor.
5. **Traces** — Enable LangSmith tracing via Infisical key names (`LANGSMITH_API_KEY`, `LANGSMITH_TRACING`). Never paste key values.

Docs: [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview), [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api).

**Done when:** a reviewer can name the state keys and the interrupt node in one minute.

## HITL `interrupt` ↔ Notion Understanding Lab

LangGraph pauses with `interrupt()` and a durable checkpointer. The human reviews in **this build’s** Notion Understanding Lab. Resume with `Command(resume=…)` on the same `thread_id`.

```python
from langgraph.types import Command, interrupt

def approval_node(state: State):
    decision = interrupt({
        "kind": "approval",
        "summary": state["summary"],
        "lab_notion": state.get("lab_notion"),
    })
    return {"decision": decision}
```

Resume (same `thread_id`):

```python
graph.invoke(Command(resume={"approved": True}), config=config)
```

Docs: [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts). Payloads are JSON-serializable. The node restarts from its beginning on resume — keep work before `interrupt()` idempotent.

### Tier mapping

| Ticket `tier:` | Graph HITL | Notion lab |
|---|---|---|
| `0` or omitted | Still pause on `interrupt()` before any client-visible or irreversible act. Short what/why on the PR. | **No lab. No CTA.** Do not invent pages. |
| `1` + `escalate:` | Interrupt payload feeds a light lab: Context ≤½ page, one Playground scenario (2–3 options), one Shared decision row. | Copy **this ticket’s** `lab_notion:` URLs only. Light PASS. |
| `2` + `escalate:` | Interrupt payload feeds the full five beats + ledger. | Copy **this ticket’s** `lab_notion:` URLs only. Full five-beat PASS. |

Canonical tier lock: `docs/understanding-lab-tiers.md`. Footer: `docs/view-understanding-lab-footer.md`. Notion playbook: `skills/notion/SKILL.md`.

### Per-build `lab_notion:` (hard gate)

- Every product / build gets its own Understanding Lab pages. Hands copies URLs from the ticket (`lab_notion:` or `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`).
- **Never** reuse Scanner / Dataroom / VertiGreen pages for LexiScan, Sustenttia, or any other product.
- Tier 1–2 without URLs: flag the Desk. Open the draft PR without a filled lab footer. Do not invent pages.
- LexiScan lab pages: FabFloow owns.

**Done when:** interrupt payload is reviewable; resume path is documented; lab URLs (if Tier 1–2) match this ticket only.

## Memory store patterns (checkpointing)

Checkpointing is the production memory store. It writes the exact graph state so HITL and crashes can resume.

| Environment | Store | Rule |
|---|---|---|
| Local / Academy mirror | `MemorySaver` | In-process only. Never a client deploy. |
| Production | Durable checkpointer (Postgres preferred) | Pin the extra package on that ticket. Same `thread_id` to resume. |
| Private residency | Stay on `127.0.0.1` | Harness private axis. Do not send raw client state off-box. |

- One `thread_id` per job or conversation. A new id starts empty state.
- Production checkpointers need Infisical for DSN / API keys — names only on the ticket.
- Do not checkpoint secrets. Redact before write.

Docs: [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence). Package pin: `langgraph-checkpoint==4.2.0`.

**Done when:** production compile uses a durable checkpointer; local tests may use `MemorySaver`.

## Eval fixtures

Ship fixtures **before** a client deploy.

1. **In-repo fixtures** — JSON or YAML cases: input state, expected interrupt kind, expected resume, expected output keys. No live tokens. No client raw PII.
2. **LangSmith dataset** — Name the dataset on the ticket (`langsmith_dataset:`). Create or update it with the Infisical `LANGSMITH_API_KEY`. Do not commit run payloads that contain secrets.
3. **Offline eval** — One documented command that runs the fixture set against the compiled graph (or a recorded trace). Fail the PR if the fixture set regresses.
4. **Online eval** — After Module 1–3 checkpoint only. Point to LangSmith Production Monitoring (later course). Do not invent an online eval on the first dogfood ticket.

Docs: [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation). SDK pin: `langsmith==0.12.4`.

**Done when:** the PR lists the fixture path, the dataset name, and a passing offline run note.

## Deploy / monitor checklist

Hands does **not** deploy. Gideon deploys after Infra PASS.

Finish **Module 1–3** (graph, state, HITL) on the owning repo before any Module 4–6 deploy work. Later tickets point at LangSmith Deployment and Production Monitoring — do not grind those courses on the first graph ticket.

Pre-deploy checklist (owning repo, after Gideon merge):

- [ ] Pins are `langgraph==1.2.11`, `langgraph-checkpoint==4.2.0`, `langsmith==0.12.4`
- [ ] Durable checkpointer compiled in; `MemorySaver` not used in prod
- [ ] HITL `interrupt` sits before irreversible acts; resume path tested
- [ ] Tier 1–2 lab URLs are this build’s only (or Tier 0 with no lab CTA)
- [ ] Eval fixtures pass; LangSmith tracing key names come from Infisical
- [ ] No secrets in git, Notion, or chat
- [ ] Draft PR reviewed; Gideon merges and deploys

Later course pointers (after the Module 1–3 checkpoint):

- Public notebooks Module 4–6: https://github.com/langchain-ai/langchain-academy (Academy README: Module 6 covers deploying agents)
- [LangSmith Deployment](https://docs.langchain.com/langsmith/deployment)
- [LangSmith observability](https://docs.langchain.com/langsmith/observability)

**Done when:** the checklist is in the PR body. Deploy stays with Gideon.

## Curriculum access

| Source | Use | Do not |
|---|---|---|
| Public notebooks https://github.com/langchain-ai/langchain-academy | Read and mirror into `langgraph-lab` (separate Hands) | Do not vendor Academy secrets |
| LangGraph docs https://docs.langchain.com/oss/python/langgraph/overview | Graph, interrupt, persistence | Do not invent APIs |
| LangSmith docs https://docs.langchain.com/langsmith | Evals, tracing, later deploy/monitor | Do not paste API keys |
| Academy video https://academy.langchain.com/courses/intro-to-langgraph | Gideon enroll **optional** | Never put Academy passwords in chat, tickets, or PRs |

API keys (`LANGSMITH_API_KEY`, model keys, checkpointer DSNs) → **Infisical only** (`skills/infisical/SKILL.md`). Ticket project / environment / key **names**. Never values.

**Done when:** Hands used public notebooks + docs only; no Academy password appeared in the run.

## Lab repo

Private `gideonblaauw-creator/langgraph-lab` holds mirrored Academy notebooks and CTH wrappers.

- Hands creates that repo on a **separate** ticket after Gideon marks the app-build row (`skills/app-build/SKILL.md`).
- This playbook does **not** create the repo, open that branch, or copy `/opt/claude-files`.
- Until the repo exists, Hands reads the public Academy notebooks and official docs.

**Done when:** a later Hands ticket has a Gideon-marked row before anyone creates `langgraph-lab`.

## Dogfood order

1. **`cth-data-room-scanner` first** — Teclogi-only Lane A repo. First production graph lives there.
2. **Then FabFloow LexiScan L2** — own lab pages. Never reuse Scanner Notion URLs.

Do not implement the scanner graph or LexiScan on a playbook-only ticket. Each dogfood step is its own `langgraph: yes` ticket on the owning repo.

**Done when:** desks ticket scanner before LexiScan; each ticket carries its own `lab_notion:` URLs.

## Rules

- No secrets in the repo, PR, Notion, or chat. Infisical is durable SoT.
- HITL before any client deploy. Draft PR only. Infra reviews. Gideon merges and deploys.
- Client / production graphs use this lane. OpenCode is OSS experiments only.
- Pin the three package versions above. No floating `latest`.
- Per-build `lab_notion:` URLs. Never reuse Scanner pages for other products.
- Do not create `langgraph-lab`, enroll Academy, or grind the LangSmith Deployment course on this playbook.

## Do not use when

- OpenCode OSS experiment or public-notebook scratch → OpenCode lane, not this skill
- Grant / donor pack → `cth-grant`
- Commercial proposal (no agent graph) → `cth-proposal-build`
- Harness / ticket rulebook only → `harness`
- Promote or create a repo → `app-build` (Gideon marks the row first)
- Fetch or rotate credentials → `infisical` / `secrets` (Claude Desktop only for `secrets`)

## Related skills

| Skill | When |
|---|---|
| `harness` | Ticket contract, token lock, Lane A repo lock, tiers |
| `notion` | Understanding Lab beats, per-build URLs, PR footer |
| `infrastructure-comms` | Infra review, Tier label in Gideon chat, no merge |
| `app-build` | Creating `langgraph-lab` after Gideon marks the row |
| `infisical` | Key names for LangSmith and checkpointer DSNs |
| `teclogi-comms` | Scanner dogfood tickets (owning repo, not this skill’s plant) |
