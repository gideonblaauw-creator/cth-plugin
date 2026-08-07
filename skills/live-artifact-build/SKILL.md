---
name: live-artifact-build
description: >
  Create and maintain persistent live artifacts in the Cowork sidebar — tabbed
  dashboards, status trackers, build monitors, pipeline diagrams, QA logs, and
  any view the user will re-open across sessions. Trigger on "dashboard",
  "tracker", "live view", "status page", "project overview", "keep this updated",
  "show me the state of the build", or "make a live artifact".
metadata:
  version: "2.0.0"
  category: infrastructure
---

# Live Artifact Build

You are responsible for creating and maintaining persistent interactive artifacts that live in the Cowork sidebar. These artifacts survive across sessions, are updatable in place, and serve as the user's go-to view for dashboards, trackers, and status pages. Build them right the first time — a broken artifact erodes trust; a well-built one becomes indispensable.

## What Is a Live Artifact

A live artifact is a self-contained HTML file that persists in the Cowork sidebar and can be updated across sessions without losing its identity or URL. Unlike a one-off SendUserFile delivery, a live artifact has a stable ID, shows up in the artifact list, and can be refreshed with new data at any time.

Use live artifacts for anything the user will come back to. If they will look at it once and move on, use SendUserFile instead.

## Good Candidates for Live Artifacts

Build a live artifact when the user needs:

- **Project dashboards** — multi-tab views combining data from several sources (Monday.com boards, GitHub repos, Pipedream logs, VPS metrics).
- **Infrastructure status pages** — Doctor_Bot output rendered as a color-coded service grid with history.
- **Build and deployment trackers** — showing the state of CI/CD pipelines, recent deployments, and rollback options.
- **Pipeline architecture diagrams** — interactive visualizations of data flows, service dependencies, or system topology.
- **Campaign performance dashboards** — social media metrics, email open rates, and funnel analytics.
- **QA run logs** — test results with pass/fail indicators, coverage metrics, and trend lines.
- **Sprint or project overviews** — task status, blockers, velocity charts, and team assignments.

## Not Good Candidates (Use SendUserFile Instead)

Do not create a live artifact for:

- One-off explanations, tutorials, or static documents — these do not need persistence or updates.
- Throwaway mockups, wireframes, or proof-of-concept demos.
- Content that will never need refreshing or revisiting.
- Files the user wants to download and open elsewhere (use SendUserFile with `display: "attach"`).

If unsure, ask the user: "Will you want to come back to this view and see updated data?" If yes, build a live artifact. If no, use SendUserFile.

## Build Rules

Follow these rules for every live artifact. They are non-negotiable — violating them produces artifacts that break, look wrong, or confuse the user.

### 1. Self-Contained

All CSS and JS must be inline in the HTML file. No external stylesheet or script references except well-known CDNs that are reliably available (and even then, prefer inline). Specifically:

- All CSS in `<style>` tags, not `<link>` tags.
- All JavaScript in `<script>` tags, not `<script src="...">` tags.
- All images as inline SVG or base64 data URIs.
- No `localStorage`, `sessionStorage`, `indexedDB`, or `cookies` — none of these are available in the artifact sandbox. All data must be embedded directly in the HTML.

### 2. Responsive Layout

The artifact must work on both wide desktop viewports and narrow sidebar panels. The Cowork sidebar can be as narrow as 380px. Design for this:

- Use CSS flexbox or grid with `min-width` constraints and `@media (max-width: 480px)` breakpoints.
- Tables: `overflow-x: auto` on the container for horizontal scroll. Minimum body text: 13px.

### 3. Dark and Light Mode

Support both modes. The Cowork sidebar can be in either mode depending on user preference and system settings:

```css
:root {
  --bg: #ffffff;
  --text: #1a1a2e;
  --surface: #f5f5f7;
  --border: #e0e0e0;
  --accent: #2563eb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f0f1a;
    --text: #e8e8f0;
    --surface: #1a1a2e;
    --border: #2a2a3e;
    --accent: #60a5fa;
  }
}

body {
  background: var(--bg);
  color: var(--text);
}
```

Use CSS custom properties for all colors — never hardcode, always reference variables.

### 4. Data Embedding

Since `localStorage` is not available, embed data directly as JavaScript variables:

```html
<script>
  const DASHBOARD_DATA = {
    lastUpdated: "2026-08-07T14:30:00Z",
    services: [
      { name: "BookStack", status: "green", uptime: "99.97%" },
      { name: "MariaDB", status: "green", uptime: "99.99%" }
    ]
  };
</script>
```

When updating, replace this data block with fresh data. Structure and styling remain the same.

### 5. Tabbed Layout for Multi-Section Content

For dashboards with more than three sections, use tabs instead of scrolling. Implement with pure CSS and minimal JS:

```html
<div class="tab-bar">
  <button class="tab active" onclick="showTab('overview')">Overview</button>
  <button class="tab" onclick="showTab('services')">Services</button>
  <button class="tab" onclick="showTab('history')">History</button>
</div>
<div id="overview" class="tab-content active">...</div>
<div id="services" class="tab-content">...</div>
<div id="history" class="tab-content">...</div>

<script>
function showTab(id) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
}
</script>
```

### 6. Visual Design Standards

Follow the `dataviz` skill for all chart colors, stat tiles, and data visualization elements. For non-chart UI elements:

- Use a clean, minimal design with generous whitespace.
- Status indicators: use filled circles (green, amber, red) — not emoji, which render inconsistently.
- Cards and sections: use subtle borders or background color differences, not heavy shadows.
- Typography: use the system font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).

## Creation Workflow

Follow these steps to create a new live artifact:

1. **Determine purpose and data sources.** What will it show? Where does the data come from? How often will it need updating?
2. **Choose a kebab-case ID** that is descriptive and unique (e.g., `infra-status`, `campaign-dashboard`). This ID is permanent.
3. **Write the complete HTML file** to the workspace. Follow all build rules above.
4. **Send the file** via SendUserFile. Capture the returned `file_uuid`.
5. **Persist as an artifact** via `create_artifact`, passing the `file_uuid`, the chosen ID, and a clear description.
6. **Confirm to the user** that the artifact is created and available in their Cowork sidebar.

## Update Workflow

When updating an existing live artifact:

1. **List artifacts** via `list_artifacts` to confirm existence and get the ID.
2. **Stage current HTML** via `device_stage_files` with the artifact's ID in `artifact_ids`.
3. **Read the staged HTML** to understand existing structure. Do not rebuild from scratch unless the user requests a redesign.
4. **Make targeted changes** — update data, add sections, fix layout. Preserve existing structure to minimize churn.
5. **Write updated HTML**, send via SendUserFile, capture `file_uuid`.
6. **Update** via `update_artifact` with `file_uuid` and a summary of changes.

Do not delete and recreate an artifact to update it — use `update_artifact` to preserve identity and bookmarks.

## Error Handling

- **`create_artifact` fails**: user may not be on the desktop app. Fall back to SendUserFile with `display: "render"` and note persistence requires the desktop app.
- **`device_stage_files` fails for staging**: build the update from your knowledge of the artifact's structure, or ask the user to describe what they see.
- **Rendering issues**: check for external resource references, CSS conflicts, or JS errors. Test via SendUserFile with `display: "render"` before persisting.

## Artifact Maintenance

Artifacts are not fire-and-forget. Update data when running related tasks (e.g., refresh the infra status artifact after a Doctor_Bot check). Archive artifacts that are no longer relevant by updating their description.

For dashboard templates, tab component patterns, stat tile designs, and chart integration examples, see references/.
