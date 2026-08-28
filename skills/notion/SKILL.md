---
name: notion
description: >
  Searches, creates, moves, and reorganizes Notion pages. Use when: Notion,
  restructure pages, move to Notion, clean up Notion.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# Notion Operations

Search, create, update, and reorganize pages and databases in Notion — manage the CTH content database, campaign calendars, project documentation, and workspace structure.

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

For Notion database schemas and workspace map, see references/.
