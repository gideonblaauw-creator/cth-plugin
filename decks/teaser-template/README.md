# CleantechHUB gap teaser template

Reusable scroll teaser (CLP26-style) for Datalab GTM gap snapshots. Each company lives in its own folder under `decks/{company}-teaser/`.

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
4. Fill **`report_evidence`** on the snapshot and on **each gap**:

   | Field | Source |
   |-------|--------|
   | `quote_es` | Exact Spanish wording from the sustainability report (`evidence_quote` in JSON) |
   | `quote_en` | Faithful English translation (labelled “Translation” in EN mode only) |
   | `pdf_url` | Report PDF base URL (`gri_report_url` or gap `evidence_url` without `#page`) |
   | `page` | PDF page number (`report_page_pdf` in JSON) |

   The page renders quotes in quotation marks and links to `{pdf_url}#page={page}`.

5. **Matches:** copy `why`, `public_quote`, `public_source_url`, stage, and website from `{company}-teaser.json`. Add **`nexus`** entries (short EN/ES descriptions + theme `CE`/`BIO`/`EN`) from Nexus startup portfolio public data.
6. **`ui`:** bilingual strings for hero, snapshot, nav, team, CTA, footer (see Celsia instance).
7. **Team:** reuse `team` block and photos from Air4U proposal (`decks.cleantechhub.net/air4u-sandbox-proposal-v5/`, `art/*.jpg`) unless the ticket says otherwise.
8. **CTA:** set `cta.url` (Google Calendar or other public link).

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

- Sticky **DRAFT · GTM hypothesis · not a CSO delivery** bar and `noindex,nofollow`.
- Manual de Marca palette; regular font weight only.
- CleantechHUB wordmark is inline SVG in `index.html` (no published official SVG on cleantechhub.net; live decks use PNG).

## First instance

`decks/celsia-teaser/` — Celsia S.A., Wave 1 CSO persona.
