# WF1 OAuth setup — CleantechHUB organization and personal publish

Internal deploy notes for Infrastructure. Gideon connects the credential. Cloud Hands does not deploy, merge, or post.

**App:** CleantechHUB n8n  
**Client ID:** `78cn54afhparm6`  
**Do not use** the older app whose Client ID starts with `782xlck`.  
**Organization:** `urn:li:organization:72031636`  
**Person:** `urn:li:person:<id>` from userinfo `sub` (see section 7). Do not commit a real member id.  
**Product:** Community Management API, Development Tier (approved)  
**n8n:** `https://n8n-li.cleantechhub.net`  
**Workflow files:** `n8n-li/workflows/wf1-org-publish-hitl.json` and `n8n-li/workflows/wf1-personal-publish-hitl.json` (both inactive on import)

## 1. Secrets (Infisical only)

Durable secrets stay in Infisical. Project **cth-agents** (slug `cth-agents-m4-gr`, id `c84fe8b3-d64e-485a-82d7-250dc57a6453`). Environment and folder path **need confirmation** (expect `prod` at `/`).

| Infisical key | Use | Status |
|---|---|---|
| `LINKEDIN_CTH_N8N_CLIENT_ID` | OAuth client id. Value must match `78cn54afhparm6`. | **Needs confirmation** that this key name exists. |
| `LINKEDIN_CTH_N8N_CLIENT_SECRET` | OAuth client secret. Paste only into the n8n credential form. | **Needs confirmation** that this key name exists. |

Do not commit either value. Do not put them in this repo, in the workflow JSON, or in chat.

The n8n workflow stores the member token inside the n8n credential after Connect. It does not read an access-token env var.

The CLI publisher (`scripts/cm/page-publish.py`) reads `LINKEDIN_ACCESS_TOKEN` from the environment only. A durable Infisical name for that runtime token **needs confirmation** before anyone creates one. Candidate name: `LINKEDIN_CTH_N8N_ACCESS_TOKEN`. Access tokens expire. The client id and client secret are the durable pair.

## 2. Why this is a generic OAuth2 credential

n8n’s built-in credential type **LinkedIn OAuth2 API** (`linkedInOAuth2Api`) hides Scope and defaults it to `w_member_social`. That scope posts as a member, not as the organization Page.

Create a generic **OAuth2 API** credential (`oAuth2Api`) instead. Name it exactly:

`LinkedIn CleantechHUB n8n (78cn54)`

The workflow HTTP node looks up that name. The imported credential id `REPLACE_LINKEDIN_CREDENTIAL_ID` is a placeholder. Rebind it after Connect.

**Needs confirmation** on the VPS n8n version: if a future LinkedIn credential exposes Scope, Infrastructure may switch the node credential type. Until then, use generic OAuth2 API.

## 3. LinkedIn app, before Connect

1. Open the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps).
2. Open **CleantechHUB n8n** (`78cn54afhparm6`), not the `782xlck` app.
3. Confirm Community Management API shows Development Tier approved.
4. Auth tab → Authorized redirect URLs. Add exactly:

`https://n8n-li.cleantechhub.net/rest/oauth2-credential/callback`

5. Confirm the app is tied to organization `72031636`.
6. Confirm Gideon is a super admin on the CleantechHUB Page (`https://www.linkedin.com/company/cleantechhub`). Development Tier tokens only work for members authorized on that app.

## 4. Create the n8n credential

1. Open `https://n8n-li.cleantechhub.net/home/credentials`.
2. **Add credential**. Search **OAuth2 API**. Do not pick **LinkedIn OAuth2 API**.
3. Set **Name** to `LinkedIn CleantechHUB n8n (78cn54)`.
4. Fill the form from Infisical. Do not copy values into git.

| Field | Value |
|---|---|
| Grant Type | Authorization Code |
| Authorization URL | `https://www.linkedin.com/oauth/v2/authorization` |
| Access Token URL | `https://www.linkedin.com/oauth/v2/accessToken` |
| Client ID | Infisical `LINKEDIN_CTH_N8N_CLIENT_ID` |
| Client Secret | Infisical `LINKEDIN_CTH_N8N_CLIENT_SECRET` |
| Scope | `w_organization_social r_organization_social w_member_social openid profile` |
| Authentication | Body (client id and secret in the token request body) |
| Auth URI Query Parameters | empty |

