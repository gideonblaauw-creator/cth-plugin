---
name: socials-loop
description: >
  Socials Desk weekly content loop — ingest (optional X research signal) →
  Hands research → Hands copy → Hands stills → Desk review → Gideon HITL →
  Workbench post (only if Hands cannot). Trigger on "socials loop", "weekly
  social", "social post pack",
  "LI/IG/FB pack", "social stills", or Socials Desk content production.
metadata:
  version: "1.0.0"
  category: operations
  desk: "Socials"
  desk_id: "22eef082"
  owner: Infrastructure desk c656afb9
---

# Socials Loop

**Owner:** Infrastructure desk c656afb9
**Desk:** Socials (22eef082)
**Status:** adopted — Orchestrator wire 2026-08-27
**Rulebook:** `skills/harness/SKILL.md` (read before any ticket)

This skill is the **production loop** for Socials Desk content. It is not a comms protocol (`skills/socials-comms/SKILL.md`) and not a campaign bootstrap (`skills/social-media-campaign/SKILL.md`). It wires ingest through HITL for one weekly pack or ad-hoc post set.

Grok Bot on Socials Desk is **coordination only** (Token lock 2026-08-26). Route, ticket, review, HITL. Do not first-draft packs in Grok.

## 1. Locked loop (Orchestrator wire 2026-08-27)

```
ingest (URL / week topic / Drive / optional X signal)
  → Hands research (Flash)
  → Hands copy (Flash, LI/IG/FB)
  → Hands stills (Images + OpenRouter or Canva)
  → Socials reviews (maker ≠ checker)
  → Gideon HITL
  → Workbench posts ONLY after yes, and only if Hands cannot post
```

Each arrow is a **separate Hands ticket** unless the seven-field ticket explicitly batches steps. No bc-id = miss.

## 2. Ingest

Socials Desk or Orchestrator supplies one of:

| Input | Source | Notes |
|---|---|---|
| URL | link to article, event page, partner page | Hands research ticket cites URL |
| Week topic | Desk brief (one sentence + brand) | No invented angles — use Desk brief |
| Drive | Archive path under `/opt/claude-files/Projects/…` or shared Drive folder | Lane B `drive-folder`; Hands returns bc-id |
| X signal (optional) | Daily **X signal** file from **X Desk**; X post URLs Gideon shares in chat | Research input only; see **X research ingest** below |

Archive stays source of truth. Do not clone VPS files into this repo. Fetch via Drive MCP / Composio / VPS `gws` per Hands-shift lock in harness §5.

### X research ingest (optional)

Gideon approved **2026-11-18** (X Desk ticket J2). Use when the weekly pack should include public X context. This step **feeds §3 Hands research only**. X is **not** a publish channel in this loop.

**Sources (read-only):**

1. The X Desk daily **X signal** file (public X trends, news, and verified posts summarized for research).
2. Public X reads via **Grok Bot** built-in public X reads (no paid X API).
3. Individual **X post URLs** Gideon pastes into the owning chat or ticket.

**Flow:** Socials or Orchestrator tickets Hands to merge X signal + URLs into the research pack inputs. Do **not** ticket X copy, X stills, or X scheduling in this loop.

**Hard rules:**

| Rule | Detail |
|---|---|
| Zero X spend | No paid X API, no purchased X credits. Reads of Gideon's bookmarks via his X connection stay **disabled** until confirmed free. |
| HITL | Every post in the loop stays HITL (§7). X ingest does not bypass Gideon yes. |
| Alerts | Slack `#CTH_OPS` when that channel exists. Never Telegram. |
| Language / topics | No German. No war, weapons, military, or defence topics. |
| Typography | No em dashes in loop copy or research notes. |
| Source links | Every fact taken from X keeps its **source post URL** in the research pack. |
| Brand separation | **CTH** and **AIC** content stay separate. AIC material never mentions Run Up, Bravo Bridge, or CleantechHUB (CTH). |
| Publish boundary | Do **not** add X copy to LinkedIn, Instagram, or Facebook drafts. Research may cite X; platforms stay LI / IG / FB only (§4). |

## 3. Hands research (Flash)

**Model:** `gemini-3.7-flash`

Desk tickets Cloud Hands. Output: short research pack (facts, quotes, links, audience hook). No copy yet.

When **X research ingest** (§2) ran, fold X-sourced facts into this pack with post URLs attached. Drop any X item that breaks §2 hard rules (topics, language, brand separation).

- Cite sources. No invented statistics.
- Brand context: read `skills/cleantechhub-brand/SKILL.md` (default) or campaign brand skill (`clp26-brand`, etc.) per `skills/socials-comms/SKILL.md` §2.
- Store: Lane B Drive folder or ticket `folder:` field. Lane A only when the artifact belongs in `cth-plugin`.

## 4. Hands copy (Flash, LI/IG/FB)

**Model:** `gemini-3.7-flash`

Platform-specific copy for **LinkedIn**, **Instagram**, and **Facebook** from the research pack.

