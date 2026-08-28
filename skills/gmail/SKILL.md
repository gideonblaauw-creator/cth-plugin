---
name: gmail
description: >
  Searches, reads, drafts, and compiles Gmail correspondence. Use when: Gmail,
  inbox, email thread, draft an email, find past exchanges.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# Gmail Operations

Search, read, draft, and manage email through Gmail — find past correspondence, prepare replies, compile communication summaries, and manage labels for organizational workflows.

## Search Query Syntax

Gmail search uses specific operators that can be combined for precise results:

### Core Operators

- `from:sender@email.com` — messages from a specific sender
- `to:recipient@email.com` — messages sent to a specific recipient
- `subject:keyword` — matches words in the subject line
- `after:2026/01/01` — messages after a date (YYYY/MM/DD format)
- `before:2026/08/01` — messages before a date
- `has:attachment` — messages with attachments
- `filename:pdf` — messages with specific attachment types
- `label:important` — messages with a specific label
- `is:unread` — unread messages
- `is:starred` — starred messages
- `in:inbox` — messages in the inbox (excludes archived)
- `in:sent` — messages in sent mail

### Combining Operators

Combine operators with spaces (implicit AND):
```
from:partner@org.com subject:grant after:2026/06/01
```

Use OR for alternatives:
```
from:partner@org.com OR from:colleague@org.com
```

Use parentheses for grouping:
```
(from:partner@org.com OR from:colleague@org.com) subject:proposal
```

Use minus for exclusion:
```
from:partner@org.com -subject:newsletter
```

### Search Best Practices

- Start broad, then narrow. A too-specific query may miss relevant messages.
- Use date ranges to limit results when searching common terms.
- Search by thread rather than individual messages for full conversation context.
- For name-based searches, try both the email address and the person's name.

## Standard Workflows

### Find Past Correspondence

1. Determine the search criteria: contact name/email, subject keywords, date range
2. Call `search_threads` with the constructed query
3. Review the thread list for relevance
4. Call `get_thread` on the most relevant results to read full conversations
5. Summarize findings for the user — highlight key decisions, action items, and dates

### Draft a New Email

1. Gather from the user: recipient, subject, purpose, and desired tone
2. Determine the sending identity — if sending as CleantechHUB, apply the CTH brand tone
3. Compose the email content
4. Call `create_draft` with to, subject, and body (HTML or plain text)
5. Present the draft to the user for review
6. Never send directly — always create as draft and let the user send manually

### Reply to a Thread

1. Call `get_thread` to read the full conversation history
2. Understand the context and what response is needed
3. Draft the reply with appropriate tone and content
4. Call `create_draft` with the thread ID to associate it as a reply
5. Present for user review before sending

### Compile an Activity Report

1. Define the date range and scope (all emails, specific contacts, specific projects)
2. Call `search_threads` with date range and relevant filters
3. Read key threads to extract substance
4. Group findings by contact, project, or topic
5. Summarize: key exchanges, decisions made, action items pending, follow-ups needed

### Manage Labels

Labels are Gmail's organizational system:
- `list_labels` — see all existing labels
- `create_label` — create a new label for a workflow
- `label_thread` / `label_message` — apply labels to organize content
- `unlabel_thread` / `unlabel_message` — remove labels

Use labels to track workflow stages (e.g., "Needs Response", "Waiting on Partner", "Archived - Q3 2026").

## Sensitive Content Handling

Use `apply_sensitive_message_label` or `apply_sensitive_thread_label` to flag content that requires special handling. This is useful for:
- Confidential partner communications
- Financial or legal correspondence
- Personal data that should be handled carefully

## Rules

### Never Send Directly
Always create drafts. The user must review and send manually. This is a hard rule with no exceptions — even for routine replies or automated workflows.

### Brand Tone
When drafting emails that represent CleantechHUB:
- Professional but approachable
- Clear and action-oriented
- Include appropriate sign-off with CTH identity
- Reference the `cleantechhub-brand` skill for detailed tone guidelines

### Sensitive Correspondence
For emails involving grants, contracts, partnerships, or legal matters:
- Flag for user attention explicitly
- Do not summarize away important details — preserve exact language for legal/financial terms
- Note any deadlines or time-sensitive elements prominently

### Thread Context
Always read the full thread before drafting a reply. Responding without context leads to tone mismatches and missed information.

## Troubleshooting

- **No results from search**: Broaden the query. Try removing date filters or using fewer keywords. Check for typos in email addresses.
- **Thread appears empty**: The thread may contain only messages in categories (Promotions, Social) that are filtered. Try `in:anywhere` in the search.
- **Draft not appearing**: Verify the draft was created successfully. Check the Drafts folder in Gmail. The draft may take a moment to sync.
- **Label operations failing**: Verify the label exists with `list_labels` before applying it. Label names are case-sensitive.

For Gmail search syntax reference and template library, see references/.
