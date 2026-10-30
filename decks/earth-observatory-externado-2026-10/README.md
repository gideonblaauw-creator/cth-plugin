# Observatorio de la Tierra - deck Externado (30 oct 2026)

Recorrido en español del white paper v1 (oct 2026) para Diego Alejandro Díaz Malagón. **Formato CLP26** (`styles.css`, `eo-extra.css`, `app.js`) más **v7 Dynamic Intelligence Hub** (`eo-hub.css`, `hub.js`): vistas interactivas (MLP, lentes, Datalab, actores, hoja de ruta) y documento WP completo (16 secciones).

**Logo:** `img/logo.png` (CleantechHUB, mismo patrón que decks.cleantechhub.net/cth-clp26/). Sin logo Externado (no autorizado).

## Secciones (16)

0. Portada (`#hero`)  
1. Resumen ejecutivo  
2. Capítulo 1 · perspectiva multinivel  
3. Notas de origen  
4. Propósito y límites  
5. Banda fundadora  
6. Mapa de actores · **comunidades y municipios**  
7. Tipos de actor  
8. Lentes y palancas (pestañas + gráficos WP)  
9. El Datalab (tabla ordenable, slider L1–L3)  
10. El papel (papeles e indicadores; fechas EUDR)  
11. Earth Data Week  
12. REIN  
13. Hoja de ruta (slider de fases)  
14. Perfiles  
15. Reunión 30 oct y cierre (Inspire. Act. Transform.)

## Archivos

- `index.html`, `styles.css` (CLP26), `eo-extra.css`, `eo-hub.css`, `app.js`, `hub.js`, `data/eo-deck.json`
- `data/col-min.geojson`, `data/nexus-co-cities.csv` (25 startups con fuente; único origen de pins)
- `lib/chart.umd.js`, `lib/d3.min.js`
- `review/v7-hero.png`, `review/v7-map.png`, `review/v7-full.png`

## Capturas

Servir el deck por HTTP (p. ej. `python3 -m http.server 8765`), luego `node capture-v7-review.mjs`. Documento WP: `node screenshot-deck.mjs` (Playwright).

## Fuentes

Solo white paper v1 (oct 2026), facts del ticket y MB para agenda de reunión. Huecos marcados **PENDIENTE**.
