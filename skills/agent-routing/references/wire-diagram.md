# Grok Bot ⇄ Cursor/Sonnet — wire diagrams

Both diagrams show the same 21-skill CTH bot roster. The only thing that
changes is **where each Bot's execution happens** and **which model pays
for it**. Nothing in the MCP config, the skill files, or the Approval Gate
changes.

## Before — everything runs inside the Grok Bot fleet

Every Bot, regardless of how mechanical its job is, lives on the same
shared cloud computer and draws from the same weekly Grok Bot token
allowance. There is no cheap tier inside the fleet itself, so trivial
daily chores and genuine strategic decisions cost the same thing.

```mermaid
flowchart TB
    G["Gideon"] -->|every request, big or small| CoS["Chief-of-Staff Bot\n(Grok Bot orchestrator)\nlives on top, routes by description"]

    subgraph FLEET["Grok Bot fleet — one shared cloud computer, one shared weekly quota"]
        CoS --> BrandBot["Brand Bot\ncleantechhub-brand / clp26-brand"]
        CoS --> GrantBot["Grant Bot\ncth-grant"]
        CoS --> PropBot["Proposal Bot\ncth-proposal-build"]
        CoS --> SEOBot["SEO Bot\ncth-seo"]
        CoS --> CampaignBot["Campaign Bot\nsocial-media-campaign"]
        CoS --> BufferBot["Buffer Bot"]
        CoS --> CanvaBot["Canva Bot"]
        CoS --> NotionBot["Notion Bot"]
        CoS --> MondayBot["Monday Bot"]
        CoS --> GmailBot["Gmail Bot"]
        CoS --> DriveBot["Drive Bot"]
        CoS --> SlackBot["Slack Bot"]
        CoS --> MiroBot["Miro Bot"]
        CoS --> BookStackBot["BookStack Bot"]
        CoS --> DoctorBot["Doctor_Bot"]
        CoS --> PDFBot["HTML→PDF Bot"]
        CoS --> OnePagerBot["Nexus One-Pager Bot"]
        CoS --> DashBot["Live Artifact / Dashboard Bot"]
        CoS --> ComposioBot["Composio Bot"]
        CoS --> SecretsBot["Secrets Bot"]
    end

    BrandBot & GrantBot & PropBot & SEOBot & CampaignBot & BufferBot & CanvaBot & NotionBot & MondayBot & GmailBot & DriveBot & SlackBot & MiroBot & BookStackBot & DoctorBot & PDFBot & OnePagerBot & DashBot & ComposioBot & SecretsBot --> Quota["Shared weekly Grok Bot quota\nburns fast — same cost for a\nBuffer re-check as a grant go/no-go"]

    Quota -.->|quota exhausted mid-week| Blocked["Fleet stalls until reset —\nincluding the tasks that\nactually needed judgment"]
```

**Problem in one sentence:** the fleet has one price tier, so the 90% of
tasks that are mechanical crowd out the 10% that actually need the Chief
of Staff's judgment.

## After — Grok Bot orchestrates, Cursor/Sonnet executes

The Chief-of-Staff Bot keeps doing exactly what it's good at: deciding
which lane a request belongs in. Everything that's routine **and**
already covered by an MCP connector or API this repo has wired up moves
to a Cursor background agent running Sonnet — a separate execution
surface with its own model choice, so it stops competing with strategic
work for the same tokens. Tasks that genuinely need Grok Bot's
browser/computer-use (no API exists) stay put. `secrets` never moves,
full stop.

```mermaid
flowchart TB
    G["Gideon"] --> CoS["Chief-of-Staff Bot\n(Grok Bot orchestrator)\nnow ONLY: triage + judgment calls"]

    CoS -->|"Axis check 1: ambiguous / high-stakes?\nAxis check 2: needs browser computer-use\n(no API — e.g. Search Console/Ads UI)?"| Decide{Route}

    Decide -->|"Yes to either axis"| STAYS

    subgraph STAYS["Stays on Grok Bot fleet"]
        direction TB
        Strategy["Strategic decisions:\ngrant go/no-go, proposal alignment gate,\ncampaign strategy, brand exceptions,\nSEO prioritization calls"]
        UIOnly["Computer-use-only work:\nGSC/Ads dashboards,\nany tool with no API"]
        SecretsLock["Secrets Bot\n(hard boundary — never mirrored)"]
    end

    Decide -->|"No to both axes\n→ routine + MCP/API covered"| Handoff["Handoff\nPhase 1: reply-line → Gideon starts a Cursor agent\nPhase 2: GitHub issue on this repo (skill, context, priority)"]

    Handoff --> CUR["Cursor IDE background agents\nmodel = Sonnet (explicit, per-agent)"]

    subgraph CURSOR["Cursor + Sonnet — mirrors the same skills/*.md library"]
        direction TB
        CUR --> DoctorBotC["Doctor_Bot scans"]
        CUR --> BufferC["Buffer_Bot"]
        CUR --> CanvaC["Canva_Bot"]
        CUR --> NotionC["Notion_Bot"]
        CUR --> MondayC["Monday_Bot"]
        CUR --> GmailC["Gmail_Bot"]
        CUR --> DriveC["Drive_Bot"]
        CUR --> SlackC["Slack_Bot"]
        CUR --> MiroC["Miro_Bot"]
        CUR --> BookStackC["BookStack_Bot"]
        CUR --> PDFC["HTML→PDF_Bot"]
        CUR --> OnePagerC["Nexus One-Pager_Bot"]
        CUR --> DashC["Dashboard build (repo-hosted, replaces Cowork-sidebar artifact)"]
        CUR --> ComposioC["Composio_Bot (once target tool is decided)"]
        CUR --> ExecHalf["Execution half of hybrids:\ncaption drafting + scheduling,\ngrant budget tables, proposal HTML/PDF build,\non-brand formatting"]
    end

    DoctorBotC & BufferC & CanvaC & NotionC & MondayC & GmailC & DriveC & SlackC & MiroC & BookStackC & PDFC & OnePagerC & DashC & ComposioC & ExecHalf --> Result["Result posted back\n(GitHub comment / Notion / Monday)"]

    Result --> Gate{"Public-voice content?"}
    Gate -->|Yes| Approval["Awaiting Gideon's approval\n(unchanged — CLAUDE.md rule)"]
    Gate -->|No| Done["Done — zero Grok Bot tokens spent"]

    Approval --> G
    Done --> G

    STAYS --> QuotaAfter["Grok Bot's weekly quota now spent\nonly on judgment calls and computer-use work —\nlasts the full week"]

    MonitorNote["Doctor_Bot gains a check_grok_bot_quota.py check:\nAMBER at 70% used w/ 3+ days left, RED at 90%.\nA RED/AMBER fire means something routine\nleaked back onto the Grok Bot fleet — audit and re-route."]
```

