# FENOGE public data — solar / ZNI / Comunidades Energéticas (Colombia)

**Desk:** Energy Coop (CleantechHUB)  
**Date:** 2026-11-03  
**Scope:** Public sources only for project-level intelligence on solar and off-grid (ZNI) work financed or executed by [FENOGE](https://www.fenoge.gov.co/), plus adjacent open data (IPSE/CNM, SECOP, MinEnergía).  
**Samples:** `data/energy-coop/fenoge/` (CSV/JSON extracts; see README).

---

## 1. Fiduciary structure and where contracts appear

| Element | Public description | Source |
|--------|---------------------|--------|
| Legal nature | FENOGE is a **patrimonio autónomo** (special-purpose fund), not a standard contracting agency with its own SECOP profile. | [FENOGE — ¿Quieres participar en contratación?](https://fenoge.gov.co/quieres-participar-en-nuestros-procesos-de-contratacion/) |
| Fideicomitente | **Ministerio de Minas y Energía** publishes FENOGE procurement and many derived contracts in **SECOP I/II** under the Ministry user. | Same; [Histórico procesos](https://fenoge.gov.co/historico/) |
| Fiduciary (fiducia) | Mercantile trust contract for recaudo, administration, investment, disbursement of FENOGE resources (e.g. **Consorcio PACC FENOGE 2023**, ~\$3.68B COP, 2023). | SECOP sample `secop2-contratos-fenoge_ref.csv`; contract `GGC-961-2023` |
| Process mirror | FENOGE publishes **invitaciones / LPI** on fenoge.gov.co with links to SECOP II notice UIDs. | [Contratación FENOGE](https://fenoge.gov.co/quieres-participar-en-nuestros-procesos-de-contratacion/) |
| MinEnergía NIT (SECOP) | **899999022** — use for `datos.gov.co` SECOP II API filters. | Socrata query 2026-11-03 |

**Implication for demos:** contract **values and contractors** are discoverable via SECOP + FENOGE PDFs; **geo-project registries** (500 comunidades, vereda-level kWp) are mostly in **process annexes and management reports**, not in a single open CSV.

---

## 2. Source table

| Source | URL | What it contains | Downloadable | Format | Usefulness (1–5) |
|--------|-----|------------------|--------------|--------|------------------|
| FENOGE contratación + histórico | https://fenoge.gov.co/quieres-participar-en-nuestros-procesos-de-contratacion/ , https://fenoge.gov.co/historico/ | IA/LPI/IC processes; SECOP links; fiduciary note | Partial (PDFs per process) | Web + SECOP | **5** — primary index for FENOGE solar/ZNI procurement |
| FENOGE project sheets | https://fenoge.gov.co/proyectos/comunidad-energetica-de-bahia-malaga/ (and press under `/proyectos/`) | Named sites, kWp, veredas, beneficiaries (narrative) | Y (page text/PDF links) | HTML | **4** — best project “cards” when published |
| FENOGE rendición / informes | https://fenoge.gov.co/rendicion-de-cuentas/ , https://www.minenergia.gov.co/documents/12628/informeGestion-FENOGE-2024.pdf , https://fenoge.gov.co/documentos-pdf/RendicionCuentas/Informe_Gestion_DireccionEjec2025.pdf | Portfolio status, AFPEI names, budgets, % execution (Nazareth, Bahía Málaga, Colombia Solar) | Y | PDF | **5** — aggregate + contract IDs; not GIS |
| SECOP II Contratos (MinEnergía) | https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h | Adjudicatario, value, dates, `descripcion_del_proceso`, `urlproceso` | Y | CSV/JSON API | **4** — money & operator; weak on lat/long |
| SECOP II Procesos | https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Procesos-de-Contrataci-n/p6dx-8zbt | Procedure metadata, phases, base price | Y | CSV/JSON API | **3** — discovery; object text truncated |
| Colombia Compra / SECOP UI | https://community.secop.gov.co/ | Full pliegos, addenda, adjudication acts | Per process | Web/PDF | **5** — authoritative detail when API lacks fields |
| MinEnergía noticias | https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/ | Press-level beneficiaries, kWp, territory | Y (HTML/PDF) | HTML | **4** — La Guajira / ZNI announcements |
| Resolución 40137 / 40509 (focalización CE) | https://gestornormativo.creg.gov.co/gestor/entorno/docs/resolucion_minminas_40137_2024.htm , https://normograma.mintic.gov.co/mintic/compilacion/docs/resolucion_minminas_40509_2024.htm | CE targeting rules (40137 derogated by 40509) | Y | HTML | **2** — policy, not project list |
| RCE list (CE registered) | https://minciencias.gov.co/sites/default/files/upload/convocatoria/listado_comunidades_energeticas_rce.pdf | Registered comunidades energéticas (mostly SIN/educational) | Y | PDF | **3** — names/locations; not FENOGE spend |
| IPSE datos abiertos | https://ipse.gov.co/mapa-del-sitio/ipse-scucha-atencion-al-ciudadano/datos-abiertos/ | Pointer to datos.gov.co IPSE datasets | Via portal | Web | **3** — ZNI context |
| CNM / telemetría ZNI | https://ipse.gov.co/cnm/ , https://ipse.gov.co/cnm/prestacion-del-servicio/ | Monthly telemetry PDFs; service monitoring | Y (PDF) | PDF | **3** — operation, rarely FENOGE-tagged |
| ZNI service status (Socrata) | https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g | Monthly energy & avg daily hours by locality | Y | CSV/API | **3** — baseline ZNI service; stale years in sample |
| ZNI localities catalog | https://www.datos.gov.co/Minas-y-Energ-a/Zonas-No-Interconectadas/qp2c-ddtg | ZNI geography catalog | Y (portal); API empty in sample | CSV | **2** — geography; verify export |
| IPSE Miichi Ka'i Guajira (related, not FENOGE) | https://ipse.gov.co/blog/2024/12/20/gobierno-nacional-entrega-80-comunidades-en-la-guajira/ | 80 CE in Guajira, \$47B COP, microrredes | N (narrative) | HTML | **3** — scale story; IPSE-led |
| Contraloría / Congreso | Search on https://www.contraloria.gov.co/ , https://www.corteconstitucional.gov.co/ | Execution audits (FENOGE cited in 2025 empalme report annex) | Case-by-case | PDF | **2** — oversight; not project GIS |
| FENOGE transparencia (Ley 1712) | https://fenoge.gov.co/transparencia/ (intermittent 500 errors 2026-11-03) | PTEP, PAA, normatividad | Partial | Web | **3** — when stable |

**Last-update notes (observed 2026-11-03):** SECOP open-data feeds update continuously; dataset `3ebi-d83g` metadata `rowsUpdatedAt` ≈ late 2026 on portal; sample rows still show **2020** monthly records. FENOGE web pages show **2026** process dates on contratación index.

---

## 3. Concrete FENOGE-linked projects (public citations)

Table lists **documented** sites where FENOGE is named as executor/financier for solar or ZNI hybrid work. Figures come **only** from cited pages/PDFs.

| # | Project / programme | Location | Beneficiaries / households | kWp / capacity | Cost / FENOGE contribution | Operator / contractor (if public) | Status (as stated) | Date / source |
|---|---------------------|----------|----------------------------|----------------|------------------------------|-----------------------------------|-------------------|---------------|
| 1 | Comunidad Energética Bahía Málaga (híbrido solar–diésel) | Veredas La Plata, Miramar, Mangaña, La Sierpe; corregimiento Bahía Málaga, Buenaventura, Valle | 235 familias (2023 launch); later 291–293 usuarios | **208 kWp** total (178 microrred + 30 aislado); 327 panels cited in 2025 press | >\$12B COP (2023); >\$16B COP (2025 project sheet) | Not in press release | Implementación / ampliación | [FENOGE 2023](https://fenoge.gov.co/en-el-pacifico-colombiano-y-en-el-marco-de-comunidades-energeticas-se-implementara-un-sistema-innovador-hibrido-solar-diesel-en-zni-inaugurado-por-minenergia-y-fenoge/) , [project sheet](https://fenoge.gov.co/proyectos/comunidad-energetica-de-bahia-malaga/) , [MinEnergía 2025](https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/comunidades-negras-en-bah%C3%ADa-m%C3%A1laga-contar%C3%A1n-con-24-horas-de-energ%C3%ADa-diarias-gracias-a-la-energ%C3%ADa-solar/) |
| 2 | SSFV + almacenamiento Nazareth & Puerto Estrella | Corregimientos Nazareth y Puerto Estrella, Uribia, **La Guajira** | >800 usuarios (2026 social update) | Not in IA page (engineering in SECOP pliego) | AFPEI mod. **~\$22.4B COP** cited in Informe Gestión 2025 table | IA-001-2025 adjudication referenced in informe | Obra ~30% físico / en alistamiento (2026) | [IA-006-2024 page](https://fenoge.gov.co/invitacion-abietno-006-de-2024-ia-006-2024-fenoge/) (coords **12.199722, -71.263889**), [Informe Gestión 2025 PDF](https://fenoge.gov.co/documentos-pdf/RendicionCuentas/Informe_Gestion_DireccionEjec2025.pdf) |
| 3 | Granja solar Cabo de la Vela & Media Luna | Alta Guajira (Wuayúu territories) | ~1,500 personas; 61 comunidades cited | **1 MW** solar farm | Not published in press note | Not published | Implementación; operación esperada 1S 2025 per 2024 note | [MinEnergía Oct 2024](https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/minenerg%C3%ADa-y-fenoge-instalar%C3%A1n-parque-solar-en-el-cabo-de-la-vela-y-media-luna-que-proveer%C3%A1-energ%C3%ADa-247/) |
| 4 | Energía Solar Población Vulnerable — Maicao | Maicao, La Guajira | ~500 familias (estrato 1–2) | **1,102 kWp**; ~1.98 GWh/año | Part of 14-farm Caribbean programme | FENOGE execution per press | Inaugurado **29 Aug 2025** | [FENOGE](https://fenoge.gov.co/gobierno-nacional-entrega-en-maicao-el-primer-territorio-energetico-de-la-guajira/) |
| 5 | Colombia Solar — Caribbean minigranjas (incl. Maicao) | 7 deptos; municipios Tierralta, San Antonio de Palmito, Arroyohondo, Manatí, Repelón, **Maicao**, Tamalameque, Pailitas | ~12,600 beneficiarios (programme) | ~**900 kW AC** per farm; ~1,830 panels/farm | Programme-level (not per site in note) | FENOGE + MinEnergía | Obras iniciadas en varios municipios (Ene 2025) | [FENOGE Ene 2025](https://fenoge.gov.co/con-la-construccion-de-minigranjas-solares-familias-de-la-region-caribe-veran-una-reduccion-de-hasta-un-35-en-sus-facturas-de-energia-electrica/) |
| 6 | Comunidades Energéticas — Tomarrazón | Tomarrazón, **La Guajira** | 180 familias | 339 × 710 W ≈ **241 kWp** (derived from panel count) | Not in post | Not in post | Socialización / proyecto CE | [FENOGE LinkedIn](https://es.linkedin.com/posts/fenoge_enfotos-comunidadesenerg%C3%A9ticas-tomarraz%C3%B3n-activity-7425237830081249280-9fsM) |
| 7 | AFPEI Comunidades Energéticas (500 CE national) | 16 deptos phase 1 (incl. Guajira, Magdalena); **40% ZNI** | Up to **500** CE; phase 1 **110** CE | IA-004-2024: **22.7 MW** / ~252 CE (SIN-focused process) | Convenio **\$349,375,701,882** COP (MinEnergía–FENOGE) | Selection via IA-003/004 SECOP | IA-004 modified/suspended Nov 2024 | [MinEnergía Sep 2024](https://minenergia.gov.co/es/sala-de-prensa/noticias-index/minenerg%C3%ADa-y-fenoge-abren-proceso-de-contrataci%C3%B3n-para-la-implementaci%C3%B3n-de-500-comunidades-energ%C3%A9ticas/) , [IA-004](https://fenoge.gov.co/invitacion-abierta-no-004-de-2024-ia-004-2024-fenoge/) |
| 8 | EN-Comunidad / Anainjak Wakuaipa (12 comunidades) | Resguardo Alta/Media Guajira (Maicao area) | 250 SSFV target (programme) | Per-system not listed | Convocatoria EN-Comunidad (OIM + FENOGE cited) | Community association + OIM + FENOGE | En implementación (2025 media) | [Las2Orillas](https://www.las2orillas.co/paneles-solares-el-poderoso-tridente-que-le-pondra-energia-con-sol-a-los-wayuu-en-la-guajira/) |
| 9 | Puerto Estrella (IA-008-2026) | La Guajira | In pliego (process open 2026) | In SECOP pliego | In process | TBD | Process **Publicado** 2026 | [FENOGE histórico](https://fenoge.gov.co/historico/) |

**Count:** **9 programme/site rows** with citable public fields; **6** with usable location + beneficiary + capacity for mapping demos.

**Not FENOGE (Promigas demo context — Paiva):** [Fundación Promigas — Paiva pilot](https://fundacionpromigas.org.co/paiva-estrena-el-primer-piloto-de-energia-solar-comunitaria-de-promigas-y-su-fundacion/) documents **vereda Paiva, Bolívar** (not La Guajira): ~450 habitantes, IE Chiricoco, **no FENOGE financing**. Promigas also cites **Misión La Guajira** at portfolio level ([Informe 2024](https://gestion2024.promigas.com/es/impulsando-el-desarrollo-page-8)).

**Adjacent public ZNI (IPSE, not FENOGE):** [80 comunidades Miichi Ka'i, Guajira](https://ipse.gov.co/blog/2024/12/20/gobierno-nacional-entrega-80-comunidades-en-la-guajira/) — \$47B COP, 148 CE total planned with IPSE.

---

## 4. SECOP / datos.gov.co usage notes

- Filter **`nit_entidad = '899999022'`** (Ministerio de Minas y Energía), then search `descripcion_del_proceso` / `referencia_del_contrato` for `FENOGE`, `SOLAR`, `FOTOVOL`, `ZNI`, `NAZARETH`, `COMUNIDAD`.
- Fiduciary contracts explicitly name FENOGE (see sample CSV); **many obra contracts** use codes like `116231-114-2024` without “FENOGE” in the description — crosswalk via [Informe Gestión 2025 PDF](https://fenoge.gov.co/documentos-pdf/RendicionCuentas/Informe_Gestion_DireccionEjec2025.pdf) or SECOP notice UID from fenoge.gov.co.
- No dedicated **“FENOGE projects”** dataset on datos.gov.co was found; SECOP aggregates are the practical open-data path.

---

## 5. Gaps and formal information requests

| Gap | Why it matters | Suggested request |
|-----|----------------|-------------------|
| Single geocoded registry of FENOGE ZNI/solar assets | Demo map layer | Annexes of AFPEI “Comunidades Energéticas” + IA evaluation reports |
| Per-project FENOGE vs cofinancing split | Finance story | Fiduciary payment schedule + AFPEI financial tables |
| Adjudicatarios for Nazareth / Cabo de la Vela obra | Operator field in coop model | SECOP acto de adjudicación PDFs (not always in API) |
| kWp at vereda level for 500 CE programme | Scale metrics | Resolución focalización + prioritized list (MME) |
| Real-time generation for FENOGE ZNI hybrids | Operations | CNM telemetry does not tag FENOGE; ask FENOGE monitoring URLs per project |

### Draft *derecho de petición* (do not send — desk draft)

**Destinatario:** Fondo de Energías No Convencionales y Gestión Eficiente de la Energía — FENOGE (info@fenoge.gov.co), con copia al Ministerio de Minas y Energía — Grupo de Energía Eléctrica.

**Asunto:** Solicitud de información pública — inventario de proyectos solares y ZNI financiados o ejecutados por FENOGE (formato abierto).

En ejercicio del derecho de petición (Ley 1755 de 2015) y acceso a información pública (Ley 1712 de 2014), solicito:

1. Listado maestro (CSV o XLSX) de proyectos **FNCE/solar en ZNI o híbridos** financiados con recursos FENOGE, vigentes 2023–2026, con campos: nombre del proyecto, departamento, municipio, corregimiento/vereda, coordenadas o shapefile, número de usuarios/hogares, kWp instalados o proyectados, valor total del proyecto, aporte FENOGE, contratista/obrero, estado, fecha de inicio/entrega, enlace SECOP del contrato derivado.
2. Anexos técnicos publicados en IA-003/IA-004/IA-006-2024 e IA-001-2025 (listas de comunidades/lotes) en formato editable.
3. Enlace o export del tablero Power BI “PMP 2025” citado en el Informe de Gestión 2025, o equivalente actualizado, con desagregación por iniciativa AFPEI.

**Finalidad:** Investigación y articulación de datos abiertos para comunidades energéticas (sin uso comercial de datos personales).

---

## 6. Recommendation — 11 Nov Promigas demo

| Narrative beat | Data to use | Caveat |
|----------------|-------------|--------|
| **Community pilot (Paiva)** | [Fundación Promigas Paiva](https://fundacionpromigas.org.co/paiva-estrena-el-primer-piloto-de-energia-solar-comunitaria-de-promigas-y-su-fundacion/) — 450 hab., comité comunitario, IE Chiricoco | **Private / CSR**, not FENOGE; Bolívar not Guajira |
| **Department scale (La Guajira)** | Stack **Maicao 1,102 kWp** + **Nazareth/Puerto Estrella** (800+ users, coords on IA page) + **Cabo de la Vela 1 MW** + **Tomarrazón 180 familias** | Mix of **SIN transition** vs **ZNI**; verify ZNI/SIN label per project in pliego |
| **Public money / governance** | FENOGE Informe Gestión 2025 (execution %, \$ Nazareth) + SECOP fiduciary **GGC-961-2023** | Shows state finance chain; heavy PDF work |
| **ZNI baseline (non-FENOGE contrast)** | IPSE [80 CE Guajira](https://ipse.gov.co/blog/2024/12/20/gobierno-nacional-entrega-80-comunidades-en-la-guajira/) + CNM telemetry portal | IPSE-led; good for “ecosystem” slide |
| **Live map demo (realistic v1)** | Pin **4 FENOGE Guajira** sites from table §3 + **Paiva** as separate layer “utility CSR pilot” | Do not imply FENOGE funded Paiva |

**Suggested demo data stack:** (1) manual GeoJSON from §3 coordinates + municipality centroids where coords missing; (2) SECOP sample CSV for contract value on fiduciary; (3) optional CNM monthly PDF for one ZNI locality near Uribia if needed for “operations” footnote.

---

## 7. Top sources (quick index)

1. https://fenoge.gov.co/quieres-participar-en-nuestros-procesos-de-contratacion/  
2. https://fenoge.gov.co/documentos-pdf/RendicionCuentas/Informe_Gestion_DireccionEjec2025.pdf  
3. https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h  
4. https://fenoge.gov.co/proyectos/comunidad-energetica-de-bahia-malaga/  
5. https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/minenerg%C3%ADa-y-fenoge-instalar%C3%A1n-parque-solar-en-el-cabo-de-la-vela-y-media-luna-que-proveer%C3%A1-energ%C3%ADa-247/

---

*Awaiting Gideon's approval if reused in external CleantechHUB communications.*
