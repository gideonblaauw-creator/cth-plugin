# Fuentes — demo Promigas

**Verificación doble fuente:** `docs/energy-coop/demo-promigas-fact-check.md`  
**Síntesis FENOGE:** `docs/energy-coop/fenoge-public-data-2026-11.md`

Pantalla 3: **SIMULACIÓN – datos de ejemplo** (estructura CEOF ilustrativa; ~30 % = propuesta CTH).

## Living lab (pantalla Data Lab, `screen-2`)

Archivos locales en `data/`, copiados el 11 nov 2026 desde `https://energiacoop.cleantechhub.net/assets/data/`:

- `ce_priorizadas_high.json` — el mapa usa solo `match_confidence === HIGH` (35 filas). El archivo también trae 28 filas `HIGH (promoted from MEDIUM)`, que no entran al mapa. Coordenadas: precisión `corregimiento`. NIT y matrícula: cruce RUES / datos.gov.co, no validados por MinEnergía (campo `highlight`).
- `irradiacion.json` — kWh/m²/día por departamento. Un departamento ausente queda en gris. Bogotá D.C. no se une a Cundinamarca.
- `colombia-departamentos.geo.json` — contorno departamental.

Cifras del embudo:

- **1.000** — Portafolio, citando a MinEnergía: las 1.000 de mayor puntaje, priorizadas para construcción rápida. https://www.portafolio.co/energia/que-son-las-comunidades-energeticas-y-que-ventajas-tienen-608384
- **221 / 212 / 186** — cruce de registro Energy Coop: 221 emparejadas, 212 con NIT, 186 de confianza media. Esas 186 no están en el archivo de esta pantalla.
- **35** — conteo de filas HIGH en el JSON anterior.

Proxy ZNI, no por comunidad: SSPD, informe sectorial 2022, capitales de San Andrés, Amazonas, Vichada, Vaupés y Guainía fuera del SIN. En las 35 solo aplican Vichada y San Andrés. https://www.superservicios.gov.co/sites/default/files/inline-files/Informe-sectorial-de-la-prestacion-del-servicio-de-energia-2022.pdf

Rendimiento, CAPEX de 90 millones COP, tarifa de sala de 700 COP/kWh, OPEX y la puerta de 8 años son **Datos demo**. No son horas medidas, ni IMPE de la localidad, ni tarifa CREG.
