---
name: social-media-campaign
description: "Reusable playbook for building, running, and monitoring automated social media campaigns for CleantechHUB and partner brands. Covers the full pipeline: Claude generates captions → Ideogram generates images → Notion stores everything → Pipedream orchestrates → Buffer publishes to LinkedIn, Instagram, Facebook. Trigger on: 'new social campaign', 'social media campaign', 'post to buffer', 'schedule posts', 'CleantechHUB campaign', 'REIN Hubs campaign', 'CLP campaign', 'fix Notion → Buffer flow', 'bulk re-push posts', 'campaign metrics'. Always run the Campaign Setup Questionnaire before bootstrapping a new campaign."
---

# Social Media Campaign Skill

End-to-end playbook for automated multi-platform social media campaigns. Built from the CLP26 Colombia campaign (ClimateLaunchpad 2026) but designed to be cloned for any campaign, brand, country, or language.

**Core principle:** Notion is the only UI the human uses. Every other system (Claude API, Ideogram, Buffer, Pipedream, Railway) operates behind Notion. The human reviews and approves in Notion — never directly in Buffer, Pipedream, or social platforms.

## When to use

**Use when:** spinning up a new social media campaign, debugging an existing campaign pipeline, re-pushing failed posts, collecting metrics, or extending to new platforms/countries.

**Do NOT use for:** one-off manual social media posts (just write them), brand guideline questions (use `cleantechhub-brand` or `clp26-brand` skills), or non-social content (blog posts, newsletters).

**Related skills:**
- `cleantechhub-brand` — brand colors, voice, visual identity for CleantechHUB
- `clp26-brand` — ClimateLaunchpad 2026 specific brand overlay
- `gideon-workflow` — parallel execution, wrap-up tables, TODO handling
- `pipedream` — Pipedream UI/CLI patterns, CodeMirror editing, deployment

---

## 1. Campaign Setup Questionnaire

**MANDATORY.** Run this questionnaire before bootstrapping ANY new campaign. Every answer becomes a configuration variable used throughout the pipeline.

### 1.1 Campaign identity

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 1 | Campaign name (short code) | `CLP26` | `CAMPAIGN_ID` |
| 2 | Campaign full name | ClimateLaunchpad 2026 Colombia | `CAMPAIGN_NAME` |
| 3 | Brand to apply | CleantechHUB / REIN Hubs / other | `BRAND_SKILL` |
| 4 | Country/region | Colombia (`CO`) | `COUNTRY_CODE` |
| 5 | Language | Spanish (`es`) / English (`en`) / Portuguese (`pt`) / French (`fr`) | `LANGUAGE` |
| 6 | Campaign objective | Get applications / Get subscribers / Get donors / Get startups / Get investors | `OBJECTIVE` |
| 7 | Campaign final date | `2026-05-15` | `CAMPAIGN_END_DATE` |
| 8 | Application/action deadline | `2026-05-15` | `APPLICATION_DEADLINE` |

### 1.2 Content & CTA

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 9 | CTA URL (THE link in every post) | `https://climatelaunchpad.org/application-form/` | `CTA_URL` |
| 10 | @-mentions to include | `@ClimateLaunchpad @ClimateKIC @PvblicFoundation` | `MENTIONS` |
| 11 | Do mentions differ per platform? | Yes: LI uses company pages, IG uses @handles | `MENTIONS_BY_PLATFORM` |
| 12 | Max hashtags per post | 3–4 (LI/FB) / 5–8 (IG) | `MAX_HASHTAGS` |
| 13 | Content angles per weekday | See §7.1 CONTENT_ANGLES | angles array |
| 14 | Posting cadence | Weekdays only, 1 post per platform per day | `CADENCE` |

### 1.3 Platforms & channels

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 15 | Which platforms? | LinkedIn, Instagram, Facebook | `PLATFORMS` array |
| 16 | Buffer channel IDs (one per platform) | LI: `69d44b...`, IG: `69d6ca...`, FB: `69d6c7...` | `BUFFER_PROFILE_*` |
| 17 | Posting times per platform (local TZ) | LI 09:00, IG 12:00, FB 18:00 | `PLATFORM_TIMES` |
| 18 | Timezone | `America/Bogota` (UTC-5) | `TIMEZONE` |
| 19 | Adding more channels later? | Possibly Twitter/X, TikTok | noted |

### 1.4 Milestones & weeks

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 20 | Milestone structure | M1 (awareness), M2 (conversion), M3 (deadline push) | `MILESTONES` |
| 21 | Weeks per milestone | 2–3 weeks each | `WEEKS_PER_MILESTONE` |
| 22 | Week start dates | W2: 2026-04-14, W3: 2026-04-21, … | `WEEK_STARTS` map |
| 23 | Posts per platform per week | 5 (one per weekday) | `POSTS_PER_WEEK` |
| 24 | post_id naming scheme | `{COUNTRY}-{MILESTONE}-{PLATFORM}-W{WEEK}-{INDEX}` | `POST_ID_FORMAT` |

### 1.5 Image generation

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 25 | Ideogram model | `V_2_TURBO` | `IDEOGRAM_MODEL` |
| 26 | Ideogram style | `DESIGN` | `IDEOGRAM_STYLE` |
| 27 | Color palette (from brand skill) | `#0C498A` (navy 50%), `#B2EEFA` (sky 30%), `#9DC384` (green 20%) | `COLOR_PALETTE` |
| 28 | Aspect ratios per platform | IG: 1:1 (square), FB: 3:4 (portrait), LI: 16:9 (landscape) | `ASPECT_RATIOS` |

### 1.6 Approval flow

| # | Question | Example (CLP26) | Variable |
|---|----------|-----------------|----------|
| 29 | Human approval required? | Yes — but NOT manual Notion clicks | `APPROVAL_MODE` |
| 30 | Approval notification channel | Slack dispatch / desktop notification / email | `APPROVAL_CHANNEL` |
| 31 | Auto-approve after N hours? | Optional: 24h auto-approve if no rejection | `AUTO_APPROVE_HOURS` |

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      HUMAN (Notion UI)                       │
│   Reviews drafts → Approves → Sees metrics & analytics       │
└──────────────┬───────────────────────────┬──────────────────┘
               │                           │
               ▼                           ▼