5. The credential screen shows the OAuth Redirect URL. It must equal `https://n8n-li.cleantechhub.net/rest/oauth2-credential/callback`. If n8n shows a different host, stop and fix the n8n public URL before Connect.
6. Save the credential once so the name exists, then Connect.

### Scopes

Request these scopes on the one generic credential. Organization posts and personal-profile posts share it.

- `w_organization_social` — create an organization post
- `r_organization_social` — read organization posts
- `w_member_social` — create a personal-profile post (`urn:li:person:<id>`)
- `openid` — OpenID Connect, required for `GET /v2/userinfo`
- `profile` — returns the member id in the userinfo `sub` field

Scope string, in this order:

`w_organization_social r_organization_social w_member_social openid profile`

The built-in n8n credential type still defaults to `w_member_social` alone and hides the Scope field. That is why this setup uses generic OAuth2 API. Do not drop the organization scopes.

Do not revive personal Share nodes on the old disabled stub. Personal publish is the inactive workflow in section 7.

Older checklist names `w_organization_social_feed` and `r_organization_social_feed` are **not** in the October 2026 Posts API permission table. Do not add them unless the portal lists those exact scope strings. **Needs confirmation.**

## 5. Where Gideon clicks Connect

1. Go to `https://n8n-li.cleantechhub.net/home/credentials`.
2. Open the credential named `LinkedIn CleantechHUB n8n (78cn54)`.
3. On that credential form, click **Connect** (some n8n versions label the same button **Sign in with LinkedIn**).
4. Sign in as the Page super admin. Accept organization scopes for CleantechHUB.
5. Confirm the form shows connected, then click **Save**.

Connect is on the credential form, not on the credentials list.

## 6. Import the workflow (leave it inactive)

1. n8n → Workflows → Import from file → `wf1-org-publish-hitl.json`.
2. Confirm **Active** is off. The file sets `"active": false`. Do not turn it on during import.
3. Open **LinkedIn Create Org Post**. Rebind credentials to `LinkedIn CleantechHUB n8n (78cn54)`.
4. Confirm there is no Schedule Trigger and no Webhook trigger. The only entry is **Manual Trigger**.
5. **Wait for Gideon** resumes on a webhook for that execution only. It has no timer resume. A yes is a POST body:

```json
{
  "decision": "yes",
  "approved_by": "gideon",
  "timestamp": "2026-10-30T16:00:00+00:00",
  "text_sha256": "<hex from the Hash Draft node>"
}
```

`approved_by` must be the lowercase string `gideon`. `text_sha256` must match the draft hash. Anything else goes to **Log Not Approved** and does not call LinkedIn.

The personal-profile workflow uses the same gate. Import it from section 7 and leave it inactive.

## 7. Person id and personal workflow

The personal author is `urn:li:person:<id>`. `<id>` is the OpenID `sub` value, not a full URN.

After Gideon connects the credential (scopes include `openid` and `profile`):

1. Copy the member access token into a shell variable for this one command. Do not write it to git, this doc, or chat.
2. Call userinfo. This is an operator step on a machine that already holds the token. Cloud Hands does not run it.

```bash
curl -sS -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  https://api.linkedin.com/v2/userinfo
```

3. Read only `sub`. Ignore `name`, `email`, and `picture`.
4. The author URN is `urn:li:person:` plus that `sub`.

Illustrative shape only. `REPLACE_PERSON_ID` is not a member:

```json
{ "sub": "REPLACE_PERSON_ID" }
```

URN: `urn:li:person:REPLACE_PERSON_ID`.

**CLI.** `LINKEDIN_PERSON_ID` is the bare id (`REPLACE_PERSON_ID`), not the URN.

