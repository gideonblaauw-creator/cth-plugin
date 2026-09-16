# Ticket Template — CTH Harness

Copy this block into a new file (e.g. `tickets/YYYY-MM-DD-short-name.md`) and fill in every field.
`desk:` is free-form — write the Desk name as it exists or will exist.
See `skills/harness/SKILL.md` for lane definitions, gate rules, and the full Desk list.

When opening Hands from a Cursor Project, name the Project and workspace lane so the agent lands on the correct repo or pack store.

---

```
desk:
folder:
cursor_project:
cursor_workspace:
done-when:
model: gemini-3.7-flash | composer-2.5 (fast=true)
lane: github-pr | drive-folder
factory: yes
ship_review: pr-agent
prove_eng: pytest+smoke | before-after
tier: 0 | 1 | 2
escalate:
langgraph: yes
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
playground_standard: lexiscan-html-v2
hitl: nothing sent/posted/paid
reviewer:
context:
```

`factory` — optional. Set `factory: yes` when the build follows **Software Factory v0** (Apps+Software conveyor). Canonical: `docs/software-factory.md`, `skills/software-factory/SKILL.md`. Conveyor: `1 Isolate → 2 Build → 3 Prove(eng) → 4 Ship → 5 Understanding Lab → Gideon merge`. Infra PASS (step 4) before step 5. Omit when not a factory build (grants, socials, skill-only edits).

`ship_review` — optional; **default `pr-agent` when `factory: yes`**. Step 4 Ship runs **PR-Agent** (GitHub Action: `/describe`, plain-English walkthrough, `/ask`) plus **visual before/after CI** (Playwright + Argos or Lost Pixel) on the owning product repo. Hands auto-loops on fail/comments until green, then pings Infra PASS. Workflow templates: `docs/examples/software-factory/` (copy into product repo — not org-wide from `cth-plugin`). Ship CI reference: `docs/software-factory-ship-ci.md`.

`prove_eng` — optional on `factory: yes`. `pytest+smoke` (default for code builds) or `before-after` when UI/behavior PRs need screenshot/video/metrics in the PR. Often both apply on UI builds. Visual CI **supplements** Hands before/after — does not replace pytest/smoke.

`tier` — Lane A Understanding Lab (Gideon lock 2026-09-12). Omit or `0` = **default Ship**: normal draft PR + short what/why; **no lab; no View Understanding Lab CTA**; on factory builds, **skip factory step 5**. `1` = Light Understanding (Context ≤½ page, Playground light, one Shared decision row). `2` = Full Lab + ledger (full five-beat PASS). **Factory step 5 hard gate (Tier 1–2):** no Gideon merge without UL PASS after Infra Ship PASS. Escalation to 1 or 2 **requires** `escalate:` one-liner. **Ticket MUST name Tier 2** — never default, never infer from scope. `major: yes` without `tier:` is a miss. Canonical: `docs/understanding-lab-tiers.md`. Footer: `docs/view-understanding-lab-footer.md`.

`langgraph` — optional. Set `langgraph: yes` for a **production / client agent graph**. Hands follows `skills/langgraph-production/SKILL.md` on the owning product repo (`composer-2.5`, Fast ON). OpenCode is OSS experiments only — never a client deploy path. Omit when the ticket is not a LangGraph build.

`lab_notion` — **required on Tier 1–2.** This build’s / this product’s Understanding Lab Notion URLs. Flat aliases: `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`. **Every build gets its own pages** (Gideon 2026-09-12 via FabFloow). Do not reuse Scanner (Dataroom / VertiGreen) URLs for LexiScan, Sustenttia, or other products. If omitted on Tier 1–2: Infra posts Tier label + View PR only and flags missing lab pages — **does not** paste Scanner links. Unused on Tier 0. LangGraph HITL maps `interrupt()` to these URLs — see `skills/langgraph-production/SKILL.md`.

`playground_standard` — optional on Tier 1–2. When set to `lexiscan-html-v2`, Hands plants the repo artifact at `understanding-lab/playground/` using the LexiScan house-tour file set (`index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh`). Canonical lock t1268u: `docs/understanding-lab-playground-standard.md`. Omit on Tier 0.

`cursor_project` — optional. Desk slug / Cursor IDE Project name when Hands is opened from a desk-scoped Project (e.g. `CTH-Infrastructure`, `CTH-Grants`, `Sustenttia`). Canonical map: `docs/cursor-projects.md`.

`cursor_workspace` — optional. Lane A repo slug (`cth-plugin`, `sustenttia-v2`, `cth-data-room-scanner`, …) or `cth-matters` for Lane B packs. Pair with `cursor_project` when the default Create Project modal would pick the wrong repo.

`model` — Cloud Hands only. Allowed: `gemini-3.7-flash` (mechanical/tiny) or `composer-2.5` with **Fast ON** (`fast=true`) for repo/code/builds (Signal Radar, LexiScan, scanner, harness, LangGraph). Empty build ticket → Composer Fast ON (not Flash). Never silently launch a build with Fast off. Review/eval/brand with no model → HOLD and flag Gideon. See BUILDING lock t1263u in `docs/hands-model-routing.md` and `skills/harness/SKILL.md` §5.