┌──────────────────────┐    ┌──────────────────────────────────┐
│  Strategy DB (Notion) │◄──│  06_analysis (scoring engine)     │
│  - top_hook           │    │  reads Campaign DB week N         │
│  - best_time_LI/IG/FB │    │  writes Strategy DB week N        │
│  - top_image_style    │    └─────────────────▲────────────────┘
│  - avg_reach          │                      │
│  - avg_engagement_rate│                      │
└───────┬──────────────┘    ┌──────────────────┴────────────────┐
        │ (read)             │  05_metrics (Buffer + Firecrawl)   │
        ▼                    │  reads Buffer Analyze API           │
┌──────────────────────┐    │  scrapes social engagement          │
│  01_generate          │    │  writes → Campaign DB               │
│  Claude API (Sonnet)  │    └─────────────────▲────────────────┘
│  + Ideogram API       │                      │
│  + Notion write       │                      │
└───────┬──────────────┘    ┌──────────────────┴────────────────┐
        │ (writes 15 posts)  │  Pipedream WF2 (poller)            │
        ▼                    │  Polls Notion for status=approved   │
┌──────────────────────┐    │  → fires /webhook/buffer-push       │
│  Campaign DB (Notion) │────┤  → fires /webhook/metrics (later)  │
│  15 posts per week    │    └──────────────────────────────────┘
│  status lifecycle:    │                      │
│  draft → approved →   │                      ▼
│  processing →         │    ┌──────────────────────────────────┐
│  scheduled → sent →   │    │  04_buffer_push (Railway server)   │
│  measured             │    │  Buffer GraphQL createPost          │
└──────────────────────┘    │  + image proxy for Meta/LinkedIn    │
                             │  writes buffer_post_id → Notion     │
                             └───────────┬──────────────────────┘
                                         │
                                         ▼
                             ┌──────────────────────────────────┐
                             │  Buffer Queue                      │
                             │  → LinkedIn (LI)                   │
                             │  → Instagram (IG)                  │
                             │  → Facebook (FB)                   │
                             └──────────────────────────────────┘
```

### Service inventory

| Service | Role | Auth env var | Rate limits |
|---------|------|-------------|-------------|
| **Notion** | Source of truth — Campaign DB + Strategy DB | `NOTION_API_KEY` | 3 req/s sustained; burst to 10/s |
| **Claude API** | Caption + prompt generation (Script 01) | `ANTHROPIC_API_KEY` | Tier-dependent; Sonnet is cheapest |
| **Ideogram** | Image generation (3 aspect ratios per post) | `IDEOGRAM_API_KEY` | ~60 req/min; 5s retry on failure |
| **Buffer** | Social media scheduling via GraphQL API | `BUFFER_ACCESS_TOKEN` | ~60 mutations/15-min window (observed) |
| **Firecrawl** | Scrapes social engagement (Script 05) | `FIRECRAWL_API_KEY` | Plan-dependent |
| **Railway** | Hosts webhook server + image proxy | Deploys from local code | Container restarts lose in-memory cache |
| **Pipedream** | Workflow orchestration — polls Notion, fires webhooks | Workspace env vars (web UI only) | 300 invocations/day (free tier) |

---

## 3. Environment Variables

### 3.1 Railway / server env vars (set via `railway variables --set`)

| Variable | Description | Example |
|----------|-------------|---------|
| `NOTION_API_KEY` | Notion integration token | `ntn_...` |
| `NOTION_CAMPAIGN_DB_ID` | Campaign database ID (no dashes) | `d2ef4ad644c34dc9bcd701c39237724f` |
| `NOTION_STRATEGY_DB_ID` | Strategy database ID | `53944751a9374b6ea8167bdff42f2a3e` |
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-...` |
| `IDEOGRAM_API_KEY` | Ideogram API key | `ide_...` |
| `BUFFER_ACCESS_TOKEN` | Buffer direct access token (no OAuth refresh needed) | `z6oe6...` |
| `BUFFER_PROFILE_LI_CO` | Buffer channel ID for LinkedIn | `69d44b...` |
| `BUFFER_PROFILE_IG_CO` | Buffer channel ID for Instagram | `69d6ca...` |
| `BUFFER_PROFILE_FB_CO` | Buffer channel ID for Facebook | `69d6c7...` |
| `FIRECRAWL_API_KEY` | Firecrawl API key for engagement scraping | `fc-...` |
| `PUBLIC_BASE_URL` | Railway public URL (used for image proxy) | `https://clp26-automation-production.up.railway.app` |
| `BUFFER_PUSH_ENABLED` | Kill switch: `true`/`false` | `true` |
| `BUFFER_PUSH_ALLOWLIST` | CSV of post_ids or page_ids to allow (empty = allow all) | `CO-M2-LI-W2-01,CO-M2-IG-W2-03` |
| `PORT` | Server port (Railway assigns automatically) | `3000` |

### 3.2 Pipedream workspace env vars (set via web UI only)

Same keys as Railway, EXCEPT: Pipedream also needs the webhook URLs:

| Variable | Value |
|----------|-------|
| `CLAUDE_CODE_WEBHOOK_BUFFER_PUSH` | `https://{railway-domain}/webhook/buffer-push` |
| `CLAUDE_CODE_WEBHOOK_METRICS` | `https://{railway-domain}/webhook/metrics` |
| `CLAUDE_CODE_WEBHOOK_GENERATE` | `https://{railway-domain}/webhook/generate` |
| `CLAUDE_CODE_WEBHOOK_ANALYSIS` | `https://{railway-domain}/webhook/analysis` |

**CRITICAL:** `pd env add` does NOT exist — the `pd` CLI has no env management. Always use the Pipedream web UI at `https://pipedream.com/settings/env-vars`.

---

## 4. Notion Schema

### 4.1 Campaign Database

This is the main operational database. One row per social media post.

| Column | Type | Written by | Description |
|--------|------|-----------|-------------|
| `post_id` | Title | Script 01 | Format: `{COUNTRY}-{MILESTONE}-{PLATFORM}-W{WEEK}-{INDEX}` e.g. `CO-M2-LI-W2-01` |
| `milestone` | Select | Script 01 | Campaign milestone: `M1`, `M2`, `M3`, etc. |
| `platform` | Select | Script 01 | `LI` / `IG` / `FB` |
| `country` | Select | Script 01 | `CO` (Colombia), etc. |
| `week` | Number | Script 01 | Week number within campaign (2, 3, 4…) |
| `caption_es` | Rich text | Script 01 / human edit | Full post copy in campaign language. Contains CTA URL, mentions, body. |
| `hashtags` | Rich text | Script 01 | Separate column. 3–4 for LI/FB, 5–8 for IG. |
| `ideogram_prompt` | Rich text | Script 01 | Visual description sent to Ideogram. Stored for reproducibility. |
| `scheduled_at` | Date | Script 01 | ISO 8601 with timezone. e.g. `2026-04-16T09:00:00-05:00` |
| `status` | Select | Various | Lifecycle status — see §4.3 |
| `image_url_square` | URL | Script 01/02 | Ideogram 1:1 image (for IG) |
| `image_url_portrait` | URL | Script 01/02 | Ideogram 3:4 image (for FB) |
| `image_url_landscape` | URL | Script 01/02 | Ideogram 16:9 image (for LI) |
| `post_url` | URL | Script 04 | Published post URL (populated after Buffer sends) |
| `buffer_post_id` | Rich text | Script 04 | Buffer's internal post ID (for metrics lookup) |
| `reach` | Number | Script 05 | From Buffer Analyze API |
| `impressions` | Number | Script 05 | From Buffer Analyze API |
| `link_clicks` | Number | Script 05 | From Buffer Analyze API |
| `public_engagement` | Number | Script 05 | Firecrawl: likes + comments + shares + reactions |

