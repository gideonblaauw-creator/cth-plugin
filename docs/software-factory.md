# Software Factory v0 (Gideon lock 2026-09-14; Ship CI t267u)

**One-liner:** Lane A Apps+Software builds follow a locked five-step conveyor through draft PR, Ship CI + Infra PASS, optional Understanding Lab, then Gideon merge.

**Owner:** Infrastructure (same ownership model as the Understanding Lab playground format lock).

**Skill:** `skills/software-factory/SKILL.md`  
**Ship CI:** `docs/software-factory-ship-ci.md`  
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
| **4** | **Ship** | Hands auto-loop + **Infra PASS** | Draft PR + **PR-Agent** + **visual before/after CI** on product repos. Hands fixes until review loop clears, then Infra PASS. Infra PASS = human half of Ship — **before** step 5. |
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

**Infra PASS before UL:** Infrastructure reviews and PASSes the draft PR (step 4) before Gideon walks step 5. Do not send Gideon to the playground on drafts that have not earned Infra PASS or while the Ship auto-loop is open.

**Playground format (Tier 1–2):** LexiScan house-tour HTML standard — `docs/understanding-lab-playground-standard.md`.

**LexiScan UL public host:** https://fabfloow-ul-playground.vercel.app — Understanding Lab playgrounds only. **Not** LexiScan product demo or production product apps.

---

## Prove split: engineering vs Understanding Lab

Two different “prove” concepts. Do not collapse them.

| Layer | Step | What it proves | Evidence |
|---|---|---|---|
| **Prove (eng)** | **3** | Code works; regressions caught; UI/behavior change visible. | pytest, smoke scripts, CI green where present. UI/behavior PRs also attach **before/after** (screenshot, video, or metrics) in the PR. |
| **Prove (understanding)** | **5** | Humans understand tradeoffs and locked decisions (Tier 1–2 only). | Understanding Lab beats + Shared decisions rows. Tier 0 skips this layer. |
| **Mic Prove (CI)** | **4** (Ship) | Pixel-level UI regression visible to reviewers. | Playwright + Argos CI or Lost Pixel on the PR. **Supplements** Hands before/after — does not replace pytest/smoke. |

Hands owns step 3 evidence. Ship CI adds step 4 visual proof. Infra checks steps 3–4 on Ship review. Step 5 is Gideon-facing after Infra PASS.

---

## Ship (step 4) — t267u locks

### Draft PR + review agents

- **Draft PR only.** No merge by Hands.
- **PR-Agent** ([Codium-ai/pr-agent](https://github.com/Codium-ai/pr-agent) / [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent), Qodo) as GitHub Action on **product repos**: `/describe`, plain-English walkthrough, `/ask` on PR comments.
- **Visual before/after CI:** Playwright (screenshots/video) + Argos CI or Lost Pixel — posts before/after visual diffs on the PR. AI reviewers do not see pixels; this is the **Mic Prove** surface in CI.

Workflow **templates** live in `docs/examples/software-factory/`. Hands copies into the owning Lane A product repo on the next factory build. **Do not** enable org-wide from `cth-plugin` alone. Full reference: `docs/software-factory-ship-ci.md`.

### Auto-loop (Hands)

On PR-Agent fail, visual CI fail, or open review comments:

1. Hands reads PR-Agent summary and visual diff comments.
2. Hands replies, fixes on the branch, pushes.
3. Re-runs **Prove(eng)** (pytest + smoke; refresh Hands before/after when UI changed).
4. Waits for PR-Agent + visual CI green and threads resolved.
5. **Only then** pings Infrastructure for **Infra PASS**.

Do **not** send Gideon to Understanding Lab until the auto-loop clears **and** Infra PASS.

### Infra PASS (human half of Ship)

Infrastructure Desk human review after the auto-loop clears:

- PR-Agent summary present and addressed
- Visual CI green (when repo has UI surface)
- pytest + smoke green; Hands before/after on UI PRs
- Short what/why; tier-appropriate CTA

See `skills/infrastructure-comms/SKILL.md` § Software Factory and `skills/software-factory/SKILL.md` § Infrastructure PASS checklist.

### Secrets (names only)

Provider keys via **Infisical → GitHub Actions secrets** on the **product repo** — never in `cth-plugin` commits:

- `OPENAI_API_KEY` (or PR-Agent-supported provider key name)
- `ARGOS_TOKEN` or `LOST_PIXEL_API_KEY` when using visual CI
- `GITHUB_TOKEN` — Actions default

Per-product `BASE_URL` / preview URL: **[PENDIENTE]** until each Lane A repo plants its workflow config.

---

## Ticket fields (optional)

```
factory: yes
ship_review: pr-agent
prove_eng: pytest+smoke | before-after
tier: 0 | 1 | 2
escalate:
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
```

- `factory: yes` — this build follows the Software Factory conveyor.
- `ship_review: pr-agent` — default when `factory: yes`. PR-Agent + visual CI Ship stack on product repos.
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
| **Enabling Ship CI on every repo from this PR** | Templates in `docs/examples/` only; product repos adopt on their next factory build. |
| **Local worktree isolate skill** | v0 Isolate = cloud Hands branch off `main` only. Worktree skill is a later increment. |
| **Gideon merge / deploy** | Always human. Never a factory step Hands executes. |

---

## Related locks

- Ship CI templates: `docs/software-factory-ship-ci.md`, `docs/examples/software-factory/`
- Understanding Lab tiers: `docs/understanding-lab-tiers.md`
- Playground format: `docs/understanding-lab-playground-standard.md`
- PR footer (Tier 1–2): `docs/view-understanding-lab-footer.md`
- App-build (new repos): `skills/app-build/SKILL.md`
- LangGraph production: `skills/langgraph-production/SKILL.md`
- Hands model routing: `docs/hands-model-routing.md`
- Secrets: `skills/infisical/SKILL.md`
