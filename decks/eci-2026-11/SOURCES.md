# Fuentes · `decks/eci-2026-11/`

Material confidencial de trabajo (no publicar en host público).

| Tema | Fuente |
|------|--------|
| Formato scroll tipo CLP26 (secciones, componentes, Chart.js/D3, tokens) | `decks/cth-clp26/FEATURE-MAP.md` (rama `cursor/cth-clp26-feature-map-e04c`) y auditoría A1 en commit `0c39db1` (`docs/deck-audit/A1.json`) |
| Cinco colores y tipografías Manual de Marca | `skills/cleantechhub-brand/brand_dna.yaml` |
| Logo CleantechHUB | `decks/_templates/clp26-rein-shell/logos/cleantechhub.png` (copiado a `img/`) |
| Logo blanco CTH (pie) | Rama `cursor/earth-observatory-externado` → `decks/earth-observatory-externado-2026-10/img/logo-white.png` |
| Logo Escuela (oficial en sitio) | `https://escuelaing.s3.amazonaws.com/production/images/Logotipo-ESCUELA-sin-VM.width-380_R7iE0XU.png` (copia local `img/escuela-colombiana.png`) |
| Logo Datalab opción A | `brand/datalab-logo-2026-11/logo/datalab-logo-light.png` |
| Fotos campus / HELIX (tema institucional) | `escuelaing.s3.amazonaws.com` (banners HELIX-A, laboratorio) |
| Fotografía energía (tema) | Unsplash (licencia) · `img/energy-wind.jpg` |
| Chart.js, D3, topojson | Copiados de `decks/_templates/clp26-rein-shell/lib/` |
| Three.js (UMD, portada 3D) | `three@0.149.0` · `build/three.min.js` desde [jsDelivr](https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js) · copia local `lib/three.min.js` |
| ClimateLaunchpad CLP26 — texto de hitos y cifras globales | Brief verificado por Gideon (nov 2026) |
| ClimateLaunchpad — gráficos (país, embudo, temas) | Únicamente desde `data/startups.json` (102 filas) |

## Datos del explorador (gráficos)

Los tres gráficos de la sección 5 se calculan en tiempo de carga a partir de `data/startups.json`: conteos por `cc`, por `stage` (orden cohort → national → semi → regional → global) y por `theme` (etiquetas en español desde el bloque `themes` del JSON). Sin otros archivos ni splits regionales de postulaciones.
