---
name: buffer
description: >
  Schedules and publishes social posts via Buffer. Use when: Buffer, schedule a
  post, bulk schedule, repush failed posts, Notion→Buffer pipeline, posting Canva
  designs.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# Buffer Operations

Manage social media publishing through Buffer — schedule posts, track engagement, and automate content pipelines across all connected platforms.

## Critical Rules

Read and internalize these rules before any Buffer operation. Violating them causes silent failures that are difficult to debug.

### Image URLs Must Be Public

Buffer requires publicly accessible image URLs for media attachments. The following will fail silently:
- Canva editor URLs (`canva.com/design/...`)
- Google Drive URLs with restricted sharing
- Local file paths
- Expired temporary URLs

Always export or download the image first and confirm the URL is publicly reachable. When sourcing images from Canva, run the `canva` skill's export workflow before passing the URL to Buffer.

### shareNow Silent-Success Trap

Buffer's `shareNow` functionality returns a success response even when the post fails to actually publish on the social platform. After using `shareNow`:
1. Wait 30-60 seconds
2. Check the post status via `get_post`
3. If possible, verify the post appeared on the actual social platform

For critical posts, prefer scheduling a few minutes in the future over `shareNow` — scheduled posts have better error reporting.

### Channel IDs Are Required

Every post creation requires an exact `channelId` obtained from `list_channels`. Never guess, construct, or reuse channel IDs from memory. Always call `list_channels` fresh at the start of a posting session.

## Standard Workflow

Follow this sequence for every posting operation:

1. **Get organization**: Call `get_account` to retrieve the organization ID. If the user has multiple organizations, list them by name and ask which one to use.
2. **List channels**: Call `list_channels` with the organization ID to get all connected social accounts.
3. **Identify the correct channel**: Match by platform name and account name. Confirm with the user if multiple channels exist for the same platform.
4. **Create the post**: Call `create_post` with:
   - `channelId`: from step 3
   - `text`: the post copy
   - `media` (optional): public image URL(s)
   - `scheduledAt` (optional): ISO 8601 timestamp for scheduled posting

## Channel-Specific Rules

### LinkedIn
- Supports text-only posts, text + single image, and link posts with preview cards
- Character limit: 3,000 characters
- Hashtags: include at the end of the post body, not as a separate field
- Images: single image per post via the standard API

### Instagram
- Requires an image — text-only posts are not supported
- Square (1:1), portrait (4:5), or landscape (1.91:1) aspect ratios
- Caption limit: 2,200 characters
- Hashtags: up to 30 per post, include in the caption text

### Facebook
- Supports text, images, videos, and link posts
- No strict character limit, but engagement drops past 80 characters
- Link posts: include the URL in the text body for automatic preview card generation

### X/Twitter
- Character limit: 280 characters
- Images: up to 4 per post
- Threads: not supported via Buffer API — post individually

### TikTok, Threads, Pinterest, YouTube
- Check channel capabilities via `get_channel` before posting
- Each platform has specific media requirements — verify before uploading

## Bulk Scheduling

When scheduling multiple posts at once:

1. Prepare all post content in advance (text + image URLs)
2. Call `list_channels` once at the start
3. Create posts sequentially, spacing API calls by 1-2 seconds
4. Use the channel's posting schedule (queue) or specify explicit `scheduledAt` times
5. Verify all posts were created by calling `list_posts` afterward

For large batches (20+ posts), process in groups of 10 and verify each batch before continuing.

## Notion to Buffer Pipeline

When content comes from a Notion content calendar:

1. Read the Notion database entries marked as "Ready to Schedule"
2. Extract: post text, platform, scheduled date, and image URL
3. For each entry, create the corresponding Buffer post
4. Update the Notion entry status to "Scheduled" after successful creation
5. Record the Buffer post ID in the Notion entry for tracking

## Metrics and Reporting

Use `get_aggregated_post_metrics` to pull engagement data:
- Specify the channel ID and date range
- Metrics include: impressions, reach, engagement, clicks, shares
- Use this data for weekly/monthly performance reports

For individual post performance, use `get_post` with the post ID.

## Troubleshooting

- **Post created but not visible on platform**: Check post status — it may be queued, not yet published. Verify the channel connection is still active in Buffer settings.
- **Image not appearing**: Confirm the image URL is publicly accessible. Try opening it in an incognito browser window.
- **Wrong channel**: Always re-verify channel IDs. Channel IDs can change if the user reconnects a social account.
- **Rate limiting**: Buffer enforces API rate limits. Space out bulk operations and implement retry logic with backoff.

For Buffer API quirks and bulk scheduling patterns, see references/.
