# CleantechHUB Fleet ↔ Atlassian wiring design

**Status:** DRAFT · design-only (no Atlassian API calls)  
**Version:** v1 · 25 Nov 2026  
**Site:** [cleantechhub.atlassian.net](https://cleantechhub.atlassian.net)  
**License:** Social Impact · Teamwork Collection (Jira, Confluence, Loom, Rovo) · annual  
**Seat policy:** ≤25 users at $0; above 25 = 75% off list; usage-based billing from **3 Dec 2026** — design stays inside 25 seats and **zero incremental budget**.

**Inputs:** `FLEET_REGISTRY.yaml` (94 bots), `PROTOCOLS.md`, `docs/fleet/**`, n8n/Slack/Gmail patterns from harness wire fixtures and desk skills.

**Artifacts:** `space-map.csv`, `master.mmd` (+ SVG/PNG), `orchestrator-dashboard.mmd` (+ SVG/PNG).

---

## 1. Executive recommendation

**Adopt a desk-first Atlassian topology, not one project per bot.**

| Layer | Jira | Confluence | Loom | Rovo |
| :--- | ---: | ---: | ---: | ---: |
| Tier 0 control plane (2) | 2 projects | 2 spaces | 2 folders | 2 fleet scopes |
| Tier 1 desks (65 active) | 65 projects | 65 spaces | 65 folders | 65 knowledge scopes |
| Tier 1b client isolated (28 strict) | 28 permission-scheme projects | 28 locked spaces | 28 client folders | 28 isolated scopes |
| Tier 2 workbenches (20) | 0 new projects · 20 **components** under parent desk | child pages under desk home | subfolders | scoped to parent |
| Tier 3 capabilities (6) | shared `CTHCAP` + 6 components | `CTHCAP` children | subfolders | tool scopes |
| Tier 4 Cloud Hands (1 registry bot) | shared `CTHHANDS` + bot label on every issue | runbooks index | ops recordings | read-only ops scope |
| **Totals (logical links)** | **69 projects** + **26 components** = **94 bot links** | same pattern | 94 folder paths | 94 scopes |

**Why not 94 Jira projects?** Bots are not humans. Ninety-four projects multiply permission-scheme maintenance, dashboard gadgets, and Rovo indexing cost without matching harness org (Desks own subjects; Workbenches are stateless I/O). Components + labels give each bot a durable `bot_id` anchor while keeping client isolation at the **desk** boundary (registry `isolation.kind: client|grant_draft`).

**Canonical keys:** see `space-map.csv` (generated from registry; keys like `CTHORCH`, `CTHOPS`, desk `CTH{SLUG4}`).

---

## 2. Service and automation identities (≤25 seats)

Bots **never** consume Atlassian seats. Use a small set of **human + service** users:

| # | Identity type | Suggested display name | Role |
| ---: | :--- | :--- | :--- |
| 1 | Human | Gideon Blaauw | Org admin, sole HITL approver, Orchestrator dashboard owner |
| 2 | Human (optional) | Core collaborator | Confluence editor on internal desks only (no client spaces) |
| 3 | Service | `cth-automation@cleantechhub.net` | n8n on VPS: create/update Jira issues, Confluence pages, no delete on client spaces |
| 4 | Service | `cth-integration@cleantechhub.net` | Atlassian remote MCP / OAuth for Rovo connectors (Slack, Gmail read **via** n8n, not raw inbox) |
| 5 | Service | `cth-ops-receipt@cleantechhub.net` | Doctor_Bot + Health workbench: post to `CTHOPS` only |
| 6–25 | Humans (as needed) | Fellows, partners, clients | **Client users:** grant view/comment **only** on their desk space via `cth-client-{slug}` groups — still counts toward 25 |

**OAuth / tokens:** stored only in Infisical project `cth-agents` (paths referenced in tickets, never in git). Gideon completes browser OAuth for Atlassian, Gmail, Slack; Control Tower · Infra writes vault references after GO.

**Rovo / AI usage:** keep agents scoped per desk; fleet-wide search runs only under Gideon's user or `cth-integration@` with read scopes — avoids billing surprises after 3 Dec 2026.

---

## 3. Per-product mapping rules

### 3.1 Jira

**Project templates**

| Template | Key | Used for |
| :--- | :--- | :--- |
| `CTH Desk (Team-managed)` | per desk | Tier 1 / 1b desks: Epic = workstream, Story = ticket, Task = workbench action, Sub-task = Hands receipt |
| `CTH Control Plane` | `CTHORCH` | Orchestrator routing, HITL queue, fleet KPIs |
| `CTH Operations` | `CTHOPS` | Control Tower, Doctor_Bot, VPS/cron health (revive dead token) |
| `CTH Hands Pool` | `CTHHANDS` | Tier 4 executions: every issue labels `bot_id`, `desk_id`, `bc-id` |
| `CTH Capabilities` | `CTHCAP` | Tier 3 thin wrappers |

**Workbench mapping:** Jira **Component** `WB-{8-char-id}` on parent desk project; default board filter `component = WB-…`.

**Issue fields (all templates):** `bot_id`, `desk_id`, `tier`, `harness_lane`, `hitl_required` (checkbox), `infisical_secret_ref` (text, ref name only).

**Naming:** `KEY` = `CTH` + 4-letter slug (collision suffix from registry id). Full table: `space-map.csv`.

### 3.2 Confluence

**One space per desk project** (same key). Template: **CTH Desk Home**

- Overview (purpose, parent Orchestrator link)
- **Runbook** (desk protocol excerpt)
- **Bot registry strip** (table: workbench/capability children)
- **HITL log** (manual + macro listing open Jira `hitl_required`)
- **Loom embed** macro for latest desk standup

**Fleet hub:** space `CTHORCH` · home = Orchestrator dashboard (mirrors Jira gadgets + embedded Rovo search).

**Client isolation:** spaces `CTH*` with `strict` flag use **CTH Client Restricted** permission scheme — no space-wide `confluence-users`; only `gideon-admins` + `client-{desk-id}`.

### 3.3 Loom

Single team library **CTH Fleet** with path convention `/Fleet/T{tier}/{bot_id}/{slug}/` (see CSV). Desk recorders use Gideon's seat; automations store **links** on Confluence, not bots uploading video.

### 3.4 Rovo

Not one Rovo "user" per bot. Configure **Rovo agents / knowledge scopes** per desk:

- **Scope id:** `scope:cth-fleet/{type}/{id8}` (CSV column `rovo_agent_scope`)
- **Connectors:** Jira + Confluence (same desk), Slack (channel allowlist via n8n ingest), Gmail (**metadata only** via Inbox desk — no full mailbox sync to Atlassian), Granola/Read AI meeting notes (action items → Jira)

**Orchestrator agent `rovo-orchestrator-fleet`:** federated search across **non-client** spaces + aggregated gadgets; client desks excluded unless ticket names `client_visible: true`.

---

## 4. Permission model and client isolation (28 strict desks)

| Scheme | Applies to | Browse | Create | Admin |
| :--- | :--- | :--- | :--- | :--- |
| `CTH-Internal-Desk` | tier 1a internal desks | Gideon + automation service | Desk editors group | Gideon only |
| `CTH-Client-Isolated` | `isolation_flag=strict` (28) | Gideon + named client group | Gideon + automation (create only in that project) | Gideon only |
| `CTH-Ops` | `CTHOPS`, `CTHHANDS` | Gideon + ops service | automation | Gideon |
| `CTH-Fleet-Read` | `CTHORCH` dashboard sources | all internal seats | Gideon | Gideon |

**Cross-desk leak prevention:** separate Jira projects **and** Confluence spaces per client desk; automation account uses **project-scoped** API tokens; n8n workflows duplicated per client only where needed (pilot uses shared workflow with `desk_id` parameter).

**Parked bot `e68ca92f`:** grey "retired" Loom/Jira components; no triggers (`FLEET_REGISTRY.yaml`).

---

## 5. Inbound flows (Hands, HITL, Slack, Gmail, meetings)

| Source | Path | Lands in Jira | HITL |
| :--- | :--- | :--- | :--- |
| Cloud Hands PR / ticket done | GitHub webhook → n8n on VPS | `CTHHANDS` story + link to desk epic | merge/deploy edges need diamond |
| Desk WorkOrder file | Orchestrator validates → n8n | Parent desk project, label `receipt` | no |
| Slack · Workbench `6b334caf` | Slack events → n8n → Jira REST | `CTHORCH` or routed desk via channel map | before external post |
| Gmail · Workbench `d040c454` | n8n poll / push → issue | Inbox desk `CTHINBO` | before send |
| Meetings desk | Granola/Read AI/calendar → n8n | `CTHMTG` action items | before client email |
| Doctor_Bot VPS | existing cron → **fix token** → `CTHOPS` | Incident/task | auto for GREEN; AMBER/RED → Gideon |
| HITL button (Gideon) | Grok/Cursor widget → n8n status transition | `hitl_required=false` transition | explicit GO |

**Preferred integration order:** (1) n8n on OVH with Infisical creds, (2) Rovo connectors for search, (3) Atlassian remote MCP in Cursor for Hands **read** — writes still via n8n service account after checker.

---

## 6. Orchestrator dashboard (tier 0 · `5dc64ea4`)

**Confluence:** `CTHORCH` home · **Jira dashboard:** `Orchestrator · Fleet Command` (gadgets below). **Rovo:** pinned agent on same page.

| Widget | Type | Source |
| :--- | :--- | :--- |
| Fleet HITL queue | Filter Results | JQL `project = CTHORCH AND hitl_required = true` |
| Open desk epics | Filter Results | `project in (CTH*) AND type = Epic AND status != Done` |
| Hands in flight | Filter Results | `project = CTHHANDS AND status in ("In Progress","In Review")` |
| Ops health | Filter Results | `project = CTHOPS AND labels = doctor-bot` |
| Client desks active | Two Dimensional Stats | `isolation = strict` custom field |
| Email actions waiting | Filter Results | label `gmail-hitl` per desk |
| Slack approvals | Filter Results | label `slack-hitl` |
| Meeting action items | Filter Results | label `meeting-ai` last 7d |
| Token audit | Confluence include | Monday audit page (report-only) |
| Quick search | Rovo embed | `rovo-orchestrator-fleet` |

Data flow detail: `orchestrator-dashboard.mmd`.

---

## 7. Doctor_Bot / `CTHOPS` fold-in

Current state: VPS Doctor_Bot posts to Jira project **CTHOPS** → **404 / dead token** (per ticket brief).

**Design actions (implementation phase, not this PR):**

1. Gideon verifies `CTHOPS` exists or recreates under Team-managed template.
2. Rotate API token → Infisical `cth-agents/prod/atlassian/CTHOPS_API_TOKEN`.
3. n8n workflow `wf-doctor-jira` (see harness wire) transitions: GREEN = comment only; AMBER/RED = issue + link to `CTHORCH` if fleet-impacting.
4. Map Health workbench `fbc6f772` and Engine Room `85949e8a` as **components** on `CTHOPS`, not separate projects.

---

## 8. Phased rollout

| Phase | Scope | Exit criteria |
| :--- | :--- | :--- |
| **P0** | Gideon SSO + Infisical paths + revive `CTHOPS` | Doctor_Bot GREEN posts test issue (then delete) |
| **P1 Pilot** | Orchestrator `CTHORCH`, Control Tower `CTHOPS`, **2 client desks** (e.g. Teclogi `27bd8324`, Sustenttia `7ffbe815`) | Dashboard live; isolation spot-check |
| **P2** | All tier 1a internal desks + workbench components | 94-row CSV keys created |
| **P3** | Remaining tier 1b client + grant desks | 28 strict schemes verified |
| **P4** | Rovo connectors (Slack, meeting AI) + usage watch before 3 Dec 2026 | Weekly cost = $0 seats |

**Pilot client desk suggestion:** Teclogi + Sustenttia (active Gmail/Monday/Hands traffic; clear isolation).

---

## 9. What Gideon must do himself

1. Sign in to **cleantechhub.atlassian.net**; confirm Social Impact license and seat count ≤25.
2. Create service accounts (Google Workspace) and invite to Atlassian **without** product admin.
3. Complete OAuth for Atlassian automation; store tokens in **Infisical `cth-agents`** (prod) — names only in tickets.
4. **GO** on pilot project creation (P1) and on any client space visibility.
5. Approve n8n workflow **activation** (not Hands) for Gmail/Slack write paths.
6. Merge this design PR; open implementation tickets per phase.

---

## 10. Risks and mitigations

| Risk | Mitigation |
| :--- | :--- |
| Seat creep above 25 | No bot users; quarterly audit; client guests time-limited |
| Usage billing after 3 Dec 2026 | Scope Rovo; disable org-wide indexing; monitor AI meters |
| Client data bleed | strict scheme + separate projects; automation scoped tokens |
| Dead `CTHOPS` token blocks ops visibility | P0 token rotation; fallback Confluence table until GREEN |
| 94 keys collision / rename pain | CSV uses stable `bot_id`; keys immutable after P1 |
| n8n becomes shadow IT | Control Tower owns workflow catalog in `CTHOPS` |

---

## 11. Seat / cost check (design)

| Item | Count | Cost @ ≤25 seats |
| :--- | ---: | :--- |
| Human admins/editors | ≤5 | $0 |
| Service accounts | 3–4 | $0 |
| Client/partner guests (pilot) | ≤2 | $0 |
| **Headroom** | ≥14 seats | reserve for 2026 fellows |
| Jira projects | 69 | $0 (not seat-based) |
| Rovo / AI usage | minimized | watch after 3 Dec 2026 |

---

## 12. Diagrams

| File | Purpose |
| :--- | :--- |
| `master.mmd` | Desk-level fleet ↔ Atlassian master wiring (four bands) |
| `orchestrator-dashboard.mmd` | Orchestrator dashboard data flow zoom-in |

Rendered: `*.svg`, `*.png` (mermaid-cli, scale 3).

---

## 13. References

- `FLEET_REGISTRY.yaml` · `PROTOCOLS.md`
- `docs/fleet/seven-gaps-2026-11-25.md` (isolation kinds)
- `skills/diagram-design/fixtures/wire/n8n-dataflows-wire.yaml`
- `skills/doctor-bot/SKILL.md`
- `skills/infisical/SKILL.md`
- `HARNESS.md` (HITL inline buttons)