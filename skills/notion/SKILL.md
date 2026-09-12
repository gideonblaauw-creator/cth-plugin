---
name: notion
description: >
  Searches, creates, moves, and reorganizes Notion pages; hosts Understanding Lab
  loops (5-beat flow: Context, Explanation, Playground, Shared decisions, Next cycle).
  Use when: Notion, restructure pages, move to Notion, clean up Notion, Understanding
  Lab, understanding loop, agent explanation page, major Lane A PR gate.
license: MIT
metadata:
  version: "2.5.0"
  category: "operations"
---

# Notion Operations

Search, create, update, and reorganize pages and databases in Notion — manage the CTH content database, campaign calendars, project documentation, workspace structure, and human-in-the-loop understanding surfaces.

## Human-in-the-loop — Understanding Lab

Notion is the default HITL surface for **understand to participate**, not thumbs-up-only verification. After meaningful agent work, desks and Hands plant **Understanding Lab** artifacts here so teammates can comment, quiz, and decide together.

**Thesis (Geoffrey Litt, Notion):** Agents increasingly handle correctness verification. Humans stay in the loop to understand across successive loops. Unexplained agent velocity = cognitive debt.

Three techniques (Geoffrey Litt pillars) — full playbook: `references/hitl-understanding-loops.md`.

**Synonym map (legacy → locked):** Home → Context · Explainer → Explanation (+ quiz) · Micro world / Microworld → Playground · Decisions DB (beat) → Shared decisions · Next loop → Next cycle · HITL Lab → Understanding Lab · View HITL Lab → View Understanding Lab. Existing Notion page titles may still use legacy names.

### Understanding Lab — 5-beat flow

For **major Lane A builds**, plant a collaborative **Understanding Lab** in Notion. Walk reviewers through five beats in this order only:

```
Context → Explanation (quiz) → Playground → Shared decisions → Next cycle
```

| Beat | Page / artifact | Purpose |
|---|---|---|
| 1. **Context** | Lab landing page | Context, links, language toggle, who is reviewing |
| 2. **Explanation** (+ quiz) | Background → Intuition → Literate walkthrough → **Quiz** (5 medium questions) | Comprehension gate |
| 3. **Playground** | Scenario-based interactive surface | **Key understanding step** — see Playground definition below |
| 4. **Shared decisions** | Shared decisions database (Notion page may still be titled Decisions DB) | Record rationale, blockers, and go/no-go rows **after** Playground choice |
| 5. **Next cycle** | Handoff page | What ships, what returns, what the next cycle needs |

**Playground sits between Explanation and Shared decisions** — comprehension first, then scenario exploration, then locked team decisions. Playground is the **key understanding step** (Explanation orients; Shared decisions records locked intent).

#### Playground definition (Gideon 2026-09-12 — hard)

Playground is **not** only scrubbing agent findings or agree/override/defer on one suggestion.

Playground **must**:

1. Give **scenarios** — concrete situations tied to the build.
2. Surface **consequences** of each path (what happens if…).
3. Give **optionality** — especially when the reviewer is less familiar with the topic: the agent proposes **2–4 clear alternative options** with tradeoffs, not a single forced recommendation.
4. Let the human pick / combine / defer **before** Shared decisions records the lock.

**Flow inside beat 3:** `scenario → consequences → options → choose` — then proceed to Shared decisions.

### Gate policy — major builds only

The Understanding Lab gate applies to **Lane A major builds only**:

- CTH Apps, client products, Tools, FabFloow products, and similar substantive PRs.
- **Not** every tiny or mechanical PR (copy tweaks, inventories, stub updates, version bumps without behavior change).

**Trigger:** major PRs only on **Lane A allowlist repos** (see `skills/harness/SKILL.md` § Lane A repo lock). Match `repo_url` to the owning repo before planting a lab. Wrong repo = miss.

**Maker ≠ checker:** Hands plants the lab and opens a **draft** PR. Infrastructure Desk reviews. Gideon merges.

### Timebox

Total human gate ≤ **10 minutes** (suggested split):

- Explanation + quiz — ~4 min
- Playground — ~3 min
- Shared decisions — ~3 min

Design each beat to respect the box. Quiz = speed regulator; do not mark **Approved** until quiz passed or waived with a one-line reason on the page.

### Collaborative — not solo Gideon

Understanding Lab is a **shared space**. Team members participate via page comments and Shared decisions rows. Do not assume Gideon reviews alone. Plant enough context for async teammates to contribute.

### EN / ES

Lab pages support a **language toggle** — either dual pages (EN + ES) or an in-page switch pattern. Default EN; mirror key beats for Spanish-speaking reviewers when the build touches ES audiences.

