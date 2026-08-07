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

Cursor reads `.cursorrules` files and MCP server configs. To use this plugin:

1. Copy `.cursorrules` from this repo to your project root (or merge with existing)
2. Copy or merge `.mcp.json` into your project's `.cursor/mcp.json`
3. Skills content is embedded in `.cursorrules` as context rules

```bash
# Quick setup for a project
cp /path/to/cth-plugin/.cursorrules ./
cp /path/to/cth-plugin/.mcp.json .cursor/mcp.json
```

## Other MCP-Compatible Environments

The plugin's skills are plain markdown files that work in any system that can load instruction documents. The `.mcp.json` defines standard MCP server connections that work with any MCP client.

### What's portable
- **Skills (markdown):** Work anywhere that accepts instruction files
- **MCP config:** Works with any MCP-compatible client
- **Brand guidelines:** Plain text/CSS — copy into any design system

### What's harness-specific
- **`.claude-plugin/plugin.json`:** Claude-specific manifest (ignored by other harnesses)
- **Slash commands:** Claude Cowork/Code specific (adapt to your harness's command system)
