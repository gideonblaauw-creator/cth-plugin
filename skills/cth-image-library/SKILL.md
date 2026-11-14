---
name: cth-image-library
description: >
  Desk playbook for sourcing CleantechHUB photos from the VPS index via cth-img.
  Use when: deck slides need CTH photos, social post images, proposal figures,
  newsletter hero, client asset photo request, Hands ticket image markers. Do not
  use when: Canva-only stock, client-owned brand assets, catalogue edits, or Lane A
  pull from Drive (use Lane B VPS instead).
license: MIT
metadata:
  version: "1.0.0"
  category: operations
compatibility: Lane B VPS SSH for cth-img query, pull, and clean; Lane A may write tickets and consume query JSON only.
---

# CTH Image Library (desk)

CleantechHUB keeps photos in Google Drive. The VPS holds a **read-only index** only. Desks request images in a Hands ticket; Infrastructure runs `cth-img` on the VPS (Lane B). Cloud Hands on Lane A must not pull files from Drive.

**Production gate:** Do not use this flow in production desk builds until **Gideon approves the catalogue**. Tools may exist earlier for Infra smoke tests only.

## When to use

Any desk that needs **CleantechHUB-owned** images for an asset:

| Desk / asset | Typical use |
|--------------|-------------|
| Presentations | Reveal or HTML deck slides, speaker notes, PDF |
| Socials | LinkedIn, Instagram, Facebook posts |
| Proposals | Client proposal figures and case photos |
| Newsletter | Hero and inline story images |
| Client desks | Co-branded assets when CTH photos are required |

Load `skills/cleantechhub-brand/SKILL.md` for tone; load this skill when the ticket includes an **image request** block. **Deck Hands builds** (reveal and HTML) should read this skill whenever slides need CTH photos.

## Image request in a Hands ticket

Desks paste a short block so Orchestrator and Lane B Hands can query and pull without guessing.

```yaml
images:
  count: 3                    # required — how many distinct photos
  orientation: landscape      # landscape | portrait | either
  purpose: "FODESEP deck — group event photos, 2025 CTH events"
  markers:                    # query hints for cth-img query (all optional but be specific)
    event_or_folder: "CTH events"
    year: 2025
    asset_type: photo
    person_count: group
    free_text: "outdoor stage"
  dest: /tmp/build-<slug>/img # Lane B path outside the library tree
  asset: fodesep-2026-11      # slug for image-use log
  desk: Presentations
```

**Markers** map to `cth-img query` filters: event/folder, year, month, `asset_type`, person count, org/sender domain, source (`drive`/`gmail`), sharing state, and free text on name and caption. State the **count**, **orientation**, and **purpose** in plain language even when markers are sparse.

Include ticket `bc-id` (or ticket id) on the pull step so log rows stay traceable.

## VPS commands (Lane B only)

Tools run on the OVH VPS. Lane A Cloud Hands **cannot** run `pull` or `clean` (no gws / Drive on GitHub runners).

### Query

```bash
cth-img query [filters...] [--include-unverified]
```

- Output: JSON lines with `drive_id`, `webViewLink`, `name`, caption/folder, `asset_type`, `conf`, `needs_review`, `date`, `also_in`.
- Default: omit rows with `needs_review=true`. Use `--include-unverified` only when Infra explicitly allows it.
- Never emit **internal** catalogue rows.

### Pull

```bash
cth-img pull --ids <id1,id2,...> --dest <build-dir> --asset <asset-name> --desk <desk>
```

- Downloads by `drive_id` with **gws read-only** into `--dest` (must be **outside** `/mnt/data/cth-reference-board/photo-library-2026-11-13/`).
- Refuses any id not in `catalogue/manifest.jsonl` or not visible per policy.
- Appends one row per file to `/mnt/data/cth-reference-board/image-use-log/image-use.jsonl` (`ts` UTC and COT, desk, asset, ticket/bc-id, `drive_id`, md5).
- Sets a 24 h auto-clean backstop on the dest folder.

### Clean

```bash
cth-img clean --dest <build-dir>
```

- Deletes pulled files under `--dest`. Run at end of every build. After clean, **only** the image-use log may retain evidence of which `drive_id`s were used.

## Rules (hard)

| Rule | Detail |
|------|--------|
| Index only | No images stored under the VPS library tree `.../photo-library-2026-11-13/`. Pulls are temporary copies in the desk build folder. |
| Read catalogue only | `catalogue/manifest.jsonl`, `catalogue/graph/*`, `catalogue/vocab.md`. **Never** read `internal/manifest-full.jsonl` or other `internal/` paths. |
| Visible rows only | Never query or pull **minor**, **excluded**, or **sensitive** rows. |
| Drive read-only | Pull by `drive_id` only. No permission changes, no deletes, no uploads to Drive from this flow. |
| No credential exposure | Never print, copy, commit, or echo **gws** credentials or tokens. |
| Post-build cleanup | After the asset ships, `cth-img clean --dest`. Do not leave pulled binaries on the VPS except during an active build window. |
| Log retention | Keep `/mnt/data/cth-reference-board/image-use-log/image-use.jsonl` as the audit trail. |

Library root (index): `/mnt/data/cth-reference-board/photo-library-2026-11-13/`.

## Review step

1. **Infrastructure** — Leak check (`check_leaks.py` key sets), smoke query/pull/clean, confirm 0 files remain in dest and 0 images added under the library tree.
2. **Gideon HITL** — Catalogue approval before desks use the flow in production; merge desk skill PR after Infra sign-off.

## Do not use when

| Instead | Path |
|---------|------|
| Stock or designed social creative | `skills/canva/SKILL.md`, `skills/buffer/SKILL.md` |
| Grant figures from sourced docs only | Ticket brief + `diagram-design` |
| Lane A repo-only build with no VPS step | Ticket must assign pull to Lane B; Hands embed only after ids are approved in ticket |

## Related skills

| Skill | When |
|-------|------|
| `reveal-deck-build` | Reveal.js deck scaffold and lint |
| `cleantechhub-brand` | Colours and voice on slides and posts |
| `harness` | Lane A vs Lane B, Hands boundary |
| `doctor-bot` | VPS health before long pull sessions |

## References

- Hands ticket: CTH Image Library desk access flow (Infrastructure owner).
- VPS index: `catalogue/manifest.jsonl` under the photo-library folder above.
- Image-use log: `/mnt/data/cth-reference-board/image-use-log/image-use.jsonl`.