| Platform | Rules |
|---|---|
| LinkedIn | Professional tone, ~1300 chars optimal, 3–5 hashtags. See `skills/social-media-campaign/SKILL.md` § Platform-Specific Rules |
| Instagram | Visual-first caption, hashtags in first comment when required |
| Facebook | Community tone, 1–2 hashtags max |

Apply the correct brand skill. Mark all public CTH copy **Awaiting Gideon's approval** before publish.

## 5. Hands stills (Images + OpenRouter or Canva)

**Model:** `gemini-3.7-flash` for mechanical pack; image generate via Tools (not a model slot).

| Route | When | Skill / Tool |
|---|---|---|
| **Canva** | Brand layouts, templates, co-brand assets | `skills/canva/SKILL.md` — export before use |
| **OpenRouter images** | Throwaway mocks, quick AI stills | OpenRouter `POST /api/v1/images` per harness §5 media bus |
| **OSS self-host** | Branded diffusion stills when GPU host live | `skills/oss-stills/SKILL.md` — ComfyUI + Flux.1-Dev + CTH LoRA; `host: HOLD` until stand-up |
| **HeyGen** | Presenter video only — not default for stills | Harness: presenter video stays HeyGen primary |

Do not pass Canva editor URLs to Buffer or Workbench. Export first.

Image URLs for publishing must be **publicly accessible** — see `skills/buffer/SKILL.md` Critical Rules.

## 6. Socials review (maker ≠ checker)

Socials Desk reviews every Hands output. The Hands run that produced the pack is **not** the reviewer.

Checklist:

- [ ] Brand skill followed — no cross-leak (`skills/socials-comms/SKILL.md` §2)
- [ ] Facts match research pack — no invented claims
- [ ] LI / IG / FB variants are distinct, not copy-paste
- [ ] Stills exported and URLs are public-ready
- [ ] Nothing marked sent/posted/scheduled

Review / eval / brand with **no model** on the ticket → **HOLD** and flag Gideon. No auto-Sonnet/Opus/Grok (Token lock 2026-08-26).

## 7. Gideon HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.

All public CTH social copy: **Awaiting Gideon's approval** before publish.

HITL gate sits **after** Desk review, **before** any publish step.

## 8. Publish — Workbench exception only

**Default:** Hands schedules or drafts via Tools (`skills/buffer/SKILL.md`, Buffer MCP) when connector session exists.

**Workbench** (LinkedIn, Instagram, Facebook, Google Ads — children of Socials Desk) posts **only when Hands cannot** (no CLI, no connector, no API). HITL before post/DM/spend/launch/pause.

Order: Gideon yes → Hands tries Buffer/API → if blocked, escalate to Workbench → Workbench posts with HITL already cleared.

Workbench is **not** a second Hands. See `skills/socials-comms/SKILL.md` §6 and harness Workbench map.

## 9. Models and tickets

| Step | Model | Lane |
|---|---|---|
| Research pack | `gemini-3.7-flash` | `drive-folder` or `github-pr` per store |
| Copy pack (LI/IG/FB) | `gemini-3.7-flash` | same |
| Stills pack | `gemini-3.7-flash` + Tools | same |
| Repo / skill edits | `composer-2.5` (`fast=true`) | Fast ON (t1263u) | `github-pr` on owning repo |

Lane A for this repo: `https://github.com/gideonblaauw-creator/cth-plugin`. Ticket template: `tickets/TEMPLATE.md`.

Never silently use Sonnet, Haiku, Opus, or Grok on Cloud Hands. Repo/code builds use Composer 2.5 Fast ON (t1263u); mechanical/tiny stay Flash.

## 10. Do not add

This loop does **not** introduce:

- LangGraph / Agent Inbox
- Agentfy / Streamlit
- Blaxel deploy
- Arcade auto-post
- Supabase asset DB
- A new repo
- A second orchestrator
- **X as a publish channel** in this loop (X is research ingest only, §2)

## 11. Keep

- Socials Desk **22eef082**
- Workbench children (LinkedIn, Instagram, Facebook, Google Ads)
- OpenRouter / Canva / HeyGen (Tools per harness media bus)
- Drive + Archive (Lane B, VPS source of truth)
- HITL before send / post / pay
- Flash for mechanical Hands work
- `composer-2.5` (`fast=true`) for repo/build Hands (t1263u)
- High-tier review with no model → HOLD, flag Gideon

## 12. Related skills

| Skill | Role |
|---|---|
| `skills/harness/SKILL.md` | Rulebook, lanes, models, Workbench map |
| `skills/socials-comms/SKILL.md` | Desk comms protocol |
| `skills/cleantechhub-brand/SKILL.md` | Default brand |
| `skills/social-media-campaign/SKILL.md` | Campaign setup and platform rules |
| `skills/buffer/SKILL.md` | Schedule / publish via Buffer |
| `skills/canva/SKILL.md` | Brand layout stills |
