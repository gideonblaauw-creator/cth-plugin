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
- **Cloud Hands agents executing a ticket** must read `skills/harness/SKILL.md` first. Ticket contracts use `tickets/TEMPLATE.md`.
- **Before promoting a tree, creating a repo, or opening a branch on any app/service/pipeline**, read `skills/app-build/SKILL.md`. Do not create a GitHub repo until Gideon marks the row.

## VPS files

Operational files on the OVH VPS (`/opt/claude-files`, reached via files-mcp there) stay on the VPS. They are the source of truth. Do not clone them into this repo. Do not add MCP tokens or invent files-mcp credentials here. Access VPS files via Remote SSH or OpenCode.

## Claude plugin

Leave `.claude-plugin/plugin.json` intact. This Cursor config must not break the existing Claude Desktop plugin.
