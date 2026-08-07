# Connectors

## How tool references work

This plugin's skills reference specific tools that CleantechHUB uses in its daily operations. When a skill mentions a tool (e.g., Buffer, Canva, Monday.com), it describes CleantechHUB's standard workflow with that tool.

If your environment uses a different tool in the same category, adapt the instructions accordingly. The skills are written as workflow guides, not hard dependencies on a specific product.

## Connectors for this plugin

| Category | CTH Standard | Alternatives | Required? |
|----------|-------------|--------------|-----------|
| Social media scheduler | Buffer | Hootsuite, Later, Sprout Social | For campaign skills |
| Design | Canva | Figma, Adobe Express | For visual content |
| Project management | Monday.com | Asana, Linear, Jira | For task tracking |
| Chat | Slack | Microsoft Teams, Discord | For team communication |
| Email | Gmail | Outlook, ProtonMail | For email workflows |
| File storage | Google Drive | OneDrive, Dropbox | For document management |
| Calendar | Google Calendar | Outlook Calendar | For scheduling |
| Knowledge base | BookStack (self-hosted) | Notion, Confluence | For wiki/docs |
| Knowledge management | Notion | Coda, Airtable | For content databases |
| Collaboration boards | Miro | FigJam, Mural | For visual collaboration |
| Integration gateway | Composio | Zapier, Make | For cross-tool automation |
| Issue tracking | Atlassian (Jira + Confluence) | GitHub Issues, Linear | For dev workflows |
| Marketing analytics | Windsor.ai | Google Analytics, Mixpanel | For ad/campaign data |

## Authentication

Each user must authenticate their own connectors. Installing this plugin does NOT grant access to any CleantechHUB accounts. Skills provide workflow instructions only — credentials are always per-user.

## Harness-Specific Setup

### Claude Cowork / Claude Desktop
Connectors are managed in Settings → MCP Connectors. Most tools above have official Claude MCP connectors available in the marketplace.

### Cursor
Add MCP servers to your `.cursor/mcp.json` or project-level `.mcp.json`. See the `.mcp.json` file in this plugin for reference configurations.

### Claude Code CLI
Add MCP servers to your `~/.claude/.mcp.json` or project-level `.mcp.json`.

### Other harnesses
Any MCP-compatible environment can use the connector definitions in `.mcp.json`. Skills are plain markdown and work in any system that loads instruction files.
