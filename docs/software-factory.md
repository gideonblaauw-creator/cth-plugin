# Software Factory v0 (Gideon lock 2026-09-14)

**One-liner:** Lane A Apps+Software builds follow a locked five-step conveyor through draft PR, Infra PASS, optional Understanding Lab, then Gideon merge.

**Owner:** Infrastructure (same ownership model as the Understanding Lab playground format lock).

**Skill:** `skills/software-factory/SKILL.md`  
**Harness pointer:** `skills/harness/SKILL.md` § Software Factory  
**Tier mapping:** `docs/understanding-lab-tiers.md`

---

## Locked conveyor

```
1 Isolate → 2 Build → 3 Prove(eng) → 4 Ship → 5 Understanding Lab → Gideon merge
```

| Step | Name | Who | PASS bar |
|---|---|---|---|
| **1** | **Isolate** | Cloud Hands | Branch off `main` on the owning Lane A repo (`cursor/<descriptive>-<suffix>`). No local worktree skill in v0. |
| **2** | **Build** | Cloud Hands | Ticket scope done; code/docs land on the branch. Model: `composer-2.5` (`fast=true`) for repo/code/build. |
| **3** | **Prove (eng)** | Cloud Hands | **pytest + smoke** for all factory builds. **+ before/after** (screenshot, video, or metrics in the PR) for UI/behavior PRs. Hands captures evidence in the PR body. |
| **4** | **Ship** | Hands self-check + **Infra PASS** | Draft PR only. No Greptile/CodeRabbit review-agent loop in v0. Infra PASS = human half of Ship — happens **before** step 5. Do not walk the playground on non-PASS drafts. |
| **5** | **Understanding Lab** | Gideon + Infra | Tier-gated. See tier mapping below. |
| **—** | **Gideon merge** | Gideon | After steps 4 (always) and 5 (Tier 1–2 only). Hands never merges. |

Step order is fixed. Do not reorder Ship and Understanding Lab.

---

## Tier mapping (step 5)

Factory step 5 is the **Understanding Lab** beat from the harness tier lock. Canonical tier rules: `docs/understanding-lab-tiers.md`.

| Tier | Step 5 | Merge gate |
|---|---|---|
| **0** (default) | **Skip** step 5. No lab, no View Understanding Lab CTA. | Ship what/why only → Infra PASS → Gideon merge. |
| **1** | **Hard gate.** Light Understanding Lab PASS required before merge. Shared decisions: **≥1 lock row** with rationale + `locked_at`. | Infra PASS → UL light PASS → Gideon merge. **No merge without UL PASS.** |
| **2** | **Hard gate.** Full five-beat Understanding Lab PASS required before merge. Shared decisions: **full beat**. | Infra PASS → UL full five-beat PASS → Gideon merge. **No merge without UL PASS.** |

**Infra PASS before UL:** Infrastructure reviews and PASSes the draft PR (step 4) before Gideon walks step 5. Do not send Gideon to the playground on drafts that have not earned Infra PASS.

**Playground format (Tier 1–2):** LexiScan house-tour HTML standard — `docs/understanding-lab-playground-standard.md`.

**LexiScan UL public host:** https://fabfloow-ul-playground.vercel.app — Understanding Lab playgrounds only. **Not** LexiScan product demo or production product apps.

---

## Prove split: engineering vs Understanding Lab

Two different “prove” concepts. Do not collapse them.

| Layer | Step | What it proves | Evidence |
|---|---|---|---|
| **Prove (eng)** | **3** | Code works; regressions caught; UI/behavior change visible. | pytest, smoke scripts, CI green where present. UI/behavior PRs also attach **before/after** (screenshot, video, or metrics) in the PR. |
| **Prove (understanding)** | **5** | Humans understand tradeoffs and locked decisions (Tier 1–2 only). | Understanding Lab beats + Shared decisions rows. Tier 0 skips this layer. |

Hands owns step 3 evidence. Infra checks step 3 on Ship review. Step 5 is Gideon-facing after Infra PASS.

---

## Ship (step 4) — v0 rules

- **Draft PR only.** No merge by Hands.
- **No review-agent loop in v0.** Greptile and CodeRabbit are **HOLD** — not factory stages.
- **Hands self-check:** scope, tests, evidence, ticket fields, tier-appropriate footers.
- **Infra PASS:** Infrastructure Desk human review = the other half of Ship. Infra posts Tier label + View PR (+ View Understanding Lab on Tier 1–2 when lab URLs exist). See `skills/infrastructure-comms/SKILL.md` § Software Factory.

---

## Ticket fields (optional)

```
factory: yes
prove_eng: pytest+smoke | before-after
tier: 0 | 1 | 2
escalate:
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
```

- `factory: yes` — this build follows the Software Factory conveyor.
- `prove_eng` — `pytest+smoke` (default for code builds) or `before-after` when UI/behavior evidence is required (often both).
- `tier` — controls step 5. Omit → Tier 0 (skip UL).
- Tier 1–2 require `escalate:` and lab URLs per `docs/understanding-lab-tiers.md`.

Full template: `tickets/TEMPLATE.md`.

---

## Out of scope (v0)

These are **not** factory stages or defaults:

| Item | Why out |
|---|---|
| **Signal Radar product** | Separate product build. May adopt the factory conveyor later; not planted inside v0. |
| **Grant packs (Lane B)** | Drive-folder lane; use `cth-grant`, not Software Factory. |
| **Socials / comms copy** | Desk Workbench + Hands mechanical lane; not Apps+Software conveyor. |
| **Greptile / CodeRabbit** | No review-agent loop in v0. |
| **Local worktree isolate skill** | v0 Isolate = cloud Hands branch off `main` only. Worktree skill is a later increment. |
| **Gideon merge / deploy** | Always human. Never a factory step Hands executes. |

---

## Related locks

- Understanding Lab tiers: `docs/understanding-lab-tiers.md`
- Playground format: `docs/understanding-lab-playground-standard.md`
- PR footer (Tier 1–2): `docs/view-understanding-lab-footer.md`
- App-build (new repos): `skills/app-build/SKILL.md`
- LangGraph production: `skills/langgraph-production/SKILL.md`
- Hands model routing: `docs/hands-model-routing.md`
