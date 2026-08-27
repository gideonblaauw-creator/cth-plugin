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

## CTH Harness rulebook vs this file

`HARNESS.md` is Cowork/CLI/Cursor **setup** docs. The CTH Harness **rulebook** is `skills/harness/SKILL.md` (tickets: `tickets/TEMPLATE.md`).

Machine-readable routing planted there includes:
- Desk/Hands boundary and Lane A repo lock
- **Token lock (2026-08-26):** Grok Bot coordinates only; allowed Cloud Hands models = `gemini-3.7-flash` and `composer-2.5` (`fast=false`); Sonnet/Opus/Haiku/Auto/Grok/Kimi cloud → HOLD flag Gideon
- **Toolkit inventory (§6):** full Claude Desktop vs Cursor skill registry and MCP connector list

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
