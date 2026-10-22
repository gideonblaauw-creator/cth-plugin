# PLAN — NCUK REIN data room (research only)

Date of this plan: 22 Oct 2026.  
Requester: Gideon Blaauw (REIN Hubs Desk).  
Consumer: Laurence (Pvblic), guided read-only room by **Wed 29 Oct 2026** for NCUK budget work ahead of **Thu 30 Oct 2026** (Manchester).  
Scope of this file: **research and plan only**. No build. No deploy. No DNS change. No Infisical write.

## Done when (this ticket)

1. This plan lists four to six Notion-like OSS options with repo links and licences.  
2. This plan recommends one primary stack and one fallback.  
3. This plan names the host, DNS ask, and auth design (secrets in Infisical `cth-agents` only).  
4. This plan gives a step list in ASD-STE100 style (cap 60 steps) with pushback and risks.  
5. Gideon approves the plan before any Hands build ticket.

## Goal

Give Laurence a **theme-indexed** REIN data room at path **`/ncuk`**: energy, health, education; decks, metrics, and cohort data by sector; sources live in a Google Drive folder; **Notion-like** reading experience; **login** for external reviewers.

## Constraints (repo facts)

- Long-running CTH services deploy on the **existing OVH VPS** with **Docker** and **Caddy** (auto-TLS). Do not spin up a new host (`CLAUDE.md`, `skills/bookstack/SKILL.md`).  
- Public CTH sites today: `cleantechhub.net`, `wiki.cleantechhub.net` (BookStack), `nexus.cleantechhub.net`. Deck work uses `decks.cleantechhub.net` in other plans — not deployed in those tickets.  
- Secrets: Infisical project **`cth-agents`** only; never commit passwords (`skills/infisical/SKILL.md`).  
- REIN Desk: no outbound to Pvblic until Gideon clears HOLD; **never cite REIN Hubs dollar amounts** (`skills/rein-hubs-comms/SKILL.md`).  
- VPS operational files stay in `/opt/claude-files`; do not clone them into this repo.

## Recommendation (executive)

