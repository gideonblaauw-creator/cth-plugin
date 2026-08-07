---
name: slack
description: >
  Search messages, read channels or threads, send or draft messages, find users,
  create or read Canvases, or schedule posts in Slack. Trigger on Slack, "DM
  someone", "post in #channel", "check Slack for…", or composing Slack messages.
metadata:
  version: "2.0.0"
  category: operations
---

# Slack Operations

Search, read, and post messages in Slack — find conversations, read channel history and threads, send or draft messages, manage Canvases, and schedule posts for the CTH workspace.

## Channel Resolution

Always resolve channel names to IDs before any operation that requires a channel. Use `slack_search_channels` with the channel name (without the # prefix) to find the correct ID.

Never hardcode or guess channel IDs. Channel IDs are workspace-specific and can change if a channel is recreated.

## Standard Workflows

### Search for Information

1. Determine what to search for: keywords, user messages, date range
2. Choose the search scope:
   - `slack_search_public`: searches only public channels
   - `slack_search_public_and_private`: searches public and private channels the user has access to
3. Use search modifiers for precision:
   - `in:#channel-name` — restrict to a specific channel
   - `from:@username` — messages from a specific user
   - `before:2026-08-01` / `after:2026-07-01` — date range
   - `has:link` / `has:reaction` / `has:file` — content filters
4. Review search results and read full threads for context

### Read Channel History

1. Resolve the channel ID using `slack_search_channels`
2. Call `slack_read_channel` with the channel ID
3. Specify a date range or message count to limit results
4. Scan for relevant messages and note thread timestamps for deeper reading

### Read a Thread

1. Obtain the thread's parent message timestamp (from search results or channel history)
2. Call `slack_read_thread` with the channel ID and thread timestamp
3. Read the full thread including all replies

### Send a Message

Choose the appropriate method based on the message's nature:

**For messages representing CTH publicly or in externally-shared channels:**
1. Resolve the channel ID
2. Draft the message content with appropriate tone
3. Call `slack_send_message_draft` — this creates a draft for user review before sending
4. Wait for user approval

**For routine internal updates:**
1. Resolve the channel ID
2. Call `slack_send_message` with the channel ID and message text
3. To reply in a thread, include the thread timestamp

### Schedule a Message

1. Resolve the channel ID
2. Prepare the message content
3. Call `slack_schedule_message` with the channel ID, message text, and scheduled time (Unix timestamp)
4. Confirm the scheduled time with the user

### Find Users

1. Call `slack_search_users` with the person's name or email
2. Use the returned user ID for mentions, DMs, or message filtering
3. Call `slack_read_user_profile` for detailed information about a user

## Canvas Operations

Slack Canvases are persistent, structured documents within channels:

### Create a Canvas
1. Prepare the content in Markdown format
2. Call `slack_create_canvas` with the channel ID and content
3. Canvases persist in the channel and can be edited later

### Read a Canvas
1. Call `slack_read_canvas` with the canvas ID
2. Extract the structured content for reference or transformation

### Update a Canvas
1. Read the current canvas content
2. Modify as needed
3. Call `slack_update_canvas` with the updated content

Use Canvases for content that needs to persist and be easily findable — meeting notes, project briefs, reference documents, and decision logs.

## Message Formatting

Slack messages support rich formatting:

- **Bold**: `*bold text*`
- **Italic**: `_italic text_`
- **Code**: `` `inline code` `` or ` ```code block``` `
- **Links**: `<https://example.com|Display Text>`
- **Mentions**: `<@USER_ID>` (resolve the user ID first)
- **Channel references**: `<#CHANNEL_ID>`
- **Bullet lists**: start lines with `- ` or `* `
- **Numbered lists**: start lines with `1. `
- **Block quotes**: start lines with `> `
- **Dividers**: use three dashes on a separate line

## Rules

### Draft vs. Direct Send

Use `slack_send_message_draft` (user reviews before sending) for:
- Messages in externally-shared channels
- Announcements or communications representing CTH
- Messages to partners, clients, or stakeholders
- Anything where tone and accuracy matter

Use `slack_send_message` (sends immediately) for:
- Internal team updates and coordination
- Quick responses in active discussions
- Automated status updates
- Thread replies in ongoing conversations

### Content Review

Before posting in any externally-shared or public-facing channel:
- Review the message for tone, accuracy, and brand alignment
- Check that links are correct and accessible
- Verify mentions tag the right people
- Confirm the channel is correct — posting in the wrong channel is visible immediately

### Thread Discipline

- Reply in threads to keep channels organized
- For important updates that the whole channel should see, post as a new message rather than buried in a thread
- When referencing a thread discussion in a new message, summarize the key point rather than just linking

## Troubleshooting

- **Channel not found**: Verify the channel name spelling. The channel may be private — check with `slack_search_public_and_private`. The channel may have been archived.
- **Message not appearing**: Check the channel ID is correct. Verify the bot/user has permission to post in that channel.
- **Search returning nothing**: Broaden search terms. Check date ranges. Some messages in private channels may not be searchable depending on permissions.
- **Scheduled message not firing**: Verify the scheduled time is in the future and in the correct timezone. Check that the channel still exists and the bot has posting permissions.

For Slack workspace structure and channel directory, see references/.
