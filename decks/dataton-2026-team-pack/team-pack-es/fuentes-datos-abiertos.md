# Fuentes de datos abiertos — panel Paisaje

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es |
| Fecha | 2026-11-21 |
| Uso | Panel **Paisaje** en Hoja 3 — solo contexto; anote licencia en Hoja 2 |
| **Fecha de verificación** | **2026-11-21** (HTTP GET, sigue redirecciones) |

Solo aparecen URLs que respondieron con **página cargable (HTTP 200)**. Las fallidas se omiten.

---

## Cómo buscar por sector (cualquier equipo)

1. **datos.gov.co** — en el inicio, abra **Explorar** o use el navegador por categoría (Ambiente, Salud, Economía, etc.) y filtre por palabra clave de su sector.
2. **DANE** (estadísticas nacionales) — consulte por tema (demografía, economía, territorio, etc.) en el portal del Departamento Administrativo Nacional de Estadística. *Desde este entorno de verificación (2026-11-21), las URLs públicas de dane.gov.co devolvieron **403**; confirme en el navegador del equipo antes de citar un enlace concreto en Hoja 2/3.*

| Recurso | URL | Verificación |
|---|---|---|
| datos.gov.co (inicio) | https://www.datos.gov.co/ | **200** |
| Explorar conjuntos | https://www.datos.gov.co/browse | **200** |
| Herramientas datos.gov.co | https://herramientas.datos.gov.co/ | **200** |
| Ejemplo: categoría Salud | https://www.datos.gov.co/browse?category=Salud | **200** |
| Ejemplo: categoría Economía | https://www.datos.gov.co/browse?category=Econom%C3%ADa | **200** |

**Nota:** Las secciones siguientes sobre **calidad del aire en Bogotá/Colombia** son un **ejemplo del piloto Air4U**. Su equipo debe elegir conjuntos de paisaje acordes a su sector y decisión en Hoja 3.

---

## Ejemplo piloto Air4U — calidad del aire (datos.gov.co)

| Fuente | URL | Verificación |
|---|---|---|
| Ambiente → «calidad del aire» | https://www.datos.gov.co/browse?category=Ambiente&q=calidad%20del%20aire | **200** |

---

## Bogotá D.C. — estaciones y contaminantes (datos.gov.co)

| Conjunto (título en portal) | URL | Verificación |
|---|---|---|
| Estación de calidad del aire. Bogotá D.C. | https://www.datos.gov.co/d/j4s3-udyr | **200** |
| PM 10 promedio anual. Bogotá D.C | https://www.datos.gov.co/d/eziv-qfph | **200** |
| PM 2,5 promedio anual. Bogotá D.C | https://www.datos.gov.co/d/aef2-hm52 | **200** |

---

## Colombia — calidad del aire (datos.gov.co)

| Conjunto | URL | Verificación |
|---|---|---|
| Calidad del Aire en Colombia | https://www.datos.gov.co/d/g4t8-zkc3 | **200** |
| Calidad del Aire en Colombia (Promedio Anual) | https://www.datos.gov.co/d/kekd-7v7h | **200** |
| Mapa Calidad Del Aire En Colombia (Promedio Anual) | https://www.datos.gov.co/d/yvig-r7vx | **200** |

---

## Contexto institucional (Bogotá)

| Fuente | URL | Verificación | Nota |
|---|---|---|---|
| Secretaría Distrital de Ambiente — Calidad del aire | https://www.ambientebogota.gov.co/web/sda/calidad-del-aire | **200** | Política y programa |
| RMCAB (red de monitoreo automático) | https://rmcab.ambientebogota.gov.co/ | **200** | Portal de la red |

---

## Verificadas y descartadas (no cite hasta revalidar)

| URL | Resultado 2026-11-21 |
|---|---|
| https://www.dane.gov.co/ | **403** (bloqueo desde entorno de verificación) |
| https://www.ideam.gov.co/ | Sin respuesta / timeout |
| https://www.rmcab.gov.co/ | Conexión fallida (use rmcab.ambientebogota.gov.co) |
| https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Calidad-del-aire-Bogot-DC- | **404** |
| https://catalogodatos.mintic.gov.co/ | Conexión fallida |

---

## Cómo usar esta lista

1. Elija **uno o dos** conjuntos de paisaje que apoyen su decisión (p. ej. PM exterior para producto indoor).
2. En Hoja 2/3 anote dueño, licencia, actualización y cobertura geográfica.
3. Los números de paisaje siguen la regla **Plata+ = firme / Bronce o menos = estimado**.
4. Antes de un tablero **público**, vuelva a verificar enlaces.