### Running demo (reference implementations)

Use these as templates when planting a new lab:

| Demo | Repo / subject | Notes |
|---|---|---|
| **Dataroom Reviewer** | `gideonblaauw-creator/cth-data-room-scanner` | Teclogi-only Lane A repo |
| **Synthetic VertiGreen** | FabFloow / client product example | Sim + decisions pattern |
| **CleantechHUB Notion lab URLs** | CTH Apps on allowlist repos | Context → Explanation → Playground → Shared decisions → Next cycle |

### i) Explanations (Geoffrey Litt pillar → beat 2)

After meaningful agent work, create an **Explanation** page in Notion:

1. Background → Intuition/essence → Literate walkthrough → Quiz (5 medium questions).
2. Prefer Notion over local-only HTML so teammates can comment.
3. Quiz = speed regulator. Do not mark **Approved** until quiz passed or waived with a one-line reason on the page.
4. Tasteful HTML blocks only (Notion HTML blocks for interactive figures). Avoid interactive slop.

### ii) Playground (Geoffrey Litt pillar → beat 3)

When prose is not enough to feel the behavior — see **Playground definition** above (hard gate):

1. Agent builds scenarios with consequences and **2–4 option paths** with tradeoffs (not a single forced recommendation).
2. Host via Notion HTML block, stable HTML (`HITL_HTML_STABLE_URL`), or local fallback.
3. Learning artifact, not product scope. Flow: `scenario → consequences → options → choose`.
4. Human picks / combines / defers **before** Shared decisions locks intent. Archive Playground when the mental model lands; keep the Explanation.

### iii) Shared spaces (Geoffrey Litt pillar → beat 4)

Plans, explanations, and decisions live in Notion multiplayer:

1. Shared threads (humans + agents).
2. Commentable plan docs.
3. Shared decisions databases with human rationale (Notion page title may still read Decisions DB).

Collective understanding beats private laptop artifacts. **Shared decisions** is beat 4 in the Understanding Lab flow.

### View Understanding Lab delivery (major Lane A)

When Hands opens a **major** Lane A draft PR on an allowlist repo, the PR body **MUST** end with this block (fill real URLs):

```markdown
## View Understanding Lab
- **Context (Notion):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (stable HTML):** HITL_HTML_STABLE_URL
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after ≤10 min Understanding Lab pass (Explanation → Playground → Shared decisions).
```

**Cursor product limit:** The cloud-agent **View PR** card cannot host a native second button. That is a Cursor product surface — we cannot add it. Infra chat **must** post **View Understanding Lab** as its own prominent link beside the agent card whenever a major Hands run finishes. Do not bury links only in the PR body.

**Stable HTML host:** Placeholder `HITL_HTML_STABLE_URL` in `skills/harness/SKILL.md` until Infra plants Vercel/Tailscale. Do not invent a fake URL. Paste helper: `docs/view-understanding-lab-footer.md`.

### HITL operating rules

- **Understand to participate** — HITL is for comprehension across loops, not rubber-stamp approval.
- **Major builds only** — Do not plant a full Understanding Lab for tiny/mechanical PRs.
- **Cognitive debt pause** — If velocity outpaces explanation, pause new work and write the Explanation first.
- **Collaborative** — Shared space; team comments and Shared decisions rows; not solo Gideon.
- **Timebox** — ≤ 10 min total human gate across Explanation, Playground, and Shared decisions.
- **Playground hard gate** — Beat 3 must follow `scenario → consequences → options → choose`; not scrub-only or single-suggestion override.
- **Secrets** — Use Infisical (`skills/infisical/SKILL.md`); never paste tokens in Notion or chat.
- **Notion is not secrets SoT** — Notion holds plans and rationale; credentials stay in Infisical.

## Workspace Overview

CleantechHUB uses Notion as a content database and knowledge management system. Key structures include:
- **Campaign content calendars**: databases tracking social media posts, newsletters, and content pipeline status
- **Project documentation**: pages and sub-pages for active programs, clients, and initiatives
- **Knowledge base**: reference materials, SOPs, and organizational guides
- **Contact and partner databases**: structured records of key relationships

## Standard Workflows

### Search for Content

1. Search by title or content keywords using the Notion search endpoint
2. Filter results by database, parent page, or page type
3. Read the page content to verify it matches what the user needs
4. Present relevant content with the page title and URL for easy access

Search tips:
- Use exact page titles when known for precise matches
- For broad searches, use key phrases that would appear in the page content
- Filter by database to narrow results when working with structured data

### Create a Page

1. Identify the target location — a database (for structured entries) or a parent page (for documentation)
2. For database entries, determine the required properties (columns) and their formats
3. Create the page with:
   - Title/name property
   - All required database properties filled in
   - Content blocks for the page body
