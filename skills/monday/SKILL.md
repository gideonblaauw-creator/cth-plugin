---
name: monday
description: >
  Expert guide for building, managing, and automating Monday.com workspaces using the Monday.com MCP tools and GraphQL API.
  Use this skill ANY TIME the user asks to do ANYTHING in Monday.com — creating boards, dashboards, items, columns, workdocs,
  widgets, or automating workflows. Trigger immediately when the user mentions Monday, Monday.com, a Monday board,
  workspace, dashboard, widget, workdoc, or any Monday.com concept. DO NOT attempt Monday.com work without reading this
  skill first — critical API patterns, parameter names, and pitfalls are documented here that will prevent hard-to-debug failures.
---

# Monday.com Skill

## Overview

This skill captures all proven patterns for building Monday.com workspaces via the MCP tools and GraphQL API.
The core principle: **always prefer `all_monday_api` with raw GraphQL over the dedicated MCP tools**, because many MCP tools have parameter mismatches or limitations. Use the dedicated MCP tools only where they are explicitly marked as working below.

---

## Core Tool: `all_monday_api`

Use this for nearly everything. Pass a GraphQL query/mutation string and a variables object.

```
all_monday_api(query: "...", variables: {})
```

**Critical**: The `variables` parameter is always required — even if you inline all values, pass `variables: {}`.

---

## 1. Workspaces

### Create workspace

```graphql
mutation {
  create_workspace(name: "My Workspace", workspaceKind: open, description: "...") {
    id
    name
  }
}
```

⚠️ The parameter is `workspaceKind` (camelCase), NOT `kind`. Using `kind` will fail silently or error.

### List workspaces

Use the dedicated MCP tool: `list_workspaces` — this one works correctly.

---

## 2. Boards

### Create a board (always use `all_monday_api`)

The dedicated `create_board` MCP tool has parameter mismatches. Use raw GraphQL:

```graphql
mutation CreateBoard($boardName: String!, $boardKind: BoardKind!, $workspaceId: ID) {
  create_board(board_name: $boardName, board_kind: $boardKind, workspace_id: $workspaceId) {
    id
    name
    url
  }
}
```

Variables:
```json
{"boardName": "Board Name", "boardKind": "public", "workspaceId": "14985829"}
```

Valid `boardKind` values: `public`, `private`, `share`

### Get board info

```graphql
query {
  boards(ids: [BOARD_ID]) {
    id
    name
    columns { id title type }
    groups { id title }
    items_page(limit: 50) { items { id name column_values { id text value } } }
  }
}
```

---

## 3. Columns

### Create columns (batch with aliases)

```graphql
mutation {
  col1: create_column(board_id: BOARD_ID, title: "Status", column_type: status) { id }
  col2: create_column(board_id: BOARD_ID, title: "Due Date", column_type: date) { id }
  col3: create_column(board_id: BOARD_ID, title: "Drive Link", column_type: link) { id }
  col4: create_column(board_id: BOARD_ID, title: "Owner", column_type: people) { id }
  col5: create_column(board_id: BOARD_ID, title: "Budget", column_type: numbers) { id }
  col6: create_column(board_id: BOARD_ID, title: "Notes", column_type: long_text) { id }
  col7: create_column(board_id: BOARD_ID, title: "Timeline", column_type: timeline) { id }
  col8: create_column(board_id: BOARD_ID, title: "Email", column_type: email) { id }
}
```

**Valid `column_type` enum values**: `text`, `status`, `date`, `link`, `people`, `numbers`, `dropdown`, `timeline`, `email`, `long_text`

⚠️ `color` is NOT a valid column type — use `status` instead. Status columns get IDs prefixed with `color_` which can be confusing, but they are status columns.

### Create a dropdown column WITH labels

Dropdown columns have no labels by default. Create them with labels using the `defaults` parameter:

```graphql
mutation CreateDropdown($boardId: ID!, $defaults: JSON) {
  create_column(board_id: $boardId, title: "Phase", column_type: dropdown, defaults: $defaults) {
    id
  }
}
```

Variables:
```json
{
  "boardId": "BOARD_ID",
  "defaults": {"labels": [{"label": "Discovery"}, {"label": "Design"}, {"label": "Build"}, {"label": "Launch"}]}
}
```

⚠️ Do NOT wrap in `{"settings": {...}}` — this causes "Column schema validation failed". Labels go directly at root of the `defaults` object.

⚠️ You cannot update dropdown labels after creation via API (requires internal `id` and `revision` fields not returned by standard queries). If you need different labels, delete the column and recreate it.

### Status column colors

You cannot update status column colors via the API — they require internal column metadata not exposed by standard queries. Provide manual UI instructions to the user for hex color changes.

---

## 4. Groups

Every new board starts with one group: `id: "topics"`, `title: "Group Title"`.

### Rename default group + add more groups (batch)

