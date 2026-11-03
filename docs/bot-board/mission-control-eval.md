# Mission Control evaluation (live bot board — track B)

**Repo:** [builderz-labs/mission-control](https://github.com/builderz-labs/mission-control)  
**License:** MIT (Copyright 2026 Builderz Labs) — compatible with CleantechHUB internal use, modification, and private deployment; retain copyright notice in distributions.  
**Version surveyed:** `2.3.0` (clone at `c1a846fe020567bb3ceb3b65db9f00db875618cd`, 2026-11-03)  
**Scope:** Read-only evaluation for a **Grok / harness bot status board**. No VPS deploy in this ticket.

## Executive summary

**Verdict: BUILD** (a thin CleantechHUB bot board + optional ingest sidecar), not ADOPT Mission Control as the primary bot board.

Mission Control is a capable **agent orchestration control plane** (tasks, agents, sessions, costs, webhooks out). Its live UI is real (SSE + gateway WebSocket), but it has **no first-class HTTP ingest** for arbitrary external agent events. Mapping our `{bot_id, bot_name, layer, type, task, link, cause_tag, ts}` shape requires a **custom adapter and/or fork**, while pulling in alpha schemas, OpenClaw-oriented UX, and ops surface we do not need for a bot fleet ticker.

Use Mission Control later on the VPS only if we also want **task dispatch and multi-runtime orchestration** beside the bot board—not as a drop-in board.

---

## Local smoke test

| Step | Result |
|------|--------|
| Shallow clone to `/tmp/mission-control` | OK |
| `docker compose up` in cloud eval VM | **Blocked** — `docker` not installed on the Cloud Agent image |
| Test compose for a real host | `docs/bot-board/mission-control.docker-compose.yml` (bind `127.0.0.1:13000`, standalone profile via env, 512M limit aligned with upstream) |

On the OVH VPS (with Docker), run the compose file above, complete `/setup`, copy the API key from Settings, then exercise the REST loop from upstream [quickstart](https://github.com/builderz-labs/mission-control/blob/main/docs/quickstart.md).

---

## (1) Agent view: live or polling?

**Both, by layer.**

| Layer | Mechanism | What it updates |
|-------|-----------|-----------------|
| **Control-plane data** (tasks, agents, activities, notifications, chat in SQLite) | **SSE** — browser `EventSource` → `GET /api/events` | Instant UI updates via `activity.created`, `agent.updated`, `task.*`, etc. (`src/lib/use-server-events.ts`, `src/app/api/events/route.ts`) |
| **Same data (fallback)** | **Smart polling** — e.g. agent squad and activity feed every 30s, paused when SSE is connected (`useSmartPoll` + `pauseWhenSseConnected: true`) | Bootstrap + resilience when SSE drops |
| **Runtime / gateway** (live sessions, logs, spawn, exec approvals) | **WebSocket** to OpenClaw (or configured) gateway (`src/lib/websocket.ts`) | Not used in standalone gateway-free mode |

**Answer:** The **fleet / activity board is live via SSE** for anything written into the MC database. **Gateway-coupled “live session” views need WebSocket** to an agent runtime. Standalone Docker (`NEXT_PUBLIC_GATEWAY_OPTIONAL=true`) still gives SSE for REST-driven agent and task state.

SSE requires authenticated **viewer+** session or API key (same auth as REST).

---

## (2) Generic HTTP event ingest from external agents?

**No dedicated “post arbitrary event” endpoint.** Ingest is **domain-specific REST**, not a generic telemetry bus.

| Endpoint | Auth (typical) | Role |
|----------|----------------|------|
| `POST /api/agents/register` | Bearer API key (viewer+) | `{ name, role?, capabilities?, framework? }` — idempotent agent upsert |
| `POST /api/connect` | operator+ | CLI-style connect; returns `sse_url`, `heartbeat_url` |
| `POST /api/agents/:id/heartbeat` | operator+ (agent-scoped keys limited to self) | `{ connection_id?, status?, last_activity?, token_usage? }` — presence + optional activity text |
| `GET /api/agents/:id/heartbeat` | viewer+ | Poll work queue (tasks, notifications) — agent-centric, not event sink |
| `POST /api/tasks` | operator+ | Task lifecycle — creates activities indirectly |
| `POST /api/chat/messages` | operator+ | Inter-agent chat; can carry `metadata` |
| `GET /api/activities` | viewer+ | **Read-only** activity stream (filters: `type`, `actor`, `entity_type`, `since`, …) |
| `POST /api/webhooks` | admin | **Outbound** subscriptions (MC → your URL on internal events), not inbound ingest |

Activities are created internally via `db_helpers.logActivity(...)` which broadcasts `activity.created` on SSE. **External callers cannot invoke that without new API or a fork.**

OpenAPI documents `GET` only on `/api/activities` (`openapi.json`).

---

## (3) Resource footprint and dependencies

| Component | Notes |
|-----------|--------|
| **Database** | **SQLite** (`better-sqlite3`) — single file under `/app/.data`; no Postgres/Redis required |
| **Runtime** | Node **22+** (Dockerfile uses Node 24 slim); Next.js app |
| **Auth** | Local users (`/setup`), **API keys** (Settings), optional Google OAuth, proxy auth headers; RBAC `admin` / `operator` / `viewer`; agent-scoped keys |
| **Optional** | OpenClaw gateway (WebSocket) for live sessions; GitHub sync; MCP server |
| **Docker (upstream)** | One service, **512M RAM / 1 CPU** cap, read-only root + tmpfs; named volume `mc-data` |
| **Alpha risk** | README warns APIs/schemas may change between releases |

Fits **one container on the existing OVH VPS** next to BookStack if we ever adopt it for orchestration—not lightweight compared to a static HTML + SSE bot board.

---

## (4) Adapter difficulty for CTH event shape

**Target shape:**

```json
{
  "bot_id": "string",
  "bot_name": "string",
  "layer": "string",
  "type": "string",
  "task": "string",
  "link": "string",
  "cause_tag": "string",
  "ts": "unix or iso"
}
```

**Difficulty: medium–high** for faithful mapping without code changes to Mission Control.

| Field | Practical mapping | Gap |
|-------|-------------------|-----|
| `bot_name` | `POST /api/agents/register` (`name`; must match `[a-zA-Z0-9][a-zA-Z0-9._-]{0,62}`) | `bot_id` not first-class; store in `capabilities` or agent `config` via operator APIs |
| `layer`, `type`, `cause_tag`, `link`, `ts` | No activity POST — pack into `task` title/description + `metadata` on `POST /api/tasks`, or `metadata` on chat messages | Pollutes task board; wrong semantics for high-volume telemetry |
| Presence | `POST .../heartbeat` with `last_activity` | One line per heartbeat, not full event history |
| Live board | SSE fires only when MC writes rows | Adapter must call MC REST for **each** event (or batch job) |

**Recommended adapter pattern if we ever pair BUILD + MC:**

1. **CTH ingest sidecar** (small service): accept our canonical JSON (HTTP POST from Grok Bot / harness).
2. Sidecar: ensure agent registered; **fork or plugin** one endpoint `POST /api/activities/ingest` calling `logActivity` (cleanest), **or** write to a separate SQLite/JSON store that a **custom MC panel** reads (heavier).
3. Do **not** spam `POST /api/tasks` for telemetry — operational noise and alpha task schema churn.

Without a fork/plugin, Mission Control is a ** poor fit** as the single sink for harness bot events.

---

## (5) Licence check

- **SPDX:** MIT  
- **File:** upstream `LICENSE` — standard MIT terms, Builderz Labs copyright 2026  
- **CTH use:** Allowed for internal deployment and modification; no copyleft obligations; document third-party notice if we ship a derivative container image  
- **Not a blocker** for ADOPT; product fit is the blocker

---

## ADOPT vs BUILD

| Criterion | Mission Control | CTH bot board (BUILD) |
|-----------|-----------------|------------------------|
| Purpose | Multi-runtime agent ops, tasks, costs, governance | Grok/harness **bot fleet visibility** and cause tagging |
| Event ingest | REST task/agent/chat; no generic ingest | Design ingest around `{bot_id, …, ts}` |
| Live UI | SSE + optional gateway WS | SSE or WS from our store |
| Weight | Full Next app, alpha API | Static HTML or minimal service (Nexus-style) |
| Brand / UX | OpenClaw operator dashboard | CleantechHUB bot board UX |

### BUILD — recommended

- Optimize for **one event schema** and **layer/cause_tag** filters.  
- Avoid coupling bot telemetry to **task inbox** semantics.  
- Keep Mission Control eval compose for a **future orchestration** experiment, not as the bot board MVP.

### ADOPT — when it would make sense

- We want **task assignment, review gates, token/cost tracking**, and **agent registration** in one product **and** accept building a **sidecar + small MC fork** for `activity` ingest.  
- Willing to track **upstream alpha** breaking changes.

---

## References (upstream)

- README — Docker, standalone mode, REST quickstart  
- `src/lib/use-server-events.ts` — SSE client  
- `src/app/api/events/route.ts` — SSE server  
- `src/lib/db.ts` — `logActivity` + SSE broadcast  
- `docker-compose.yml` — resource limits and volumes  
- `docs/quickstart.md` — gateway-free agent loop  

---

## Artifacts in this repo

- `docs/bot-board/mission-control-eval.md` (this file)  
- `docs/bot-board/mission-control.docker-compose.yml` — localhost-bound test install  
