# CleantechHUB Quarto tool

Reusable **Quarto** toolkit for data-heavy static sites: Presentations demos, Datalab reports, and Living Lab dashboards. Output is a static `_site/` folder — **no deploy from this repo**; Infra hosts after Gideon GO.

## When to use Quarto vs Reveal Tool

| Need | Tool |
|------|------|
| Multi-page **reports**, notebooks, CSV-driven charts, frozen reproducible renders, dashboards | **Quarto** (`tools/quarto/`) |
| Slide **decks**, stage/scroll HTML presentations, PDF deck protocol | **Reveal Tool** (`tools/reveal/`) — `skills/reveal-deck-build/SKILL.md` |
| Existing Datalab **JS app** at `/app/` | Keep the app; add Quarto **next to** it for published reports |

Quarto does **not** replace the Datalab application or existing demo decks. Hands commit **source** under `tools/quarto/sites/<slug>/` on `github-pr` lane; render artifacts (`_site/`, `_freeze/`, `.quarto/`) stay gitignored.

## Prerequisites

- Linux amd64 (`.deb` installer pinned in `versions.json`)
- `jq`, `curl`, `python3`, **`python3-venv`** (Debian/Ubuntu: `apt install python3-venv`)
- **`sudo`** — `install-quarto.sh` runs **`sudo dpkg -i`** on first Quarto install
- Network to download Quarto release and Python wheels on first `build.sh`

## Quick start

```bash
cd tools/quarto
chmod +x install-quarto.sh setup-python.sh new-site.sh build.sh

./new-site.sh my-demo demo en
./build.sh my-demo
# static output: sites/my-demo/_site/  (not committed)
```

Templates: `demo` | `datalab` | `living-lab` · Language: `en` (default) or `es`.

## Pin versions

| Component | Location |
|-----------|------|
| Quarto CLI `1.6.40` + SHA-256 | `versions.json`, `install-quarto.sh` |
| Python libs (pandas, plotly, jupyter, itables, kaleido) | `requirements.txt`, `setup-python.sh` |

## Theme

Self-contained CleantechHUB branding in `theme/` (`cleantechhub.scss`, `_brand.yml`). Not shared with `tools/reveal/` (merge in a later small PR if needed).

## Access vs search hints (default)

- **`noindex, nofollow`** (via `theme/includes/robots-noindex.html` + `_metadata.yml`) only **discourages search indexing**. It is **not** access control.
- **Real gating** is **Caddy + oauth2-proxy** on the OVH host. Infra configures that **after Gideon GO per slug**. Until then, do not publish client-facing URLs.

See `skills/quarto-site-build/SKILL.md`.

## Hands workflow

Desk tickets use `skills/quarto-site-build/SKILL.md` (slug, template, data paths, audience, language). Cloud Hands runs `new-site.sh` then `build.sh`; commit `sites/<slug>/` source to the PR; attach render log and screenshots of `_site/`.

## Sample data

All template CSV/JSON files are labelled **EXAMPLE DATA** / **DATOS DE EJEMPLO**. Never commit client exports or secrets.