```graphql
mutation {
  g1: update_group(board_id: BOARD_ID, group_id: "topics", group_attribute: title, new_value: "Active Projects") { id }
  g2: create_group(board_id: BOARD_ID, group_name: "Completed") { id }
  g3: create_group(board_id: BOARD_ID, group_name: "On Hold") { id }
}
```

---

## 5. Items

### Create items with column values

`column_values` must be a **JSON STRING** (stringified), not an object. Batch with aliases.

```graphql
mutation {
  i1: create_item(
    board_id: BOARD_ID,
    group_id: "topics",
    item_name: "Project Alpha",
    column_values: "{\"status_col_id\": {\"label\": \"Working on it\"}, \"date_col_id\": {\"date\": \"2026-03-01\"}, \"link_col_id\": {\"url\": \"https://...\", \"text\": \"Drive\"}}"
  ) { id }
  i2: create_item(
    board_id: BOARD_ID,
    group_id: "topics",
    item_name: "Project Beta",
    column_values: "{\"status_col_id\": {\"label\": \"Done\"}}"
  ) { id }
}
```

### Column value JSON formats by type

| Column Type | JSON format |
|-------------|-------------|
| **Status** | `{"label": "Done"}` |
| **Date** | `{"date": "2026-03-01"}` |
| **Timeline** | `{"from": "2026-03-01", "to": "2026-05-15"}` |
| **Link** | `{"url": "https://...", "text": "Display Text"}` |
| **Email** | `{"email": "user@example.com", "text": "user@example.com"}` |
| **Numbers** | `"650000"` (as plain string) |
| **Text** | `"plain text value"` |
| **Dropdown** | `{"ids": [1, 2, 3]}` (numeric IDs from settings_str) |
| **People** | `{"personsAndTeams": [{"id": USER_ID, "kind": "person"}]}` |

⚠️ Default status labels on new columns: `"Working on it"`, `"Done"`, `"Stuck"`. Custom label names like `"In Progress"` do not exist by default and will fail silently.

### Update a column value on an existing item

```graphql
mutation {
  change_column_value(
    board_id: BOARD_ID,
    item_id: ITEM_ID,
    column_id: "col_id",
    value: "{\"label\": \"Done\"}"
  ) { id }
}
```

### Delete an item

```graphql
mutation { delete_item(item_id: ITEM_ID) { id } }
```

---

## 6. Dashboards

### Create a dashboard (use the dedicated MCP tool — it works)

```
create_dashboard(name: "Dashboard Name", board_ids: ["123", "456"], workspace_id: "14985829", kind: "PUBLIC")
```

⚠️ `board_ids` must be an **array of strings** — not integers, not a single string.

### Dashboard URL format

Dashboard URLs use `/overviews/[id]`, NOT `/dashboards/[id]`.

```
https://ACCOUNT.monday.com/overviews/DASHBOARD_ID
```

### Delete a dashboard

```graphql
mutation { delete_dashboard(id: DASHBOARD_ID) }
```

⚠️ No subfields — returns Boolean. `delete_dashboard(id: ID) { id }` will error.

---

## 7. Widgets

### Create a widget (use the dedicated MCP tool)

```
create_widget(
  parent_container_id: "DASHBOARD_ID",
  parent_container_type: "DASHBOARD",
  widget_kind: "BATTERY",
  widget_name: "Widget Name",
  settings: {...}
)
```

### Widget settings by type

**BATTERY (progress bar)**
```json
{
  "done_text": "Done",
  "battery_data": {
    "status_column_ids_per_board": {"BOARD_ID": ["status_col_id"]}
  }
}
```

**NUMBER (counter)**
```json
{
  "counter_data": {
    "calculation_type": "count",
    "column_ids_per_board": {"BOARD_ID": ["col_id"]},
    "counter_type": "sum",
    "should_count_items": true
  },
  "suffix": "tasks"
}
```

**GANTT (timeline chart)**
Requires a `timeline` column type — separate date columns do NOT work.
```json
{
  "columnIdsByBoardId": {"BOARD_ID": ["timeline_col_id"]},
  "colorByIdPerBoardId": {"BOARD_ID": ["status_col_id"]},
  "label_by_id_per_board": {"BOARD_ID": ["name"]},
  "color_by_type": "color",
  "label_by_type": "name",
  "show_today_line": true,
  "show_weekends": false,
  "is_docked": true
}
```

**CHART (pie)**
```json
{
  "graph_type": "pie",
  "x_axis_columns": {"BOARD_ID": ["status_col_id"]},
  "y_axis_columns": {"BOARD_ID": ["default-label-count"]},
  "x_axis_group_by": "color",
  "y_axis_group_by": "default-label-count"
}
```

**CHART (bar with numeric sum)**
```json
{
  "graph_type": "bar",
  "x_axis_columns": {"BOARD_ID": ["dropdown_col_id"]},
  "y_axis_columns": {"BOARD_ID": ["numbers_col_id"]},
  "x_axis_group_by": "color",
  "y_axis_group_by": "numeric",
  "calc_function_type": "sum"
}
```

