# Seed structure — NCUK Docmost workspace

Apply after first Docmost setup on the VPS. **Placeholders only** — paste exports from Google Drive; invent no metrics or deck text.

## Spaces (create in Docmost)

| Space | Slug suggestion | Drive source folder |
|-------|-----------------|---------------------|
| Energy | `energy` | https://drive.google.com/drive/folders/1IlkGkKEpv8VTQgGc3LsnNo9EMoj5CwFV |
| Health | `health` | https://drive.google.com/drive/folders/1SJQQ6FQ4daAxwNi1h5GY4RrKwtt6nU2w |
| Education | `education` | https://drive.google.com/drive/folders/1ahC3o8hAO8GaI2g-StWTze-JODQ8Wafq |

**Root Drive folder (all themes):** https://drive.google.com/drive/folders/1SbHKtgtLRVDmVp4_wofcRDYqZRVpzzO9

## Guided start page

1. Create a page **“Start here for NCUK”** (workspace root or pinned page).
2. Use body from `seed/guided-start-page.md`.
3. Link each theme in order: Energy → Health → Education.

## Per-theme home pages

Each space gets one home page:

- `seed/spaces/energy/home.md`
- `seed/spaces/health/home.md`
- `seed/spaces/education/home.md`

Add **Last updated:** `[DATE]` when content is exported.

## Viewer role (read-only)

Follow `seed/VIEWER-ROLE.md`. Suggested account: `ncuk-viewer@cleantechhub.net` with password from Infisical `NCUK_DOCMOST_VIEWER_PASSWORD`.

Disable public self-registration in Docmost settings.

## Content rules

- Prefer **PDF/PNG snapshots** for frozen Manchester numbers.
- Live Google Sheets only if Gideon accepts drift risk.
- Do not embed Drive URLs with sharing tokens in git; operator paste in Docmost UI.
