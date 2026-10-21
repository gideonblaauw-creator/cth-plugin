---
name: nexus-onepager
description: >
  Builds bilingual Nexus startup one-pagers at nexus.cleantechhub.net/s/{slug}.
  Use when: startup one-pager, Nexus profile, deploy to /s/.
license: MIT
metadata:
  version: "2.1.0"
  category: "programs"
---

# Nexus One-Pager Pipeline

## Overview

Nexus is CleantechHUB's startup portfolio platform. Each CLP alumni startup gets a bilingual (EN/ES) HTML profile page at nexus.cleantechhub.net/s/{slug}.

## Data Sources

1. BookStack wiki — primary source for startup profiles.
2. Notion — campaign databases with supplementary info.
3. User input — founder interviews, pitch decks.

## One-Pager Structure

### Required Sections

1. Hero — startup name, tagline, logo, key visual.
2. Problem — what problem the startup solves.
3. Solution — the product/service and how it works.
4. Impact — environmental/social metrics and goals.
5. Team — founder photos and bios (1–3 people).
6. Cleantech Taxonomy — CT category tags (Energy, Water, Waste, Agriculture, etc.).
7. Contact — email, website, social links.
8. CLP Badge — ClimateLaunchpad alumni badge with year.

### Language Toggle

Include a language toggle (EN/ES) that switches all text content. Both languages must be present in the HTML file. Default to Spanish (primary LATAM audience).

## Build Process

1. Extract startup data from BookStack and/or user input.
2. Build single-file HTML with responsive design (mobile-first).
3. Apply CleantechHUB brand colors as base, startup branding as accent.
4. Test both language toggles.
5. Deploy to VPS at /var/www/nexus/s/{slug}/index.html.
6. Verify live URL.

## Known Failure Modes

- Image paths: use absolute URLs or data URIs — relative paths break on deployment.
- Font loading: inline critical fonts, lazy-load the rest.
- LinkedIn carousel export: ensure 1080x1080px output with readable text at mobile resolution.

## Deployment

**GitHub-before-live (HARD, Gideon 20 Oct 2026).** Scope: every Desk and every Hands job. Every build, including this VPS sub-site deploy (`/var/www/nexus/s/{slug}/`).

1. Name the full commit SHA on the deploy ticket.
2. Confirm that this SHA exists on origin before you deploy. Use `git ls-remote` or the GitHub API.
3. Record the pushed branch or the pull request on the receipt. Record the same SHA on the receipt.
4. Stop when the push fails. Escalate the failure to the Desk. Do not deploy. Do not use a workaround.
5. Confirm that the live SHA is present on GitHub.

Canonical: `skills/harness/SKILL.md` § GitHub-before-live HARD.

All deployment goes to the OVH VPS — never spin up a new host.

For HTML templates and the SUI framework reference, see references/.