### 4.2 Strategy Database

One row per week. Written by Script 06 (analysis), read by Script 01 (generation) for the next week's content.

| Column | Type | Description |
|--------|------|-------------|
| `week` | Number | Week number (primary key) |
| `top_hook` | Rich text | First line of the best-performing post's caption |
| `best_time_LI` | Rich text | Best posting time for LinkedIn (HH:MM) |
| `best_time_IG` | Rich text | Best posting time for Instagram |
| `best_time_FB` | Rich text | Best posting time for Facebook |
| `top_image_style` | Rich text | First 120 chars of the best post's Ideogram prompt |
| `top_format` | Select | Best-performing milestone type |
| `avg_reach` | Number | Average reach across all posts that week |
| `avg_engagement_rate` | Number | Average engagement rate (%) |
| `top_milestone_type` | Select | Milestone with highest avg score |
| `notes` | Rich text | JSON blob: top_post_id, top_score, scored_at, post_count |

### 4.3 Status lifecycle

```
draft → approved → processing → scheduled → sent → measured
```

| Status | Set by | Meaning |
|--------|--------|---------|
| `draft` | Script 01 (on create), Script 02 (on regen — **known bug**) | Post exists but not yet approved |
| `approved` | Approval flow (see §8) | Ready for Buffer push — Pipedream WF2 picks this up |
| `processing` | Script 04 (atomic lock) | Buffer push in progress — prevents duplicate pushes |
| `scheduled` | Script 04 (after Buffer confirms) | In Buffer queue, waiting for scheduled time |
| `sent` | Buffer (external) → detected by Script 05 | Published on social platform |
| `measured` | Script 05 | Metrics collected and written back |
| `image_failed` | Script 02 | All 3 Ideogram aspect ratios failed — needs manual intervention |

**Known bug:** Script 02 (`02_ideogram.js:36`) resets status to `draft` after image regen, even if the post was already `approved`. Workaround: after running a manual image regen, flip the post back to `approved`. Fix: Script 02 should preserve existing status unless images failed.

---

## 5. Pipeline Scripts

### 5.1 Script 01 — Generate (`/webhook/generate`)

**What it does:** Generates an entire week of content (15 posts: 5 days × 3 platforms).

**Inputs (webhook payload):**
```json
{
  "week": 2,
  "milestone_id": "M2",
  "country": "CO",
  "application_deadline": "2026-05-15",
  "cta_url": "https://climatelaunchpad.org/application-form/"
}
```

**Steps:**
1. Loads Strategy DB for the prior week (`getLatestStrategy(week)`) — reads top_hook, best_time, etc.
2. Loads brand skill from filesystem (`/mnt/skills/user/clp26-brand/SKILL.md` or fallback)
3. Calls Claude API (`claude-opus-4-6`, 8192 max_tokens) with system prompt (brand) + user prompt (campaign params, content angles, platform rules)
4. Claude returns a JSON array of 15 post objects (caption_es, hashtags, ideogram_prompt, platform, day_index)
5. For each post: calls Ideogram API to generate 3 aspect ratios (square, portrait, landscape) — with retry
6. Writes all 15 posts to Notion Campaign DB with status=`draft`

**Content angles (one per weekday, shared across platforms):**
- Monday: `entrepreneur_opportunity` — address climate entrepreneurs
- Tuesday: `climate_impact` — lead with environmental problem
- Wednesday: `ecosystem_support` — highlight mentors, funding, REIN Hubs
- Thursday: `success_story` — country-relevant cleantech success
- Friday: `deadline_urgency` — deadline push, clear CTA

**Platform-specific rules (enforced in Claude prompt):**
- LI: 150–300 words, professional, tag company pages
- IG: 50–100 words, punchy hook on line 1, 5–8 hashtags
- FB: 80–150 words, conversational, full URL prominent
- ALL: campaign language, include CTA URL, include support line with @-mentions

**Cost per run:** ~15 Ideogram images (3 ratios × 5 days) + 1 Claude API call. Use Sonnet to keep costs low unless quality demands Opus.

### 5.2 Script 02 — Ideogram regen (`/webhook/ideogram`)

**What it does:** Regenerates images for a single existing post. Manual/retry use.

**Inputs:**
```json
{ "notion_page_id": "34372766-dd2e-81b2-..." }
```
or
```json
{ "ideogram_prompt": "A Colombian city...", "post_id": "CO-M2-LI-W2-01" }
```

**Steps:**
1. If `notion_page_id` provided, reads the ideogram_prompt from Notion
2. Calls `generateAllImages(prompt)` — 3 aspect ratios in parallel
3. Writes image URLs back to Notion
4. Sets status to `draft` (or `image_failed` if all 3 failed)

**⚠ Known bug:** Resets status to `draft` unconditionally. If post was `approved`, it drops back. Workaround: manually re-approve after regen.

### 5.3 Script 03 — Notion write (`/webhook/notion-write`)

**What it does:** Bulk-writes post objects to Notion Campaign DB. Used for manual/retry operations.

**Inputs:**
```json
{ "posts": [{ "post_id": "...", "milestone": "M2", ... }] }
```

### 5.4 Script 04 — Buffer push (`/webhook/buffer-push`)

**What it does:** Takes an approved Notion post and pushes it to Buffer's scheduling queue via GraphQL.

**Inputs:**
```json
{
  "notion_page_id": "34372766-dd2e-81b2-...",
  "post_id": "CO-M2-LI-W2-01"
}
```

Accepts both `notion_page_id` and `pageId` (Pipedream WF2 contract).

