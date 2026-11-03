---
name: desks-workbenches-hands-tickets
description: Desks, Workbenches, Cloud Hands, and ticket contracts — routing, layers, and bot board status posting.
---

# Desks · Workbenches · Cloud Hands · Tickets

Canonical harness layers and ticket flow live in **`skills/harness/SKILL.md`**. Hands-ticket HARD lock: **`skills/harness/references/hands-ticket-hard.md`**. Ticket contract: **`tickets/TEMPLATE.md`**.

## Status posting (bot board)

Every **desk** and **workbench** POSTs lifecycle signals to the bot-events log so the bot board stays current.

**Endpoint:** `POST https://<host>/event`  
**Auth:** Bearer token from Infisical secret **`BOT_EVENTS_TOKEN`** (never commit or echo the token).

**When to post:** on **start**, **finish**, **blocked**, **needs_gideon**.

**`cause_tag` (required on blocked and failed events only):** one of:

- `unclear_ticket`
- `missing_map`
- `wrong_model`
- `waiting_on_gideon`
- `broken_connector`
- `other`

Omit `cause_tag` (or send `null`) for start, finish, and needs_gideon when not blocked/failed.

**JSON body shape:**

```json
{
  "bot_id": "desk-slug-or-workbench-id",
  "bot_name": "Human-readable desk or workbench name",
  "layer": "desk",
  "type": "start",
  "task": "Short task or ticket title",
  "link": "https://…",
  "cause_tag": null,
  "ts": "2026-11-03T12:00:00Z"
}
```

| Field | Notes |
| --- | --- |
| `bot_id` | Stable slug for this desk or workbench |
| `bot_name` | Display name on the board |
| `layer` | `desk`, `workbench`, or `hands` as appropriate |
| `type` | `start`, `finish`, `blocked`, `needs_gideon` |
| `task` | Ticket title or one-line summary |
| `link` | Ticket URL, PR URL, or trace link |
| `cause_tag` | Set only for `blocked` / failed paths (see list above) |
| `ts` | ISO 8601 UTC timestamp |

**Example (desk start):**

```bash
curl -sS -X POST "https://<host>/event" \
  -H "Authorization: Bearer <BOT_EVENTS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "desk-grants",
    "bot_name": "Grants Desk",
    "layer": "desk",
    "type": "start",
    "task": "Draft CTCN Suriname comms pack",
    "link": "https://github.com/gideonblaauw-creator/cth-plugin/issues/123",
    "cause_tag": null,
    "ts": "2026-11-03T12:00:00Z"
  }'
```

Replace `<host>` with the bot-events host Gideon configured, and `<BOT_EVENTS_TOKEN>` with the Infisical value.
