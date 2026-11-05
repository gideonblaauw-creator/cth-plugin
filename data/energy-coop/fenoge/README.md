# FENOGE public data samples (Energy Coop desk)

Small extracts pulled **2026-11-03** for desk research. Full datasets are much larger; do not commit bulk downloads.

| File | Source API / portal | Notes |
|------|---------------------|--------|
| `secop2-procesos-minenergia-fenoge.csv` | [SECOP II Procesos (`p6dx-8zbt`)](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Procesos-de-Contrataci-n/p6dx-8zbt) — Socrata `$where` on `entidad` containing Minas + Energía and FENOGE | 100 most recent processes (sample) |
| `secop2-contratos-minenergia-solar-zni.csv` | [SECOP II Contratos (`jbjy-vk9h`)](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h) — `nit_entidad='899999022'` + solar/ZNI/FENOGE keywords in `descripcion_del_proceso` | 80 contracts (sample) |
| `secop2-contratos-fenoge_ref.csv` | Same dataset — `referencia_del_contrato` or description mentions FENOGE | 5 contracts (fiduciary + advisory) |
| `zni-service-status-sample.json` | [Estado prestación ZNI (`3ebi-d83g`)](https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g) — `$limit=3` | Monthly kWh / hours by locality (2020 sample rows) |
| `zni-ipse-sample.json` | [Zonas No Interconectadas (`qp2c-ddtg`)](https://www.datos.gov.co/Minas-y-Energ-a/Zonas-No-Interconectadas/qp2c-ddtg) — `$limit=5` | API returned empty column objects at pull time; use portal export |
| `secop2-minenergia-solar-zni-head.json` | Contratos sample (5 rows) | Head-only JSON for inspection |

**SECOP entity key:** FENOGE contracts are published under the **fideicomitente** [Ministerio de Minas y Energía](https://fenoge.gov.co/quieres-participar-en-nuestros-procesos-de-contratacion/) (`nit_entidad` **899999022**), not a separate FENOGE NIT.
