# n8n-li workflow feature map

**Instance:** [https://n8n-li.cleantechhub.net](https://n8n-li.cleantechhub.net)  
**Review copy (workflow JSON):** `n8n-li/workflows/` in this repo  
**VPS source of truth:** `/opt/n8n-li` (see `n8n-li/docs/WF1-OAUTH-SETUP.md`)

This map is derived from `n8n-li/workflows/*.json`, `n8n-li/docs/WF1-OAUTH-SETUP.md`, `n8n-li/scripts/cm/page-publish.py`, `n8n-li/tests/test_page_publish.py`, and the **Infra deploy record (30 Oct 2026)** for live instance ids and VPS paths. Remaining gaps are marked **TBD**.

---

## Global operations

### Import and activation

- Workflow JSON sets `"active": false`. Import **inactive**. Do not turn **Active** on during import or before Gideon sign-off on a HITL test (`WF1-OAUTH-SETUP.md` §6, §9).
- Even after activation, these WF1 canvases have **no** Schedule, Cron, or Webhook **trigger**; a run starts only from **Manual Trigger** and still stops at **Wait for Gideon** until resume (`test_page_publish.py` `WorkflowContractTests`).

### Secrets (Infisical only)

- Durable OAuth client material lives in Infisical project **cth-agents** (slug `cth-agents-m4-gr`, id `c84fe8b3-d64e-485a-82d7-250dc57a6453`). Environment/folder path: **TBD** (docs expect **prod** at `/`).
- Do not commit secret values. Do not paste them into workflow JSON, this repo, or chat.
- The n8n workflow stores the member access token **inside the n8n credential** after **Connect**; it does not read an access-token env var in the workflow JSON.
- Infisical key names referenced in repo docs (confirm they exist in **prod** before use):

| Key name | Use | Status in repo |
|---|---|---|
| `LINKEDIN_CTH_N8N_CLIENT_ID` | OAuth client id (must match app `78cn54afhparm6`) | Needs confirmation |
| `LINKEDIN_CTH_N8N_CLIENT_SECRET` | OAuth client secret → n8n credential form only | Needs confirmation |
| `LINKEDIN_CTH_N8N_ACCESS_TOKEN` | Candidate durable name for CLI runtime token | Needs confirmation |

CLI adjunct (`page-publish.py`, not an n8n workflow): reads `LINKEDIN_ACCESS_TOKEN`, optional `LINKEDIN_PERSON_ID`, `LINKEDIN_VERSION`, `CM_LIVE`, `N8N_LI_ROOT` from the **environment** only — Infisical mapping for those runtime vars is **TBD** except where operators inject them at deploy time.

### Back up `database.sqlite` before import

Live n8n SQLite (Infra deploy record, 30 Oct 2026):

`/mnt/data/docker/volumes/n8n_li_data/_data/database.sqlite`

Before **any** workflow import or credential edit, copy it beside the live file:

```bash
cp /mnt/data/docker/volumes/n8n_li_data/_data/database.sqlite \
  "/mnt/data/docker/volumes/n8n_li_data/_data/database.sqlite.bak-<tag>-$(date -u +%Y%m%dT%H%M%SZ)"
```

Replace `<tag>` with a short operator label (for example `pre-import-wf1`).

### Docker socket mount

**Open trap (30 Oct 2026):** `/var/run/docker.sock` is mounted in the **n8n-li** container again, despite an earlier removal fix (cloud agent run `bc-3ea6d70c`). Treat this as an open security/ops issue — do not rely on the socket being absent when reviewing blast radius or hardening. Remove or document the mount explicitly on the VPS stack; do not assume the fix stuck.

### How to verify

**Automated (repo):**

```bash
python3 -m unittest discover -s n8n-li/tests -p 'test_*.py'
```

`WorkflowContractTests` asserts both workflow files are inactive, manual+wait gated, no schedule/cron/webhook trigger nodes, credential placeholder id, and no secrets in JSON blobs.

**Manual / operator (from `WF1-OAUTH-SETUP.md` §9):**

1. Credential **Connect** at `https://n8n-li.cleantechhub.net/home/credentials` for `LinkedIn CleantechHUB n8n (78cn54)`.
2. Import both JSON files; confirm **Active** off; rebind LinkedIn HTTP nodes to credential id `KkT9AyzpMcfZD0qv` (`LinkedIn CleantechHUB n8n (78cn54)`). Repo exports still ship placeholder `REPLACE_LINKEDIN_CREDENTIAL_ID`.
3. Canvas check: no Schedule Trigger, Cron, or Webhook trigger; only Manual Trigger.
4. CLI dry-run (no `CM_LIVE`, no token): expect `"status": "dry_run"` and `"linkedin_api": false`.
5. Person CLI dry-run: set bare `LINKEDIN_PERSON_ID`, `--author person`; expect `payload.author` `urn:li:person:<id>` and no HTTP.
6. Do not set `CM_LIVE=1` or activate workflows until Gideon sign-off on one HITL test.

**Healthy n8n execution (after approved resume POST):**

- Success path ends at **Log Published** with `linkedin_api: true`, `event` `wf1_published` (org) or `wf1_personal_published` (personal), and optional `post_urn` from response header `x-restli-id`.
- Rejection path ends at **Log Not Approved** with `linkedin_api: false` and no LinkedIn HTTP call.

---

## WF1 Org Publish — HITL (INACTIVE — DO NOT AUTO-POST)

| Field | Value |
|---|---|
| **File** | `n8n-li/workflows/wf1-org-publish-hitl.json` |
| **n8n workflow id** | `4yGEg8ju8UmjZEwl` (imported inactive, 30 Oct 2026) |
| **Timezone** | `America/Bogota` (`settings.timezone`) |
| **Active in repo export** | `false` |

### Trigger

- **Manual Trigger** only (`n8n-nodes-base.manualTrigger`).
- No schedule, cron, or webhook **workflow** trigger (verified in tests).

### Inputs

Set in **Set Draft Post** before execute (defaults in JSON):

| Field | Default / notes |
|---|---|
| `post_text` | Draft copy; edit before execute |
| `visibility` | `PUBLIC` |
| `reshare_parent` | Empty for text post, or `urn:li:share:` / `urn:li:ugcPost:` URN |
| `organization_urn` | `urn:li:organization:72031636` |
| `publish_target` | `organization_page` |

**Hash Draft** computes SHA-256 (UTF-8, exact `post_text`) as `text_sha256`.

**HITL resume** (POST to this execution’s **Wait for Gideon** resume URL, single-use, webhook resume, no timer):

```json
{
  "decision": "yes",
  "approved_by": "gideon",
  "timestamp": "2026-10-30T16:00:00+00:00",
  "text_sha256": "<hex from Hash Draft>"
}
```

### Outputs

- **Log Published** (approved + LinkedIn success): `event: wf1_published`, `publish_target: organization_page`, `organization_urn`, `post_urn` (from `x-restli-id`), `text_sha256`, `approved_by`, `timestamp`, `http_status`, `linkedin_api: true`.
- **Log Not Approved** (gate fail): `event: wf1_not_approved`, `linkedin_api: false`, partial approval fields.

LinkedIn call: `POST https://api.linkedin.com/rest/posts` with headers `LinkedIn-Version: 202610`, `X-Restli-Protocol-Version: 2.0.0`.

### HITL gates

1. **Wait for Gideon** — execution pauses until resume POST (`webhookId`: `wf1-gideon-yes`).
2. **IF Gideon Approved** — all must pass: `decision` = `yes`, `approved_by` = `gideon`, non-empty timezone-aware `timestamp`, `text_sha256` equals **Hash Draft** output.
3. False branch → **Log Not Approved** (no LinkedIn).
4. **Approval Request** node does not send email/Slack; out-of-band only.

### Infisical keys (cth-agents, prod — names only)

- `LINKEDIN_CTH_N8N_CLIENT_ID` — fill n8n OAuth2 credential (needs confirmation key exists).
- `LINKEDIN_CTH_N8N_CLIENT_SECRET` — fill n8n OAuth2 credential (needs confirmation).

Workflow JSON does not reference Infisical directly.

### Credentials (n8n)

| Name | Type | Notes |
|---|---|---|
| `LinkedIn CleantechHUB n8n (78cn54)` | OAuth2 API (`oAuth2Api`) | Live id `KkT9AyzpMcfZD0qv` (30 Oct 2026). Repo export placeholder: `REPLACE_LINKEDIN_CREDENTIAL_ID`. **Observed scope on credential:** `w_organization_social r_organization_social`. OAuth setup doc lists additional scopes for personal/userinfo — reconcile before personal live tests. |

Do **not** use built-in **LinkedIn OAuth2 API** (`linkedInOAuth2Api`) — it hides scope and defaults to member-only posting.

### Healthy-run signs

- Execution stops at **Wait for Gideon** until resume (expected during HITL).
- After valid resume: **LinkedIn Create Org Post** → **Log Published** with `event: wf1_published`, `linkedin_api: true`.
- LinkedIn create expects HTTP **201** and post URN in `x-restli-id` (documented in `WF1-OAUTH-SETUP.md` §11; n8n node uses full response).
- Repo contract tests pass for this file.

### Known traps

- Import with **Active** on or enabling schedule later — file is intentionally inactive.
- Wrong LinkedIn app: use client id `78cn54afhparm6`, **not** `782xlck` (also forbidden in workflow JSON per tests).
- Rebind credential after import; placeholder id will not work.
- Built-in LinkedIn credential → org posts fail or post as member.
- Resume URL is **single-use**; wrong body → **Log Not Approved**, no LinkedIn.
- Changing `post_text` after **Hash Draft** without matching new hash in resume → gate fails.
- **Build Org Post**: do not send `reshareContext.root`; reshare uses `parent` only.
- **Hash Draft** uses `require('crypto')` — confirm VPS n8n Code node allows it (**TBD** on deploy).
- **LinkedIn-Version** `202610` may sunset; confirm on deploy day (`WF1-OAUTH-SETUP.md` §11).
- OAuth redirect must be exactly `https://n8n-li.cleantechhub.net/rest/oauth2-credential/callback`.
- Back up live `database.sqlite` before import or credential edits (see global section).

---

## WF1 Personal Publish — HITL (INACTIVE — DO NOT AUTO-POST)

| Field | Value |
|---|---|
| **File** | `n8n-li/workflows/wf1-personal-publish-hitl.json` |
| **n8n workflow id** | `GzmvJoo23Zx4LEIh` (imported inactive, 30 Oct 2026) |
| **Timezone** | `America/Bogota` |
| **Active in repo export** | `false` |
| **Live draft (30 Oct 2026)** | **Set Draft Post** still has `urn:li:person:REPLACE_PERSON_ID` on the instance |

### Trigger

- **Manual Trigger** only.
- No schedule, cron, or webhook workflow trigger.

### Inputs

Set in **Set Draft Post**:

| Field | Default / notes |
|---|---|
| `post_text` | Draft copy |
| `visibility` | `PUBLIC` |
| `reshare_parent` | Empty or share/ugcPost URN |
| `person_urn` | `urn:li:person:REPLACE_PERSON_ID` — replace with real URN from userinfo `sub` before live test |
| `publish_target` | `personal_profile` |

Same **HITL resume** JSON as org workflow (`webhookId`: `wf1p-gideon-yes`).

Person id source (operator, not stored in git): `GET https://api.linkedin.com/v2/userinfo` → `sub` → `urn:li:person:<sub>` (`WF1-OAUTH-SETUP.md` §7).

### Outputs

- **Log Published**: `event: wf1_personal_published`, `publish_target: personal_profile`, `person_urn`, `post_urn`, `text_sha256`, `approved_by`, `timestamp`, `http_status`, `linkedin_api: true`.
- **Log Not Approved**: `event: wf1_personal_not_approved`, `linkedin_api: false`.

Same LinkedIn endpoint and headers as org workflow; author in body is **person URN**.

### HITL gates

Same as org workflow: **Wait for Gideon** → **IF Gideon Approved** (decision, approver, timestamp, hash) → build → LinkedIn or **Log Not Approved**.

### Infisical keys (cth-agents, prod — names only)

Same OAuth pair as org workflow:

- `LINKEDIN_CTH_N8N_CLIENT_ID` (needs confirmation)
- `LINKEDIN_CTH_N8N_CLIENT_SECRET` (needs confirmation)

No separate Infisical keys for person id in workflow JSON; person URN is edited in **Set Draft Post**.

### Credentials (n8n)

| Name | Type | Notes |
|---|---|---|
| `LinkedIn CleantechHUB n8n (78cn54)` | OAuth2 API (`oAuth2Api`) | Live id `KkT9AyzpMcfZD0qv`. **Observed scope (30 Oct 2026):** `w_organization_social r_organization_social` only. Personal posting additionally requires LinkedIn Developer Portal products **Sign In with OpenID** and **Share on LinkedIn** enabled on app `78cn54afhparm6`. Node notes scope `w_member_social` for the HTTP post — confirm token scopes and products before any personal live test. |

### Healthy-run signs

- Same wait/resume pattern as org.
- Success: **Log Published** with `event: wf1_personal_published`, `linkedin_api: true`, `person_urn` set to real URN (not `REPLACE_PERSON_ID`).
- Repo `test_personal_workflow_is_inactive_and_uses_person_urn` passes.

### Known traps

- All org-workflow traps apply (inactive import, credential rebind, HITL hash, reshare shape, wrong LinkedIn app).
- Leaving `urn:li:person:REPLACE_PERSON_ID` in production draft (still true on live workflow `GzmvJoo23Zx4LEIh` as of 30 Oct 2026).
- Posting as org vs person: author must be person URN; scope `w_member_social`. Credential may not yet include member/openid scopes — see credential table and LinkedIn products above.
- Do not revive personal Share nodes on old stub workflow — use this inactive workflow (`WF1-OAUTH-SETUP.md` §9).
- Confirm `sub` from userinfo matches `urn:li:person:<id>` on Development Tier app before any personal live test (**TBD** until operator confirms).

---

## Related (not n8n workflows)

| Artifact | Role |
|---|---|
| `n8n-li/scripts/cm/page-publish.py` | CLI publisher with parallel Gideon gate via approval files under `/opt/n8n-li/data/cm/approvals/` |
| `n8n-li/docs/WF1-OAUTH-SETUP.md` | OAuth, import, deploy checklist, rollback |

---

## Document history

| Date | Change |
|---|---|
| 2026-11-02 | Initial feature map (Gideon approved). |
| 2026-11-02 | Live workflow ids, credential id/scope, SQLite backup path, docker.sock trap (Infra deploy record 30 Oct 2026). |
