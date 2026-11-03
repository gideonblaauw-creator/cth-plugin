# Google Solar API coverage — Energy Coop Colombian sites (November 2026)

**Desk:** Energy Coop  
**Date:** 2026-11-03  
**Scope:** `buildingInsights:findClosest`, `dataLayers:get`, and Detected Arrays (`additionalInsights=DETECTED_ARRAYS`) for five reference points.

## Executive summary

Google documents **BASE**-quality Solar API data as generally available for **residential building areas in Colombia** (alongside Brazil, Peru, and Puerto Rico). That tier uses enhanced satellite imagery at 0.25 m/pixel and is distinct from legacy **LOW** satellite quality in older API docs. **Detected Arrays** (GA May 2026; blog July 2026) is shown on Google’s public coverage map as separate from BASE; none of the geocoded points below fall inside the May 2026 Detected Arrays GeoJSON.

**Live API probes were not run:** no `GOOGLE_MAPS_API_KEY` (or equivalent) was available in this Cloud Agent environment. Infisical project `cth-agents` was not reachable (CLI absent; Composio Infisical connection inactive). Re-run with a key using the curl templates in §5.

**Coverage-map approximation (official GeoJSON, 2026-05-06):** point-in-polygon checks against Google’s downloadable layers suggest **partial** BASE coverage at our coordinates—Corozal and Uribia inside BASE polygons; Quibdó and Bahía Solano outside; Chocó Pacific sites may return **404** even though Colombia is a BASE GA country. Google warns the map is approximate and building-level results can still 404.

### Verdict (3 lines)

1. **Energy Coop scoring:** Useful only where BASE/buildingInsights returns data; expect **gaps in Chocó (Quibdó, Bahía Solano)** and weak rural roof matching—use `requiredQuality=BASE` (not default HIGH), and treat API output as a **screening layer**, not ground truth for off-grid coops.  
2. **Promigas Paiva demo:** The Dec 2025 pilot is a **new** rooftop install at Centro Educativo Chiricoco; Detected Arrays is **unlikely to help validate that demo in Colombia** (no DA polygon hit; feature targets existing panels in high-res regions). Potential/buildingInsights at **published coordinates** is **unknown** until geocoded and probed with a key.  
3. **Next step:** Inject `GOOGLE_MAPS_API_KEY` via Infisical for `cth-agents`, probe each row with `requiredQuality=LOW` (ticket) **and** `requiredQuality=BASE` (Colombia GA), radius 50 m on `dataLayers:get`, plus `additionalInsights=DETECTED_ARRAYS`.

---

## 1. What official docs say about Colombia

| Topic | Official statement | URL |
| --- | --- | --- |
| Coverage tiers | `HIGH`, `MEDIUM`, `BASE`; interactive map + GeoJSON downloads | https://developers.google.com/maps/documentation/solar/coverage |
| Colombia BASE (GA) | From **2025-09-04**, BASE-quality data GA for **residential building areas** in **Brazil, Colombia, Peru, Puerto Rico** (standard billing; no `EXPANDED_COVERAGE` flag required in those countries) | https://developers.google.com/maps/documentation/solar/release-notes |
| Expanded / BASE definition | BASE = enhanced satellite @ 0.25 m/pixel; Colombia listed as GA BASE; elsewhere BASE may need `experiments=EXPANDED_COVERAGE` | https://developers.google.com/maps/documentation/solar/expanded-coverage |
| Map disclaimer | Coverage map is an **approximation**; **404** possible near borders or where map shows coverage | https://developers.google.com/maps/documentation/solar/coverage |
| Detected Arrays | Request via `additionalInsights=DETECTED_ARRAYS` on `buildingInsights`; coverage map includes **Detected Arrays** layer; early access described US/EU/Japan for high-res areas | https://developers.google.com/maps/documentation/solar/building-insights , https://mapsplatform.google.com/resources/blog/turning-raw-data-into-spatial-intelligence/ |
| Detected Arrays GA | **2026-05-11** release notes: Detected Arrays generally available | https://developers.google.com/maps/documentation/solar/release-notes |
| Product guidance | For maximum building coverage in Data Layers / matching buildings for Detected Arrays, use **`requiredQuality=BASE`** | https://mapsplatform.google.com/maps-products/solar/ |
| Quality enums | REST `ImageryQuality` includes `HIGH`, `MEDIUM`, `BASE` (and legacy `LOW` in some reference pages—prefer **BASE** for Colombia satellite tier) | https://developers.google.com/maps/documentation/solar/reference/rest/v1/ImageryQuality |

---

## 2. Site table

**Legend — API columns:** `Not probed (no key)` unless noted. **Map check** = point inside Google’s **20260506** GeoJSON (`BASE` or `DA`) from the coverage page downloads.

