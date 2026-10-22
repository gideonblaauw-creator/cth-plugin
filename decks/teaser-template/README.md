# CleantechHUB gap teaser template

Reusable scroll teaser (CLP26-style) for Datalab GTM gap snapshots. Each company lives in its own folder under `decks/{company}-teaser/` in this repo and is served at **`https://proposals.cleantechhub.net/{company}-teaser/`** (not `decks.cleantechhub.net`).

## Folder layout (per company)

```
decks/{company}-teaser/
  data.json       # all copy, gaps, matches, Nexus blurbs (required)
  brand.logo      # official CleantechHUB logo from cleantechhub.net (e.g. img/cth-logo.png)
  index.html      # shell (copy from teaser-template)
  render.js       # shell (copy from teaser-template)
  img/            # team photos, optional assets
```

## New teaser from cth-nexus sources

1. In **cth-nexus**, open `docs/teasers/{company}/{company}-teaser.md` and `{company}-teaser.json`.
2. Create `decks/{company}-teaser/` and copy the shell:
   ```bash
   cd decks/teaser-template
   ./sync-shell.sh ../{company}-teaser
   ```
3. Copy `decks/celsia-teaser/data.json` as a schema reference, then replace content from the MD/JSON sources only (no invented numbers).
4. Fill **`report_evidence`** on **each gap** (gap sections show verbatim report quotes; the snapshot / transparency frame does not):

   | Field | Source |
   |-------|--------|
   | `quote_es` | Exact Spanish wording from the sustainability report (`evidence_quote` in JSON) |
   | `quote_en` | Faithful English translation (labelled “Translation” in EN mode only) |
   | `pdf_url` | Report PDF base URL (`gri_report_url` or gap `evidence_url` without `#page`) |
   | `page` | PDF page number (`report_page_pdf` in JSON) |

   The page renders quotes in quotation marks and links to `{pdf_url}#page={page}`.

5. **Matches:** copy `why`, `public_quote`, `public_source_url`, stage, and website from `{company}-teaser.json`. Add **`nexus`** entries (short EN/ES descriptions + theme `CE`/`BIO`/`EN`) from Nexus startup portfolio public data.
6. **`ui`:** bilingual strings for hero, snapshot, nav, team, CTA, footer (see Celsia instance).
7. **Team:** reuse `team` block and photos from Air4U proposal (`https://proposals.cleantechhub.net/air4u-sandbox-proposal-v5/`, `art/*.jpg`) unless the ticket says otherwise.
8. **CTA:** set `cta.url` (Google Calendar or other public link).
9. **Canonical:** `render.js` sets `<link rel="canonical">` to `https://proposals.cleantechhub.net/{slug}/` from `meta.slug` in `data.json`.

## Preview locally

`fetch('./data.json')` needs HTTP (not `file://`):

```bash
cd decks/{company}-teaser
python3 -m http.server 8765
```

Open `http://127.0.0.1:8765/`.

## Validate

```bash
python3 -m json.tool decks/{company}-teaser/data.json > /dev/null
```

## Brand / policy

- `noindex,nofollow` on every teaser (no green DRAFT top bar; draft status is in hero copy only).
- Manual de Marca palette; regular font weight only.
- CleantechHUB wordmark is inline SVG in `index.html` (no published official SVG on cleantechhub.net; live pages on proposals.cleantechhub.net use PNG).

## Hosting

Deploy each built folder to the proposals site root, e.g. `https://proposals.cleantechhub.net/celsia-teaser/`. Keep repo paths as `decks/{company}-teaser/`; only the public URL uses the proposals domain.

## First instance

`decks/celsia-teaser/` — Celsia S.A., Wave 1 CSO persona. Public URL: `https://proposals.cleantechhub.net/celsia-teaser/`.
