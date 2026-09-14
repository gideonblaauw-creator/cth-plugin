---
name: software-factory
description: >
  Software Factory v0 — Lane A Apps+Software conveyor for Cloud Hands and
  Infrastructure review. Use when: factory, Software Factory, Apps+Software
  build, Prove(eng), Ship (PR-Agent + visual CI), draft PR conveyor, or
  Infrastructure PASS on a product repo. Do not use when: grant packs (Lane B),
  socials copy, or Signal Radar product work (separate build; may adopt factory later).
license: MIT
metadata:
  version: "0.2.0"
  category: infrastructure
  owner: Infrastructure
  adopted: "2026-09-14"
  ship_ci_lock: "t267u"
---

# Software Factory v0

**Owner:** Infrastructure  
**Date:** 2026-09-14  
**Canonical doc:** `docs/software-factory.md`  
**Ship CI:** `docs/software-factory-ship-ci.md` · Templates: `docs/examples/software-factory/`

Lane A Apps+Software builds follow a locked conveyor. Cloud Hands executes steps 1–3, opens the draft PR, runs the Ship auto-loop (PR-Agent + Playwright/Argos visual CI), then pings Infra PASS (step 4). Understanding Lab (step 5) is tier-gated. Gideon merges.

## When to use

- Desk tickets a **repo/code/build** on a Lane A product or harness repo.
- Ticket sets `factory: yes` or the Desk names Software Factory explicitly.
- Infrastructure reviews a factory draft PR.

Do **not** use for:

- Lane B grant/client packs (`cth-grant`).
- Socials, newsletter, or comms-only copy.
- **Signal Radar** product implementation (separate product; not a factory stage in v0).

## Locked conveyor

```
1 Isolate → 2 Build → 3 Prove(eng) → 4 Ship → 5 Understanding Lab → Gideon merge
```

Read the full gate table in `docs/software-factory.md`.

## Step duties

### 1 — Isolate

- Branch off `main` on the **owning** Lane A repo (harness repo lock: `skills/harness/SKILL.md` § Lane A repo lock).
- Branch name: `cursor/<descriptive-name>-<suffix>`.
- v0: cloud Hands branch only. Local worktree isolate skill is later.

### 2 — Build

- Implement ticket scope on the branch.
- Model: `composer-2.5` (`fast=true`) for repo/code/build (BUILDING t1263u).
- Commit logically; push before Ship.

### 3 — Prove (eng)

Hands must leave engineering proof in the PR:

| Build type | Required proof |
|---|---|
| All factory code builds | **pytest + smoke** (or repo-equivalent test + smoke script) |
| UI / behavior changes | **+ before/after** — screenshot, video, or metrics embedded or linked in the PR body (Hands auto) |

Ticket field: `prove_eng: pytest+smoke` or `prove_eng: before-after` (use both when UI and code change).

This step is **not** the Understanding Lab. Do not skip pytest/smoke because a Tier 1–2 lab exists. Visual CI in step 4 **supplements** Hands before/after — does not replace pytest/smoke.

### 4 — Ship

- Open a **draft PR** only. Never merge.
- On **product repos** with factory Ship CI planted (from `docs/examples/software-factory/`):
  - **PR-Agent** ([Codium-ai/pr-agent](https://github.com/Codium-ai/pr-agent)) — `/describe`, plain-English walkthrough, `/ask` on comments.
  - **Visual before/after CI:** Playwright + Argos CI posts pixel diffs on the PR (Mic Prove in CI).
- **Auto-loop YES (t267u):** On PR-Agent fail, visual CI fail, or open review comments:
  1. Read PR-Agent summary and visual diff comments.
  2. Reply on the PR, fix on the branch, push.
  3. Re-run **Prove(eng)** — pytest + smoke; refresh Hands before/after when UI changed.
  4. Wait for PR-Agent + visual CI green and threads resolved.
  5. **Only then** ping Infrastructure for **Infra PASS**.
- Do **not** send Gideon to Understanding Lab until auto-loop clears **and** Infra PASS.
- First factory build on a repo: copy workflow templates from `docs/examples/software-factory/` into that repo’s `.github/workflows/` (not org-wide from `cth-plugin`).
- Secrets: Infisical → GitHub Actions on the product repo — `OPENAI_API_KEY`, `ARGOS_TOKEN` (names only in tickets). Per-product `BASE_URL` / preview URL **[PENDIENTE]** until planted.

### 5 — Understanding Lab (tier-gated)

| Tier | Step 5 |
|---|---|
| **0** (default) | **Skip.** No lab. Ship what/why → Infra PASS → Gideon merge. |
| **1** | **Hard gate.** Light UL PASS + ≥1 Shared decisions lock row before merge. |
| **2** | **Hard gate.** Full five-beat UL PASS + full Shared decisions beat before merge. |

**No merge without UL PASS on Tier 1–2.** Do not soften this gate.

Playground: LexiScan house-tour standard — `docs/understanding-lab-playground-standard.md`.  
UL public host: https://fabfloow-ul-playground.vercel.app — **not** product demo/prod apps (cross-link; PR #31).

Tier rules: `docs/understanding-lab-tiers.md`. Tier 1–2 PR footer: `docs/view-understanding-lab-footer.md`.

### Gideon merge

Gideon merges after step 4 PASS and, when Tier 1–2, step 5 UL PASS. Hands does not merge or deploy.

---

## Ticket fields

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
playground_standard: lexiscan-html-v2
```

See `tickets/TEMPLATE.md` for full contract.

---

## Infrastructure PASS checklist (step 4)

Infra reviews **before** UL walk — **after** Hands Ship auto-loop clears. Confirm:

- [ ] Owning repo and branch match ticket (`repo_url` / Lane A lock)
- [ ] Draft PR only — no merge by Hands
- [ ] **Prove (eng):** pytest + smoke passed (or documented equivalent)
- [ ] UI/behavior PRs include Hands before/after evidence in PR (visual CI supplements, does not replace)
- [ ] **PR-Agent:** `/describe` or equivalent summary present; open review comments resolved
- [ ] **Visual CI:** Playwright + Argos green when repo has UI surface (or legit skip noted on ticket)
- [ ] Short what/why in PR body
- [ ] Tier label correct: Tier 0 = no lab CTA; Tier 1–2 = lab URLs on ticket + PR footer when URLs exist
- [ ] **Do not** post View Understanding Lab or walk playground until this checklist PASSes

After Infra PASS on Tier 1–2, post Tier label → View PR → View Understanding Lab (when lab URLs exist). Merge remains blocked until UL PASS.

Infra chat protocol: `skills/infrastructure-comms/SKILL.md` § Software Factory.

---

## Out of scope (v0)

- Signal Radar as a factory stage
- Grant packs, socials
- Enabling Ship CI org-wide from `cth-plugin` alone (templates only)
- Gideon merge or deploy by Hands
- Local worktree isolate (later)

Full list: `docs/software-factory.md` § Out of scope.
