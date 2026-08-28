---
name: monday
description: >
  Manages Monday.com workspaces, boards, dashboards, automations. Use when:
  Monday.com, boards, workdocs, widgets.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# Monday.com Operations

Manage CleantechHUB project boards, delegation workflows, dashboards, and automation on Monday.com. Handle board creation, item management, column value formatting, and team coordination.

## CTH Workspace

CleantechHUB uses Monday.com for project management and team delegation. Key structures include:
- **CTH Team Delegation board**: central hub for task assignment and tracking
- **Project-specific boards**: individual boards for active programs and client projects
- **Dashboards**: aggregated views across multiple boards for management oversight

## API Patterns

Monday.com uses a GraphQL API. All operations go through GraphQL queries and mutations.

### Discovery and Navigation

- **Get user context**: Call `get_user_context` first to understand the current user's permissions and workspace membership.
- **List workspaces**: Call `list_workspaces` to see all available workspaces.
- **Search**: Use `search` to find boards, items, or content by keyword.
- **Board info**: Call `get_board_info` with a board ID to see its structure — columns, groups, and settings.

### Board Operations

- **Get board items**: Call `get_board_items_page` with the board ID. Results are paginated — handle the cursor for large boards.
- **Create items**: Use `create_item` with board_id, group_id, item_name, and column_values.
- **Create multiple items**: Use `create_items` for batch creation — more efficient than individual calls.
- **Update items**: Use `update_items` or `change_item_column_values` to modify existing item data.

### Column Value Format

Column values must be passed as JSON strings matching Monday's expected format. This is the single most common source of errors. Always check the column type before setting values.

#### Common Column Types and Formats

**Status column**:
```json
{"label": "Done"}
```
Or by index: `{"index": 2}`. Use `get_column_type_info` to find available labels and indices.

**Date column**:
```json
{"date": "2026-08-15"}
```
Optional time: `{"date": "2026-08-15", "time": "14:00:00"}`

**Person column**:
```json
{"personsAndTeams": [{"id": 12345, "kind": "person"}]}
```
Get person IDs from `list_users_and_teams`.

**Text column**:
Plain string value — no JSON wrapping needed.

**Numbers column**:
Plain number as string: `"42"` or `"3.14"`

**Timeline column**:
```json
{"from": "2026-08-01", "to": "2026-08-31"}
```

**Dropdown column**:
```json
{"labels": ["Option A", "Option B"]}
```

**Link column**:
```json
{"url": "https://example.com", "text": "Display text"}
```

Always call `get_column_type_info` for a column before constructing its value. The exact format varies by column type and incorrect formatting causes silent failures.

## Delegation Workflow

When a task needs CTH team delegation:

1. **Create the item** on the CTH Team Delegation board with:
   - Clear, actionable item name
   - Status set to "Pending"
   - Assigned person (use their Monday.com person ID)
   - Deadline date
   - Description with full context in the updates section
2. **Add an update** (comment) to the item with detailed instructions using `create_update`
3. **Set priority** if applicable via the priority column
4. **Mark approval requirement**: If the output involves CTH's public voice (social media, external communications, published content), note "Awaiting Gideon's approval" in the status or update

## Dashboard and Widget Management

### Create a Dashboard
1. Call `create_dashboard` with a name and optional description
2. Add widgets using `create_widget` — specify the widget type and configuration
3. Connect widgets to board data sources

### Widget Types
- **Chart widgets**: bar, line, pie charts from board data
- **Number widgets**: single KPI or metric display
- **Table widgets**: tabular view of board items with filters
- **Battery widgets**: progress visualization

Use `all_widgets_schema` to see available widget types and their configuration options.

## Workdoc Operations

Monday Workdocs are rich documents embedded in the workspace:
- **Create**: Call `create_doc` with the workspace or board context
- **Read**: Call `read_docs` to retrieve document content
- **Update**: Call `update_doc` to modify content

Workdocs support structured content blocks — headings, text, tables, images, and embedded board views.

## Automation Management

- **List automations**: Call `list_automations` for a board to see existing rules
- **Create automations**: Use `create_automation` or `plan_workflow` for complex automation logic
- **Monitor runs**: Call `get_automation_runs` to check execution history and errors

## Best Practices

- Always call `get_board_info` before creating items to understand the board's column structure
- Use `get_column_type_info` to verify the exact format before setting column values
- For bulk operations, use batch endpoints (`create_items`, `update_items`) instead of individual calls
- Check user and team IDs with `list_users_and_teams` before assigning people
- Use groups to organize items logically within a board — call `create_group` to add new sections

## Views and Filtering

Monday.com boards support multiple views for different perspectives on the same data:

- **Main table view**: the default spreadsheet-like view showing all columns and groups
- **Kanban view**: cards organized by status or any status-type column
- **Timeline view**: Gantt-style view using date or timeline columns
- **Calendar view**: calendar display using date columns
- **Chart view**: visual analytics from board data

Use `create_view` to add views to a board and `update_view` to modify existing views. Views are useful for presenting board data to different stakeholders without changing the underlying structure.

## Updates and Communication

Monday.com updates (comments on items) serve as the communication layer:

- **Create updates**: Use `create_update` to add comments with context, instructions, or status reports to any item
- **Read updates**: Use `get_updates` to see the conversation history on an item
- **Notifications**: Use `create_notification` to alert specific users about important changes

Updates support rich text formatting and file attachments. Use them for detailed task instructions, progress reports, and handoff notes between team members.

## Troubleshooting

- **Column value errors**: Almost always a formatting issue. Call `get_column_type_info` and match the format exactly.
- **Item not appearing**: Check that the correct group_id was used. Items created without a group go to the default group.
- **Permission errors**: Verify the user has write access to the target board and workspace.
- **Pagination**: Large boards return paginated results. Always handle the cursor to retrieve all items.
- **GraphQL syntax errors**: Use `get_graphql_schema` to verify field names and types. Monday's schema evolves — do not assume field names from memory.

For Monday.com GraphQL patterns and board schemas, see references/.