| Site | Coordinates (WGS84) + public source | buildingInsights (live) | dataLayers (live) | Detected Arrays (live) | Notes |
| --- | --- | --- | --- | --- | --- |
| **1. Corozal, Sucre (town centre)** | **9.31778, -75.29583** — Wikipedia municipality coordinates (“town and municipality”) | Not probed (no key) | Not probed (no key) | Not probed (no key) | **Map check:** inside **BASE** GeoJSON; outside HIGH/MEDIUM/DA. Urban Caribbean; best candidate among Sucre point for BASE. |
| **2. Paiva solar pilot (Promigas, Dec 2025)** | **Coordinates: location not found** in public geocoded sources. Site: **Centro Educativo Chiricoco**, vereda Chiricoco — press places event in **Paiva, Bolívar** (Dec 11, 2025) | Not probed (no key) | Not probed (no key) | Not probed (no key) | DANE code **113683000727**; address **Vda. de Chiricoco**, municipio **Santa Rosa**, Bolívar (not a separate Paiva municipality). No lat/lng in MEN/DANE listings found. **Map check:** skipped (no coords). |
| **3. Quibdó, Chocó (urban control)** | **5.69222, -76.65806** — Wikipedia capital coordinates | Not probed (no key) | Not probed (no key) | Not probed (no key) | Municipal portal gives cabecera **5°41′13″N, 76°39′40″W** (alternate control point). **Map check:** outside BASE/HIGH/MEDIUM/DA polygons at Wikipedia point—**high 404 risk** despite national Colombia BASE GA. |
| **4. Rural Chocó (Bahía Solano)** | **6.22622, -77.40439** — GeoNames feature `3689325` (populated place) | Not probed (no key) | Not probed (no key) | Not probed (no key) | Pacific off-grid proxy. **Map check:** outside all downloaded quality/DA polygons. |
| **5. Rural La Guajira (Uribia)** | **11.71389, -72.26583** — Wikipedia municipality coordinates | Not probed (no key) | Not probed (no key) | Not probed (no key) | Alta Guajira / Wayuu capital. **Map check:** inside **BASE** GeoJSON; outside DA. Sparse urban fabric—building match uncertain. |

---

## 3. Coverage-map point-in-polygon (no API key)

Downloaded from Google’s coverage page (2026-05-06 filenames):

- BASE: https://developers.google.com/maps/documentation/solar/coverage/20260506_BASE.geojson  
- Detected Arrays: https://developers.google.com/maps/documentation/solar/coverage/20260506_DA.geojson  

| Point | Inside BASE polygon? | Inside Detected Arrays polygon? |
| --- | --- | --- |
| Corozal (9.31778, -75.29583) | Yes | No |
| Quibdó (5.69222, -76.65806) | No | No |
| Bahía Solano (6.22622, -77.40439) | No | No |
| Uribia (11.71389, -72.26583) | Yes | No |

---

## 4. Infisical / API key status

| Check | Result |
| --- | --- |
| Env vars `GOOGLE_MAPS_API_KEY`, `GOOGLE_API_KEY`, `GCP_API_KEY`, `MAPS_API_KEY` | Unset in Cloud Agent VM |
| Infisical CLI | Not installed |
| Composio Infisical toolkit | No active connection (cannot list `cth-agents` secrets without HITL auth) |

**Do not** commit or paste API keys. When a key is available, run §5 locally or via Infisical-injected Hands.

---

## 5. Probe templates (when key available)

Replace `YOUR_API_KEY` via Infisical injection—never store in git.

**buildingInsights** (ticket: `requiredQuality=LOW`; also run `requiredQuality=BASE` for Colombia):

```bash
curl -sS -w "\nHTTP:%{http_code}\n" \
  "https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude=LAT&location.longitude=LON&requiredQuality=LOW&key=YOUR_API_KEY"
```

**Detected Arrays** (same location; requires building match first):

```bash
curl -sS -w "\nHTTP:%{http_code}\n" \
  "https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude=LAT&location.longitude=LON&requiredQuality=BASE&additionalInsights=DETECTED_ARRAYS&key=YOUR_API_KEY"
```

**dataLayers** (small radius):

```bash
curl -sS -w "\nHTTP:%{http_code}\n" \
  "https://solar.googleapis.com/v1/dataLayers:get?location.latitude=LAT&location.longitude=LON&radiusMeters=50&requiredQuality=LOW&key=YOUR_API_KEY"
```

Record: HTTP status, `imageryQuality` / `imagery_quality`, `detectionStatus` / `detectedArrays` if present, and whether URLs or insights body returned.

---

## 6. Sources (coordinates and context)

### Corozal

- Wikipedia, Corozal, Sucre: https://en.wikipedia.org/wiki/Corozal,_Sucre  

### Paiva / Promigas pilot

- Fundación Promigas (2025-12-12, event 2025-12-11): https://fundacionpromigas.org.co/paiva-estrena-el-primer-piloto-de-energia-solar-comunitaria-de-promigas-y-su-fundacion/  
- Centro Educativo de Chiricoco (DANE **113683000727**, Vda. de Chiricoco, Santa Rosa, Bolívar): https://co.institucioneducativa.info/bolivar/centro-educativo-de-chiricoco-2998/  

### Quibdó

- Wikipedia: https://en.wikipedia.org/wiki/Quibd%C3%B3  
- Alcaldía — Información del municipio (cabecera coords): https://www.quibdo-choco.gov.co/MiMunicipio/Paginas/Informacion-del-Municipio.aspx  

### Bahía Solano

- GeoNames `3689325`: https://www.geonames.org/3689325/bahia-solano.html  

### Uribia

- Wikipedia: https://es.wikipedia.org/wiki/Uribia  

### Google Solar API

- Coverage: https://developers.google.com/maps/documentation/solar/coverage  
- Release notes: https://developers.google.com/maps/documentation/solar/release-notes  
- Building insights (Detected Arrays): https://developers.google.com/maps/documentation/solar/building-insights  
- Blog (Detected Arrays / spatial intelligence, July 2026): https://mapsplatform.google.com/resources/blog/turning-raw-data-into-spatial-intelligence/  

---

*Awaiting Gideon's approval if this memo is reused in external Energy Coop materials.*
