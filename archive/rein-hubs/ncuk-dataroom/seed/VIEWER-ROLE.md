# Docmost viewer — read-only access

## Goal

External reviewers (e.g. Laurence) can read **Energy**, **Health**, and **Education** only. They must not edit pages or spaces.

## Steps (Docmost admin UI)

1. Sign in as workspace admin.
2. Open **Settings → Users** (or **Members**).
3. Invite **`ncuk-viewer@cleantechhub.net`** (or your chosen viewer email).
4. Assign the **lowest privilege role** available (Member/Guest — not Admin).
5. For each NCUK space (Energy, Health, Education):
   - Open space **Settings → Members** (or **Permissions**).
   - Add the viewer with **read-only** / **viewer** access if the role exists.
   - If only space-level roles exist, use **Viewer** or restrict write via group policy per Docmost version.
6. **Do not** add the viewer to other spaces.
7. Set password from Infisical key **`NCUK_DOCMOST_VIEWER_PASSWORD`** (communicate only after Gideon HITL on REIN outbound).

## Edge auth

Reviewers also use Caddy Basic Auth user **`rein`** + **`NCUK_DATAROOM_BASIC_AUTH_PASSWORD`**. That is separate from Docmost login; both may apply.

## Verification

1. Sign in as viewer (or use a private window with viewer session).
2. Confirm edit controls are absent or edits fail.
3. Confirm other workspace spaces are not visible.