**Steps:**
1. Kill-switch check: `BUFFER_PUSH_ENABLED` + `BUFFER_PUSH_ALLOWLIST`
2. Re-reads Notion row, confirms status = `approved`
3. Atomic lock: flips status → `processing`
4. Selects correct image URL by platform (square/portrait/landscape)
5. Probes image dimensions from PNG/JPEG headers (pre-supplies to Buffer)
6. Rewrites image URL through Railway image proxy (`/image-proxy?url=...`)
7. Builds Buffer `createPost` input with platform-specific metadata:
   - FB: `metadata.facebook.type = 'post'`
   - IG: `metadata.instagram.type = 'post'`, `shouldShareToFeed = true`
   - LI: no required metadata
8. Calls Buffer GraphQL `createPost` mutation
9. Writes `buffer_post_id` + `post_url` to Notion, sets status → `scheduled`
10. On failure: resets status → `approved` for retry

**Critical details:**
- Image URLs are proxied through Railway for ALL platforms (not just Meta) — LinkedIn's media fetcher also fails on Ideogram's Cloudflare-fronted ephemeral URLs
- Dimension probe handles PNG (bytes 16–23 = width/height big-endian uint32) and JPEG (walk SOF segments)
- Buffer `dueAt` must be in the future — posts with past dates are rejected
- If `dueAt` would be in the past: bump forward by 7 days, but NEVER beyond `CAMPAIGN_END_DATE`

### 5.5 Script 05 — Metrics (`/webhook/metrics`)

**What it does:** Collects post-publish metrics and writes to Notion.

**Steps:**
1. Queries Buffer Analyze API for impressions, reach, link_clicks
2. Falls back to Buffer GraphQL `post.status` if Analyze isn't available
3. Scrapes social engagement via Firecrawl (likes, comments, shares, reactions → `public_engagement`)
4. Writes metrics to Notion Campaign DB, sets status → `measured`

### 5.6 Script 06 — Analysis (`/webhook/analysis`)

**What it does:** Scores the week's posts and writes strategy insights for the next week.

**Scoring formula:**
```
composite_score = reach × (1 + engagement_rate) × (1 + link_clicks)
```
Normalised to 0–100 within the week.

**Outputs (to Strategy DB):**
- `top_hook` — first line of the best-performing caption
- `best_time_*` — best posting time per platform (from top-scoring post)
- `top_image_style` — first 120 chars of best post's Ideogram prompt
- `avg_reach`, `avg_engagement_rate` — weekly averages

**Learning loop:** Script 01 reads the latest Strategy DB row (week N-1) when generating week N's content. The prompt includes the prior week's top hook, best times, and image style as context.

---

## 6. Server & Image Proxy

### 6.1 Webhook server (`server.js`)

Node.js HTTP server on Railway. No Express — uses built-in `http` module.

**Routes:**

| Method | Path | Handler |
|--------|------|---------|
| GET | `/health` | Returns `{ ok: true, ts }` |
| GET, HEAD | `/image-proxy?url=<encoded>` | Proxies upstream image with 24h cache |
| POST | `/webhook/generate` | Script 01 |
| POST | `/webhook/ideogram` | Script 02 |
| POST | `/webhook/notion-write` | Script 03 |
| POST | `/webhook/buffer-push` | Script 04 |
| POST | `/webhook/metrics` | Script 05 |
| POST | `/webhook/analysis` | Script 06 |

All POST routes: respond with `202 Accepted` immediately (Pipedream webhooks time out), then run handler async (fire-and-forget).

### 6.2 Image proxy

**Why it exists:** Meta's Graph API (IG/FB) AND LinkedIn's media fetcher both fail on Ideogram's ephemeral URLs. Cloudflare blocks their user agents or egress IPs. Routing through our Railway domain makes the social platforms fetch from a host they trust.

**How it works:**
1. Buffer creates a post with `assets.images[].url` pointing to our proxy: `https://{railway}/image-proxy?url={encoded-ideogram-url}`
2. When the social platform fetches the image, our server fetches from Ideogram (or serves from cache) and streams the bytes back
3. In-memory cache (Map) with 24h TTL — key = full upstream URL, value = `{ buf, contentType, fetchedAt }`
4. HEAD support: LinkedIn probes file type/size via HEAD before GET. Server returns headers only (no body) for HEAD requests. Includes `Accept-Ranges: bytes`.

**URL rewriting (`toProxyUrl`):**
- Rewrites ALL http(s) image URLs through the proxy (not just Ideogram — defensive)
- Skips already-proxied URLs (prevents double-wrap)
- Skips non-http URLs (data:, blob:, etc.)

**Cache limitation:** In-memory only — lost on Railway container restart. Acceptable for campaigns where posts are pushed within 24h of image generation. For longer horizons, consider persistent storage (Redis, S3).

### 6.3 Railway deployment

```bash
cd clp26-automation
railway up --detach          # Deploy from local code
railway logs --deployment     # Stream logs
railway variables             # List env vars
railway variables --set "KEY=VALUE"   # Set env var
railway variables delete KEY          # Unset env var (--set "KEY=" does NOT work)
railway status                # Check service/environment
```

**After deploying:** Always verify with `curl https://{domain}/health`.

---

## 7. Pipedream Orchestration

### 7.1 WF2 — Approved post poller

Polls Notion Campaign DB every ~30 seconds for `status = approved` posts. For each found, fires a webhook:

```json
POST /webhook/buffer-push
{ "pageId": "<notion-page-id>", "source": "pipedream_wf2", "ts": "..." }
```

**Important:** WF2 sends `pageId` (not `notion_page_id`). Script 04 accepts both via alias.

**Race condition protection:** Script 04 uses an atomic lock (status → `processing`) before pushing. If WF2 fires twice for the same post, the second invocation sees `processing` (not `approved`) and aborts.

### 7.2 Adding a scraper step

Before cloning WF2 for a new campaign, determine if you need:
- A scraper at the beginning (e.g. to pull trending topics from news sites)
- Additional webhook triggers (e.g. for metrics collection on a cron schedule)
- Filters (e.g. only process posts for a specific country/milestone)

Pipedream's platform offers built-in cron triggers, HTTP triggers, and data stores for dedup.

### 7.3 Pipedream UI quirks

- **`pd` CLI does NOT manage env vars** — use web UI only (`https://pipedream.com/settings/env-vars`)
- **`form_input` does NOT work** on Pipedream's React UI — use `left_click` + `type` instead
- **CodeMirror 6 editing:** Use `querySelectorAll('.cm-content')` and check content to find the right editor (multiple editors may be open)
- See the `pipedream` skill for full details

