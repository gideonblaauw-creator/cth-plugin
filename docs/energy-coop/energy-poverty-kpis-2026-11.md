# Energy poverty KPIs — Promigas × Dutch Embassy prep (11 Nov 2026)

**Desk:** Energy Coop (CleantechHUB)  
**Purpose:** Evidence pack for the Embassy meeting with Promigas. **No demo code changes** (demo work lives in [PR #110](https://github.com/gideonblaauw-creator/cth-plugin/pull/110)).  
**Method:** Primary PDFs downloaded under `/opt/cursor/artifacts/energy-poverty-research/`; extracts via `pdftotext` + targeted grep. Facts use **two independent sources** where possible; otherwise **PARCIAL**.

---

## 1. How Promigas defines and measures energy poverty (IMPE)

### 1.1 Primary corporate / foundation sources

| Source | Year | Role |
|--------|------|------|
| **Informe Integrado de Gestión (IIG) 2024** — Promigas (cap. prosperidad / sostenibilidad) | 2024 | Strategy, connections, IMPE as management tool |
| **Informe IMPE 2025** (III edición) — Fundación Promigas + Inclusión SAS | Nov 2025 | **Canonical KPI definitions, thresholds, national & dept. values** |
| Comunicado / nota Fundación Promigas (III IMPE) | Nov 2025 | Second source for national headline numbers |

**Note:** Direct download of `informe-integrado-gestion-2024.pdf` from `gestion2024.promigas.com` returned a non-PDF payload from this environment; IIG wording below is cross-checked against the public **prosperidad** chapter text and the IMPE 2025 report (independent).

### 1.2 Definition (IMPE)

> «El Índice Multidimensional de Pobreza Energética (IMPE) es una herramienta diseñada para medir la pobreza energética a partir de la acumulación de diversas privaciones que limitan la posibilidad de las personas de realizar actividades esenciales mediadas por el uso de la energía. Su construcción se basa en el enfoque de medición de pobreza multidimensional de Alkire y Foster (AF), y considera cuatro dimensiones y quince indicadores.»

— *Informe IMPE 2025*, p. 8 ([PDF](https://fundacionpromigas-offloadmedia.s3.amazonaws.com/wp-content/uploads/2025/11/18082502/Informe-IMPE-2025.pdf))

> «De acuerdo con la metodología del IMPE, se considera en pobreza energética a los miembros de un hogar que acumulan al menos el **30%** de las privaciones ponderadas.»

— *Informe IMPE 2025*, p. 9 (same PDF)

**Four dimensions (weights in IMPE 2025, Tabla 1, pp. 9–10):**

1. **Acceso y calidad de la energía (40%)** — e.g. access to electricity (ECV), quality of supply (SSPD/IPSE), safe/convenient cooking fuel, thermal comfort, washer, fridge, modern stove, dedicated cooking space.  
2. **Vivienda funcional y liberadora de tiempo (25%)**  
3. **Aprender y comunicarse (25%)**  
4. **Territorio equipado para el bien-estar (10%)**

**Example indicator — cooking fuel (links to DANE ECV):**

> «Una persona se encuentra privada si el principal energético para cocinar del hogar es carbón, leña, o material de desecho.»

— *Informe IMPE 2025*, Tabla 1, p. 10

**Promigas (IIG 2024 narrative, independent of IMPE PDF):**

> «Esta herramienta pionera en Colombia mide la relación entre acceso energético y bienestar humano. Su implementación ha permitido identificar hogares con carencias simultáneas en acceso, calidad y aprovechamiento de la energía… En 2024, fortalecimos la herramienta para llegar a **nivel municipal** y presentamos la **segunda edición del IMPE**, a nivel departamental.»

— Promigas, *Informe Integrado de Gestión 2024* (prosperidad / sostenibilidad chapter, [prosperidad.pdf](https://gestion2024.promigas.com/recursos/docs/prosperidad.pdf)) — **PARCIAL** (page number not verified here; text matches public chapter)

### 1.3 Headline KPIs, targets, and latest values (Promigas IMPE)

| KPI | Definition | Latest value | Target / roadmap | Year | Source 1 | Source 2 | Status |
|-----|------------|--------------|------------------|------|----------|----------|--------|
| **IMPE incidence (persons)** | Share of population in energy poverty (≥30% weighted deprivations, AF) | **15,4%** (~**8,1 M** persons) | **9,5%** by 2030 (~5,17 M); −2,9 M persons vs 2024 | 2024 | IMPE 2025, pp. 12, 1135 ([PDF](https://fundacionpromigas-offloadmedia.s3.amazonaws.com/wp-content/uploads/2025/11/18082502/Informe-IMPE-2025.pdf)) | [Fundación Promigas, 18 Nov 2025](https://fundacionpromigas.org.co/mas-de-300-000-personas-salieron-de-la-pobreza-energetica-en-2024-sin-embargo-1-de-cada-6-colombianos-continua-en-esta-situacion/) | OK |
| **IMPE incidence (YoY)** | Change in national incidence | 16,1% → **15,4%** (−0,7 p.p.; >300k persons left poverty in 2024) | Maintain acceleration vs ~300k/year (else 2034 for single digit) | 2023→2024 | IMPE 2025, p. 12 | [Promigas IMPE 2025 news](https://www.promigas.com/Paginas/NoticiasESP/IMPE-2025.aspx) | OK |
| **IMPE intensity** | Mean share of weighted deprivations among energy-poor | **46,7%** (stable); adjusted incidence **0,072** (2024) | Reduce to **43,2%** by 2030 | 2024 | IMPE 2025, pp. 12–13, 1137 | IMPE 2025 executive summary ([PDF](https://fundacionpromigas-offloadmedia.s3.amazonaws.com/wp-content/uploads/2025/11/14145438/VF-IMPE-2025-Indice-Multidimensional-de-Pobreza-Energetica-Promigas.pdf)) | OK |
| **IMPE — rural remote vs urban** | Incidence by degree of urbanization | Rural remote **44,3%** vs urban **~4–5%** (**~10×** gap, 2024) | Close territorial gap (policy differentiated by territory) | 2024 | IMPE 2025, p. 18 | Fundación IMPE 2023 release (47,9% vs 4,3% large cities, 2022 base) — [Promigas comunicado](https://www.promigas.com/Paginas/NoticiasESP/Comunicado-IMPE.aspx) | OK (2024 + historical second source) |
| **Cooking fuel deprivation (IMPE indicator)** | Population share deprived: wood/coal/waste as main cooking energy | **9,9%** national (2024); **56,6%** among energy-poor vs ~0% among non-poor | PNSL / IMPE “Apuesta 2” (−4 p.p. scenario to 2030) | 2024 | IMPE 2025, Tabla 2 / narrative pp. 15–16, 1032 | [DNP TEJ brief](https://www.dnp.gov.co/publicaciones/Planeacion/Paginas/transicion-energetica.aspx) (1,6 M households on wood — different unit) | OK (national); PARCIAL (dept.) |
| **New connections (Promigas ops KPI)** | New gas + electricity users connected | **421.719** new users; **109.727** conversions from LPG/wood to gas | Prosperidad energética / poverty reduction | 2024 | IIG 2024 prosperidad chapter ([URL](https://gestion2024.promigas.com/recursos/docs/prosperidad.pdf)) | IMPE 2025 case studies (Misión La Guajira) p. 1790+ | PARCIAL (IIG page #) |
| **IMPE La Guajira** | Dept. incidence (persons) | **63,1%** (2024); **65%** (2023) | Dept. differentiated route in IMPE 2025 | 2024 | IMPE 2025, Fig. 7 / dept. table (~p. 22) | [Promigas IMPE 2025 news](https://www.promigas.com/Paginas/NoticiasESP/IMPE-2025.aspx) (periphery emphasis) | OK |
| **IMPE Bolívar** | Dept. incidence | **24,9%** (2024); **30,4%** (2023); −119.792 persons | Same | 2024 | IMPE 2025, pp. 22–23 | Fundación press (national context) | OK |
| **IMPE Chocó** | Dept. incidence | **52,8%** (2024); **54%** (2023) | Same | 2024 | IMPE 2025, dept. table (~p. 22) | IMPE 2025 Fig. 7 narrative (periphery) | OK |

**Quote — 2030 roadmap (Promigas):**

> «… reducir la pobreza energética de **15,4%** a **9,5%**… pasar de **8,11 millones** de pobres energéticos en 2024 a **5,17 millones** en 2030.»

— *Informe IMPE 2025*, pp. 1135–1137

---

## 2. DANE / ECV — access, cooking fuel, multidimensional poverty

| KPI | Definition | National | La Guajira | Bolívar | Chocó | Year | Source 1 | Source 2 | Status |
|-----|------------|----------|------------|---------|-------|------|----------|----------|--------|
| **Households with electricity (ECV)** | Vivienda con energía eléctrica (incl. red, solar, etc., per ECV rules) | **96,3%** (81.940 / 85.106 HH in public microdata extract) | **PARCIAL** — UPRA cites **99,4% urban / 37,5% rural** HH with electricity | **PARCIAL** | **PARCIAL** | 2024 / 2022 | [DANE microdatos ECV 2024, P8520S1](https://microdatos.dane.gov.co/index.php/catalog/861/variable/F1/V20?name=P8520S1) | [UPRA La Guajira kit (ECV 2022)](https://upra.gov.co/Kit_Territorial/2-%20Informaci%C3%B3n%20por%20Departamentos/LA%20GUAJIRA/2-%20Documento%20Regional%20UPRA%20La%20Guajira.pdf) | PARCIAL (dept. 2024) |
| **Gas natural connected (ECV)** | HH with gas natural on public grid | **PARCIAL** national in open bulletins | Rural **8,5%**, urban **37,5%** (HH) | **PARCIAL** | **PARCIAL** | 2022 (Guajira) | UPRA (DANE ECV 2022) | ECV 2024 form P3162 ([formulario](https://www.dane.gov.co/files/operaciones/ECV/formulario-ECV-2024.pdf)) | PARCIAL |
| **Campesino HH — electricity / gas** | Subpopulation ECV bulletin | **97,7%** elec.; **36,0%** gas | **PARCIAL** | **PARCIAL** | **PARCIAL** | 2024 | [bol-campesinos ECV 2024](https://www.dane.gov.co/files/operaciones/ECV/bol-campesinos-ECV-2024.pdf) | DANE ECV 2024 catalog ([microdatos](https://microdatos.dane.gov.co/index.php/catalog/861)) | OK (national subpop) |
| **PDET municipalities — electricity / gas** | HH in PDET areas | **98,0%** elec.; **31,8%** gas | Relevant (La Guajira PDET) | Partial PDET | Partial PDET | 2024 | [bol-PDET ECV 2024](https://www.dane.gov.co/files/operaciones/ECV/bol-PDET-ECV-2024.pdf) | DANE ECV 2024 overview | OK (PDET, not dept.) |
| **NARP HH — electricity / gas** | HH jefe NARP | **99,6%** elec.; **46,6%** gas (Bolívar/Chocó have high NARP share) | **PARCIAL** | Context: **20,9%** NARP pop. (dept.) | **74,4%** NARP pop. (dept.) | 2024 | [bol-NARP ECV 2024](https://www.dane.gov.co/files/operaciones/ECV/bol-NARP-ECV-2024.pdf) | Same bulletin (dept. composition) | OK (national NARP); dept. composition OK |
| **Cooking with wood (ECV)** | Main cooking fuel leña/madera | ~**1,5–1,8 M HH** (orders of magnitude; year varies) | **PARCIAL** | **PARCIAL** | **PARCIAL** | 2022–2024 | [El Tiempo / Naturgas citing ECV 2022](https://www.eltiempo.com/economia/sectores/colombia-tiene-cerca-de-1-6-millones-de-hogares-en-pobreza-energetica-839798) | [Bancolombia Capital Inteligente citing DANE ECV](https://www.bancolombia.com/empresas/capital-inteligente/actualidad-economica-sectorial/rol-gas-natural-sustitucion-lena) | PARCIAL (exact 2024 national %) |
| **IPM (DANE)** | Multidimensional poverty (not energy-specific) | See DANE IPM bulletins | **PARCIAL** | **PARCIAL** | **PARCIAL** | 2024 | [DANE ECV/IPM program pages](https://www.dane.gov.co/index.php/estadisticas-por-tema/salud/calidad-de-vida-ecv/encuesta-nacional-de-calidad-de-vida-ecv-2024) | — | PARCIAL (not extracted this pass) |
| **Censo 2018 — electricity** | Housing with electricity service | Historical baseline | **PARCIAL** | **PARCIAL** | **PARCIAL** | 2018 | DANE Censo 2018 (not re-pulled) | ICEE / UPME uses DANE housing stock projections | PARCIAL |

**ECV variables for hands-on measurement:** `P8520S1` (electricity in dwelling), `P3162` (gas grid), `P8540` (main cooking fuel) — [data dictionary](https://microdatos.dane.gov.co/index.php/catalog/861/data-dictionary/F2?file_name=Servicios+del+hogar).

---

## 3. FENOGE / MinEnergía / UPME / IPSE — coverage & official poverty index

| KPI | Definition | National | La Guajira | Bolívar | Chocó | Year | Source 1 | Source 2 | Status |
|-----|------------|----------|------------|---------|-------|------|----------|----------|--------|
| **ICEE (UPME)** | Residential electric coverage = VCS / VT | **93,12%** (urban **98,71%**, rural **75,92%**) | **54,28%** | **88,2%** | **93,9%** | 2024 | [Boletín ICEE 2024](https://docs.upme.gov.co/SIMEC/Energia%20Electrica/Documents/Informes_cobertura/Boletin_ICEE_2024.pdf) | [UPME news 93,12%](https://www.upme.gov.co/upme_noticias/colombia-alcanza-9312-de-cobertura-elctrica-tras-llevar-energa-a-539351-nuevos-hogares-y-registrar-el-mayor-avance-en-la-ruralidad/) | OK |
| **Viviendas sin servicio (ICEE)** | VT − VCS | **1.326.971** VSS | **PARCIAL** (high VSS; low ICEE) | **PARCIAL** | **PARCIAL** | 2024 | Boletín ICEE 2024 | UPME ICEE methodology page ([UPME](https://www.upme.gov.co/simec/energia-electrica/cobertura/indice-de-cobertura-de-energia-electrica-icee/)) | OK (national); PARCIAL (dept. VSS) |
| **New connections (ICEE narrative)** | Households electrified in period | **539.351** new VCS vs 2023 | — | — | — | 2024 | UPME news | Boletín ICEE 2024 | OK |
| **IPEM (MinEnergía)** | Official multidimensional **household** energy poverty index (different from IMPE) | **22,3%** HH (from **24,3%** in 2023); ~**760k** persons | **42,19%** HH (IPEM dept.) | **PARCIAL** | **PARCIAL** | 2024 | [MinEnergía press, 10 Dec 2025](https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/colombia-saca-a-760000-personas-de-la-pobreza-energetica-en-2024-un-avance-historico-del-gobierno-del-cambio/) | [El Tiempo on IPEM](https://www.eltiempo.com/economia/sectores/colombia-reduce-la-pobreza-energetica-ministerio-de-energia-asegura-que-265-886-hogares-salieron-de-esta-condicion-en-2024-3515871) | OK (national); PARCIAL (Bolívar/Chocó dept.) |
| **IPEM methodology** | Dimensions: electricity + food prep, functional housing, connectivity/services | See methodological doc | — | — | — | 2025 | [Documento metodológico IPEM MME](https://www.minenergia.gov.co/documents/13468/Documento-metodologico-IPEM-MME-2025.pdf) | MinEnergía press | OK |
| **FENOGE** | Financing non-conventional energy / access projects | Project-level KPIs (kWp, beneficiaries) — see `docs/energy-coop/fenoge-public-data-2026-11.md` (PR #109) | Maicao, Media Luna, etc. | — | — | 2024–2026 | FENOGE public records (PR #109) | UPME/IPSE rural/ZNI context | PARCIAL (not duplicated here) |
| **IPSE / ZNI quality** | Hours of supply in non-interconnected zones | Used in IMPE “calidad” for ZNI (IPSE) | Relevant La Guajira ZNI | — | — | 2024 | IMPE 2025 Tabla 1, p. 10 | IPSE (via IMPE citation) | PARCIAL |

**Important:** **IMPE (Promigas)** and **IPEM (MinEnergía)** are both “multidimensional energy poverty” but **different constructs** (person vs household, indicators, cutoffs). Do not merge without relabeling. El Tiempo (Dec 2025) explicitly contrasts **22,3% (IPEM)** with **15,4% (IMPE)**.

---

## 4. Additional independent sources (Colombia metrics)

| Source | Metric | Value | Year | Use in demo narrative | Status |
|--------|--------|-------|------|------------------------|--------|
| **IDB (BID)** | Household energy poverty (7 basic energy services, Colombia) | **73%** HH in PE; **53,9%** severe PE (ENCV 2019) | 2019 | Long-run structural gap; **not** current headline | OK (historical); label year |
| **IDB** | Among HH without cooking access, **62%** use wood most often (Colombia) | 62% | 2019 | Cooking / leña storyline | OK |
| **DNP** | People without electricity; HH cooking with wood | ~**4 M** people; ~**1,6 M** HH wood | 2024 pub. | TEJ / policy framing | OK (DNP + IMPE wood narrative) |
| **World Bank** | Access to electricity (% population) | ~**97%+** (WB series; differs from ICEE/ECV housing unit) | 2023–2024 | Cross-check only | PARCIAL (not pulled this pass) |

Publications: [BID — Pobreza energética en hogares (Colombia)](https://publications.iadb.org/publications/spanish/document/Pobreza-energetica-en-los-hogares-y-su-relacion-con-otras-vulnerabilidades-en-America-Latina-el-caso-de-Argentina-Brasil-Colombia-Peru-y-Uruguay.pdf)

---

## 5. KPI master table (meeting-ready)

| KPI | Definition | Latest value (Nat \| La Guajira \| Bolívar \| Chocó) | Year | Source 1 | Source 2 | Status |
|-----|------------|------------------------------------------------------|------|----------|----------|--------|
| IMPE incidence | AF ≥30% weighted deprivations (persons) | **15,4%** \| **63,1%** \| **24,9%** \| **52,8%** | 2024 | IMPE 2025 PDF | Fundación Promigas Nov 2025 | OK |
| IMPE 2030 target | Policy ambition | **9,5%** national | 2030 | IMPE 2025 | Promigas news IMPE 2025 | OK |
| ICEE total | Electric coverage (VCS/VT) | **93,12%** \| **54,28%** \| **88,2%** \| **93,9%** | 2024 | UPME Boletín ICEE 2024 | UPME press | OK |
| IPEM (MME) | HH multidimensional energy poverty | **22,3%** \| **42,19%** \| PARCIAL \| PARCIAL | 2024 | MinEnergía press | El Tiempo | PARCIAL (dept.) |
| ECV electricity (HH) | Dwelling with electricity | **96,3%** \| PARCIAL \| PARCIAL \| PARCIAL | 2024 | DANE microdatos | ECV 2024 form | PARCIAL (dept.) |
| Cooking fuel deprivation (IMPE) | Wood/coal/waste main fuel (persons deprived) | **9,9%** \| PARCIAL \| PARCIAL \| PARCIAL | 2024 | IMPE 2025 | DNP / PNSL context | PARCIAL (dept.) |
| Rural remote IMPE | Territorial gap | **44,3%** vs urban ~**4–5%** | 2024 | IMPE 2025 p. 18 | IMPE 2023 comunicado | OK |
| Promigas connections | New users (gas + electricity) | **421.719** (109.727 fuel switch) | 2024 | IIG prosperidad | IMPE 2025 La Guajira case | PARCIAL (page) |

---

## 6. Promigas KPI alignment — demo screens ([PR #110](https://github.com/gideonblaauw-creator/cth-plugin/pull/110))

| Demo screen | Content (PR #110) | KPIs that fit (real data) | Notes |
|-------------|-------------------|---------------------------|--------|
| **1 — Paiva solar pilot** | Fundación Promigas community solar, ~450 hab., CSR (not FENOGE) | National **IMPE 15,4%** trend; **cooking fuel 9,9%**; **Promigas 421k connections**; optional **IDB** cooking/leña context | Map approximate — pair with **qualitative** Misión La Guajira / Paiva story, not dept. ICEE precision on pin |
| **2 — La Guajira (FENOGE map)** | FENOGE PV projects (Maicao, Media Luna, Nazareth, Tomarrazón) | **ICEE La Guajira 54,28%**; **IMPE 63,1%**; **IPEM HH 42,19%**; ECV **rural elec. 37,5% / gas 8,5%** (2022, Guajira) | Strongest screen for **territorial gap**; cite **year** on each layer |
| **3 — CEOF wizard** | **Simulated** example data | Use as **scenario shell** only; overlay **recommended KPIs** in facilitator script, not as live API | Do not present wizard numbers as DANE/UPME |

---

## 7. Recommended 3–4 KPIs for the live demo (with cited values)

Use these in talking points and optional static callouts on screens 1–2 (not wizard metrics):

1. **IMPE national incidence — 15,4% (2024), ~8,1 M persons**  
   - Fundación Promigas, 18 Nov 2025; IMPE 2025, p. 12.  
   - *Why:* Promigas’s own flagship metric for the Embassy host.

2. **IMPE La Guajira — 63,1% (2024)**  
   - IMPE 2025, Fig. 7 (~p. 22); corroborate territorial priority with **ICEE 54,28%** (UPME Boletín 2024).  
   - *Why:* Anchors **screen 2** (FENOGE La Guajira) in independent stats.

3. **ICEE national — 93,12%; rural 75,92% (2024)**  
   - UPME Boletín ICEE 2024; UPME press release.  
   - *Why:* Official **access** gap vs “almost universal” narrative; complements IMPE quality dimension.

4. **Cooking fuel (IMPE indicator) — 9,9% national deprivation (2024)**  
   - IMPE 2025, Tabla 2; **56,6%** among energy-poor still on wood/coal/waste (p. 1032 narrative).  
   - *Why:* Links gas expansion / **PNSL** to measurable deprivation (Promigas core business).

**Optional fifth (government cross-check):** **IPEM 22,3% households (2024)** — MinEnergía + El Tiempo; use only if discussing **public policy** alignment, with explicit “different index from IMPE”.

---

## 8. Gaps and caveats for the 11 Nov meeting

1. **Two multidimensional indices (IMPE vs IPEM)** — both legitimate; incidence differs (**15,4%** persons vs **22,3%** HH). Align with Promigas on which to lead.  
2. **Departmental ECV 2024** for gas/electricity/leña by La Guajira / Bolívar / Chocó — not fully extracted; UPRA **2022** Guajira figures are latest dept. split found (**PARCIAL**).  
3. **IIG 2024 PDF** not retrievable as binary from automation host; prosperidad chapter used for quotes (**PARCIAL** page cites).  
4. **ICEE >100% / Chocó drop 100%→93,9%** — UPME flags DANE projection vs reporting issues; explain when showing Chocó ICEE.  
5. **FENOGE project KPIs** — live in sibling doc from PR #109; not re-validated here.  
6. **Censo 2018 / IPM 2024** — not built into table this pass (**PARCIAL**).  
7. **Demo code** — intentionally unchanged; integrate KPI copy via content/PR review on #110 separately.

---

## Document control

| Field | Value |
|-------|--------|
| Author | Cloud Hands (Energy Coop desk ticket) |
| Created | 2026-11-03 |
| Promigas reports used | IIG 2024 (narrative); **Informe IMPE 2025** (primary KPIs) |
| Validation | JSON/manifest N/A; repo `jq` + skill YAML checks per `AGENTS.md` |

**Awaiting Gideon's approval** if any excerpt is reused as external CleantechHUB voice; internal meeting prep only.

---

## Meta 2030 y rutas

*Actualización PR #111 — reuniones Embajada de Países Bajos × Promigas. Sin metas inventadas: solo cifras y formulaciones citadas.*

### A. ¿Qué meta 2030 declara Promigas?

#### A.1 Meta explícita de pobreza energética (IMPE) — **sí existe, con números**

Promigas y Fundación Promigas presentan en la **III edición del IMPE (2025)** un escenario prospectivo (microsimulación) hacia **2030**, no como meta climática corporativa sino como **hoja de ruta país** para “pobreza energética de un dígito”:

> «El objetivo que se propone hacia 2030 es reducir el porcentaje de personas en pobreza energética de **15,4% en 2024 a 9,5%**, lo que equivale pasar de **8,11 millones** de pobres energéticos en 2024 a **5,17 millones** en 2030, reduciendo en **2,9 millones** el total de personas en esta condición.»

— *Informe IMPE 2025*, p. 33 ([PDF](https://fundacionpromigas-offloadmedia.s3.amazonaws.com/wp-content/uploads/2025/11/18082502/Informe-IMPE-2025.pdf))

Meta complementaria de **intensidad** (profundidad de privaciones entre quienes siguen siendo pobres energéticos):

> «… de **46,7% a 43,2%** [privaciones promedio que acumulan los hogares pobres energéticos].»

— *Informe IMPE 2025*, p. 33 (mismo PDF)

Ritmo que el informe asocia al cumplimiento de esa meta:

> «… acelerar su ritmo actual de reducción —que hoy es de **0,75 puntos porcentuales por año**— y llevarlo al menos a **1,0** durante los próximos seis años, reduciendo el total de pobres en promedio cerca de **490 mil personas por año**.»

— *Informe IMPE 2025*, p. 33

**Segunda fuente (comunicación Promigas):** [IMPE 2025 — Promigas.com](https://www.promigas.com/Paginas/NoticiasESP/IMPE-2025.aspx): más de **300.000** personas salieron de la pobreza energética en 2024; si se mantiene ese ritmo, la meta de un dígito llegaría **hasta 2034**, pero el IMPE 2025 presenta hoja de ruta para **anticiparla a 2030**.

**Cuatro “apuestas” ligadas a la simulación 2030** (IMPE, pp. 33–34):

1. Calidad eléctrica + soluciones no convencionales (solar, híbrida) en rural disperso.  
2. Plan Nacional de Sustitución de Leña — «sustituir cerca de **540 mil hogares**».  
3. Dotación de electrodomésticos y dispositivos (“Modo ON”).  
4. Colegios con electricidad — «entre **1300 y 1800** instituciones educativas».

#### A.2 Informe Integrado de Gestión / prosperidad energética — **sin meta numérica 2030 de IMPE**

En el **IIG 2024** (texto público verificado vía documento corporativo en promigas.com), Promigas enmarca **“Nuestra Energía 2040”** y la prioridad **“Prosperidad energética — Energía confiable y reducción de la pobreza energética”**, con **resultados operativos 2024** (p. ej. **421.719** nuevos usuarios, **7,2 millones** de clientes), pero **no se encontró una meta cuantitativa corporativa 2030** del tipo “X % IMPE” o “Y millones de conexiones en 2030” distinta del escenario IMPE país.

| Tema | Meta / horizonte citado | Baseline | Fuente 1 | Fuente 2 | Status |
|------|-------------------------|----------|----------|----------|--------|
| Pobreza energética (IMPE país) | **9,5%** personas, **5,17 M** pobres energéticos | **15,4%**, **8,11 M** (2024) | IMPE 2025 p. 33 | [Fundación Promigas Nov 2025](https://fundacionpromigas.org.co/mas-de-300-000-personas-salieron-de-la-pobreza-energetica-en-2024-sin-embargo-1-de-cada-6-colombianos-continua-en-esta-situacion/) | OK |
| Intensidad IMPE | **43,2%** privaciones promedio (pobres) | **46,7%** (2024) | IMPE 2025 p. 33 | Resumen ejecutivo IMPE ([PDF](https://fundacionpromigas-offloadmedia.s3.amazonaws.com/wp-content/uploads/2025/11/14145438/VF-IMPE-2025-Indice-Multidimensional-de-Pobreza-Energetica-Promigas.pdf)) | OK |
| Carbono neutralidad | **2040** (alcances 1, 2 y parte 3) | Línea base emisiones **2021** | [Promigas descarbonización 2022](https://www.promigas.com/Paginas/NoticiasESP/PROMIGAS-IMPLEMENTA-HOJA-DE-RUTA-DE-DESCARBONIZACI%C3%93N.aspx) | [Estrategia climática EN](https://www.promigas.com/Paginas/Sostenibilidad/ENG/EstrategiaClimatica.aspx) | OK |
| Emisiones intermedias | **~50%** reducción intensidad vs 2021 | 2021 | Noticia descarbonización 2022 | IIG 2024 acción climática ([gestion2024](https://gestion2024.promigas.com/es/accion-climatica)) | OK |
| SBTi | **Alineación con lineamientos generales**; no meta SBTi validada citada | — | IIG 2024 (acción climática) | SBTi net-zero framework (referencia sectorial) | OK (alineación declarada; **no** target SBTi publicado) |
| Conexiones anuales | **Resultado** 2024: 421.719 nuevos usuarios; 2025 IIG web: 292.255 | — | IIG / prosperidad 2024 (narrativa) | [Informe gestión 2025 web](https://www.promigas.com/Paginas/Especiales/Informe-gestion-2025.aspx) | OK (hechos, **no** meta 2030) |
| ODS / eficiencia web | Estrategia **2030** — mercados más eficientes, renovables | — | [Promigas ODS](https://www.promigas.com/Paginas/Sostenibilidad/ESP/ODS.aspx) | — | PARCIAL (cualitativo, sin KPI único pobreza) |

**Conclusión A:** La **única meta 2030 cuantitativa explícita sobre pobreza energética** localizada en fuentes Promigas/Fundación es el **escenario IMPE 9,5% / −2,9 M personas**, con metas satélite (intensidad, PNSL **540 mil hogares**, colegios **1300–1800**). Metas corporativas 2030 en clima son **50% (2028)**; **2040** es carbono neutralidad — distinto eje.

---

### B. Brecha actual vs meta — aritmética solo con cifras citadas

**Stock de personas (IMPE 2025, p. 33):**

| Concepto | Valor |
|----------|--------|
| Pobres energéticos 2024 | **8.117.357** (figura p. 33; texto redondea **8,11 millones**) |
| Pobres energéticos 2030 (meta escenario) | **5.171.498** (**5,17 millones**) |
| Personas que deben salir | **2.945.859** (= 8.117.357 − 5.171.498) ≈ **2,9 millones** (redondeo informe) |

**Horizonte:** seis años de esfuerzo **2025–2030** (implícito en “próximos seis años”, p. 33).

#### B.1 Ritmo en personas

| Escenario | Supuesto (fuente) | Cálculo | Tiempo para cerrar ~2,9 M | ¿Alcanza 2030? |
|-----------|-------------------|---------|---------------------------|----------------|
| **Observado 2022–2024** | ~**300 mil** personas/año (IMPE p. 12) | 2.900.000 ÷ 300.000 = **9,67 años** | Desde 2024 → ~**2034** | No (IMPE p. 12: «**nueve años adicionales**» para un dígito al ritmo 2022–2024 → ~**2033**) |
| **Comunicación 2024** | **>300.000** en un solo año (Fundación / Promigas news) | Mismo orden de magnitud | [Promigas IMPE 2025](https://www.promigas.com/Paginas/NoticiasESP/IMPE-2025.aspx) cita **2034** si se mantiene **300.000/año** | No |
| **Meta IMPE 2030** | ~**490.000** personas/año × 6 años (IMPE p. 33) | 490.000 × 6 = **2.940.000** ≈ 2,9 M | **6 años** → **2030** | Sí (por construcción del escenario) |

#### B.2 Ritmo en puntos porcentuales (incidencia)

| Concepto | Valor |
|----------|--------|
| Brecha incidencia | 15,4% − 9,5% = **5,9 p.p.** |
| Ritmo observado 2022–2024 | 1,5 p.p. / 2 años = **0,75 p.p./año** (IMPE p. 12 y p. 33) |
| Años al ritmo 0,75 | 5,9 ÷ 0,75 = **7,87 años** → ~**2032** | 
| Ritmo requerido (informe) | **≥ 1,0 p.p./año** (IMPE p. 33) |
| Años a 1,0 p.p./año | 5,9 ÷ 1,0 = **5,9 años** → ~**2030** |

*Nota:* No extrapolar **9,5%** como “cero pobreza”; es la meta del escenario IMPE, no erradicación total.

---

### C. Rutas para cerrar la brecha (evidencia + encaje cooperativo)

Cada ruta indica **dimensión / indicador IMPE** (peso dimensión acceso y calidad **40%** salvo donde aplica vivienda, aprender, territorio).

#### 1) Calidad y continuidad eléctrica + no convencionales en última milla

- **Qué es:** Mejorar **calidad de la energía eléctrica** (interrupciones) e implementar **solar / híbrido / microrred** donde la red es débil o ausente.  
- **IMPE:** Dimensión **Acceso y calidad de la energía** — indicadores **acceso a electricidad** (13,3%) y **calidad del servicio** (13,3%); apuesta 1 IMPE pp. 33–34.  
- **Escala citada:** UPME conectó **539.351** viviendas nuevas en 2024 (**ICEE** 93,12%); PIEC 2024–2028 estima **32,23 billones COP** inversión universalización ([UPME PIEC](https://www.upme.gov.co/simec/planeacion-energetica/plan-de-expansion-de-cobertura/)); **148** comunidades energéticas La Guajira, **1.409 familias** ([IPSE](https://ipse.gov.co/blog/2024/12/20/gobierno-nacional-entrega-80-comunidades-en-la-guajira/)); meta nacional **500 comunidades 2024–2025**, **40% ZNI** ([FENOGE](https://fenoge.gov.co/minenergia-y-fenoge-inician-el-proceso-de-contratacion-para-la-implementacion-de-comunidades-energeticas/)).  
- **Referencia costo (histórico, no 2030):** PIEC 2019–2023: **8,93 billones COP / 486.637 viviendas** ≈ **18,3 M COP/vivienda** (orden de magnitud; solución varía por sitio).  
- **Propuesta CTH Energy Coop *(propuesta, no hecho)*:** Modelo **cooperativo / comunidad energética** para reparto de beneficio, O&M local y gobernanza en proyectos FENOGE-ZNI (p. ej. pantalla 2 demo La Guajira), complementando utility/IPSE sin sustituir ICEE oficial.

#### 2) Sustitución de leña y combustibles sólidos (gas, GLP, inducción)

- **Qué es:** Implementar **Plan Nacional de Sustitución de Leña (PNSL)** y conversiones **leña/GLP → gas natural**.  
- **IMPE:** **Energético adecuado para cocinar**; **Estufa de gas o eléctrica**; privación nacional **9,9%** (2024); **56,6%** de pobres energéticos aún en leña/carbón/desechos (IMPE 2025). Meta simulación: **~540 mil hogares** (IMPE p. 34).  
- **Escala citada:** Promigas **109.727** conversiones GLP/leña a gas (**2024**, IIG prosperidad); **56.083** conversiones (**2025**, [IIG 2025 web](https://www.promigas.com/Paginas/Especiales/Informe-gestion-2025.aspx)); PNSL orienta sustitución gradual ([UPME / Bancolombia citing DANE](https://www.bancolombia.com/empresas/capital-inteligente/actualidad-economica-sectorial/rol-gas-natural-sustitucion-lena)).  
- **Propuesta CTH *(propuesta)*:** Cooperativa como **canal de adopción** (educación, financiación grupal, inducción eficiente) alineada a apuesta 2 IMPE, especialmente Caribe/Chocó/rural.

#### 3) Dotación y “Modo ON” (electrodomésticos, digitalización)

- **Qué es:** Nevera, lavadora, conectividad — uso productivo de la energía.  
- **IMPE:** Dimensión **Vivienda funcional** (nevera, lavadora, estufa, espacio cocina) y **Aprender y comunicarse** (internet, smartphone, etc.).  
- **Escala citada:** Programa **Brilla** — financiación inclusiva para bienes esenciales (IIG 2024); FENOGE **Hogares Energéticamente Sostenibles** — **>2.000 familias** Cali, ahorros factura **30–100%** ([FENOGE](https://fenoge.gov.co/cali-brillara-con-energia-solar-100-nuevos-hogares-seran-beneficiados-por-el-programa-hogares-energeticamente-sostenibles/)).  
- **Propuesta CTH *(propuesta)*:** Paquetes **coop + Brilla-like** para electrodomésticos eficientes vinculados a indicadores IMPE (nevera/lavadora), con trazabilidad de salida de privación.

#### 4) Electrificación educativa (colegios)

- **Qué es:** Electricidad continua en **1.300–1.800** colegios (meta escenario IMPE p. 34).  
- **IMPE:** Indicador **estudiantes en colegios con electricidad** (dimensión **Territorio equipado para el bienestar**).  
- **Escala citada:** Solo meta cualitativa/cuantitativa en IMPE 2025; **PARCIAL** en segunda fuente independiente en este ticket.  
- **Propuesta CTH *(propuesta)*:** Articular demo **CEOF wizard (pantalla 3)** como **plantilla de gobernanza/financiación**, no como dato real — facilitación post-electrificación (efficiency, mantenimiento comunitario).

#### 5) Aceleración territorial (La Guajira, Caribe, Amazonía)

- **Qué es:** Política diferenciada donde IMPE departamental es máximo (**La Guajira 63,1%**, 2024) e **ICEE** bajo (**54,28%**).  
- **IMPE:** Cierre brecha centro–periferia; microsimulación con reducciones dept. hasta **20 p.p.** (IMPE p. 35).  
- **Escala citada:** **Misión La Guajira** — **>3.000 familias** (~25.000 beneficiarios) agua/energía (IIG 2024); IPSE/FENOGE en Guajira (arriba).  
- **Propuesta CTH *(propuesta)*:** **Cooperativa multi-stakeholder** (Promigas, FENOGE, comunidad Wayúu, cooperación internacional) para escalar post-piloto **Paiva** (pantalla 1) con métricas IMPE/ICEE locales.

---

### D. Mensaje sugerido para la reunión (1 frase)

Promigas ancla el debate país en **IMPE 9,5% en 2030** (−**2,9 M** personas), pero el ritmo observado (**~300 k/año**, **0,75 p.p./año**) deja la meta en **~2033–2034** salvo aceleración (**~490 k/año**, **≥1 p.p./año**) vía las **cuatro apuestas** — donde cooperación holandesa puede apoyar **comunidades energéticas, PNSL y equipamiento**, sin confundir **IMPE** con **IPEM MinEnergía (22,3% hogares)** ni con metas **climáticas 2040**.
