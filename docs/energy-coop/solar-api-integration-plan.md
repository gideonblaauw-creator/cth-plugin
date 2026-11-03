# Google Solar API — Energy Coop integration plan

**Desk:** Energy Coop  
**Date:** 2026-11-03  
**App:** `energiacoop.cleantechhub.net` — mapa `/casos` (pines comunitarios, Colombia)  
**Coverage baseline:** [`solar-api-coverage-2026-11.md`](./solar-api-coverage-2026-11.md) (PR #107)

## Goal

Add roof-level solar intelligence where Google Solar API returns data, without exposing keys in the browser or repo. Where the API returns **404** or weak building match (Chocó Pacific, sparse rural fabric), keep today’s **NASA POWER** / **Global Solar Atlas** irradiance path used in **pipeline-minminas** scoring so site ranking never goes blank.

## Architecture (plain language)

```
Browser (/casos map)          Energy Coop backend (VPS)              Google Solar API
     |                                  |                                    |
     |  GET /api/solar/site?lat&lng     |  buildingInsights:findClosest      |
     | -------------------------------> |  (requiredQuality=BASE, CO)        |
     |                                  | ---------------------------------> |
     |                                  |  optional: dataLayers:get (cache)  |
     |                                  | ---------------------------------> |
     |  JSON: coverage tier, kWp,       |  key from Infisical at runtime     |
     |  panels, CO2, assets flag        |                                    |
     | <------------------------------- |                                    |
     |                                  |                                    |
     |  if 404 / no coverage            |  fallback: NASA POWER + GSA GHI    |
     | <------------------------------- |  (existing minminas fetchers)        |
```

1. **Server-side proxy only.** The Next/static app calls **your** API routes on the OVH stack (same host as Energy Coop). Those routes hold the Google key in memory after startup injection — never in `.env` committed to git, never in client bundles, never in browser `localStorage`.
2. **Secret source:** Infisical project **`cth-agents`**, environment Gideon assigns (typically `prod` or `staging`), key name e.g. `GOOGLE_MAPS_API_KEY` with Solar API enabled on the GCP billing account. Hands read via Infisical CLI / runtime inject on deploy — same pattern as other CTH agents ([`skills/infisical/SKILL.md`](../../skills/infisical/SKILL.md)).
3. **Two upstream endpoints (REST v1):**
   - **`buildingInsights:findClosest`** — primary for pin click: max panels, kW, kWh/year, sunshine hours, imagery quality, financial hints, optional **`additionalInsights=DETECTED_ARRAYS`** for “existing assets”.
   - **`dataLayers:get`** — optional second call with small `radiusMeters` (50 m per coverage memo) when the UI needs layer URLs or richer geometry; **cache aggressively** (see below) because this SKU is expensive.
4. **Colombia defaults:** Use **`requiredQuality=BASE`** for production Colombia pins ([release notes GA BASE for CO residential](https://developers.google.com/maps/documentation/solar/release-notes)). Log **`requiredQuality=LOW`** only for diagnostics parity with desk probes.
5. **Caching:** Redis or file cache on VPS keyed by `(lat,lng)` rounded to ~5 decimal places (~1 m) plus endpoint name. TTL suggestion: **30 days** for successful `buildingInsights` (roofs change slowly); **7 days** for `dataLayers` URLs (Google URLs expire — refresh on 403). Cache **404** responses **24 h** to avoid hammering Chocó pins. Invalidate on manual “refresh site” admin action.
6. **Rate limiting:** Enforce app-level limits per IP/session on `/api/solar/*` so map exploration cannot burn quota.

## Cost and quotas (official — do not treat as budget)

| Item | Source |
| --- | --- |
| Billing model | Pay-as-you-go per SKU; billing must be enabled; key or OAuth on every request | https://developers.google.com/maps/documentation/solar/usage-and-billing |
| **Building Insights** SKU | Essentials; **10,000** free billable events/month, then tiered USD per 1,000 (e.g. **$10.00** for 10,001–100,000 tier on global list) | https://developers.google.com/maps/billing-and-pricing/pricing#environment-apis (row *Solar API Building Insights*) |
| **Data Layers** SKU | Enterprise; **1,000** free billable events/month, then tiered USD per 1,000 (e.g. **$75.00** for 1,001–100,000 tier) | Same pricing page (row *Solar API Data Layers*) |
| Throughput caps | **600 queries/minute** per project for Building Insights and for Data Layers | https://developers.google.com/maps/documentation/solar/usage-and-billing |
| Quota management | Set daily caps in Cloud Console → Maps Platform → Quotas | Same usage-and-billing page |

**Product implication for Energy Coop:** Default UX should rely on **one Building Insights call per pin open** (cached). Call **Data Layers** only from an explicit “Ver capas / detalle técnico” action or batch jobs — not on every map click.

## Coverage fallback

| Situation | UX badge | Data source | Scoring behaviour |
| --- | --- | --- | --- |
| HTTP 200 + `imageryQuality` BASE/HIGH | **Cobertura Google Solar** | Map `solarPotential`, `financialAnalyses` fields into UI | Full **solar resource** + roof **existing assets** (if Detected Arrays present) |
| HTTP 404, outside BASE polygon, or rural non-match (Quibdó, Bahía Solano per [coverage memo](./solar-api-coverage-2026-11.md)) | **Sin cobertura – usando NASA POWER** | Existing pipeline: NASA POWER daily GHI/DNI + Global Solar Atlas long-term averages at pin | **Solar resource** signal from irradiance only; **existing assets** = unknown / manual coop survey |
| Coords uncertain (Paiva / Chiricoco) | **Cobertura por confirmar** until probed | Try Google once; on failure fall back as above | Same as no coverage until live probe |

Fallback must reuse the **same normalised schema** the map panel expects (`kWhPerYear`, `sunHours`, `source: google_solar | nasa_power_gsa`) so `/casos` does not fork UI logic.

## Feeding pipeline-minminas scoring

The minminas pipeline already scores community cases using a **solar resource** dimension (irradiance, seasonality) from NASA POWER / GSA. After integration:

| Signal | Google Solar path | Fallback path |
| --- | --- | --- |
| **Solar resource** (0–1 or tier) | Normalise `maxSunshineHoursPerYear`, `maxArrayPanelsCount` × panel wattage, and annual kWh from `buildingInsights` vs regional benchmark | Keep current GHI/kWh/m²/year from NASA POWER + GSA; flag `confidence: medium` |
| **Existing assets** (diesel offset, prior PV) | `detectedArrays` / `detectionStatus` when `DETECTED_ARRAYS` requested; panel count & capacity on matched roof | `null` + desk note “sin detección satelital”; coop questionnaire fields unchanged |

Persist per pin: `solarDataSource`, `imageryQuality`, raw API snapshot (server-side only), and derived features consumed by the scoring job. Re-score on cache refresh, not on every page view.

## Phased delivery

| Phase | Scope | Effort |
| --- | --- | --- |
| **0 — Secrets & GCP** | Enable Solar API on CTH GCP project; store key in Infisical `cth-agents`; wire VPS inject; document key rotation | Small (ops + Infisical) |
| **1 — Proxy + Building Insights** | `/api/solar/insights?lat=&lng=` with BASE quality, caching, 404 handling, structured JSON for map panel | Medium (backend + tests with real key) |
| **2 — Map UX** | `/casos` pin click → panel “Potencial solar”; badges from coverage rules; example numbers replaced by API | Medium (frontend; mock-up at `mockups/energy-coop-solar/index.html`) |
| **3 — Scoring hook** | Extend pipeline-minminas ingest with Google fields; dual-path solar resource + existing assets; regression on Corozal/Uribia/Chocó fixtures | Medium–large (data pipeline) |
| **4 — Data Layers (optional)** | On-demand layer fetch, tile URL proxy if needed, stricter cache + admin quota alerts | Small–medium (cost-sensitive) |
| **5 — Hardening** | Quota dashboards, Cloud daily caps, audit log, re-probe script from coverage memo §5 | Small |

**Mock-up (this PR):** Phase 2 visual/ copy reference only — static HTML, no API, all figures labelled *DATOS DE EJEMPLO*.

## Security checklist

- [ ] Key only in Infisical `cth-agents`; runtime inject on VPS  
- [ ] Solar API routes authenticated or same-origin + session as Energy Coop admin where appropriate  
- [ ] No key in client, git, CI logs, or Composio configs  
- [ ] Cached responses strip Google-internal URLs from client payloads if they are short-lived secrets  

## References

- Coverage tiers & GeoJSON: https://developers.google.com/maps/documentation/solar/coverage  
- Building insights & Detected Arrays: https://developers.google.com/maps/documentation/solar/building-insights  
- REST `findClosest`: https://developers.google.com/maps/documentation/solar/reference/rest/v1/buildingInsights/findClosest  
- REST `dataLayers:get`: https://developers.google.com/maps/documentation/solar/reference/rest/v1/dataLayers/get  
- Usage, billing, QPM: https://developers.google.com/maps/documentation/solar/usage-and-billing  
- Global SKU pricing (Environment APIs table): https://developers.google.com/maps/billing-and-pricing/pricing  

---

*Internal engineering plan — not for external publication without Gideon's approval.*
