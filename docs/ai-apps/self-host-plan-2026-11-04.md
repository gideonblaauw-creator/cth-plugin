# AI Apps for Good — CTH VPS self-host plan (2026-11-04)

Read-only feasibility review for six adopted apps from [`docs/research/aiappsforgood-eval-2026-11-04.md`](../research/aiappsforgood-eval-2026-11-04.md) (branch `cursor/aiappsforgood-eval-2026-11-04-086f`). Target: **`apps.cleantechhub.net`**, one path per app, Google SSO via Caddy `forward_auth` to `auth.cleantechhub.net` (same pattern as [`services/bot-events/Caddy.snippet`](../../services/bot-events/Caddy.snippet)). Static roots under **`/opt/cth-apps/<slug>/`**, analogous to `/opt/cth-decks`.

**Scope of this PR:** planning doc only — no app code copied into the repo, no VPS deploy.

## Research constraints

| Constraint | Notes |
| --- | --- |
| File size cap | No repo file reads &gt; 200 KB (SecureCheck JS bundle ~366 KB inspected via remote `curl` + `rg` only). |
| `aiappsforgood.org` | Cloudflare blocks VM `curl` and headless Chrome on app HTML; architecture for project apps inferred from site copy, eval CSV, and Org360/Impaque/Jess pages via WebFetch and reachable static assets. |
| Artifact source | Project apps are described as single-file HTML uploads; **no public GitHub mirror found** for Pitch/MEL/Compass/Tough HTML. Self-host needs **author-provided files** or a one-time browser save (HITL), not scraper copy in this ticket. |

---

## Summary table