---

## 8. Approval Flow

**Core requirement:** The human must NEVER have to manually click in Notion to approve posts. Approval must be triggered via conversation (Slack, desktop notification, or email).

### 8.1 Recommended flow

1. Script 01 writes 15 posts to Notion with status = `draft`
2. System sends a summary to the human via their preferred channel (Slack/email/desktop):
   - "Week 3 content ready — 15 posts generated. Review: [Notion link]"
   - Include a preview: sample caption, sample image thumbnail
3. Human reviews in Notion (read-only scan), then responds in the conversation:
   - "Approve all" → bulk-flip all 15 to `approved`
   - "Approve except CO-M2-IG-W3-02" → flip 14, leave 1 as `draft`
   - "Reject — redo the Friday posts" → leave as `draft`, give feedback
4. Pipedream WF2 picks up `approved` posts and fires Buffer push

### 8.2 Notification options

| Channel | How | Best for |
|---------|-----|----------|
| **Slack** | Use `slack_send_message` MCP tool to post in a campaign channel | Fast response; team visibility |
| **Desktop** | Use system notification via Claude Code | Solo operators |
| **Email** | Use `gmail_create_draft` MCP tool + send | When Slack isn't available |

### 8.3 Auto-approve (optional)

If `AUTO_APPROVE_HOURS` is set (e.g. 24), posts that remain `draft` for longer than N hours are auto-approved. Implement via a Pipedream cron workflow that checks `created_time` on draft posts.

---

## 9. Buffer GraphQL API Reference

### 9.1 Endpoint

```
POST https://api.buffer.com/graphql
Authorization: Bearer {BUFFER_ACCESS_TOKEN}
Content-Type: application/json
```

### 9.2 Mutations

**createPost:**
```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess {
      post { id status dueAt externalLink channelId }
    }
    ... on NotFoundError     { message }
    ... on UnauthorizedError { message }
    ... on UnexpectedError   { message }
    ... on RestProxyError    { message code link }
    ... on LimitReachedError { message }
    ... on InvalidInputError { message }
  }
}
```

`CreatePostInput` fields:
- `channelId` (NON_NULL) — Buffer channel ID
- `text` (String) — post body (caption + hashtags)
- `schedulingType` — `'automatic'` or `'notification'`
- `mode` — `'customScheduled'` (use dueAt) or `'addToQueue'`
- `dueAt` (DateTime) — ISO 8601, MUST be in the future
- `source` (String) — e.g. `'clp26-automation'`
- `assets` — `{ images: [{ url(NON_NULL), metadata: { altText(NON_NULL), dimensions: { width, height } } }] }`
- `metadata` — platform-specific:
  - FB: `{ facebook: { type: 'post' } }` — **REQUIRED, or error**
  - IG: `{ instagram: { type: 'post', shouldShareToFeed: true } }` — **shouldShareToFeed is NON_NULL**
  - LI: no required metadata fields

**deletePost:**
```graphql
mutation DeletePost($input: DeletePostInput!) {
  deletePost(input: $input) {
    __typename
    ... on DeletePostSuccess { id }
    ... on VoidMutationError { message }
  }
}
```

**No `updatePost` mutation exists.** To edit a scheduled post: delete → recreate.

### 9.3 Queries

**post (single):**
```graphql
query GetPost($input: PostInput!) {
  post(input: $input) {
    id status dueAt sentAt externalLink
    error { message }
  }
}
```
Note: argument is `input: PostInput!` (NOT `id: PostId!`). PostInput has one field: `{ id: PostId! }`.

### 9.4 No updatePost — the delete+recreate pattern

When you need to modify a scheduled post (e.g. fix a URL):

1. Delete old post: `deletePost(input: { id: oldBufferId })`
2. Update Notion caption
3. Flip Notion status → `approved` (clear `buffer_post_id` and `post_url`)
4. Fire `/webhook/buffer-push` — creates a new Buffer post with corrected content
5. Verify new `buffer_post_id` in Notion

This was battle-tested on 14 posts simultaneously (CLP26 URL fix, April 2026).

---

## 10. Platform-Specific Rules

### 10.1 LinkedIn (LI)

| Property | Value |
|----------|-------|
| Image aspect ratio | 16:9 landscape (`ASPECT_16_9`) |
| Image field | `image_url_landscape` |
| Caption length | 150–300 words |
| Tone | Professional, authoritative |
| Hashtags | 3–4, in separate column |
| @-mentions | Company page tags |
| Buffer metadata | None required |
| Media fetch | HEADs first (checks size/type), then GETs |

### 10.2 Instagram (IG)

| Property | Value |
|----------|-------|
| Image aspect ratio | 1:1 square (`ASPECT_1_1`) |
| Image field | `image_url_square` |
| Caption length | 50–100 words |
| Tone | Punchy hook on line 1, short paragraphs |
| Hashtags | 5–8, in separate column |
| Buffer metadata | `{ instagram: { type: 'post', shouldShareToFeed: true } }` — **REQUIRED** |
| Media fetch | Meta Graph API fetches the image URL server-side — MUST be reachable by Meta's crawlers |

### 10.3 Facebook (FB)

| Property | Value |
|----------|-------|
| Image aspect ratio | 3:4 portrait (`ASPECT_3_4`) — Ideogram v2 doesn't support 4:5 |
| Image field | `image_url_portrait` |
| Caption length | 80–150 words |
| Tone | Conversational, accessible |
| Hashtags | 3–4, in separate column |
| Full URL | Must appear prominently in caption body |
| Buffer metadata | `{ facebook: { type: 'post' } }` — **REQUIRED, or error** |
| Media fetch | Same as IG — Meta Graph API fetches server-side |

---

## 11. Kill Switches & Safety

### 11.1 Kill switches

| Switch | Env var | Effect |
|--------|---------|--------|
| **Global pause** | `BUFFER_PUSH_ENABLED=false` | All buffer-push webhooks return `{ skipped: true }` |
| **Allowlist mode** | `BUFFER_PUSH_ALLOWLIST=CO-M2-LI-W2-01,CO-M2-IG-W2-03` | Only listed post_ids or page_ids are pushed; all others skipped |
| **Clear allowlist** | Delete `BUFFER_PUSH_ALLOWLIST` env var entirely | Returns to "push all approved" mode |

**When to use:**
- **Global pause:** When debugging, during rate-limit cooldown, or when you suspect a bug in the push flow
- **Allowlist:** When testing a single platform (e.g. push one LI post first, verify, then IG, then FB)
- **Clear allowlist:** When testing is done and you want to open floodgates for WF2