| Role | Choice |
|------|--------|
| **Primary** | **[Docmost](https://github.com/docmost/docmost)** (AGPL-3.0), new subdomain `dataroom.cleantechhub.net`, app path `/ncuk` via Caddy reverse proxy |
| **Fallback** | **Static [Docusaurus](https://github.com/facebook/docusaurus)** (MIT) site at the same host and path, protected by **Caddy HTTP Basic Auth** only |

### Why Docmost (primary)

1. **Notion-like UI** is the product goal; Docmost targets that use case openly ([Docmost docs](https://docmost.com/docs/)).  
2. **Licence**: AGPL-3.0 on the open-source edition ([LICENSE](https://github.com/docmost/docmost/blob/main/LICENSE)). Internal CTH use on owned VPS is a normal self-host case; confirm AGPL obligations with Legal if you modify and expose the app.  
3. **Auth**: Email and password on the community edition ([authentication docs](https://docmost.com/docs/user-guide/authentication)). SSO is enterprise-only.  
4. **Guided read-only**: Use three **spaces** (Energy, Health, Education) and a **viewer** account with read-only space access; share one landing page as the tour start.  
5. **Google Drive**: No native Drive mount in OSS docs; use **published links**, **iframe embeds** where Drive allows, or **exported PDFs** copied into Docmost for frozen metrics. Drive folder remains SoT; Docmost is the guided shell.  
6. **Docker on VPS**: Official compose uses Docmost + PostgreSQL + Redis ([installation](https://docmost.com/docs/installation)). Fits existing Docker + Caddy pattern.  
7. **Timeline**: Compose and TLS are ~**half a day** for Infra; **2–4 days** for content and QA if Drive exports start immediately. That fits **29 Oct** if build starts **23–24 Oct**.

### Why Docusaurus + Basic Auth (fallback)

1. Fastest **read-only** path: MDX pages per theme, sidebar = guided tour, no extra DB.  
2. **MIT** licence ([Docusaurus repo](https://github.com/facebook/docusaurus)).  
3. **Auth** matches Gideon’s **`rein`** gate: Caddy `basicauth` with password from Infisical — no OAuth requirement.  
4. **Trade-off**: Weaker Notion feel; more manual export from Drive to git or static assets.

### Why not the others (summary)

| Option | Repo | Licence | Blocker for this job |
|--------|------|---------|----------------------|
| Outline | [outline/outline](https://github.com/outline/outline) | [BSL 1.1](https://github.com/outline/outline) (not OSI “open source”) | No native email/password; needs Google/OIDC/Slack ([requirements](https://docs.getoutline.com/s/hosting/doc/requirements-ULdYnwi4wG)) |
| AppFlowy Cloud self-host | [AppFlowy-SelfHost-Commercial](https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial) | Commercial self-host licence | Heavy stack; free tier **one seat**; desktop client is AGPL but server path is commercial ([AppFlowy repo](https://github.com/AppFlowy-IO/AppFlowy) is AGPL for client only) |
| AFFiNE self-host | [toeverything/AFFiNE](https://github.com/toeverything/AFFiNE) | MIT (client) + [EE licence on backend/server](https://github.com/toeverything/AFFiNE/blob/canary/packages/backend/server/LICENSE) | Large compose; licence mix; OIDC for SSO; slower content ops |
| BookStack (existing) | [BookStackApp/BookStack](https://github.com/BookStackApp/BookStack) | MIT | Already at `wiki.cleantechhub.net`; not Notion-like; **NCUK donor pack must not mix with public wiki** |
| Wiki.js | [requarks/wiki](https://github.com/requarks/wiki) (stable **2.x**: [wiki-v2](https://github.com/requarks/wiki-v2)) | AGPL-3.0 | Solid wiki, not Notion-like; extra PG instance; less “guided doc” feel for Laurence |
| Nextra (static) | [shuding/nextra](https://github.com/shuding/nextra) | MIT | Good Notion-*ish* docs theme; needs Node build pipeline; similar to Docusaurus fallback |

## Host name and DNS (Gideon action)

| Item | Value |
|------|--------|
| **Public URL** | `https://dataroom.cleantechhub.net/ncuk` |
| **Path rule** | `/ncuk` = NCUK REIN room only; leave `/` for a neutral landing or redirect |
| **DNS record** | Type **`A`**, name **`dataroom`** (or **`dataroom.cleantechhub.net`** per registrar UI), target **`<<OVH_VPS_IPV4>>`** (placeholder — Infra fills from VPS) |
| **Optional IPv6** | Type **`AAAA`**, same host, target **`<<OVH_VPS_IPV6>>`** if Caddy serves v6 |
| **TLS** | Caddy on VPS obtains certificate after DNS propagates |

Pushback: Do **not** reuse `wiki.cleantechhub.net` for NCUK. BookStack is the org wiki, not a donor data room.

## Auth design

### Layer 1 — Edge (required for external reviewers)

- **Mechanism**: Caddy **`basicauth`** on `dataroom.cleantechhub.net` (at least on `/ncuk` and sensitive paths).  
- **Username**: `rein` (matches Gideon brief).  
- **Password**: Generate a **random passphrase** (minimum 20 characters; use a password manager). **Do not** use the string `rein` as the password.  
- **Storage**: Infisical project **`cth-agents`**, environment **`prod`** (or Infra-standard env), suggested key name **`NCUK_DATAROOM_BASIC_AUTH_PASSWORD`**. Optional companion **`NCUK_DATAROOM_BASIC_AUTH_USER`** = `rein`.  
- **Runtime**: VPS Caddy reads a **hashed** secret from env file populated by Infisical sync — **never** in git. Use Caddy-compatible bcrypt hash.  
- **Rotation**: Rotate in Infisical; redeploy Caddy env; send Laurence the new secret via an approved channel after Gideon HITL.

### Layer 2 — Application (Docmost primary)

- **Admin**: CTH operator account (MFA if available).  
- **Viewer**: e.g. `ncuk-viewer@cleantechhub.net` with **read-only** rights on the three NCUK spaces only.  
- **Viewer password**: Separate Infisical key, e.g. **`NCUK_DOCMOST_VIEWER_PASSWORD`**. Laurence may use edge Basic Auth only; app login is optional second factor.  
- **Do not** create a Docmost account literally named `rein` unless email format is `rein@…` — Basic Auth username is enough at the edge.

### Fallback static site

- Layer 1 only (Caddy Basic Auth). No app login.  
- Optional Cloudflare Access later — **not** in scope for 29 Oct unless Infra already has Zero Trust on the zone.

## Content architecture (themes)

| Space / section | Contents |
|-----------------|----------|
| **Energy** | Decks, sector metrics, cohort tables (export from Drive) |
| **Health** | Same pattern |
| **Education** | Same pattern |
| **Landing `/ncuk`** | Short guide: read order, “last updated”, contact line, link back to Drive folder (view-only link — store URL in Infisical or ticket, not in public repo) |

Use **fixed snapshots** (PDF or PNG) for numbers that must not change during Manchester week. Link live Sheets only if Gideon accepts drift risk.

## OSS comparison matrix

| Product | Repo | Licence | Docker self-host | RAM (estimate) | Simple login | Drive | Guided read-only | Setup vs 29 Oct |
|---------|------|---------|------------------|----------------|--------------|-------|------------------|-----------------|
| **Docmost** | [docmost/docmost](https://github.com/docmost/docmost) | [AGPL-3.0](https://github.com/docmost/docmost/blob/main/LICENSE) | Yes — PG + Redis ([compose](https://github.com/docmost/docmost/blob/main/docker-compose.yml)) | ~1–2 GB stack | Email/password (OSS) | Link/embed/export | Spaces + viewer role | **Medium** — fits if start ≤24 Oct |
| **Outline** | [outline/outline](https://github.com/outline/outline) | [BSL 1.1](https://github.com/outline/outline) | Yes — PG + Redis ([Docker docs](https://docs.getoutline.com/s/hosting/doc/docker-7pfeLP5a8t)) | 512 MB min; 1 GB+ recommended ([requirements](https://docs.getoutline.com/s/hosting/doc/requirements-ULdYnwi4wG)) | OAuth/OIDC only | Embeds | Collections + guest accounts | **Hard** — auth mismatch |
| **AppFlowy Cloud** | [AppFlowy-SelfHost-Commercial](https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial) | Commercial | Yes — many services ([deployment docs](https://docs.appflowy.io/docs/documentation/appflowy-cloud/deployment)) | ~2 GB+ | GoTrue; commercial seats | [Connections guide](https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial) (Google) | Guest editors (limited) | **Hard** — licence + seats + time |
| **AFFiNE** | [toeverything/AFFiNE](https://github.com/toeverything/AFFiNE) | Mixed MIT + [EE server](https://github.com/toeverything/AFFiNE/blob/canary/packages/backend/server/LICENSE) | Docker Compose ([self-host](https://affine.pro/self-host)) | ~2 GB+ | Workspace accounts; OIDC optional | Manual | Permissions per doc | **Hard** — weight + licence |
| **BookStack** | [BookStackApp/BookStack](https://github.com/BookStackApp/BookStack) | MIT | Already on VPS (`wiki.cleantechhub.net`) | Existing MariaDB stack | Local auth | Attachments | Shelf/book tour | **Ill-fit** — wrong surface + commingling |
| **Wiki.js 2.x** | [requarks/wiki-v2](https://github.com/requarks/wiki-v2) | AGPL-3.0 | [Docker](https://docs.requarks.io/en/install/docker) + external PG | ~512 MB–1 GB | Local auth | Link | Sidebar nav | **Medium** — not Notion-like |
| **Docusaurus (static)** | [facebook/docusaurus](https://github.com/facebook/docusaurus) | MIT | Build artifact + Caddy | Minimal runtime | Caddy Basic Auth | Link/export | Sidebar + docs order | **Fast** — best fallback |
| **Nextra (static)** | [shuding/nextra](https://github.com/shuding/nextra) | MIT | Next build + Caddy | Minimal runtime | Caddy Basic Auth | Link/export | Docs theme | **Fast** — alternate fallback |

## Step plan (ASD-STE100)

Use this list for the **follow-on build ticket** after Gideon approves this plan.

1. Confirm Gideon approves Docmost primary and Docusaurus fallback.  
2. Confirm REIN HOLD allows Laurence access credentials.  
3. Confirm Google Drive folder ID and view-only sharing policy.  
4. Confirm which metrics are snapshot vs live links.  
5. Open Infrastructure ticket for VPS capacity check.  
6. Record current free RAM and disk on OVH VPS.  
7. Confirm Docker network name used by Caddy and BookStack.  
8. Choose Docmost compose directory on VPS under `/opt/claude-files/…` (not this git repo).  
9. Generate `APP_SECRET` with `openssl rand -hex 32`.  
10. Generate strong Basic Auth password; store in Infisical `cth-agents`.  
11. Store Docmost viewer and admin passwords in Infisical.  
12. Add DNS **A** record `dataroom` → `<<OVH_VPS_IPV4>>`.  
13. Wait for DNS propagation; verify with `dig`.  
14. Pull Docmost compose from [GitHub](https://github.com/docmost/docmost/blob/main/docker-compose.yml).  
15. Set `APP_URL` to `https://dataroom.cleantechhub.net/ncuk` or root URL per path routing decision.  
16. Pin image tags; do not use unpinned `latest` in production.  
17. Start PostgreSQL and Redis containers.  
18. Start Docmost container.  
19. Run Docmost health check at `/api/health`.  
20. Add Caddy site block for `dataroom.cleantechhub.net`.  
21. Route `/ncuk` to Docmost upstream (strip prefix only if Docmost expects root — test both).  
22. Enable Caddy `basicauth` on `/ncuk`.  
23. Load Basic Auth hash from Infisical-synced env file.  
24. Reload Caddy; verify TLS certificate issues.  
25. Create Docmost workspace admin account.  
26. Create spaces: Energy, Health, Education.  
27. Create landing page “Start here for NCUK”.  
28. Set viewer account to read-only on those spaces.  
29. Export deck PDFs from Drive for each theme.  
30. Upload PDFs or embed Drive links per slide deck.  
31. Export cohort tables to CSV or PDF snapshots.  
32. Paste metrics into Docmost pages or attach files.  
33. Add “Last updated” date on each theme home page.  
34. Disable public self-registration in Docmost.  
35. Test login with `rein` + Infisical password at edge.  
36. Test viewer login inside Docmost if enabled.  
37. Test read-only: viewer cannot edit pages.  
38. Test on mobile width for Laurence review.  
39. Run second reviewer pass (maker ≠ checker).  
40. Prepare one-page email for Laurence with URL and credentials.  
41. Send only after Gideon HITL on REIN outbound.  
42. Log deploy date and version in Infrastructure desk note.  
43. **Fallback trigger**: If step 19 fails by **27 Oct 17:00 UTC**, switch to Docusaurus static path.  
44. Scaffold Docusaurus with docs sidebar order Energy → Health → Education.  
45. Copy approved markdown exports into `docs/` tree.  
46. Build static files on VPS or CI artifact rsync to VPS.  
47. Point Caddy `file_server` or static root at `/ncuk` path.  
48. Keep same Basic Auth block as steps 22–23.  
49. Re-test Laurence journey on fallback site.  
50. Document rollback: stop Docmost containers; keep DNS.  
51. Document backup: PG dump for Docmost; include in VPS backup job.  
52. Do not commit Infisical values or Drive URLs with tokens to git.  
53. Add Doctor_Bot check for TLS expiry on new host (optional).  
54. Schedule post-Manchester teardown or archive decision with Gideon.  
55. Update REIN Desk ticket with “room live” only after step 41.  
56. Archive this PLAN.md outcome in PR linked to build ticket.

## Pushback (say no early)

1. **Outline** for a single shared `rein` password — OAuth setup blows the 29 Oct date.  
2. **AppFlowy** — commercial server licence and seat limits fight a multi-reviewers donor room.  
3. **BookStack on wiki.cleantechhub.net** — wrong brand surface and risk of NCUK data beside public wiki.  
4. **Password = `rein`** — trivial to guess; use random secret in Infisical.  
5. **Live Google Sheets as sole metrics source** during Manchester — drift can embarrass the budget pitch; prefer snapshots.  
6. **New VPS host** — violates CTH infrastructure rule; use OVH.  
7. **Secrets in docker-compose in git** — forbidden; Infisical → VPS env only.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| VPS RAM full after Docmost PG+Redis | Slow or failed deploy | Infra RAM check before compose; fallback to static Docusaurus |
| DNS or TLS delay | Laurence blocked Wed | Add DNS early; use short TTL |
| Drive embed blocked by Google | Broken deck view | Export PDF to Docmost or static `/assets` |
| AGPL compliance question on Docmost | Legal uncertainty | Use unmodified OSS image; Legal review if custom forks |
| REIN HOLD on outbound | Credentials not sent | Gideon explicit go before step 41 |
| Content not ready by 28 Oct | Empty room | Prioritize one theme complete over three partial |
| Basic Auth password shared in email | Leak | One-time channel; rotate after Manchester |
| Path `/ncuk` vs Docmost base URL mismatch | 404 loops | Test Caddy strip_prefix and `APP_URL` together in staging |
| Outline BSL if someone overrides plan | Licence breach | Hold build to Docmost or MIT static only |

## Follow-on ticket sketch (not executed here)

```yaml
desk: REIN Hubs
folder: /opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom/
lane: github-pr  # plan only in cth-plugin; deploy lane B on VPS
model: composer-2.5
done-when: Laurence can open https://dataroom.cleantechhub.net/ncuk with edge login and read three themes.
hitl: Gideon approves credentials send to Laurence.
reviewer: Infrastructure Desk
```

## References

- Docmost: https://github.com/docmost/docmost  
- Docusaurus: https://github.com/facebook/docusaurus  
- Outline: https://github.com/outline/outline  
- AppFlowy (client): https://github.com/AppFlowy-IO/AppFlowy  
- AppFlowy self-host: https://github.com/AppFlowy-IO/AppFlowy-SelfHost-Commercial  
- AFFiNE: https://github.com/toeverything/AFFiNE  
- BookStack: https://github.com/BookStackApp/BookStack  
- Wiki.js stable 2.x: https://github.com/requarks/wiki-v2  
- Nextra: https://github.com/shuding/nextra  
- CTH BookStack ops: `skills/bookstack/SKILL.md`  
- Infisical pointer: `skills/infisical/SKILL.md`

---

**Status:** Draft — Awaiting Gideon's approval before build ticket.