| App | URL (source) | Licence | Static / backend | External deps (runtime) | Verdict | Effort |
| --- | --- | --- | --- | --- | --- | --- |
| **Pitch Builder** | [pitchbuilder.html](https://aiappsforgood.org/pitchbuilder.html) | **CC BY 4.0** (site-wide, project apps) — see quote below | Single-page **static HTML/JS** in browser; **LLM proxy required** (Claude today) | Author LLM proxy (URL not readable behind CF); **Anthropic Claude** (via proxy); Web Speech API (browser); optional fonts/CDN if embedded in artifact | **Host** (after proxy + artifact HITL) | **M** |
| **MEL Builder** | [melbuilder.html](https://aiappsforgood.org/melbuilder.html) | **CC BY 4.0** — see quote below | Static HTML/JS + **LLM proxy**; optional **web-search** step for NGO examples | Claude (proxy); **Perplexity or search API** for “real-world examples” (per eval CSV); [BetterEvaluation.org](https://www.betterevaluation.org/) links (user browser) | **Host** (proxy + artifact; disable or rewire search if no search key) | **M–L** |
| **Compass** | [compass.html](https://aiappsforgood.org/compass.html) | **CC BY 4.0** — see quote below | Mostly static; **game + browse** paths local; **“Ask Claude”** path needs LLM proxy | Claude (proxy); OG/images on `nonprofitbuilder.org` if referenced in artifact | **Host** (proxy + artifact; game-only mode works without LLM) | **M** |
| **Tough Conversations** | [toughconversations.html](https://aiappsforgood.org/toughconversations.html) | **CC BY 4.0** (project app; no per-app LICENSE file) — see quote below | Static HTML/JS + **LLM proxy**; printable Help Kit (browser print/PDF) | Claude (proxy); Org360 OG assets (`assessments.org360.app`) | **Host** (proxy + artifact) | **M** |
| **Jess's Calendar Colorizer** | [calendar-colorizer](https://jessicaeastmanstewart.com/calendar-colorizer) | **none found** (no LICENSE, no CC notice on page) | **Squarespace-hosted generator** (client-side rules → Apps Script text); **no server** on Jess’s site; execution is **Google Apps Script** in the user’s Google account | Squarespace CDN, Adobe Typekit, Google `script.google.com` (user install); not a runnable “app” on CTH VPS for coloring | **Host after author OK** *or* **don't host — use extracted rubric** for rule/schema only | **S** (link/embed) / **L** (full re-host of widget) |
| **SecureCheck** (Impaque) | [securecheck.impaque.com](https://securecheck.impaque.com/) | **none found** (no LICENSE file or OSS repo for this product) | **Next.js static export** (client-only SPA); questions/scoring in JS bundles; **localStorage** only | Google Fonts; outbound links to EFF, CISA, etc. in copy; **no LLM** observed in bundles | **Host after author OK** *or* **don't host — use extracted rubric** | **L** (mirror) / **M** (rubric-only) |

### Licence quotes (exact text + source)

**AI Apps for Good — project-developed apps (Pitch, MEL, Compass, Tough Conversations):**

> All apps developed by AI Apps for Good are open source. You are welcome to copy, adapt, and distribute them — including commercially — as long as you provide attribution. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

Source: [https://aiappsforgood.org/](https://aiappsforgood.org/) (Open source section).

**Jess's Calendar Colorizer:** none found on [https://jessicaeastmanstewart.com/calendar-colorizer](https://jessicaeastmanstewart.com/calendar-colorizer) (Squarespace page; no footer licence).

**SecureCheck (Impaque):** none found on [https://securecheck.impaque.com/](https://securecheck.impaque.com/) or Impaque blog; unrelated GitHub repos named “SecureCheck” are different products (AGPL/MIT).

**Community / author contact (if licence needed):**

| App | Contact |
| --- | --- |
| Calendar Colorizer | Jessica Eastman Stewart — [jessicaeastmanstewart.com](https://jessicaeastmanstewart.com/calendar-colorizer), [LinkedIn](https://www.linkedin.com/in/jessicaestewart/) |
| SecureCheck | Impaque — [https://www.impaque.com/contact](https://www.impaque.com/contact) |
| AI Apps for Good artifacts / proxy | Daniele D'Esposito / Nonprofit Builder — site offers proxy help: [https://aiappsforgood.org/](https://aiappsforgood.org/) |

---

## Per-app architecture (detail)

### Pitch Builder

- **UI:** 10-question intake (voice via Web Speech API or text), AI follow-ups, 10-slide deck output ([page copy](https://aiappsforgood.org/pitchbuilder.html)).
- **Backend:** None on CTH unless we add a **tiny LLM proxy**; upstream today uses the author’s hosted proxy (browser must not hold API keys — stated on [aiappsforgood.org](https://aiappsforgood.org/)).
- **Database / login:** None.
- **CTH feasibility:** Copy artifact to `/opt/cth-apps/pitch-builder/`; rewrite proxy base URL to same-origin `https://apps.cleantechhub.net/api/llm/` (see proxy section).
- **Agent use:** Extract the 10 prompts (+ follow-up rubric) to `docs/ai-apps/rubrics/pitch-builder-questions.json` for grant/deck skills; headless flow = POST structured answers to OpenRouter via internal proxy, skip browser.

### MEL Builder

- **UI:** Two-step card intake, open-text org description, pick among recommended MEL approaches (BetterEvaluation library embedded in page), optional “find real-world examples”.
- **Backend:** LLM for matching + design guide; eval CSV notes **Claude + Perplexity** for live example search.
- **Database / login:** None.
- **CTH feasibility:** Static tree + proxy; treat example search as **optional** (feature-flag off until search credentials exist).
- **Agent use:** Extract card option sets + approach catalog to `docs/ai-apps/rubrics/mel-builder-intake.json` and `docs/ai-apps/rubrics/mel-builder-approaches.json`.

### Compass

- **UI:** Three paths — 5-minute prioritization game, three-question Claude roadmap, browse 80 projects / 14 themes ([compass.html](https://aiappsforgood.org/compass.html)).
- **Backend:** LLM only on “Ask Claude” path; game/browse likely pure client data.
- **Database / login:** None.
- **CTH feasibility:** Static host; LLM path wired like other apps.
- **Agent use:** Extract project/theme catalog to `docs/ai-apps/rubrics/compass-projects.json` for capacity planning tickets.

### Tough Conversations

- **UI:** Situation text → pick support area → AI-applied technique; session kit + print/PDF ([toughconversations.html](https://aiappsforgood.org/toughconversations.html)).
- **Backend:** LLM proxy only; **no storage** (page disclosure).
- **Database / login:** None.
- **CTH feasibility:** Static host + proxy; Org360 branding only in meta/OG.
- **Agent use:** **15 techniques** already described on-page → `docs/ai-apps/rubrics/tough-conversations-techniques.json`; agents can apply rubric without UI.

### Jess's Calendar Colorizer

- **UI:** Wizard builds **Google Apps Script**; user pastes into `script.google.com` and sets time-driven trigger ([page](https://jessicaeastmanstewart.com/calendar-colorizer)).
- **Backend:** None on publisher site; **Google** runs the script.
- **CTH feasibility:** Re-hosting is mostly **marketing/generator UX** (Squarespace embed). CTH could iframe or rebuild a thin static clone **after licence confirmation**. Self-host does **not** remove Google dependency.
- **Agent use:** Document rule schema + sample rules in `docs/ai-apps/rubrics/calendar-colorizer-rules-schema.json`; Hands generate script text without loading Squarespace.

### SecureCheck (Impaque)

- **UI:** Quick (10 Q) vs full (31–51 Q) assessment; adaptive wording by size/region; scores + PDF report ([blog](https://www.impaque.com/blog/securecheck-free-security-assessment-for-nonprofits)).
- **Backend:** **None** — answers in **browser localStorage**; static Next chunks under `/_next/static/`.
- **Database / login:** None; no telemetry claimed.
- **CTH feasibility:** Technically mirror static assets to `/opt/cth-apps/securecheck/` **if Impaque grants redistribution**; otherwise **extract question bank** from JS (large bundle) into repo rubric JSON for agent-only assessments.
- **Agent use:** `docs/ai-apps/rubrics/securecheck-questions.json` + scoring weights for VPS/inbox hygiene checklists.

---

## LLM proxy (CTH)

Do **not** embed API keys in HTML. Pattern from AI Apps for Good site + CTH secrets policy:

| Item | Proposal |
| --- | --- |
| Service | Tiny reverse proxy on VPS (e.g. `127.0.0.1:8787`) — Node, Caddy `reverse_proxy`, or existing gateway if present |
| Secret | Infisical project **`cth-agents`**, key name **`OPENROUTER_API_KEY`** (name only; value never in repo/chat) |
| Upstream | OpenRouter chat/completions with Anthropic models (e.g. `anthropic/claude-sonnet-4` — exact model locked at deploy time) |
| Browser URL | `https://apps.cleantechhub.net/api/llm/v1/chat/completions` (same-origin, behind `forward_auth`) |
| Hardening | Rate limit per email (`X-Forwarded-Email`), max tokens, allowlist models, no CORS for public internet |

MEL “live examples” search: separate Infisical key (e.g. **`PERPLEXITY_API_KEY`** or search-via-OpenRouter) — only if Gideon approves; otherwise disable button in hosted artifact.

---

## DNS

| Record | Value |
| --- | --- |
| `apps.cleantechhub.net` | **A** → `<OVH_VPS_IP_SAME_AS_DECKS>` |

Use the same OVH VPS as `decks.cleantechhub.net` ([`docs/infra/caddy/decks.cleantechhub.net.caddy`](../infra/caddy/decks.cleantechhub.net.caddy)). Replace placeholder at deploy time from Infrastructure Desk / VPS SoT.

---

## Draft Caddy site block (doc only — not applied)

```caddy
# apps.cleantechhub.net — AI Apps for Good (CTH self-host)
# Merge into OVH Caddyfile after DNS + /opt/cth-apps sync.
# Google SSO gate: same oauth2-proxy as bot-events.

apps.cleantechhub.net {
	encode gzip zstd
	header {
		X-Content-Type-Options nosniff
		Referrer-Policy strict-origin-when-cross-origin
		X-Robots-Tag "noindex, nofollow"
	}

	# Same-origin LLM proxy (authenticated Hands/agents in browser)
	handle /api/llm/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		reverse_proxy 127.0.0.1:8787
	}

	# Optional: trailing-slash normalization per app
	@pitch path /pitch-builder /pitch-builder/
	handle @pitch {
		redir * /pitch-builder/ 308
	}
	handle_path /pitch-builder/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/pitch-builder
		try_files {path} {path}/ /index.html
		file_server
	}

	handle /mel-builder {
		redir * /mel-builder/ 308
	}
	handle_path /mel-builder/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/mel-builder
		try_files {path} {path}/ /index.html
		file_server
	}

	handle /compass {
		redir * /compass/ 308
	}
	handle_path /compass/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/compass
		try_files {path} {path}/ /index.html
		file_server
	}

	handle /tough-conversations {
		redir * /tough-conversations/ 308
	}
	handle_path /tough-conversations/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/tough-conversations
		try_files {path} {path}/ /index.html
		file_server
	}

	handle /calendar-colorizer {
		redir * /calendar-colorizer/ 308
	}
	handle_path /calendar-colorizer/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/calendar-colorizer
		file_server
	}

	handle /securecheck {
		redir * /securecheck/ 308
	}
	handle_path /securecheck/* {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/securecheck
		try_files {path} {path}/ /index.html
		file_server
	}

	handle {
		forward_auth auth.cleantechhub.net {
			uri /oauth2/auth
			copy_headers X-Forwarded-User X-Forwarded-Email
		}
		root * /opt/cth-apps/index
		file_server
	}
}
```

Adjust `try_files` if artifacts are single `.html` files instead of `index.html` directories.

---

## VPS folder layout

```text
/opt/cth-apps/
├── index/                      # optional landing: links to six apps (CTH-branded)
├── pitch-builder/              # from aiappsforgood.org (CC BY 4.0)
├── mel-builder/
├── compass/
├── tough-conversations/
├── calendar-colorizer/           # re-hosted generator OR static wrapper + link
├── securecheck/                  # static mirror of Next export (if authorised)
└── llm-proxy/                    # deploy metadata only; binary lives in /opt or container

# Repo (skills/agents) — rubrics only, no proprietary JS
docs/ai-apps/rubrics/
├── pitch-builder-questions.json
├── mel-builder-intake.json
├── mel-builder-approaches.json
├── compass-projects.json
├── tough-conversations-techniques.json
├── calendar-colorizer-rules-schema.json
└── securecheck-questions.json
```

Sync playbook (future ticket): `rsync` or git-less copy from HITL artifact store on VPS `/opt/claude-files` — **do not** commit app HTML to `cth-plugin`.

---

## Rollout order

| Phase | App | Rationale |
| --- | --- | --- |
| **0** | DNS + Caddy + `forward_auth` + LLM proxy | Shared gate for all apps; unlocks AI Apps for Good clones |
| **1** | **SecureCheck** | No API key; highest ops value for VPS/Gmail hygiene; agent rubric useful even if UI blocked on licence |
| **2** | **Tough Conversations** | Single LLM surface; technique JSON unblocks Meetings/Inbox skills immediately |
| **3** | **MEL Builder** | Grant/Nexus workflows; optional search can ship later |
| **4** | **Pitch Builder** | Decks lane; EN/FR; same proxy |
| **5** | **Compass** | Useful game path without LLM first; Claude path second |
| **6** | **Calendar Colorizer** | Lowest marginal value on VPS (Google execution); prefer rubric + link until Jess confirms licence |

Parallel **HITL:** email Daniele (HTML artifacts + proxy URL map), Impaque (SecureCheck redistribution), Jessica (Calendar Colorizer licence).

---

## Blockers

1. **No downloadable HTML from `aiappsforgood.org` on the VM** (Cloudflare) — need author files or manual export.
2. **No public git repo** for project app sources — CC BY 4.0 allows copy, but Hands need a lawful artifact source.
3. **SecureCheck** and **Calendar Colorizer** — **no licence text found**; mirror only after author OK.
4. **MEL example search** — extra API credential and cost cap; scope separately.
5. **Proxy endpoint mapping** — exact `fetch()` URL in each HTML file unknown until artifact inspection; rewrite pass required.
6. **Approval gate** — external AI tools remain subject to CTH approval and secrets policy (eval doc note).

---

*Internal CleantechHUB planning doc. No deploy in this PR.*
