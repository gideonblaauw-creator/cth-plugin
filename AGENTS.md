# AGENTS.md

Cursor-oriented pointer for this repo. Keep `CLAUDE.md` as-is for the Claude Desktop plugin.

This repository is the skill source of truth for CleantechHUB. Open this folder as the Cursor project. Do not copy playbooks into a second tree.

## Skills

CTH skills live in `skills/<name>/SKILL.md`. Cursor cannot auto-discover that folder, so `.cursor/skills/<name>/SKILL.md` files are thin stubs. When a stub matches, read the canonical `skills/<name>/SKILL.md` and follow it. Do not fork or rewrite playbooks under `.cursor/skills/`.

Edit skills in `skills/<name>/SKILL.md` (see `CLAUDE.md`). Stubs only need a description update if the canonical trigger text changes.

### Skip

- `skills/secrets` — do not load this skill in Cursor. Do not copy its contents into Cursor config.
- `dual-desktop-macos` — Claude Desktop only. It is not on `main`. Do not invent it.

### Routing

- Grant, donor, and competitive-bid work uses `cth-grant`.
- Commercial client service proposals use `cth-proposal-build`.
- Never mix those two playbooks.
- CleantechHUB brand work uses `cleantechhub-brand`.
- Never cite REIN Hubs dollar amounts.
- **Cloud Hands agents executing a ticket** must read `skills/harness/SKILL.md` first. Ticket contracts use `tickets/TEMPLATE.md`. The Desk/Hands boundary and Hands-shift lock (2026-08-17) are in §5 "Operating protocol": any first-draft file pack = Hands ticket (bc-id required); mechanical jobs and Researcher/Scraper/Infra inventories = Hands tickets; desks stay ~30%+ (HITL, routing, credentials, REIN HOLD); all Drive writes go through Hands (Drive MCP → Composio Drive → VPS `gws`). Lane A repo lock (2026-08-19) is in the same §5: Hands tickets must use the owning `repo_url` (`cth-data-room-scanner` is Teclogi-only; AIC → `americas-innovation-hub`; Almendra → `almendra`; harness → `cth-plugin`). Model routing (2026-08-19) is in the same §5: desks put the model on the Hands ticket; empty model on a mechanical job = `gemini-3.7-flash`. Table has official model ids + $ in / $ out. OSS-first + tiny/private (2026-08-20) is in the same §5: coding default is OpenCode Go `opencode-go/kimi-k2.7-code`; Composer 2.5 (`fast=false`) is the Cursor Hands fallback when Go is blocked; tiny and private are two axes.
- **Before promoting a tree, creating a repo, or opening a branch on any app/service/pipeline**, read `skills/app-build/SKILL.md`. Do not create a GitHub repo until Gideon marks the row.

## VPS files

Operational files on the OVH VPS (`/opt/claude-files`, reached via files-mcp there) stay on the VPS. They are the source of truth. Do not clone them into this repo. Do not add MCP tokens or invent files-mcp credentials here. Access VPS files via Remote SSH or OpenCode.

## Claude plugin

Leave `.claude-plugin/plugin.json` intact. This Cursor config must not break the existing Claude Desktop plugin.

## Cursor Cloud specific instructions

This repo is content-only: Markdown skill playbooks (`skills/<name>/SKILL.md`), Cursor stubs (`.cursor/skills/<name>/SKILL.md`), and two JSON manifests (`.claude-plugin/plugin.json`, `.mcp.json`). There is **no** application, dev server, build system, test framework, lint config, or dependency manifest (no `package.json`, lockfile, or `requirements.txt`). Do not add a build toolchain to "make it runnable" — nothing compiles or serves here.

The base image already provides everything needed: `node`, `npm`, `python3` (with `pyyaml`), `jq`, `git`, and `google-chrome-stable`. The startup update script is intentionally a no-op because there are no dependencies to refresh.

The closest thing to lint/test/build is validating that the content is well-formed and consistent — a harness parses these files, so "valid" means "loads":

- JSON manifests: `jq empty .claude-plugin/plugin.json .mcp.json`
- Skill frontmatter + stub/canonical parity: parse every `SKILL.md` frontmatter with `python3` + `pyyaml`, assert `name` matches its directory, and assert every canonical skill has a matching `.cursor/skills/` stub. Note: `skills/secrets` intentionally has **no** Cursor stub (see the Skip list above), so exclude it from the stub-parity check.

To preview an HTML artifact produced by a skill (e.g. `cleantechhub-brand`, `nexus-onepager`, `cth-proposal-build`), render it headlessly:
`google-chrome-stable --headless --no-sandbox --disable-gpu --screenshot=out.png --window-size=820,860 file:///abs/path.html`
(harmless `dbus`/`NameHasOwner` errors are expected in headless mode). The `html-to-pdf` skill uses Playwright, which is not preinstalled — install it on demand only if that skill is exercised.
