# CleantechHUB Cowork Plugin

Operational plugin for CleantechHUB collaborators — brand guidelines, program management, tool integrations, and infrastructure monitoring. Harness-agnostic: works in Claude Cowork, Claude Code CLI, Cursor, and any MCP-compatible environment.

**Version:** 2.0.1  
**Author:** [CleantechHUB Foundation](https://cleantechhub.net)  
**License:** MIT

---

## What This Plugin Does

The CTH Plugin provides **21 skills** organized across **4 categories** that encode CleantechHUB's operational knowledge — from brand guidelines and grant writing to infrastructure monitoring and social media campaigns. Each skill is a structured markdown file that teaches an AI assistant how to perform a specific CTH workflow correctly, including hard-won lessons and failure modes.

The plugin also defines **13 connector categories** mapping CleantechHUB's standard tools (Buffer, Canva, Monday.com, etc.) to their MCP integrations, with documented alternatives for teams using different products.

---

## Quick Start

### Claude Cowork (primary)

1. Install the plugin via Claude Desktop → Settings → Plugins
2. Connect the MCP connectors you need (see [CONNECTORS.md](CONNECTORS.md))
3. Skills activate automatically based on your prompts

### Claude Code CLI

```bash
# Option 1: Clone directly
cd ~/.claude/plugins/
git clone https://github.com/gideonblaauw-creator/cth-plugin.git

# Option 2: Symlink from your projects
ln -s /path/to/cth-plugin ~/.claude/plugins/cth-plugin
```

Skills are available as slash commands. MCP servers from `.mcp.json` load automatically.

### Cursor

1. Copy `.cursorrules` from this repo to your project root (or merge with existing)
2. Copy or merge `.mcp.json` into your project's `.cursor/mcp.json`
3. Skills content is embedded in `.cursorrules` as context rules

```bash
cp /path/to/cth-plugin/.cursorrules ./
cp /path/to/cth-plugin/.mcp.json .cursor/mcp.json
```

For detailed multi-harness setup instructions, see [HARNESS.md](HARNESS.md).

---

## Skill Inventory

### Brand Identity

| Skill | What It Does |
|-------|-------------|
| `cleantechhub-brand` | Apply CleantechHUB brand guidelines — colors, typography, tone, and visual identity — to any external-facing content |
| `clp26-brand` | Apply ClimateLaunchpad 2026 campaign brand for the CleantechHUB social media campaign across Colombia, Peru, El Salvador, Guatemala, and Costa Rica |

### Programs

| Skill | What It Does |
|-------|-------------|
| `social-media-campaign` | End-to-end social media campaign playbook — Claude generates captions, Canva/Ideogram generates images, Notion stores content, Pipedream orchestrates, Buffer publishes |
| `cth-grant` | Grant lifecycle management — go/no-go assessment, scoping, budgeting, theory of change, deliverables, and submission for CTH funders |
| `cth-proposal-build` | Build polished client-facing service proposals — research, alignment gate, HTML build, PDF export, and deployment |
| `cth-seo` | SEO command center for cleantechhub.net subdomains — keywords, schema markup, content strategy, Google Ads Grant, AEO, and technical audits |
| `nexus-onepager` | Build and deploy bilingual (EN/ES) startup one-pager profile pages at nexus.cleantechhub.net |

### Operations

| Skill | What It Does |
|-------|-------------|
| `bookstack` | Deploy, configure, and manage the BookStack wiki instance at wiki.cleantechhub.net via Docker and REST API |
| `buffer` | Schedule, draft, and publish social media posts via Buffer — includes image URL requirements and silent-failure traps |
| `canva` | Export designs, prepare images for downstream tools — includes critical export-before-use sequencing rules |
| `monday` | Build and manage Monday.com workspaces, boards, dashboards, items, and automation for CTH project management |
| `gmail` | Search, read, draft, and manage email through Gmail — query syntax, threading rules, and correspondence compilation |
| `google-drive` | Search, read, upload, and manage files in Google Drive — document retrieval, content reading, and file organization |
| `slack` | Search, read, and post messages in Slack — channel resolution, message drafting, and Canvas management |
| `notion` | Search, create, move, and reorganize Notion pages — content databases, campaign calendars, and workspace structure |
| `composio` | Connect to hundreds of third-party services through Composio's integration gateway when no dedicated connector exists |
| `miro` | Read and create content on Miro boards — diagrams, structured docs, tables, and workflow visualizations |

### Infrastructure

| Skill | What It Does |
|-------|-------------|
| `doctor-bot` | Invoke and interpret Doctor_Bot — infrastructure health agent monitoring MCP connectors, OVH VPS services, and Pipedream workflows |
| `secrets` | Secrets management protocol for all CTH projects — storing, rotating, scanning, and recovering API keys, tokens, and credentials |
| `html-to-pdf` | Convert self-contained HTML documents to high-quality PDF using Playwright — proposals, reports, one-pagers, and invoices |
| `live-artifact-build` | Create and maintain persistent live artifacts in the Cowork sidebar — dashboards, trackers, status pages, and build monitors |

---

## Connectors

The plugin references specific tools that CleantechHUB uses daily. If your environment uses a different tool in the same category, adapt the instructions accordingly.

| Category | CTH Standard | Alternatives |
|----------|-------------|--------------|
| Social media scheduler | Buffer | Hootsuite, Later, Sprout Social |
| Design | Canva | Figma, Adobe Express |
| Project management | Monday.com | Asana, Linear, Jira |
| Chat | Slack | Microsoft Teams, Discord |
| Email | Gmail | Outlook, ProtonMail |
| File storage | Google Drive | OneDrive, Dropbox |
| Calendar | Google Calendar | Outlook Calendar |
| Knowledge base | BookStack (self-hosted) | Notion, Confluence |
| Knowledge management | Notion | Coda, Airtable |
| Collaboration boards | Miro | FigJam, Mural |
| Integration gateway | Composio | Zapier, Make |
| Issue tracking | Atlassian (Jira + Confluence) | GitHub Issues, Linear |
| Marketing analytics | Windsor.ai | Google Analytics, Mixpanel |

For full connector details and per-harness authentication setup, see [CONNECTORS.md](CONNECTORS.md).

---

## Security

Installing this plugin does **NOT** share any credentials or grant access to CleantechHUB accounts. Skills provide workflow instructions only — each user must authenticate their own connectors independently. API keys, tokens, and passwords are never embedded in skill files.

---

## Project Structure

```
cth-plugin/
├── .claude-plugin/
│   └── plugin.json          # Claude plugin manifest
├── skills/
│   ├── cleantechhub-brand/  # Brand identity skills
│   ├── buffer/              # Operations skills
│   ├── doctor-bot/          # Infrastructure skills
│   └── ...                  # 21 skill directories total
├── .cursorrules             # Cursor IDE context rules
├── .mcp.json                # MCP server configurations
├── CLAUDE.md                # AI assistant context
├── CONNECTORS.md            # Tool mapping and alternatives
├── HARNESS.md               # Multi-harness setup guide
├── CHANGELOG.md             # Version history
└── README.md                # This file
```

---

## Links

- **Website:** [cleantechhub.net](https://cleantechhub.net)
- **Repository:** [github.com/gideonblaauw-creator/cth-plugin](https://github.com/gideonblaauw-creator/cth-plugin)
- **Setup Guide:** [HARNESS.md](HARNESS.md)
- **Connector Details:** [CONNECTORS.md](CONNECTORS.md)
