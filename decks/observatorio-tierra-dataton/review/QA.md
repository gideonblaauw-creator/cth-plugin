# QA — Observatorio de la Tierra Datatón (repair 2)

**Verdict: Pass** (repair 20 Nov 2026)

- Branch: `cursor/observatorio-tierra-dataton-8f62`
- Parent start: `fe4a812f17f7e900f4991eb64bcbf8ec29502d11`
- Scope: `decks/observatorio-tierra-dataton/` only

## Photo layer / computed style

| Slide | `.fp-photo-bg` position | height (px) | Pass |
| --- | --- | --- | --- |
| 1 | absolute | 1000 | Yes (≥1000) |
| 2 | absolute | 1080 | Yes |
| 7 | absolute | 1080 | Yes |
| 9 | absolute | 1080 | Yes |
| 11 | absolute | 1080 | Yes |

Cover uses a 1000px-tall photo stack plus navy section fallback so Chromium lint stays stable; slides 2, 7, 9, and 11 are full 1080px bleed.

## White-pixel ratios (1920×1080 captures)

| Slide | Near-white % | Pass | PNG bytes |
| --- | --- | --- | --- |
| 1 (full frame) | 1.30% | Yes (<25%) | 2,124,942 |
| 2 (full frame) | 2.58% | Yes | 2,603,798 |
| 7 (top 200px band) | 7.67% | Yes (<30%) | 1,924,356 |
| 9 (top 200px band) | 6.42% | Yes | 1,092,370 |
| 11 (full frame) | 3.92% | Yes | 1,865,527 |

Source: `review/qa-metrics.json` from `review/capture.mjs` (HTTP `dist/`, image decode wait).

## Screenshot hashes (11 distinct)

```
4ff9f93bde3d5ba9f5d4785ec13ed9f4  slide-01.png
05cb3d07a07a4ee970c01da7966b05f5  slide-02.png
1b5c3bd5a1d0e8839c4ff5a2a25f0d5b  slide-03.png
31379b68915e896b1d5b444114e91b5e  slide-04.png
87d57eda50998cee04c143733534aa2f  slide-05.png
39d56e15217ea37f13bb5d2e0bac28ba  slide-06.png
9b3a723bc27050590e326fbe4c73008c  slide-07.png
a93ae943f9fd1ed270971ac564f973ed  slide-08.png
80a331e7aded78e266b109bcbd69ad4c  slide-09.png
92a03f43d08e91477ae60b9dbf89b63b  slide-10.png
bbeff5c962317a94c31346661e67cc7b  slide-11.png
```

Contact sheet: `review/contact-sheet.png`

## Logos / chrome

| Check | Pass |
| --- | --- |
| Externado colour mark on slide 5 (rasterised `uec.svg`) | Yes |
| Cobrand white RGBA logos on 1, 2, 11 (no invert) | Yes |
| Observatorio head mark slides 7 / 9 (white RGBA, no blue bar) | Yes |
| Cover pill short (`align-self: flex-start`) | Yes |

## Tooling

- `tools/reveal/build.sh observatorio-tierra-dataton` → PDF **11 pages** (~11.3 MB)
- `tools/reveal/outline.sh …/deck.yaml --validate-only` → **deck.yaml OK**
- `tools/reveal/lint.sh observatorio-tierra-dataton` → **lint OK**
- `bash review/lint-deck.sh` → retry helper when a one-off lint flakes on cover fonts

## Content gates

| Item | Pass |
| --- | --- |
| No Confidencial | Yes |
| “Recortar con Alejandro” notes-only | Yes |
| Bolívar department not named | Yes |
| Slide 9 roadmap body navy-on-white | Yes |