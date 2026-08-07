---
name: miro
description: >
  Read or create content on Miro boards — diagrams, structured docs, tables,
  or image/text extraction. Trigger on Miro, "check the Miro board", "create
  a diagram", "map this on Miro", or turning workflows into visuals.
metadata:
  version: "2.0.0"
  category: operations
---

# Miro Operations

Read, create, and manage content on Miro boards — build diagrams, extract information, create structured documents, and visualize workflows for the CTH team.

## Board Discovery

Before working with a Miro board, locate it:

1. List available boards to see what exists in the workspace
2. Search by board name if looking for a specific board
3. Note the board ID — required for all subsequent operations
4. Check board permissions to ensure the authenticated user can read/write

## Standard Workflows

### Read Board Content

Extract information from an existing board:

1. Get the board by ID or search by name
2. List all items on the board to see its contents
3. Filter items by type (sticky notes, shapes, text, frames, connectors)
4. Extract text content from relevant items
5. If the board is large, focus on specific frames or regions

Reading tips:
- Frames act as containers — list frame contents to get logically grouped items
- Sticky notes contain short text — useful for brainstorming outputs
- Shapes with text often represent process steps or categories
- Connectors show relationships between items

### Create a Diagram

Build a visual diagram on a Miro board:

1. Identify the target board (or create a new one)
2. Plan the diagram structure before creating items:
   - Define nodes (shapes with labels)
   - Define connections (arrows between nodes)
   - Define layout (left-to-right, top-to-bottom, radial)
3. Create shapes for each node with position coordinates and text
4. Create connectors between shapes using their item IDs
5. Optionally wrap the diagram in a frame for organization

### Create a Flowchart

For process flows and decision trees:

1. Define the process steps, decision points, and endpoints
2. Use standard flowchart shapes:
   - Rectangles: process steps
   - Diamonds: decision points
   - Rounded rectangles: start/end points
   - Parallelograms: input/output
3. Create shapes with appropriate text labels
4. Connect shapes with directional arrows
5. Add labels to connectors for decision branches (Yes/No, True/False)
6. Arrange in a clear top-to-bottom or left-to-right flow

### Create Structured Documents

Use Miro for visual documentation:

1. Create a frame as the document boundary
2. Add a title text element at the top
3. Build sections with headings and body text
4. Include tables for structured data:
   - Create a table widget with rows and columns
   - Populate cells with data
5. Add visual elements (icons, images, dividers) to improve readability

### Architecture Diagrams

For system and infrastructure diagrams:

1. Define components (servers, services, databases, users)
2. Create shapes representing each component with descriptive labels
3. Use different colors or shapes to distinguish component types:
   - Blue: compute/application services
   - Green: databases and storage
   - Orange: external services and APIs
   - Gray: infrastructure (networks, load balancers)
4. Connect components with labeled arrows showing data flow or dependencies
5. Group related components in frames (e.g., "VPS Services", "External APIs")
6. Add a legend explaining the color and shape conventions

## DSL Syntax

Miro supports a DSL (Domain-Specific Language) for creating diagrams programmatically. Key rules:

- Follow the exact syntax specification — Miro's DSL parser is strict
- Whitespace and indentation matter in some contexts
- Test with simple diagrams before building complex ones
- If DSL creation fails, fall back to creating individual items via the API

DSL is best for:
- Org charts and hierarchies
- Simple flowcharts
- Relationship diagrams

For complex visuals with precise positioning, use the item creation API directly.

## Working with Frames

Frames are the organizational backbone of Miro boards:

- Use frames to group related content (a single diagram, a document section, a brainstorming cluster)
- Name frames descriptively — they serve as landmarks on large boards
- When reading a board, iterate through frames first to understand the board's structure
- Position new content within existing frames when adding to an established board

## Visual Best Practices

### Colors and Styling

- Use consistent colors across a diagram to represent categories
- Limit the palette to 4-6 colors to avoid visual noise
- Use color to encode meaning, not just decoration
- Maintain readable contrast between text and background colors

### Layout and Spacing

- Align elements to a grid for clean presentation
- Maintain consistent spacing between related items
- Leave adequate margins within frames
- Flow direction should be consistent (pick one: left-to-right or top-to-bottom)

### Text and Labels

- Keep text on shapes concise — one line or two maximum
- Use frames or separate text blocks for detailed descriptions
- Label all connectors when the relationship is not obvious
- Include a title and date on major diagrams

## Use Cases at CTH

- **VPS architecture diagrams**: map out Docker containers, Caddy routes, and service dependencies on the OVH VPS
- **Campaign workflow visualizations**: show the content pipeline from ideation through publication across platforms
- **Workshop and brainstorming boards**: capture ideas, group themes, and prioritize during team sessions
- **Project roadmaps**: timeline-style boards showing milestones, dependencies, and team responsibilities
- **Client-facing presentations**: visual summaries of project plans and deliverables

## Known Issues

- **DSL syntax errors**: The DSL parser is strict about formatting. If creation fails, check for extra whitespace, missing brackets, or unsupported characters. Fall back to individual API calls if DSL does not work.
- **Item listing pagination**: Large boards may return items in pages. Always handle pagination to get complete board contents.
- **Board permissions**: Operations fail silently if the authenticated user lacks write access. Verify permissions before attempting to create or modify items.
- **Position coordinates**: Miro uses a coordinate system centered on the board. When placing items programmatically, calculate positions to avoid overlapping with existing content.

## Troubleshooting

- **Board not found**: Verify the board ID or name. Check that the board has not been archived or moved to a different team.
- **Items overlapping**: Calculate positions based on item dimensions and desired spacing. Use frames to define layout regions.
- **Connectors not attaching**: Verify the start and end item IDs are correct. Items must exist before connectors can reference them.
- **Slow operations on large boards**: Filter by item type or frame to reduce the data volume. Process regions of the board incrementally.

For Miro DSL syntax reference and board templates, see references/.
