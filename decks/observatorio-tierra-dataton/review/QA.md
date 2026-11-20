# QA — Observatorio de la Tierra Datatón (repair 3)

**Verdict: Pass** (repair 20 Nov 2026)

- Branch: `cursor/observatorio-tierra-dataton-8f62`
- Parent start: `d0293a18de3a7c0b87f8cfa2c945b9796cd6981b` (repair 2)
- Scope: `decks/observatorio-tierra-dataton/` only
- Draft PR: #163

## Repair 3 fixes verified

| Check | Result |
| --- | --- |
| Official EO lockup in `observatorio-color.png` / `observatorio-white.png` (not CTH bytes) | Pass |
| Cover cobrand: Externado + CTH + Observatorio (three distinct marks) | Pass |
| Cover `.fp-cover__meta` computed colour | `rgb(255, 255, 255)` (#ffffff), opacity 1 |
| Cover `.fp-photo-bg` height | 1080px, `position: absolute` |
| Bottom 40px strip on cover (not flat navy bar) | ~2.3% navy-like pixels; mean RGB (21, 72, 124) |
| Removed cover `height: 1000px` photo stack cap | Pass |

Logo byte identity: `observatorio-white.png` ≠ `cleantechhub-white.png`; `observatorio-color.png` ≠ `cleantechhub.png`.

## Photo layer / computed style

| Slide | `.fp-photo-bg` position | height (px) | Pass |
| --- | --- | --- | --- |
| 1 | absolute | 1080 | Yes (≥1070) |
| 2 | absolute | 1080 | Yes |
| 7 | absolute | 1080 | Yes |
| 9 | absolute | 1080 | Yes |
| 11 | absolute | 1080 | Yes |

## White-pixel ratios (1920×1080 captures)

| Slide | Near-white % | Pass | PNG bytes |
| --- | --- | --- | --- |
| 1 (full frame) | 1.32% | Yes (<25%) | 2,267,911 |
| 2 (full frame) | 2.59% | Yes | 2,603,933 |
| 7 (top 200px band) | 8.25% | Yes (<30%) | 1,925,460 |
| 9 (top 200px band) | 6.95% | Yes | 1,094,926 |
| 11 (full frame) | 3.93% | Yes | 1,866,968 |

Source: `review/qa-metrics.json` from `review/capture.mjs`.

## Screenshot hashes (11 distinct)

```
76877b088ec98da18a79b2ed23c52d7e  slide-01.png
e2b829488ec84494e2fe8fb0e8f38760  slide-02.png
6b34ca0a51bc09c53ad5136e48f1a967  slide-03.png
4e3bd13b92586ef016c32ed2115a5065  slide-04.png
bcc6ec87ee2292f2c0a6aa29ed2a2304  slide-05.png
1ced85da8b1a85ec130195a987f371bd  slide-06.png
99be39a32637cea8abaa288b58fd3550  slide-07.png
ddd7a668bcd4699f5917513062c13166  slide-08.png
b9ec4470d84b756e750e54c74a85fe04  slide-09.png
ba04ac0e977e5e3ffa07071b3f2a1b62  slide-10.png
0c21189e49e99433bd5ed52a44415852  slide-11.png
```

Contact sheet: `review/contact-sheet.png`

## Tooling

- `tools/reveal/build.sh observatorio-tierra-dataton` → PDF **11 pages**
- `deck.yaml` validate → **OK**
- `tools/reveal/lint.sh observatorio-tierra-dataton` → **lint OK**
- `node review/capture.mjs` → **capture ok**

## Content gates

| Item | Pass |
| --- | --- |
| No Confidencial | Yes |
| “Recortar con Alejandro” notes-only | Yes |
| Bolívar department not named | Yes |
| Slide 9 roadmap body navy-on-white | Yes |