**How to set:**
```bash
railway variables --set "BUFFER_PUSH_ENABLED=false"      # Pause
railway variables --set "BUFFER_PUSH_ALLOWLIST=CO-M2-LI-W2-01"  # Gate
railway variables delete BUFFER_PUSH_ALLOWLIST             # Open floodgates
railway up --detach                                        # Redeploy to apply
```

**IMPORTANT:** `railway variables --set "KEY="` does NOT unset a variable — it sets it to empty string (which is truthy). Use `railway variables delete KEY` instead.

### 11.2 Past-date protection

Buffer rejects `dueAt` in the past with error: "dueAt must be in the future".

**Automated rule:** If `scheduled_at` in Notion is in the past at push time, bump by 7 days. But NEVER bump beyond `CAMPAIGN_END_DATE`. If bumping would exceed the end date, mark the post as `skipped` and log a warning.

### 11.3 Duplicate post prevention

**Atomic lock:** Script 04 flips status → `processing` immediately after confirming `approved`. If two webhooks fire simultaneously, only one sees `approved`; the other sees `processing` and aborts.

**Scan for duplicates:** Before any bulk operation, query Notion for posts with identical `caption_es` or `image_url_*` within the same week. Flag duplicates for human review.

**Ghost post risk:** If Buffer push succeeds but the subsequent Notion update fails, a Buffer post exists without a `buffer_post_id` in Notion. Reconciliation query:
```javascript
// Find Buffer posts not tracked in Notion — run periodically
const bufferPosts = await listScheduledBufferPosts(); // via GraphQL
const notionPosts = await getWeekPosts(week);
const trackedIds = new Set(notionPosts.map(p => p.buffer_post_id).filter(Boolean));
const orphans = bufferPosts.filter(bp => !trackedIds.has(bp.id));
```

### 11.4 Rate limits reference

| Service | Limit | Window | Error shape | Recovery |
|---------|-------|--------|-------------|----------|
| Buffer GraphQL | ~60 mutations | 15 minutes | `LimitReachedError { message }` or HTTP 429 | Wait 15 min; use kill-switch to prevent WF2 flood |
| Notion API | 3 req/s sustained | Rolling | HTTP 429 with `Retry-After` header | Built-in SDK retry; space bulk writes |
| Ideogram | ~60 req/min | Rolling | HTTP 429 | 5s retry built into `generateWithRetry`; second failure returns null |
| Claude API | Tier-dependent | Per-minute | HTTP 429 | Retry with backoff; use Sonnet to stay in budget |
| Firecrawl | Plan-dependent | Daily | HTTP 429 | Degrade gracefully (metrics show 0) |

---

## 12. Ideogram Image Generation

### 12.1 Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Model | `V_2_TURBO` | Fast, good quality for social media |
| Style | `DESIGN` | Clean, professional — suits brand aesthetics |
| Endpoint | `https://api.ideogram.ai/generate` | POST with `Api-Key` header |

### 12.2 Color palette

Loaded from the campaign's brand skill. CleantechHUB default:

```json
{
  "members": [
    { "color_hex": "#0C498A", "color_weight": 0.5 },
    { "color_hex": "#B2EEFA", "color_weight": 0.3 },
    { "color_hex": "#9DC384", "color_weight": 0.2 }
  ]
}
```

**Per-campaign override:** If using REIN Hubs brand or another brand, load the palette from that brand's skill file.

### 12.3 Aspect ratios