4. Verify the page was created in the correct location

### Update a Page

1. Search for and read the existing page to get its current state
2. Modify properties (database columns) or content blocks as needed
3. For property updates, match the exact property format expected by the database
4. Confirm the update was applied correctly

### Content Calendar Management

The content calendar workflow is central to CTH operations:

1. **Search the campaign database** for existing entries by date range, platform, or status
2. **Create new entries** with required fields:
   - Title: descriptive content title
   - Platform: LinkedIn, Instagram, Facebook, etc.
   - Scheduled date: publication date
   - Status: Draft, Ready, Scheduled, Published
   - Image URL: link to the visual asset (from Canva export)
   - Copy: the post text content
3. **Update entry status** as content moves through the pipeline:
   - Draft: content is being written
   - Ready: content approved and image prepared
   - Scheduled: posted to Buffer or the platform's scheduler
   - Published: live on the platform
4. **Track metrics**: update entries with engagement data after publication

### Workspace Reorganization

When restructuring the Notion workspace:

1. **Audit the current structure**: scan top-level pages and databases to understand the existing layout
2. **Map the desired structure**: define the target hierarchy before making changes
3. **Move pages systematically**: relocate pages to their new parents, working top-down
4. **Update cross-references**: after moving pages, check and fix any internal links that may have broken
5. **Archive obsolete content**: move outdated pages to an Archive section rather than deleting them

## Database Properties

Notion databases use typed properties. Common types and their formats:

- **Title**: the page name (every database has exactly one title property)
- **Select**: single choice from predefined options — `{"name": "Option A"}`
- **Multi-select**: multiple choices — `[{"name": "Tag1"}, {"name": "Tag2"}]`
- **Date**: `{"start": "2026-08-15"}` or with end: `{"start": "2026-08-15", "end": "2026-08-20"}`
- **URL**: plain string URL
- **Email**: plain string email
- **Number**: plain number value
- **Checkbox**: `true` or `false`
- **Rich text**: array of text objects with optional formatting
- **Relation**: links to pages in another database — requires the related page IDs
- **Status**: similar to select but with groups (To Do, In Progress, Done)

Always inspect the database schema before creating or updating entries to ensure property formats match.

## Content Blocks

Page content is built from blocks:

- **Paragraph**: standard text content
- **Headings**: H1, H2, H3 for document structure
- **Bulleted list**: unordered list items
- **Numbered list**: ordered list items
- **To-do**: checkbox items
- **Toggle**: collapsible content sections
- **Callout**: highlighted information boxes
- **Quote**: block quotes
- **Divider**: visual separator
- **Table**: structured data within a page
- **Code**: formatted code blocks with language syntax highlighting

Build pages with clear hierarchy: heading, then supporting content, then sub-sections. Use callouts for important notes and toggles for detailed reference material that does not need to be visible by default.

## Integration with Other Tools

### Notion to Buffer Pipeline
1. Query the content calendar for entries with status "Ready" and a scheduled date
2. Extract post text, platform, and image URL
3. Hand off to the `buffer` skill for scheduling
4. Update the Notion entry status to "Scheduled" with the Buffer post ID

### Notion from Google Drive
1. Find the relevant document in Drive
2. Extract or summarize the content
3. Create a Notion page with the content
4. Link back to the original Drive document

## Rules

- **Audit before reorganizing**: Never move or restructure pages without first understanding the current layout. Map current state, then plan changes.
- **Batch operations**: Space out API calls to avoid rate limits. For large-scale operations (50+ pages), process in batches of 10-20.
- **Confirm destructive operations**: Never delete pages without explicit user confirmation. Prefer archiving over deletion.
- **Preserve existing content**: When updating a page, read it first to avoid overwriting content that others may have added.
- **Cross-references**: After moving pages, verify internal links still work. Notion usually handles this, but confirm for critical documentation.

## Troubleshooting

- **Page not found**: Try searching by exact title. The page may be in a different workspace or shared space. Check if the integration has access to the relevant pages.
- **Property format errors**: Read the database schema to check the exact property types and allowed values. Select/multi-select options must match existing options exactly.
- **Rate limiting**: Notion enforces rate limits on API calls. Implement delays between batch operations. Retry with exponential backoff on 429 responses.
- **Missing content after update**: Always read the full page before updating to avoid overwriting. Notion page updates can replace content if not handled carefully.

## References

- `references/hitl-understanding-loops.md` — HITL understanding loops (explainers, micro worlds, shared spaces); load when planting or reviewing agent explainers.
- Other Notion database schemas and workspace map — see `references/` when present.
