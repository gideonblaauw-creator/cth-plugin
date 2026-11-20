# QA — Observatorio de la Tierra Datatón (FODESEP frame + EO skin)

**Verdict: Pass** (rebuild 20 Nov 2026 — requires Gideon approval before publish)

- Branch: `cursor/observatorio-tierra-dataton-8f62`
- Starting SHA: `81bc910005832277c6801789726dfdd633e0f145`
- Layout: FODESEP `fp-*` + `assets/deck.css`; EO typography/logos via `assets/eo-skin.css`
- Capture: `review/capture.sh` (committed) — `Reveal.slide(i)`, final fragment state, 1920×1080

## Screenshot hash assertion

```
md5sum review/slide-*.png | awk '{print $1}' | sort -u | wc -l  → 11
```

| Slide | MD5 | Type |
| --- | --- | --- |
| 01 | `cb41ec67b2eda259ceaaf53fab565851` | cover |
| 02 | `e57a4256a5482194cbc71404e5083cf0` | statement |
| 03 | `129102ead8c5a56d9ed2dc3a30d8e925` | title-bullets |
| 04 | `60e88bb8b1263228e068856642aa2bf3` | ecosystem |
| 05 | `b8bf92e763e3a785433719048b07fd9d` | partner-cards |
| 06 | `c974db02ddaed41d1eca05b543df2384` | key-facts |
| 07 | `ed41df7ba92f9144842f70b182b6bd58` | focus-areas (photo) |
| 08 | `9a19e6c0c627b52d5431a5797619438e` | title-bullets |
| 09 | `17ef4cd391e23e1e03ff8d45bc7278f6` | process (photo) |
| 10 | `06b6879a8239a1483c74afa90e92848e` | focus-areas |
| 11 | `2388eb66f206ddd4a29ef74a59e846ca` | closing |

Contact sheet: `review/contact-sheet.png` (11 distinct tiles; visually verified).

FODESEP type compares: `review/refs/compare-*.png` (read-only live layer under `/tmp/fodesep`).

## WCAG AA contrast (sampled)

| Element | Foreground | Background | Ratio (approx.) | Pass |
| --- | --- | --- | --- | --- |
| Cover title | `#FFFFFF` | `#0C498A` scrim ~88% | 8.5:1 | Yes |
| Cover tagline | `#9DC384` | scrim | 5.2:1 | Yes |
| Statement quote | `#FFFFFF` | scrim | 8.5:1 | Yes |
| Close tagline | `#9DC384` | scrim | 5.2:1 | Yes |
| Slide 9 phase body | `#0C498A` | `#FFFFFF` card | 8.6:1 | Yes |
| White-slide card body | `#0C498A` | `#FFFFFF` | 8.6:1 | Yes |

## Tooling

- `tools/reveal/build.sh observatorio-tierra-dataton` → PDF **11 pages**
- `tools/reveal/lint.sh observatorio-tierra-dataton` → **lint OK** (requires `pypdf` in environment)
- `tools/reveal/outline.sh …/deck.yaml --validate-only` → **deck.yaml OK**

## Content gates

- No Confidencial / Confidential footer
- "Recortar con Alejandro" only in speaker notes (slides 5–6), not on canvas
- Official logo PNGs from brand-book v3 cover (not text-SVG cobrand)
- Tagline: **Observa. Actúa. Transforma.** (sentence case)

## Per-slide visual pass

| # | Pass | Notes |
| --- | --- | --- |
| 01–11 | Yes | Verified from `review/slide-*.png`; slide 9 roadmap body readable (navy on white) |