| Platform | Ratio name | Ideogram enum |
|----------|-----------|---------------|
| Instagram | 1:1 square | `ASPECT_1_1` |
| Facebook | 3:4 portrait | `ASPECT_3_4` (note: Ideogram v2 doesn't support `ASPECT_4_5`) |
| LinkedIn | 16:9 landscape | `ASPECT_16_9` |

All 3 ratios are generated in parallel via `Promise.all`. Each has a retry (5s delay, 1 retry). If both attempts fail for a ratio, that URL is `null`.

### 12.4 Ephemeral URLs

Ideogram returns URLs like `https://ideogram.ai/api/images/ephemeral/...?exp=...`. These expire (typically 24–48h). They are:
- Served via Cloudflare, which blocks some server-side fetchers (Meta Graph API, LinkedIn)
- Cached in our Railway image proxy for 24h (see §6.2)
- Stored in Notion as the `image_url_*` field values

**Risk:** If Ideogram URLs expire before Buffer publishes, the social platform gets a 404. Mitigation: warm the proxy cache immediately after generating images, or push to Buffer within 24h of generation.

---

## 13. Runbook

### 13.1 Emergency pause all pushes

```bash
cd clp26-automation
railway variables --set "BUFFER_PUSH_ENABLED=false"
railway up --detach
# Verify:
curl -s https://{domain}/health | python3 -m json.tool
```

All WF2 webhooks will return `{ skipped: true, reason: 'BUFFER_PUSH_ENABLED=false' }`.

To resume:
```bash
railway variables --set "BUFFER_PUSH_ENABLED=true"
railway up --detach
```

### 13.2 Re-push failed or edited posts to Buffer

Use case: URL was wrong, caption needs editing, image needs replacing.

**Step 1 — Fix content in Notion** (update caption_es, image URLs, etc.)

**Step 2 — Delete old Buffer posts:**
```javascript
const DELETE = `mutation($input: DeletePostInput!) {
  deletePost(input: $input) {
    __typename
    ... on DeletePostSuccess { id }
    ... on VoidMutationError { message }
  }
}`;
await bufferGraphQL(DELETE, { input: { id: oldBufferPostId } });
```

**Step 3 — Reset Notion row:**
```javascript
await notion.pages.update({
  page_id: pageId,
  properties: {
    status: { select: { name: 'approved' } },
    buffer_post_id: { rich_text: [] },
    post_url: { url: null },
  }
});
```

**Step 4 — Fire webhook:**
```bash
curl -X POST https://{domain}/webhook/buffer-push \
  -H "Content-Type: application/json" \
  -d '{"notion_page_id":"<page_id>","post_id":"<post_id>"}'
```

**Step 5 — Verify:**
- Check Notion: status = `scheduled`, new `buffer_post_id` present
- Check Buffer: `post(input: { id: newBufferPostId }) { status error { message } }` — should be `scheduled`, no error

### 13.3 Add a new platform channel

1. Create the channel in Buffer (connect the social account)
2. Get the Buffer channel ID from Buffer settings
3. Add env var: `BUFFER_PROFILE_{PLATFORM}_{COUNTRY}={channel_id}` on Railway
4. Add the platform to `CHANNEL_IDS` map in `lib/buffer.js`
5. Add platform-specific metadata in `pushPost()` if required
6. Add aspect ratio mapping in `lib/ideogram.js` `ASPECT_RATIOS`
7. Add image field mapping in Script 04 (`imageUrlField` switch)
8. Redeploy Railway

### 13.4 Add a new country

1. Run the Campaign Setup Questionnaire (§1) for the new country
2. Clone or create Notion Campaign DB + Strategy DB
3. Set new env vars for the country's Buffer channel IDs
4. Update `WEEK_STARTS` in Script 01 for the new campaign timeline
5. Update brand skill reference if language/palette differs
6. Clone Pipedream WF2 or add a filter for the new country
7. Update `post_id` format with new country code
8. Test with kill-switch + allowlist before opening floodgates

### 13.5 Rotate API tokens

| Token | Where to update | Notes |
|-------|----------------|-------|
| `NOTION_API_KEY` | Railway + Pipedream + local `.env` | Generate at Notion Settings → Integrations |
| `BUFFER_ACCESS_TOKEN` | Railway + Pipedream + local `.env` | Buffer Account → Apps → Access Token |
| `ANTHROPIC_API_KEY` | Railway + local `.env` | Anthropic Console → API Keys |
| `IDEOGRAM_API_KEY` | Railway + local `.env` | Ideogram dashboard |
| `FIRECRAWL_API_KEY` | Railway + local `.env` | Firecrawl dashboard |

After updating: `railway up --detach` to redeploy with new tokens.

### 13.6 Warm the image proxy cache

Run after generating images, or before a scheduled publish window:

```javascript
// Warm all images for a week through the proxy
const posts = await getWeekPosts(weekNumber);
for (const post of posts) {
  const imgField = { LI: 'image_url_landscape', IG: 'image_url_square', FB: 'image_url_portrait' }[post.platform];
  const url = post[imgField];
  if (!url) continue;
  const proxyUrl = `${PUBLIC_BASE_URL}/image-proxy?url=${encodeURIComponent(url)}`;
  await fetch(proxyUrl); // GET → caches for 24h
}
```

---

## 14. War Stories & Troubleshooting

Lessons learned from the CLP26 Colombia campaign (April 2026). Each entry documents the failure, root cause, and fix.

### 14.1 Buffer REST API deprecated → GraphQL migration

**Symptom:** `api.buffer.com/updates/create` returned HTTP 400: "GraphQL operations must contain a non-empty `query`".

**Root cause:** Buffer retired the REST `/updates/create` endpoint. All operations now go through `api.buffer.com/graphql`.

**Fix:** Complete rewrite of `lib/buffer.js` to use GraphQL mutations. Key discovery: Buffer's GraphQL schema has only 3 mutations (`createPost`, `deletePost`, `createIdea`) — no `updatePost`. Schema was discovered via introspection.

### 14.2 Pipedream WF2 payload mismatch

**Symptom:** Script 04 crashed with "notion_page_id is required" despite WF2 sending the page ID.

**Root cause:** WF2 sends `pageId`, Script 04 expected `notion_page_id`.

**Fix:** Accept both: `const notion_page_id = payload.notion_page_id || payload.pageId;`

### 14.3 Buffer 429 rate limit flood

**Symptom:** After fixing the WF2 payload alias, WF2 flooded Buffer with ~15 simultaneous pushes, burning the 15-min rate limit window.

**Root cause:** No throttle on WF2 — it fires for ALL approved posts on every poll cycle.

**Fix:** Added `BUFFER_PUSH_ENABLED` and `BUFFER_PUSH_ALLOWLIST` env-var gates in Script 04. Test individual posts via allowlist, then open floodgates only after confirming the pipeline works.

### 14.4 Facebook metadata requirement

**Symptom:** Buffer GraphQL returned `InvalidInputError`: "Facebook posts require a type".

**Root cause:** Facebook channel requires `metadata: { facebook: { type: 'post' } }` in `CreatePostInput`.

**Fix:** Added platform-specific metadata branching in `pushPost()`.

### 14.5 Past-date rejection

**Symptom:** Buffer rejected `dueAt` for 3 posts with "dueAt must be in the future".

**Root cause:** `scheduled_at` in Notion was set to dates that had already passed by the time the pipeline ran.

**Fix:** Manual bump +7 days. Automation should detect past dates and auto-bump (within campaign end date).

### 14.6 Meta Graph API can't reach Ideogram URLs

**Symptom:** Instagram posts created in Buffer but image showed as broken/missing. Buffer logs showed "Not Found" when fetching the image.

**Root cause:** Ideogram URLs are served via Cloudflare, which blocks Meta's Graph API crawlers (user agent or IP block).

**Fix chain:**
1. First tried pre-supplying image dimensions in Buffer metadata (altText + width/height) — helped Buffer skip its own probe but Meta's fetch still failed
2. Then tried to find a Buffer image upload mutation — introspection showed none exists (`ImageAssetInput.url` is NON_NULL, no binary upload)
3. Final fix: added `/image-proxy` endpoint on Railway that fetches from Ideogram and streams bytes. Buffer post's image URL points to our proxy. Meta fetches from Railway (trusted host). 24h in-memory cache prevents upstream hammering.

### 14.7 LinkedIn HEAD before GET

**Symptom:** LinkedIn posts had image issues similar to IG/FB.

**Root cause:** LinkedIn's media fetcher sends HEAD request first (checks file size and content type), then GET. Our proxy initially only handled GET — HEAD returned 405.

**Fix:** Added HEAD support to `/image-proxy` route. Returns same headers (Content-Type, Accept-Ranges, Cache-Control) but no body.

### 14.8 Railway `variables --set "KEY="` doesn't unset

**Symptom:** After trying to clear `BUFFER_PUSH_ALLOWLIST` with `--set "BUFFER_PUSH_ALLOWLIST="`, the env var persisted as empty string, which is truthy.

**Root cause:** Railway CLI treats `--set "K="` as setting to empty string, not deleting.

**Fix:** Use `railway variables delete BUFFER_PUSH_ALLOWLIST` instead.

### 14.9 Wrong CTA URL in all 15 posts (bulk fix)

**Symptom:** All 15 Week 2 posts contained `https://climatelaunchpad.org/colombia` instead of `https://climatelaunchpad.org/application-form/`.

**Root cause:** Wrong URL was provided as `cta_url` when Script 01 generated the content.

**Fix procedure (completed in ~3 minutes for 14 posts):**
1. Bulk-updated all 15 `caption_es` fields in Notion (string replace)
2. For each of 14 scheduled posts: Buffer `deletePost` → Notion status reset to `approved` → webhook fire → verify new Buffer post
3. 1 already-published LinkedIn post: manually edited on LinkedIn
4. All 14 re-pushed successfully with new Buffer IDs, correct URL verified in Buffer text

### 14.10 Script 02 status downgrade bug

**Symptom:** After regenerating images for an approved post, status silently dropped to `draft`.

**Root cause:** `02_ideogram.js:36` unconditionally sets `status: { select: { name: images.image_failed ? 'image_failed' : 'draft' } }`.

**Workaround:** Manually flip back to `approved` after regen.

**Proper fix (TODO):** Read current status before regen; only downgrade to `draft` if current status is `draft`. Otherwise preserve.

---

## 15. Cost Tracking

Track costs per campaign run to stay within budget.

### 15.1 Per-week generation costs (15 posts)

| Service | Usage per week | Approximate cost |
|---------|---------------|-----------------|
| Claude API (Sonnet) | 1 call, ~8K output tokens | ~$0.10–0.30 |
| Claude API (Opus) | 1 call, ~8K output tokens | ~$1.00–3.00 |
| Ideogram | 15 images (5 days × 3 ratios) | Plan-dependent |
| Buffer | 15 createPost mutations | Included in plan |
| Railway | Always-on container | ~$5/mo |
| Firecrawl | 15 scrapes (metrics) | Plan-dependent |
| Notion API | ~100 calls | Free |

**Recommendation:** Use Sonnet for generation (`model: 'claude-sonnet-4-20250514'`) unless caption quality visibly drops. Opus costs 10x more per call.

### 15.2 Tracking

Maintain a cost log per campaign:

| Campaign | Week | Claude cost | Ideogram cost | Total |
|----------|------|------------|---------------|-------|
| CLP26-CO | W2 | $0.25 | $0.00 (free tier) | $0.25 |

---

## 16. Bootstrap: New Campaign Checklist

Follow these steps IN ORDER when spinning up a new campaign.

### Phase 1 — Configuration (30 min)

- [ ] Run Campaign Setup Questionnaire (§1) — fill all 31 fields
- [ ] Confirm brand skill exists or create one (`cleantechhub-brand`, `rein-hubs-brand`, or new)
- [ ] Confirm CTA URL is live and reachable
- [ ] Confirm social accounts exist on all target platforms
- [ ] Confirm Buffer channels exist for each platform (or create them)

### Phase 2 — Infrastructure (1 hour)

- [ ] Clone `clp26-automation` repo or create a new one
- [ ] Update `WEEK_STARTS`, `PLATFORMS`, `PLATFORM_TIMES`, `CONTENT_ANGLES` in Script 01
- [ ] Update `COLOR_PALETTE` in `lib/ideogram.js` (from brand skill)
- [ ] Update `CHANNEL_IDS` in `lib/buffer.js`
- [ ] Create Notion Campaign DB (clone schema from §4.1)
- [ ] Create Notion Strategy DB (clone schema from §4.2)
- [ ] Set all env vars on Railway (§3.1)
- [ ] Deploy to Railway: `railway up --detach`
- [ ] Verify: `curl https://{domain}/health`

### Phase 3 — Pipedream (30 min)

- [ ] Clone WF2 (approved-post poller) or create new
- [ ] Determine if scraper/additional steps needed
- [ ] Set workspace env vars (web UI only — §3.2)
- [ ] Deploy workflow, verify it polls without errors

### Phase 4 — First week test (1 hour)

- [ ] Set `BUFFER_PUSH_ENABLED=false` (safety)
- [ ] Fire `/webhook/generate` with week 1 params
- [ ] Verify: 15 posts appear in Notion with status=`draft`, images populated
- [ ] Review content quality — adjust Claude prompt if needed
- [ ] Approve 1 test post per platform
- [ ] Set `BUFFER_PUSH_ALLOWLIST` to those 3 post_ids
- [ ] Set `BUFFER_PUSH_ENABLED=true`, redeploy
- [ ] Verify: 3 posts in Buffer queue, correct images, correct text
- [ ] Spot-check one post: "Share Now" in Buffer to verify end-to-end publish
- [ ] If all 3 work: clear allowlist, approve remaining posts, open floodgates

### Phase 5 — Monitoring (ongoing)

- [ ] Monitor first publish window — confirm posts appear on social platforms
- [ ] After 24h: run `/webhook/metrics` for published posts
- [ ] After week completes: run `/webhook/analysis` to populate Strategy DB
- [ ] Next week's generation reads strategy insights automatically

---

## 17. Dependencies

```json
{
  "@anthropic-ai/sdk": "^0.36.3",
  "@notionhq/client": "^2.2.15",
  "dotenv": "^17.4.2"
}
```

Node.js >= 18 required (for native `fetch`).

---

## 18. File Map

```
clp26-automation/
├── server.js              — HTTP server + /image-proxy + webhook router
├── package.json
├── .env                   — Local env vars (NOT committed)
├── lib/
│   ├── buffer.js          — Buffer GraphQL API (createPost, deletePost, probe, proxy)
│   ├── notion.js          — Notion API (read/write Campaign DB + Strategy DB)
│   ├── ideogram.js        — Ideogram API (3 aspect ratios, retry logic)
│   └── firecrawl.js       — Firecrawl API (engagement scraping)
├── scripts/
│   ├── 01_generate.js     — Claude + Ideogram → Notion (full week)
│   ├── 02_ideogram.js     — Standalone image regen
│   ├── 03_notion_write.js — Standalone Notion bulk write
│   ├── 04_buffer_push.js  — Notion → Buffer (with kill-switch)
│   ├── 05_metrics.js      — Buffer + Firecrawl → Notion metrics
│   └── 06_analysis.js     — Scoring → Strategy DB
```

---

## 19. Related skills

- `cleantechhub-brand` — base brand rules applied to all campaigns run by CleantechHUB
- `clp26-brand` — the ClimateLaunchpad 2026 overlay applied to CLP campaigns specifically
- `canva` — the source of campaign visuals; the Imgur rehost pattern in §4 of the canva skill is what makes Buffer posting work
- `buffer` — the destination for all published posts; this skill relies on the Buffer connector rules documented there
- `notion` — the human UI layer; all campaign pages, reviews, and approvals happen in Notion
- `claude-cowork` — campaign orchestration runs as a scheduled Cowork task
- `gmail` — weekly metrics emails and status reports are drafted via the Gmail MCP