- `--author person` reads `LINKEDIN_PERSON_ID`.
- Dry-run never calls LinkedIn. A person dry-run needs `LINKEDIN_PERSON_ID` or it stops with `person_id_required`.
- A live run (`CM_LIVE=1`, `--no-dry-run`, and a passing `--approved-id`) calls `GET https://api.linkedin.com/v2/userinfo` only when `LINKEDIN_PERSON_ID` is unset, then posts with `author` set to `urn:li:person:<sub>`. The same Gideon gate applies. Scope for the post is `w_member_social`.
- `--author org` (the default) ignores `LINKEDIN_PERSON_ID` and keeps `urn:li:organization:72031636`.

**n8n.** Import `wf1-personal-publish-hitl.json` and leave **Active** off.

1. Open **Set Draft Post**. Replace `urn:li:person:REPLACE_PERSON_ID` with the real person URN before any future live test.
2. Open **LinkedIn Create Personal Post**. Rebind credentials to `LinkedIn CleantechHUB n8n (78cn54)`. The node notes scope `w_member_social`.
3. The HITL body is the same as the organization workflow: `decision=yes`, `approved_by=gideon`, a timezone-aware timestamp, and `text_sha256` equal to Hash Draft.
4. Text posts omit `reshareContext`. A reshare sets `reshareContext.parent` only.
5. Do not activate this workflow. Do not turn on a schedule.

## 8. CLI publisher (optional, still gated)

Repo path `n8n-li/scripts/cm/page-publish.py` deploys to `/opt/n8n-li/scripts/cm/page-publish.py`.

Dry-run is the default. It makes no HTTP call:

Organization (default) dry-run:

```bash
python3 /opt/n8n-li/scripts/cm/page-publish.py \
  --text "Exact approved commentary" \
  --author org \
  --dry-run
```

Personal dry-run. No HTTP. `LINKEDIN_PERSON_ID` is the bare id:

```bash
LINKEDIN_PERSON_ID=REPLACE_PERSON_ID \
  python3 /opt/n8n-li/scripts/cm/page-publish.py \
  --text "Exact approved commentary" \
  --author person \
  --dry-run
```

A reshare adds `--reshare-parent urn:li:share:…` or `urn:li:ugcPost:…` for either author. The payload `author` is the organization URN or `urn:li:person:<id>`.

A live run needs all of these:

- `CM_LIVE=1`
- `--no-dry-run`
- `--approved-id <id>`
- `LINKEDIN_ACCESS_TOKEN` in the environment
- an approval file at `/opt/n8n-li/data/cm/approvals/<id>.json` (override the directory with `--approvals-dir` or `N8N_LI_ROOT`)

Approval file:

```json
{
  "id": "apr-example-001",
  "approved_by": "gideon",
  "timestamp": "2026-10-30T16:00:00+00:00",
  "text_sha256": "<sha256 hex of the exact commentary>",
  "reshare_parent": ""
}
```

`text_sha256` is SHA-256 of the exact UTF-8 commentary, with no trim and no escaping. For a reshare, set `reshare_parent` to the same post URN passed as `--reshare-parent`. The live body sends `reshareContext.parent` and does not send `reshareContext.root`. The gate does not change for `--author person`: `approved_by` is `gideon`, the timestamp has a timezone, and the hash is of the exact commentary. A live person run with no `LINKEDIN_PERSON_ID` resolves the id from userinfo `sub` only after that gate passes.

Hash helper:

```bash
python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest())' 'Exact approved commentary'
```

The script refuses a live POST when any gate fails. It never prints the token.

## 9. Infrastructure deploy checklist

Do this on the existing OVH VPS. Do not create a new host. Source of truth for the running stack remains `/opt/n8n-li`. This repo is the review copy.

