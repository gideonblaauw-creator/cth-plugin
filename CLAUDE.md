# CLAUDE.md

This is the CleantechHUB plugin for Claude-compatible AI assistants.

## Communication

- Communicate in neutral English by default.
- Switch to Spanish when the user writes in Spanish or the task explicitly targets a Spanish-speaking audience.
- Keep tone expert but accessible, action-oriented, and concise.

## Brand Rules

Before drafting any branded content, identify which brand applies:

**CTH brands (owned by CleantechHUB Foundation):**
- CleantechHUB — the foundation itself
- ClimateLaunchpad / CLP26 — green business competition (CTH is National Organizer)
- Dialogos del Futuro — higher education transformation program
- TecAlianza — technical education initiative (joint with Uniandes + Colsubsidio)
- Nexus — startup portfolio platform

**Client brands (separate identity, do not mix with CTH):**
- Sustenttia — sustainability consulting firm (CTH client)

Each brand has its own skill in `skills/` with colors, typography, and tone rules. Never apply CleantechHUB visual identity to client brand materials unless explicitly co-branding.

## Approval Gate

Mark any public-voice CleantechHUB content (social media posts, newsletter copy, website text, external communications) as **"Awaiting Gideon's approval"** before publishing or sending. Internal drafts and working documents do not require this gate.

## Infrastructure

- **VPS:** OVH VPS — all long-running CleantechHUB services deploy here alongside BookStack. Never spin up a new host.
- **Containers:** Docker-based — BookStack, Caddy (reverse proxy), MariaDB, Chroma (Sustenttia), and other services run as containers.
- **Monitoring:** Doctor_Bot checks VPS health, MCP connectors, TLS certificates, disk, and memory.

## Domains

- `cleantechhub.net` — Main website (WordPress)
- `wiki.cleantechhub.net` — Knowledge base (BookStack)
- `nexus.cleantechhub.net` — Startup portfolio (static HTML)

## Plugin Structure

- `skills/` — 24 skill directories, each with a `SKILL.md` and optional `references/` for detailed knowledge
- `.cursorrules` — Cursor IDE context (brand colors, infrastructure rule, code standards)
- `.mcp.json` — MCP server configurations for connectors
- `CONNECTORS.md` — Tool category mapping with CTH standards and alternatives
- `HARNESS.md` — Setup instructions for Claude Cowork, Claude Code CLI, Cursor, and other harnesses (this is setup docs, not the CTH Harness rulebook)

For detailed operational knowledge on any topic, read the relevant `skills/<name>/SKILL.md` file.

## CTH Harness

Cloud Hands agents (Cursor cloud agents executing tickets) must read `skills/harness/SKILL.md` before starting any task. That file is the CTH Harness rulebook: five terms (Workbench, Tools, Tickets, Cloud Hands, Desks), ticket lanes, store hierarchy, org, and gates. Ticket contracts live in `tickets/TEMPLATE.md`. Note: `HARNESS.md` in this repo is Cowork/CLI/Cursor setup docs — it is not the CTH Harness rulebook.

## App-build protocol

Before promoting a tree to GitHub, creating a repo, or opening a branch on any service/app/pipeline, Cloud Hands must read `skills/app-build/SKILL.md`. That file is the app-build protocol: classify (Archive vs existing repo vs new repo), the three-condition gate for new repos, the path (Desk tickets → Infrastructure classifies → Gideon locks → Hands writes → Gideon merges and deploys), and Hands rules (no secrets, no UUIDs, no Mac as SoT, no deploy by Hands).
