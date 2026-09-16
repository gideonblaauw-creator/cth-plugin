# Changelog

All notable changes to the CleantechHUB Cowork Plugin are documented in this file.

## [Unreleased]

### Cursor Projects ↔ Desk map (Infra ownership)

- New doc: `docs/cursor-projects.md` — locked convention: one Cursor Project ≈ one durable workstream; Lane A product repos vs Lane B `cth-matters`; Layer 0–4 pods/desks/bench/personal tables; rollout phases; optional ticket fields
- Updated: `skills/harness/SKILL.md` — § Cursor Projects ↔ Desks pointer
- Updated: `skills/infrastructure-comms/SKILL.md` — § Cursor Projects ↔ Desk map (Infra ownership)
- Updated: `tickets/TEMPLATE.md` — optional `cursor_project`, `cursor_workspace` when opening Hands from a desk Project
- HITL: Gideon creates/merges Cursor IDE Projects; Infra seeds map + Grok Bot shards; no Projects API from code

### Legal dual entity lock t1353u (2026-09-15)

- Updated: `skills/legal-comms/SKILL.md` — dual CTH entity lock (S.L. for commercial consulting; Foundation for grants/convenios); wrong entity = `blocker`; intake captures `cth_party: sl | foundation`
- Updated: `skills/legal-eval/SKILL.md` — same dual lock; entity check as hard stop; doc-type matrix maps consulting → S.L. (NIF B19439389), grant/convenio/foundation → Foundation
- Updated: `skills/legal-eval/references/severity-rubric.md` — wrong-entity hard stop (#6)
- Updated: `skills/legal-eval/references/playbook-example.yaml` — dual-entity EXAMPLE skeletons (S.L. + Foundation commented block); NIF B19439389 on S.L.
- Updated: `skills/legal-eval/references/clause-taxonomy-v0.md`, `example-memo.md` — parties/entity family notes for both entities; Foundation example memo

### Legal desk plant t1338u (2026-09-15)

- New Desk: **Legal** — agreements, MOUs, LOIs, compliance, governance packs (owner **4b96b1e8**; first matter **AURA**)
- New skill: `skills/legal-comms/SKILL.md` + Cursor stub — coordination-only desk comms; tickets Hands via `legal-eval`; HITL before sign/send/pay; `[INTERNAL]`/`[EXTERNAL]` firewall; Spanish **S.L.** entity lock (**CLEANTECHHUB INTERNATIONAL S.L.**)
- New skill: `skills/legal-eval/SKILL.md` + Cursor stub + `references/` — clause review playbook; coarse review modes (`strict`|`moderate`|`loose`); fine modes; severity enum `blocker`|`negotiate`|`accept`|`info`|`unknown`; six-stage loop; example playbook YAML (EXAMPLE ONLY)
- Updated: `skills/harness/references/skill-toolkit.json`, `skills/harness/SKILL.md` (Desks that exist + inventory counts)

### Understanding Lab playground host live — LexiScan example (2026-09-14)

- Planted live Understanding Lab stable host (Infra harness): https://fabfloow-ul-playground.vercel.app as `HITL_HTML_STABLE_URL` reference in harness docs — exemplified by the LexiScan product example (FabFloow internal client)
- Clarified LexiScan **product** apps are not the UL harness host: DEMO https://fabfloow-lexiscan.vercel.app · PROD https://fabfloow-lexiscan-app.vercel.app
- Updated: `docs/understanding-lab-playground-standard.md`, `docs/understanding-lab-tiers.md`, `docs/view-understanding-lab-footer.md`, `skills/harness/SKILL.md`, `skills/infrastructure-comms/SKILL.md` §7

### Software Factory UL ownership lock t269u (2026-09-14)

- **FabFloow** = internal client; **LexiScan** = FabFloow product — neither is the Understanding Lab harness
- UL harness / format / `HITL_HTML_STABLE_URL` = **Infrastructure** (`cth-plugin`)
- LexiScan house-tour + https://fabfloow-ul-playground.vercel.app = canonical **example** only — not LexiScan DEMO/PROD apps
- Updated: `docs/software-factory.md`, `skills/software-factory/SKILL.md`, `skills/harness/SKILL.md` § Software Factory

### Software Factory Ship CI locks t267u (2026-09-14)

- **Overrides v0 HOLD on review agents** — step 4 Ship now includes PR-Agent + visual before/after CI
- **PR-Agent:** Codium-ai/pr-agent / The-PR-Agent/pr-agent (Qodo) — `/describe`, walkthrough, `/ask` on PR comments
- **Visual CI:** Playwright + Argos CI or Lost Pixel — before/after pixel diffs on PR (Mic Prove in CI)
- **Auto-loop YES:** Hands fix → re-Prove(eng) → wait for green → then Infra PASS; no UL until loop clears + Infra PASS
- New: `docs/software-factory-ship-ci.md`, `docs/examples/software-factory/` (pr-agent.yml + visual-ci.yml templates for product repos)
- Secrets note: Infisical → GH Actions (`OPENAI_API_KEY`, `ARGOS_TOKEN` / `LOST_PIXEL_API_KEY` — names only); per-product `BASE_URL` **[PENDIENTE]**
- Updated: `docs/software-factory.md`, `skills/software-factory/SKILL.md`, `skills/infrastructure-comms/SKILL.md`, `skills/harness/SKILL.md`, `tickets/TEMPLATE.md` (`ship_review: pr-agent`)
- Non-goals: no workflow install on Signal Radar/scanner/LexiScan in this PR; templates only

### Software Factory v0 (2026-09-14)

- **Locked Apps+Software conveyor:** `1 Isolate → 2 Build → 3 Prove(eng) → 4 Ship → 5 Understanding Lab → Gideon merge`
- New doc: `docs/software-factory.md` — gates, tier mapping, Prove split (eng vs UL), out-of-scope (Signal Radar product, grants, socials)
- New skill: `skills/software-factory/SKILL.md` + Cursor stub — Hands steps, ticket fields, Infra PASS checklist
- **Tier 0:** skip step 5 (UL); ship what/why after Infra PASS. **Tier 1–2:** step 5 hard gate before Gideon merge
- **Prove(eng):** pytest + smoke; + before/after for UI/behavior PRs. **Infra PASS** = human half of Ship, before UL
- **UL host reference:** https://fabfloow-ul-playground.vercel.app (not product demo/prod apps)
- Updated: `docs/understanding-lab-tiers.md`, `docs/understanding-lab-playground-standard.md`, `skills/harness/SKILL.md`, `skills/infrastructure-comms/SKILL.md`, `tickets/TEMPLATE.md`

### Understanding Lab playground standard t1268u (2026-09-13)

- **LexiScan house-tour HTML = canonical playground format** for all Tier 1–2 Understanding Lab / HITL microworlds
- New doc: `docs/understanding-lab-playground-standard.md` — checklist, anti-patterns, ownership (FabFloow product / Infra format lock)
- Canonical refs: repo `fabfloow-lexiscan`, path `understanding-lab/playground/` (PR #16 MERGED), Notion Playground + Shared decisions (LexiScan example) URLs, Vercel `fabfloow-ul-playground` (UL host, not product demo; FabFloow will publish URL), LexiScan skin = FabFloow cream/mustard/copper; optional ticket field `playground_standard: lexiscan-html-v2`
- Updated: `docs/understanding-lab-tiers.md`, `docs/view-understanding-lab-footer.md`, `skills/harness/SKILL.md`, `skills/infrastructure-comms/SKILL.md` §7, `skills/notion/references/hitl-understanding-loops.md`, `tickets/TEMPLATE.md`
- Legacy Scanner tabbed microworld documented as anti-pattern; remediation PRs separate

### BUILDING model lock t1263u (2026-09-13)

- **BUILDING = Composer 2.5 Fast ON** — hardens t1242u: repo/code/build Hands launch `composer-2.5` (`fast=true`); empty build tickets fill Fast ON (not Flash)
- Explicit build surfaces: repo/code, LangGraph lane, Lane A product apps, **Signal Radar**, **LexiScan**, **scanner**, harness code
- **Never silently launch a build with Fast off** — `composer-2.5 (fast=false)` on a build = miss → remap to `fast=true` and flag; HITL: no silent model swap to Fast off
- Mechanical/tiny still `gemini-3.7-flash` when named; review/eval/brand still HOLD; no Opus/Grok auto-fill
- Canonical: `docs/hands-model-routing.md`; harness §5 BUILDING lock; `skills/langgraph-production/SKILL.md`; `skills/infrastructure-comms/SKILL.md` §5; desk comms §5; `tickets/TEMPLATE.md`

### LangGraph production Hands lane (2026-09-12)

- Added `skills/langgraph-production/SKILL.md` plus Cursor stub (HITL `interrupt` ↔ Notion Understanding Lab, checkpoint memory, eval fixtures, deploy/monitor pointer)
- Ticket field `langgraph: yes` in `tickets/TEMPLATE.md`; brief desk routing in harness and `infrastructure-comms`
- Version pins (PyPI 2026-09-12): `langgraph==1.2.11`, `langgraph-checkpoint==4.2.0`, `langsmith==0.12.4`
- Client / production graphs on this lane only; OpenCode remains OSS experiments only
- Dogfood order documented: `cth-data-room-scanner` first, then FabFloow LexiScan L2. Lab repo `langgraph-lab` is a separate Hands ticket

### BUILDING model lock t1242u (2026-09-12)

- **BUILDING = Composer 2.5 Fast ON** — repo/code/build Hands launch `composer-2.5` (`fast=true`); empty build tickets fill Fast ON (not Flash)
- Mechanical/tiny still `gemini-3.7-flash` when named; review/eval/brand still HOLD
- Canonical: `docs/hands-model-routing.md`; harness §5 BUILDING lock; desk comms §5; `tickets/TEMPLATE.md`
- Supersedes prior repo/code `fast=false` default from Token lock 2026-08-26

### Infra chat delivery — Tier label first (Gideon 2026-09-12)

- Every Hands completion in Gideon chat **leads with the Tier label** (`**Tier 0** — Ship` / `**Tier 1** — Light Understanding` / `**Tier 2** — Full Lab + ledger`) before View PR / View Understanding Lab
- Tier 0 announces Tier 0 with no lab CTA; Tier 1–2 announce the tier, then View PR, then lab links
- Surfaces: `skills/infrastructure-comms/SKILL.md` §7; `docs/understanding-lab-tiers.md` Delivery; `docs/view-understanding-lab-footer.md`; harness Cursor-product-limit line

### Understanding Lab tier lock (Gideon 2026-09-12)

- Locked Tier 0 / Tier 1 / Tier 2 balance: desks **default Tier 0**; escalate only with a named `tier:` + `escalate:` reason
- One-liner: Push product at Tier 0; earn trust at Tier 1; prove it at Tier 2
- View Understanding Lab CTA + full five-beat PASS **only** for Tier 1–2 (Tier 1 = light PASS; Tier 2 = full five beats + `events.jsonl`). Not every Lane A merge
- Playground hard lock stays for Tier 1–2: `scenario → consequences → options → choose`
- `major: yes|no` from PR #24 is superseded — do not infer a lab from scope
- Canonical lock: `docs/understanding-lab-tiers.md`; ticket field in `tickets/TEMPLATE.md`

### View Understanding Lab delivery (major Lane A)

- Locked lab name **Understanding Lab**; CTA **View Understanding Lab**; 5 beats: Context → Explanation (quiz) → Playground → Shared decisions → Next cycle
- Playground hard gate (Gideon 2026-09-12): scenarios, consequences, 2–4 option paths with tradeoffs; flow `scenario → consequences → options → choose` before Shared decisions
- Harness, Notion, and Infrastructure comms: mandatory PR footer + Infra chat link beside View PR for major Lane A draft PRs
- Major vs tiny classification on tickets (`major: yes|no` or scope inference); tiny/mechanical skips full lab
- Paste helper: `docs/view-understanding-lab-footer.md`; stable HTML placeholder `HITL_HTML_STABLE_URL` until Infra plants host
- Synonym map for legacy Notion page titles in Notion skill + `hitl-understanding-loops.md`

### Cursor-native project config (Claude plugin unchanged)

- Added `AGENTS.md` as a thin Cursor pointer; `CLAUDE.md` is unchanged
- Added `.cursor/rules/cleantechhub.mdc` for always-on CTH policy
- Added `.cursor/skills/` discovery stubs that point at canonical `skills/<name>/SKILL.md` (no playbook forks; `secrets` omitted)
- Documented opening this folder in Cursor and keeping VPS files on `/opt/claude-files`

## [2.0.1] — 2026-08-07

### Removed client brand skills — plugin now contains only CTH-owned brands.

- Removed `sustenttia-brand`, `dialogos-del-futuro-brand`, `tec-alianza-brand` (client/partner brands managed separately)
- Updated skill count from 24 to 21

## [2.0.0] — 2026-08-07

### Major update — harness-agnostic architecture and expanded skill coverage.

**Skills: 21 (up from 15)**
- **Brand Identity (2):** cleantechhub-brand, clp26-brand
- **Programs (5):** social-media-campaign, cth-grant, cth-proposal-build, cth-seo, nexus-onepager
- **Operations (10):** bookstack, buffer, canva, monday, gmail, google-drive, slack, notion, composio, miro
- **Infrastructure (4):** doctor-bot, secrets, html-to-pdf, live-artifact-build

**Architecture**
- Harness-agnostic design — works in Claude Cowork, Claude Code CLI, Cursor, and any MCP-compatible environment
- Added `.cursorrules` for Cursor IDE integration
- Added `HARNESS.md` with per-harness setup instructions
- Added `CONNECTORS.md` mapping 13 connector categories with CTH standards and alternatives
- Added `CLAUDE.md` for AI assistant context
- Progressive disclosure with `references/` directories inside skills for detailed knowledge

**Breaking changes**
- Skill directory structure reorganized — all skills now live under `skills/<name>/SKILL.md`
- Plugin manifest moved to `.claude-plugin/plugin.json`

## [1.2.0] — 2026-05-20

### Initial public release.

**Skills: 15**
- 3 brand skills (cleantechhub-brand, clp26-brand, sustenttia-brand)
- 9 operational skills (buffer, canva, monday, gmail, google-drive, slack, notion, bookstack, composio)
- 3 slash commands (doctor-bot, secrets, html-to-pdf)

**Connectors**
- 2 MCP servers configured (Slack, Google Drive)

**Notes**
- First version shared externally as a Claude Cowork plugin
- Skills encoded as flat markdown files
- Limited to Claude Cowork as the only supported harness
