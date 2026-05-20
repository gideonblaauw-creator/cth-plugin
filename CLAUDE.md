# CleantechHUB Plugin — Source of Truth

This directory is the **source** for the `cleantechhub` plugin (version 1.2.0).
Claude Desktop caches plugins to a read-only location inside `~/Library/Application Support/Claude/`.
Edits to that cache are lost on restart and may be blocked by the sandbox.

## How to edit skills

**Always edit skills here** at their source path:

```
/Users/gideonblaauw/Documents/Claude/Projects/cth-plugin/skills/<skill-name>/SKILL.md
```

Never edit the cached copy at `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/`.

After editing a skill SKILL.md here, Claude Desktop picks up the change on the next session or plugin reload — no manual copy needed.

## Connecting this folder in Claude Desktop

For a Cowork/sandbox session to edit skills, this folder must be connected:

1. Open Claude Desktop
2. Start or open a Cowork session
3. Click the folder icon (connected folders)
4. Add: `/Users/gideonblaauw/Documents/Claude/Projects/cth-plugin`

Once connected, the session can read and write all skills in `skills/`.

## Skill inventory

| Skill | Purpose |
|-------|---------|
| bookstack | BookStack wiki API patterns |
| buffer | Buffer GraphQL publishing |
| canva | Canva design API |
| cleantechhub-brand | CTH brand identity + voice |
| clp26-brand | CLP26 campaign brand |
| cth-grant | Grant writing workflow |
| cth-proposal-build | Proposal assembly |
| cth-seo | SEO command center |
| doctor-bot | Infrastructure health bot |
| dual-desktop-macos | Dual Claude Desktop setup |
| gmail | Gmail MCP patterns |
| google-drive | Google Drive MCP patterns |
| monday | Monday.com API patterns |
| secrets | Infisical secrets protocol |
| social-media-campaign | Social media workflow |
| sustenttia-brand | Sustenttia diagnostic brand |

## Important: Anthropic built-in skills are separate

Skills prefixed `anthropic-skills:` (like `schedule`, `consolidate-memory`, `setup-cowork`, `xlsx`, `pdf`) are **Anthropic-managed** and live in a separate read-only cache. These cannot and should not be edited. They are NOT part of this plugin.

## For subagents (Claude Code)

Subagents spawned with `isolation: "worktree"` cannot access `~/.claude/`.
If a subagent needs skill content, copy the relevant SKILL.md into the project working directory before spawning.
See Rule 5 in the gideon-workflow skill.
