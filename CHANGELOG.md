# Changelog

All notable changes to the CleantechHUB Cowork Plugin are documented in this file.

## [Unreleased]

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