## Per-skill scoring (both axes)

"MCP/API?" = Cursor already has a wired connector or API/CLI path for
this (see `.mcp.json` + BookStack's Docker/REST API + local Playwright for
HTML→PDF). "Judgment?" = does the core of the task require a real
decision, not just execution.

| Skill (CTH Bot) | MCP/API available? | Judgment-heavy? | Verdict |
|---|---|---|---|
| `doctor-bot` | Yes (MCP connector health + Shell/SSH for VPS) | No — read-only by design | **Full mirror → Cursor/Sonnet.** Best first candidate. |
| `buffer` | Yes (Buffer MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `canva` | Yes (Canva MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `notion` | Yes (Notion MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `monday` | Yes (Monday MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `google-drive` | Yes (Drive MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `slack` | Yes (Slack MCP) | Mostly no (sensitive comms = escalate) | **Mirror, with an escalation rule for sensitive threads.** |
| `gmail` | Yes (Gmail MCP) | Mostly no (sensitive replies = escalate) | **Mirror, with an escalation rule for sensitive replies.** |
| `miro` | Yes (Miro MCP) | No | **Full mirror → Cursor/Sonnet.** |
| `bookstack` | Yes (Docker/REST API via Shell) | No | **Full mirror → Cursor/Sonnet.** |
| `html-to-pdf` | Yes (local Playwright, no external site) | No | **Full mirror → Cursor/Sonnet.** |
| `composio` | Yes (it's the gateway itself) | No, once target tool is picked | **Mirror once Grok Bot/user names the target integration.** |
| `live-artifact-build` | Partial — the "Cowork sidebar" mechanic is Claude-Cowork-specific | No | **Adapt, don't mirror 1:1** — Cursor produces a repo-hosted HTML/Markdown dashboard file instead. |
| `nexus-onepager` | Yes (static HTML, file-based deploy) | Only the content/brand call | **Hybrid** — content approved on Grok Bot, page build on Cursor/Sonnet. |
| `cleantechhub-brand` | Yes (formatting existing content) | Only co-branding edge cases | **Hybrid** — standard application on Cursor, exceptions escalate. |
| `clp26-brand` | Yes | Only edge cases | **Hybrid**, same pattern as above. |
| `social-media-campaign` | Yes (Buffer/Canva/Notion MCP) | Only the strategy-setup phase | **Hybrid** — strategy (brand/platforms/pillars/approval flow) stays on Grok Bot; captions, scheduling, monitoring, reporting → Cursor/Sonnet. |
| `cth-grant` | Partial (Drive/Gmail MCP for research/drafting) | Yes — go/no-go, budget/scope | **Hybrid** — decision stays on Grok Bot; drafting, budget tables, logframe assembly → Cursor/Sonnet. |
| `cth-proposal-build` | Yes (HTML build + local PDF export) | Yes — alignment gate | **Hybrid** — alignment gate stays on Grok Bot; HTML build/PDF export/deploy → Cursor/Sonnet. |
| `cth-seo` | Partial — no MCP for Google Search Console/Ads listed in `.mcp.json` | Yes — prioritization, cannibalization calls | **Mostly stays on Grok Bot.** Strategy and any GSC/Ads-dashboard work needs Grok Bot's computer-use; only in-repo work (meta tags, schema markup, on-page content in code) moves to Cursor/Sonnet. |
| `secrets` | N/A | N/A | **Never mirrored.** Stays exclusively on Grok Bot / VPS. Hard rule, not a judgment call. |

## Reading the diagrams

- The **shape of the fleet doesn't change** — same 21 bots, same jobs.
  What moves is the *execution surface* for the bottom two-thirds of the
  table.
- The Chief-of-Staff Bot's job description on Grok Bot should be edited to
  say explicitly: *"For any task that is routine and covered by an
  existing Cursor MCP connector or API, hand off to Cursor via GitHub
  issue instead of executing it yourself."* That one line is the entire
  implementation of Phase 2.
- Doctor_Bot's new quota check is the feedback loop that catches drift —
  if routine work quietly creeps back onto the Grok Bot fleet, it shows up
  as an unexplained rise in weekly token burn before the quota actually
  runs out.
