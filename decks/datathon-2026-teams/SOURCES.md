# Sources — datathon-2026-teams

Deck for Datatón pilot (24 Nov 2026). Spanish primary; English toggle. No invented figures.

## Background photos

**Canva-cleaned Air4U photos** (1080×1350 PNG, `/opt/cth-decks/.../canva-out/g*-canva.png`). Full-bleed **16:9** crops under `assets/photos/canva-g*-crop.jpg` (`scripts/crop-canva-air4u.py`, 1920px JPEG). Photo slides use a **light scrim** in `assets/deck.css` (~50% flat navy + L→R text gradient). People/logos allowed on this deck. **One unique crop per photo slide.**

| Slide | g-source | Crop box (x0,y0,x1,y1) | Asset |
|-------|----------|-------------------------|-------|
| 1 cover | g3 Medellín | (0,500,1080,1108) | canva-g3-crop.jpg |
| 2 statement | g4 gloved hand | (0,380,1080,988) | canva-g4-crop.jpg |
| 3–5 | white | — | — |
| 6 statement | g2 technician | (0,140,1080,748) | canva-g2-crop.jpg |
| 7 showcase | g6 AHU | (0,220,1080,828) | canva-g6-crop.jpg |
| 8 showcase | g7 nurse | (0,300,1080,908) | canva-g7-crop.jpg |
| 9–11 living-lab L1–L3 | white (map on L1) | — | — |
| 12–14 Air4U examples | navy | — | — |
| 15 dashboard-template | white | — | — |

Legacy social JPEG crops (`air4u-*-crop.jpg`) retained in repo but unused after this pass.

## Content

| Claim / slide | Reader-facing source on slide |
|---------------|-------------------------------|
| Method, funnel, agenda | Metodología Datatón CTH v0.3 (21 nov 2026); Paquete de equipo Datatón (ES) |
| Air4U clinic example | Paquete de equipo Datatón (ES) |
| Hoja 4 template (slide 12) | Native HTML fp-h4 (team pack template); **Hoja 4b** in pack only (caption) |
| Living lab L1 map | `assets/datalab-living-lab-l1-map-cropped.png` (cropped from skeleton-v2 render; full UI in `datalab-living-lab-l1-map.png`); hourly PM from `data/lab-data-snapshot.mjs` (4 Oct 2026 09:00 COT) |
| Living lab L2/L3 | `data/lab-data-snapshot.mjs` (EXAMPLE slots); Clínica Colombia framing from taller Air4U (synthetic, no numeric series in deck) |
| Heatmap D1 | `air4u-drl-heatmap-ladder-confirmed.png` |
| Finals 16:00 | Team pack agenda |
| Contact | info@cleantechhub.net |

## Figures / screenshots

| Asset | Source |
|-------|--------|
| Air4U_BMC_preview*.png | Bundle bmc previews |
| method-flow.svg | Hands illustration from methodology (no numeric claims) |