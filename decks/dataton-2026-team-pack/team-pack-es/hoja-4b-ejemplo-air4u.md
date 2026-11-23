# Hoja 4b — Ejemplo Air4U (relleno) · una clínica en Bogotá (piloto)

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es (ilustrativo) |
| Fecha | 2026-11-21 |
| Fuente de números | Ejemplo estricto del método CTH (sin exportación real del piloto) |
| Cliente | Solo «una clínica en Bogotá (piloto)» — sin nombre propio |
| Estado | Ejemplo de mesa; la empresa piloto no ha diligenciado las hojas |

---

## Encabezado

| Campo | Valor |
|---|---|
| Usuario (rol) | Gestor de instalaciones / sitio en la clínica piloto (Bogotá) |
| Decisión (una frase) | ¿Debe activar ventilación extra o revisión de filtros **esta semana** porque el PM₂.₅ en interior podría superar la referencia OMS en su sitio? |

*Referencia de redacción:* ¿Qué decisión concreta enfrentan esta semana?

---

## Tres paneles + puente de valor

<div class="callout-delta">Delta: donde el dato se vuelve valor — Línea base + Paisaje → Delta → valor</div>

### Panel 1 — Línea base del cliente · N1

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** (el BMC no declara cifra de PM₂.₅ en interior) |
| Rango (o +/-) | **[sin dato]** |
| Unidad | µg/m³ (métrica nombrada en el ejemplo) |
| Fuente | D1 — lecturas del sensor en sitio |
| Grada escalera | **Ninguno** |
| Confianza | **estimado** |
| Por qué (una línea) | Valor no declarado en el BMC; línea base del piloto citada sin cifra exportable |

*Supuestos (N1):* sin lecturas de interior almacenadas en el piloto.

### Panel 2 — Delta del innovador · N2

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** (brecha interior − referencia; no calculable sin N1) |
| Rango (o +/-) | Referencia **5 µg/m³** (media anual OMS PM₂.₅, usada como referencia) |
| Unidad | µg/m³ |
| Fuente | D1 |
| Grada escalera | **Ninguno** |
| Confianza | **estimado** |
| Por qué (una línea) | Referencia identificada pero no aplicada a lecturas almacenadas; sin línea base (N1) no hay brecha |

*Supuestos (N2):* referencia OMS definida; sin cálculo de brecha sin N1.

### Panel 3 — Panorama de datos abiertos · N3

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** |
| Rango (o +/-) | **[sin dato]** |
| Unidad | µg/m³ (contexto PM₂.₅ exterior) |
| Fuente | **[sin dato]** — capa paisaje sin conjunto de datos enlazado |
| Grada escalera | **Ninguno** (fuente abierta no elegida) |
| Confianza | **estimado** |
| Por qué (una línea) | Datos abiertos de aire ambiente = Paisaje (fuente por elegir) |

*Supuestos (N3):* paisaje sin enlace a datos.gov ni IDEAM en este ejemplo.

### Puente — Delta: donde el dato se vuelve valor

| Enlace | Detalle |
|---|---|
| Entradas | Línea base (D1, sin cifra) + Paisaje (sin fuente abierta aún) |
| Salida | Delta: seguimiento en operación frente a referencia OMS (sin brecha calculable) |
| Hacia el pie | Ver línea de valor abajo |

*Boceto de tablero:* tres paneles etiquetados; gradas **Ninguno** en el ejemplo estricto.

---

## Antes / después (un solo sitio — clínica piloto)

*Etiqueta usada:* **antes/después** (un sitio piloto; no mapa de varios sitios).

| Antes | Después (monitoreo con intervención Air4U) |
|---|---|
| Período de línea base del piloto — PM₂.₅ en interior: **[sin dato]** | Seguimiento frente a referencia OMS — brecha: **[sin dato]** |
| Nota: sin reidentificar sitio en mapa público | Misma restricción de audiencia interna |

| Contexto exterior (paisaje) | Detalle |
|---|---|
| PM₂.₅ ambiental Bogotá | **[sin dato]** — fuente por definir |

---

## Pie de página

| Línea de valor | Actuar esta semana evita aire interior poco saludable prolongado, protege salud de pacientes y personal y reduce riesgo de perder confianza en el piloto. |
|---|---|

**Texto fijo:** *sin tablero público mientras los derechos de datos estén abiertos*

*Audiencia:* tablero público **No** (propiedad **ABIERTO**, asesoría jurídica pendiente).

---

**Equipo:** Air4U (ilustrativo)  **Fecha:** 2026-11-21