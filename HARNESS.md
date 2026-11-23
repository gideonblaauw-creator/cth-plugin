# Multi-Harness Compatibility

This plugin is designed to work across multiple AI coding and knowledge-work environments. Here's how to use it in each.

## Claude Cowork (primary)

Install via the `.plugin` file or clone this repo into your plugins directory. Skills appear automatically in the Cowork sidebar and trigger contextually during conversations.

**Setup:**
1. Install the plugin via Claude Desktop → Settings → Plugins
2. Connect the MCP connectors you need (see CONNECTORS.md)
3. Skills activate automatically based on your prompts

## Claude Code CLI

Clone or symlink this repo into your Claude Code plugins directory:

```bash
# Option 1: Clone directly
cd ~/.claude/plugins/
git clone https://github.com/gideonblaauw-creator/cth-plugin.git

# Option 2: Symlink from your projects
ln -s /path/to/cth-plugin ~/.claude/plugins/cth-plugin
```

Skills are available as slash commands. MCP servers from `.mcp.json` load automatically.

## Cursor

Open this repository folder in Cursor. Do not copy skills, VPS files, or MCP tokens into another project.

1. **File → Open Folder** on this repo.
2. `AGENTS.md` and `.cursor/rules/` load as always-on project policy.
3. `.cursor/skills/` contains discovery stubs. When a stub matches, the agent reads the canonical `skills/<name>/SKILL.md`.
4. VPS files at `/opt/claude-files` stay on the OVH VPS. Access them via Remote SSH or OpenCode, not by copying.
5. Leave `.claude-plugin/` unchanged so the Claude Desktop plugin keeps working.

See the README section **Using this repo in Cursor**.

## Machine-readable routing (Cloud Hands + Desktop)

This section points at paths that exist on `main`. It is not the CTH Harness rulebook — that lives in `skills/harness/SKILL.md`.

| Path | Role |
|---|---|
| `skills/harness/SKILL.md` | CTH Harness rulebook — five terms, Desk/Hands boundary, Lane A repo lock, **Token lock 2026-08-26**, media routing |
| `skills/skill-template/SKILL.md` | Skill authoring template — Agent Skills spec + CTH routing |
| `skills/skill-template/references/SKILL-TEMPLATE.md` | Copy-paste skeleton for new skills |
| `skills/harness/references/skill-toolkit.json` | Skill inventory — canonical `skills/<name>/SKILL.md`, Cursor stubs, skip list |
| `skills/harness/references/hands-ticket-hard.md` | Desks + Workbenches → Cloud Hands lock (24 Sep 2026); Mail Finder pattern — pointer only |
| `skills/harness/references/harness-engineering.md` | CTH-adapted harness-engineering patterns (verification, context map, loops, autonomy bands) — pointer only; rulebook stays in `skills/harness/SKILL.md` |
| `tickets/TEMPLATE.md` | Seven-field ticket contract |
| `AGENTS.md` | Cursor pointer, Skip list, Cursor Cloud validation |
| `CLAUDE.md` | Claude Desktop plugin pointer |

**Token lock 2026-08-26 (Cloud Hands):** Grok Bot = coordination only. File/research/code/copy → Cloud Hands. Allowed models: `gemini-3.7-flash` (mechanical/tiny) and `composer-2.5` (`fast=true`) (repo/code/build — Fast ON, t1263u). Review/eval/brand with no model → HOLD and flag Gideon (no auto-Sonnet). Full lock in `skills/harness/SKILL.md` §5.

**Skill toolkit:** 52 canonical skills under `skills/` (25 core + 27 desk comms); 51 Cursor stubs; `secrets` skipped in Cursor. Author new skills with `skills/skill-template/SKILL.md`. See `skill-toolkit.json` for paths.

## Other MCP-Compatible Environments

The plugin's skills are plain markdown files that work in any system that can load instruction documents. The `.mcp.json` defines standard MCP server connections that work with any MCP client.

### What's portable
- **Skills (markdown):** Work anywhere that accepts instruction files
- **MCP config:** Works with any MCP-compatible client
- **Brand guidelines:** Plain text/CSS — copy into any design system

### What's harness-specific
- **`.claude-plugin/plugin.json`:** Claude-specific manifest (ignored by other harnesses)
- **`AGENTS.md` and `.cursor/`:** Cursor project rules and skill discovery stubs (canonical playbooks stay in `skills/`)
- **Slash commands:** Claude Cowork/Code specific (adapt to your harness's command system)

## Operating protocol (HITL)

Applies to every Orchestrator, desk, workbench, tool and bot that talks to Gideon Blaauw.

### GO / NO GO decisions: inline buttons (Gideon 22 Nov 2026)

1. When an Orchestrator, desk, workbench, tool or bot needs a GO or NO GO (or any HITL approval) from Gideon, it MUST ask with the harness's inline button or widget (Grok Bot: SendToUser `type: widget`) with clickable options. Do not ask in prose only.
2. Use one decision per widget. Write the prompt in one line. State what, where, and the consequence (example: `Deploy Datatón teams deck to decks.cleantechhub.net/datathon-2026-teams/?`). Use options **GO** (`style: primary`) and **NO GO**. Add one more real option only when it exists (example **GO with changes**, `allowCustom`). Use `style: danger` for destructive actions.
3. Send a short text message first with the link or file to review (preview URL, PR, draft card). Send the widget as the last message of the turn.
4. When several decisions are pending, use one widget with steps (one step per decision). Do not send one long message.
5. When a desk needs a GO relayed by the Orchestrator, the desk sends the Orchestrator the exact one-line question and options. The Orchestrator shows the widget to Gideon.
6. A widget pick is Gideon's own words. Quote the picked value and the widget or message id in the ticket or log. Treat a dismissed widget as NO GO. Do not ask again.
7. Draft cards (email, X, WhatsApp) that already have their own Send button do not need an extra widget.
