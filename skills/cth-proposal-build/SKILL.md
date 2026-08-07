---
name: cth-proposal-build
description: >
  Build, iterate, and deploy polished client-facing service proposals for
  CleantechHUB. Trigger on "build a proposal", "respond to an RFP", "write up
  a services doc", "create a pitch for [client]", "redo the HTML", or "update
  the proposal". Governs the full pipeline: research → alignment gate → HTML
  build → PDF export → deploy.
metadata:
  version: "2.0.0"
  category: program
---

# CTH Proposal Build Pipeline

## Pipeline Overview

```
Research → HITL Alignment Gate → HTML Proposal Build → PDF Export → Deploy
```

Every proposal goes through these phases. Do not skip the alignment gate.

## Phase 1: Research

1. Gather all context about the client/opportunity.
2. Map CTH capabilities to client needs.
3. Identify relevant past work, case studies, and references.

## Phase 2: HITL Alignment Gate

Present a proposal outline to the user before building:

- Target client and opportunity
- Proposed services / scope
- Pricing approach
- Key differentiators
- Suggested structure

Wait for explicit approval before proceeding to build.

## Phase 3: HTML Proposal Build

Build the proposal as a single self-contained HTML file:

1. Apply CleantechHUB brand guidelines (read the cleantechhub-brand skill).
2. Use CSS custom properties for brand colors.
3. Structure with clear sections, professional typography.
4. Include SVG logo construction (inline SVG, not external file).
5. Ensure print CSS is included for PDF generation.

## Phase 4: PDF Export

Convert HTML to PDF. Critical points:
- Print CSS must handle page breaks properly.
- Embed fonts or use system fonts that render consistently.
- Test at A4 and Letter sizes.

## Phase 5: Deploy (Optional)

If the proposal needs a web-accessible version, deploy to VPS or Vercel.

## Known Failure Modes

- SVG logos breaking in PDF: use inline SVG with explicit viewBox attributes.
- Animated elements in PDF: disable animations in @media print.
- Font rendering inconsistency: include font-display: swap and system fallbacks.

For past proposal templates, see references/.
