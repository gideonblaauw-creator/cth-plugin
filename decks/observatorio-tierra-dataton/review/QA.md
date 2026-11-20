# QA — Observatorio de la Tierra Datatón (repair 4)

**Verdict: Pass** (repair 4, 20 Nov 2026)

- Branch: `cursor/observatorio-tierra-dataton-8f62`
- Parent start: `8d8a1d353c5bd72a666a7de5bd2a9bd3862ad5ac` (repair 3)
- Scope: `decks/observatorio-tierra-dataton/` only
- Draft PR: #163

## Repair 4 — cover motion in present mode

Removed the unconditional `.fp-cover--eo` animation freeze in `assets/eo-skin.css`. Print / export / `prefers-reduced-motion` freezes unchanged (lines 88–93, 127–140).

Orbit drift animation runs on an inner `<g class="fp-orbit-drift">` inside the cover SVG so Chromium lint does not treat rotated SVG bounds as slide overflow.

### Present-mode computed styles (slide 1)

| Element | `animation-name` | Duration |
| --- | --- | --- |
| Cover `.fp-kenburns` | `eo-kenburns` | 28s |
| Cover `.fp-orbit-drift` | `eo-orbit-drift` | 42s |

Source: `review/motion/present-mode-computed.json`

### Cover timed stills (0 / 2.5 / 5 / 8 s)

| Pair (vs t=0) | RMS |
| --- | --- |
| t=2500 ms | 131.89 |
| t=5000 ms | 142.16 |
| t=8000 ms | 143.10 |

Artifacts: `review/motion/cover-t0000ms.png` … `cover-t8000ms.png`, `review/motion/cover-timed-contact.png`

`node review/motion-check.mjs` → **motion-check ok**

## Repair 3 checks (unchanged)

Official EO lockups, white cover meta ≥ 4.5:1, cover photo 1080px height, card contrast, notes-only “Recortar con Alejandro”, no Confidencial, Bolívar not named — still pass.

## Screenshot hashes (11 distinct)

```
f5ab2c313be9ad6c13ba14041259cfdd  slide-01.png
31f710fed791dab0b075b3b586358cc0  slide-02.png
6b34ca0a51bc09c53ad5136e48f1a967  slide-03.png
4e3bd13b92586ef016c32ed2115a5065  slide-04.png
d859ef9ba47db0f8fa80e1d5a4d500a0  slide-05.png
1ced85da8b1a85ec130195a987f371bd  slide-06.png
6327450b670cb3bf483afb403b9d9170  slide-07.png
87caea76748b00cb46d73d6c6ff31ba1  slide-08.png
59ae5274218ff9cfc41568f160f260e3  slide-09.png
ceeaa09f4163ffd2cec613c882ca874f  slide-10.png
6bd65e356471467b13208a1074b4eea7  slide-11.png
```

Contact sheet: `review/contact-sheet.png`

## Tooling

- `tools/reveal/build.sh observatorio-tierra-dataton` → PDF **11 pages**
- `deck.yaml` validate → **OK**
- `tools/reveal/lint.sh observatorio-tierra-dataton` → **lint OK**
- `node review/capture.mjs` → **capture ok**