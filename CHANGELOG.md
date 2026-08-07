# Changelog

All notable changes to the CleantechHUB Cowork Plugin are documented in this file.

## [2.0.0] — 2026-08-07

### Major update — harness-agnostic architecture and expanded skill coverage.

**Skills: 24 (up from 15)**
- **Brand Identity (5):** cleantechhub-brand, clp26-brand, sustenttia-brand, dialogos-del-futuro-brand, tec-alianza-brand
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
