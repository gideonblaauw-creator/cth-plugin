---
name: social-media-campaign
description: >
  Reusable playbook for building, running, and monitoring automated social media
  campaigns for CleantechHUB and partner brands. Covers the full pipeline: Claude
  generates captions, Canva/Ideogram generates images, Notion stores content,
  Pipedream orchestrates, Buffer publishes to LinkedIn, Instagram, Facebook.
  Trigger on "new social campaign", "social media campaign", "post to buffer",
  "schedule posts", "CleantechHUB campaign", "CLP campaign", "bulk re-push posts",
  or "campaign metrics".
metadata:
  version: "2.0.0"
  category: program
---

# Social Media Campaign Playbook

## Pipeline Architecture

```
Claude (captions) → Canva/Ideogram (visuals) → Notion (content DB) → Pipedream (orchestration) → Buffer (publishing) → LinkedIn / Instagram / Facebook
```

## Campaign Setup Questionnaire

Before bootstrapping any new campaign, gather:

1. Brand — which brand guidelines apply? (CleantechHUB, CLP26, Sustenttia, etc.)
2. Platforms — which channels? (LinkedIn, Instagram, Facebook, all)
3. Duration — campaign window (start → end date)
4. Frequency — posts per week per platform
5. Language — Spanish, English, or bilingual
6. Content pillars — 3–5 recurring themes
7. Visual style — Canva templates, photo-forward, illustration, data graphics
8. Approval flow — does content need approval before scheduling?

## Content Creation Workflow

### Step 1: Generate Captions

For each post in the content calendar:

1. Apply the correct brand skill for tone, hashtags, and formatting.
2. Write platform-specific copy (LinkedIn ≠ Instagram ≠ Facebook).
3. Include CTA, hashtags, and any required attribution.
4. Store in Notion content database with status "Draft".

### Step 2: Generate or Source Visuals

- Canva route: search for brand templates → create design from template → export as PNG.
- Ideogram route: generate AI image with brand-aligned prompt → download.
- Attach image URL to the Notion record.

### Step 3: Schedule via Buffer

- Use Buffer to create posts with the correct channel ID.
- Attach the image URL (must be publicly accessible — not a Canva editor URL).
- Set scheduled time according to the content calendar.
- Mark Notion record status as "Scheduled".

### Step 4: Monitor and Report

- Check Buffer for failed posts → re-push if needed.
- Pull engagement metrics via Buffer aggregated post metrics.
- Update Notion records with performance data.

## Platform-Specific Rules

### LinkedIn
- Professional tone, 1300-char max for optimal engagement.
- Tag company pages, use 3–5 hashtags.
- Best posting times: Tue–Thu 8–10am local time.

### Instagram
- Visual-first, caption up to 2200 chars.
- 20–30 hashtags in first comment (not caption body).
- Use carousel for storytelling.

### Facebook
- Community tone, shareable format.
- Link posts for traffic, image posts for engagement.
- 1–2 hashtags maximum.

## Troubleshooting

- Buffer image failure: confirm image URL is publicly accessible.
- shareNow silent success: Buffer's shareNow returns success even when it silently fails — always verify the post appeared on the platform.
- Pipedream webhook timeout: check the workflow run logs at pipedream.com.

For content calendar templates and Notion database schema, see references/.