- [ ] Copy `n8n-li/scripts/cm/page-publish.py` to `/opt/n8n-li/scripts/cm/page-publish.py`.
- [ ] Copy this doc to `/opt/n8n-li/docs/WF1-OAUTH-SETUP.md`.
- [ ] Stop calling `page-publish-stub.py` for WF1. Leave the stub on disk until Gideon says to remove it.
- [ ] Create `/opt/n8n-li/data/cm/approvals/` mode `0700`, owned by the n8n/hands user.
- [ ] Confirm Infisical key names in section 1, then create the OAuth2 credential in section 4.
- [ ] Add the redirect URL on app `78cn54afhparm6` before Connect.
- [ ] Gideon clicks **Connect** at `https://n8n-li.cleantechhub.net/home/credentials` (section 5).
- [ ] Import `wf1-org-publish-hitl.json`. Confirm the workflow is **inactive**.
- [ ] Import `wf1-personal-publish-hitl.json`. Confirm that workflow is **inactive** too.
- [ ] Rebind **LinkedIn Create Org Post** and **LinkedIn Create Personal Post** to `LinkedIn CleantechHUB n8n (78cn54)`.
- [ ] Replace `urn:li:person:REPLACE_PERSON_ID` in the personal draft only when Gideon is ready to test. Do not commit the real id.
- [ ] Confirm each canvas has no Schedule Trigger, no Cron, and no Webhook trigger.
- [ ] Dry-run the CLI with no `CM_LIVE` and no token. Expect `"status": "dry_run"` and `"linkedin_api": false`.
- [ ] Person dry-run: set `LINKEDIN_PERSON_ID` to the bare id and pass `--author person`. Expect `payload.author` `urn:li:person:<id>` and no HTTP call.
- [ ] Do not set `CM_LIVE=1` until Gideon has connected and has signed off one HITL test.
- [ ] Do not activate either workflow until that same sign-off. Activation still has no schedule. A run starts only from Manual Trigger and still waits.
- [ ] Do not enable personal Share nodes on the old stub workflow. Use the inactive personal workflow instead.
- [ ] Hands does not deploy. Gideon merges. Infrastructure copies files and imports. Nobody live-posts from this change.

## 10. Rollback

1. Leave the workflow inactive (toggle Active off if it was turned on).
2. `export CM_LIVE=0` in the hands shell or `.env.hands`.
3. Do not delete the credential unless Gideon asks. A connected credential does not post by itself.
4. Keep using the operator path that was live before this import.

## 11. Open points for Gideon / Infrastructure

- **LinkedIn-Version `202610`.** Docs for October 2026 use version view `li-lms-2026-10`. The header value is `YYYYMM`. Confirm `202610` is still an active version on deploy day. Override the CLI with `LINKEDIN_VERSION`. The workflow header is fixed in the HTTP node until someone edits it. Versions sunset, so this date will go stale.
- **Header spelling.** This stack sends `LinkedIn-Version`. Microsoft Learn writes `Linkedin-Version`. HTTP header names are case-insensitive. Confirm with one dry-run review, not with a surprise live post.
- **`X-Restli-Protocol-Version: 2.0.0`** is required on `/rest/posts`.
- **Response.** A create returns `201` and the new post URN in `x-restli-id` (`urn:li:share:…` or `urn:li:ugcPost:…`). The CLI does not retry a `201`, even if that header is missing, so a retry cannot double-post.
- **Visibility.** Samples use `PUBLIC`. The CLI also accepts `LOGGED_IN` because the old stub did. Confirm organization posts accept `LOGGED_IN` before anyone uses it.
- **Commentary.** The approved string is sent unchanged. LinkedIn “little” text reserves characters for mentions and hashtags. Escaping would change the hashed text. Confirm whether operators must escape before approval.
- **n8n Code node `require('crypto')`.** Hash Draft uses Node’s `crypto`. Confirm the VPS n8n Code node allows that built-in.
- **Generic OAuth2 vs LinkedIn OAuth2 API** and the old `*_feed` scope names, as marked above. The credential scope list is now `w_organization_social r_organization_social w_member_social openid profile`. `openid` and `profile` are required so `GET /v2/userinfo` can return `sub`.
- **Person id.** Confirm `sub` from `/v2/userinfo` is the id inside `urn:li:person:<id>` on this Development Tier app before any personal live test. The CLI stores nothing. Set `LINKEDIN_PERSON_ID` in the runtime environment, not in git.