**LISTVIEW**
```json
{
  "additional_columns": ["col_id1", "col_id2", "col_id3"],
  "is_docked": true,
  "item_height": "single"
}
```

### Widget types NOT available via API

These widget types cannot be created via `create_widget` and must be added manually in the Monday.com UI:
- `VIDEO`
- `IMAGE` / media files
- `TEXT` / rich text blocks
- `TEAM` (team members widget)

When a user needs these, add them to a Workdoc instead, or provide step-by-step manual instructions.

---

## 8. Workdocs

### Create a Workdoc (use `all_monday_api` — MCP tool has type issues)

The `create_doc` MCP tool expects `workspace_id` as a number but validates as string inconsistently. Use raw GraphQL:

```graphql
mutation {
  create_doc(location: {
    workspace: {
      name: "Doc Title",
      workspace_id: WORKSPACE_ID,
      kind: public
    }
  }) {
    id
    object_id
  }
}
```

⚠️ The doc URL uses `object_id`, NOT `id`:
```
https://ACCOUNT.monday.com/docs/OBJECT_ID
```

### Add content to a Workdoc (use the dedicated MCP tool)

```
add_content_to_doc(doc_id: "DOC_ID", markdown: "# Heading\n\nContent here...")
```

Use `doc_id` (the `id` returned from creation, not `object_id`).

---

## 9. Discovery & Search

### Find board/doc URLs when the API doesn't return them directly

```
search(query: "Board Name", searchType: "BOARD")
```

### Discover column settings (e.g. dropdown label IDs)

```graphql
query {
  boards(ids: [BOARD_ID]) {
    columns { id title type settings_str }
  }
}
```

Parse `settings_str` JSON to get dropdown option IDs, status label indices, etc.

### Discover API schema

```
get_type_details(type_name: "ColumnType")
get_column_type_info(column_type: "dropdown")
get_graphql_schema(query_type: "mutation")
```

---

## 10. Batching Pattern

Always batch related mutations using GraphQL aliases to avoid rate limits and speed up builds:

```graphql
mutation {
  board1: create_board(board_name: "Board A", board_kind: public, workspace_id: WS_ID) { id }
  board2: create_board(board_name: "Board B", board_kind: public, workspace_id: WS_ID) { id }
  board3: create_board(board_name: "Board C", board_kind: public, workspace_id: WS_ID) { id }
}
```

This pattern works for columns, groups, and items too. Use `i1:`, `i2:`, `col1:`, `col2:` etc. as alias prefixes.

---

## 11. Common Error Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `kind` not recognized | Workspace creation uses `workspaceKind` | Change to `workspaceKind: open` |
| `color` is not a valid ColumnType | `color` doesn't exist | Use `status` instead |
| "Column schema validation failed" | Dropdown defaults wrapped in `{"settings": {...}}` | Use `{"labels": [...]}` directly |
| Dashboard not showing in sidebar | First dashboard creation bug | Delete and recreate |
| `delete_dashboard` error | Selecting subfields on Boolean return | Remove `{ id }` — use bare `delete_dashboard(id: ID)` |
| GANTT widget not populating | Using separate date columns | Create a `timeline` column type instead |
| Status label fails silently | Using custom label name like "In Progress" | Use "Working on it", "Done", or "Stuck" |
| Doc URL 404 | Using `id` instead of `object_id` | URL = `monday.com/docs/OBJECT_ID` |
| `create_board` MCP param mismatch | MCP uses `boardName` not `board_name` | Use `all_monday_api` with raw GraphQL |
| `variables` required error | Forgot variables param | Always pass `variables: {}` even for inline queries |
| Session state interruption | Mid-build session error | Query current board state before resuming |

---

## 12. Recommended Build Order

When building a workspace from scratch:

1. Create workspace (`all_monday_api`)
2. Create all boards in one batched mutation
3. For each board: create columns in one batched mutation
4. Create groups (rename `topics` + add new ones)
5. Create items with column values
6. Create dashboard (MCP `create_dashboard` with string array board_ids)
7. Add widgets (MCP `create_widget` per widget)
8. Create Workdoc (`all_monday_api`) → populate with `add_content_to_doc`
9. Provide manual instructions for any non-API widgets (video, image, text, team)

---

## 13. Getting User Context

```
get_user_context()
```

Returns the current user's ID, account slug, and workspace list. Use the account slug to construct URLs:
```
https://ACCOUNT_SLUG.monday.com/overviews/DASHBOARD_ID
```

---

## 14. Related skills

- `gmail` / `google-drive` — the research trinity; pair Monday searches with email and Drive for client activity reports
- `slack` — when decisions in Monday boards were discussed in Slack threads
- `notion` — when a workspace reorg involves mirroring or migrating content from Monday into Notion
- `claude-code` — for larger automations (GraphQL scripts, bulk board migrations) that belong in a persistent project
