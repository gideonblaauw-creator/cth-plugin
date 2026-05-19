# Buffer GraphQL Schema Reference

Discovered via introspection of `https://api.buffer.com/graphql` (April 2026).

## Authentication

```
Authorization: Bearer {BUFFER_ACCESS_TOKEN}
```

Direct access token — no OAuth2 refresh flow needed. Token obtained from Buffer Account Settings → Apps.

## Available Mutations (only 3)

| Mutation | Input type | Return type |
|----------|-----------|-------------|
| `createPost` | `CreatePostInput!` | `PostActionPayload` (union) |
| `deletePost` | `DeletePostInput!` | `DeletePostPayload` (union) |
| `createIdea` | `CreateIdeaInput!` | `IdeaActionPayload` (union) |

**There is no `updatePost` mutation.** To modify a scheduled post, delete and recreate.

## CreatePostInput (full field reference)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `channelId` | `ChannelId!` | YES | Buffer channel ID |
| `text` | `String` | No | Post body (caption + hashtags combined) |
| `schedulingType` | `String` | No | `'automatic'` or `'notification'` |
| `mode` | `String` | No | `'customScheduled'` (use dueAt), `'addToQueue'`, etc. |
| `dueAt` | `DateTime` | No | ISO 8601, MUST be in the future |
| `source` | `String` | No | Identifier string, e.g. `'clp26-automation'` |
| `assets` | `AssetsInput` | No | Images/video |
| `metadata` | `PostMetadataInput` | No | Platform-specific — see below |

### AssetsInput

```graphql
assets: {
  images: [{
    url: String!        # NON_NULL — no binary upload exists
    metadata: {
      altText: String!  # NON_NULL — required
      dimensions: {     # Optional but recommended
        width: Int
        height: Int
      }
    }
  }]
}
```

### PostMetadataInput (platform-specific)

**Facebook (REQUIRED):**
```json
{ "facebook": { "type": "post" } }
```
`PostTypeFacebook` values: `post`, `story`, `reel`

**Instagram (REQUIRED):**
```json
{ "instagram": { "type": "post", "shouldShareToFeed": true } }
```
`shouldShareToFeed` is `Boolean!` (NON_NULL).

**LinkedIn:** No required metadata fields.

## PostActionPayload (createPost return union)

| Type | Fields | Meaning |
|------|--------|---------|
| `PostActionSuccess` | `post { id status dueAt externalLink channelId }` | Success |
| `NotFoundError` | `message` | Channel not found |
| `UnauthorizedError` | `message` | Bad token |
| `UnexpectedError` | `message` | Server error |
| `RestProxyError` | `message code link` | Upstream proxy failure |
| `LimitReachedError` | `message` | Rate limit exceeded |
| `InvalidInputError` | `message` | Validation failure (missing metadata, past dueAt, etc.) |

Always check `__typename` before accessing fields.

## DeletePostInput

```graphql
input DeletePostInput {
  id: PostId!
}
```

## DeletePostPayload (deletePost return union)

| Type | Fields | Meaning |
|------|--------|---------|
| `DeletePostSuccess` | `id` | Successfully deleted |
| `VoidMutationError` | `message` | Error |

**Note:** This is a DIFFERENT union than `PostActionPayload` — do not reuse `PostActionSuccess` fragments.

## PostInput (for queries)

```graphql
input PostInput {
  id: PostId!
}
```

Usage: `query { post(input: { id: "69e03558..." }) { ... } }`

**NOT** `query { post(id: "...") }` — the argument name is `input`, not `id`.

## Post fields (query)

```graphql
type Post {
  id: PostId!
  status: String          # "scheduled", "sent", "pending", etc.
  dueAt: DateTime
  sentAt: DateTime
  externalLink: String    # URL to the published post (populated after send)
  channelId: ChannelId
  error: PostError        # { message: String }
  text: String            # Post body
}
```

## Introspection query (for discovering schema changes)

```graphql
{
  __schema {
    mutationType {
      fields {
        name
        args {
          name
          type { kind name ofType { kind name } }
        }
      }
    }
  }
}
```

Type details:
```graphql
{
  __type(name: "CreatePostInput") {
    inputFields {
      name
      type {
        kind
        name
        ofType { kind name ofType { kind name } }
      }
    }
  }
}
```
