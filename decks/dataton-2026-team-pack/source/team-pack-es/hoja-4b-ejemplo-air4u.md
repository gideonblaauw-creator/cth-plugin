# Hoja 4b — Ejemplo Air4U (relleno) · una clínica en Bogotá (piloto)

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es (ilustrativo) |
| Fecha | 2026-11-21 |
| Fuente de números | Drive `q3-worked-example.md` (`1-xlrQBGIwS7Dtd6SueqHG-ZHBQQz9G08`) — escenario estricto |
| Cliente | Solo «una clínica en Bogotá (piloto)» — sin nombre propio |
| Estado | Ejemplo de mesa; la empresa piloto no ha diligenciado las hojas |

---

## Encabezado

| Usuario (rol) | Gestor de instalaciones / sitio en la clínica piloto (Bogotá) |
|---|---|

| Decisión (una frase) | ¿Debe activar ventilación extra o revisión de filtros **esta semana** porque el PM₂.₅ indoor podría superar la referencia OMS en su sitio? |
|---|---|

*Citación decisión:* `1-xlrQBGIwS7Dtd6SueqHG-ZHBQQz9G08` §2 «What one decision do they face?»

---

## Tres paneles + puente de valor

```
                    ┌──────────────────────────────────────┐
                    │ Delta: donde el dato se vuelve valor  │
                    │  Línea base + Paisaje ──► Delta ──► valor │
                    └──────────────────────────────────────┘
```

### Panel 1 — Línea base del cliente · N1

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** (el BMC no declara cifra de PM₂.₅ indoor) |
| Rango (o +/-) | **[sin dato]** |
| Unidad | µg/m³ (métrica nombrada en el ejemplo) |
| Fuente | D1 — lecturas sensor Air4U Track |
| Grada escalera | **Ninguno** |
| Confianza | **estimado** |
| Por qué (una línea) | Valor no declarado en BMC; baseline del piloto citado sin cifra exportable |

*Citación:* mismo archivo §4 fila N1 y § «Assumptions» (N1).

### Panel 2 — Delta del innovador · N2

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** (brecha indoor − referencia; no calculable sin N1) |
| Rango (o +/-) | Referencia **5 µg/m³** (media anual OMS PM₂.₅, usada como benchmark nombrado en la tarea borrador Q2) |
| Unidad | µg/m³ |
| Fuente | D1 |
| Grada escalera | **Ninguno** |
| Confianza | **estimado** |
| Por qué (una línea) | G2 = N: referencia identificada pero no aplicada a lecturas almacenadas; sin N1 no hay brecha |

*Citación:* mismo archivo §4 fila N2, §3 Q2, § «Assumptions» (N2).

### Panel 3 — Panorama de datos abiertos · N3

| Campo | Respuesta |
|---|---|
| Valor | **[sin dato]** |
| Rango (o +/-) | **[sin dato]** |
| Unidad | µg/m³ (contexto PM₂.₅ exterior) |
| Fuente | **[sin dato]** — capa paisaje sin dataset enlazado |
| Grada escalera | **Ninguno** (fuente abierta no elegida) |
| Confianza | **estimado** |
| Por qué (una línea) | «public ambient air data = Landscape (source to choose)» en el ejemplo estricto |

*Citación:* mismo archivo §4 fila N3 y § «Assumptions» (N3).

### Puente — Delta: donde el dato se vuelve valor

| Enlaces | |
|---|---|
| Entradas | Línea base (D1, sin cifra) + Paisaje (sin fuente abierta aún) |
| Salida | Delta: seguimiento en operación vs referencia OMS (sin brecha calculable) |
| Hacia el pie | Ver línea de valor abajo |

*Citación:* mismo archivo §7 «Dashboard sketch» (paneles y etiquetas None).

---

## Antes / después (un solo sitio — clínica piloto)

*Etiqueta usada:* **antes/después** (un sitio piloto; no mapa multi-sitio).

| Antes | Después (monitoreo con intervención Air4U) |
|---|---|
| Período baseline piloto — PM₂.₅ indoor: **[sin dato]** | Seguimiento vs referencia OMS — brecha: **[sin dato]** |
| Nota: sin reidentificar sitio en mapa público | Misma restricción de audiencia interna |

*Citación:* mismo archivo §7 notas bajo paneles («baseline period pilot», «guideline gap»).

| Contexto exterior (paisaje) | |
|---|---|
| PM₂.₅ ambiental Bogotá | **[sin dato]** — fuente TBD |

*Citación:* mismo archivo §7 («Bogotá ambient (TBD)»).

---

## Pie de página

| Línea de valor | Actuar esta semana evita aire indoor poco saludable prolongado, protege salud de pacientes y personal y reduce riesgo de perder confianza en el piloto. |
|---|---|

*Citación:* mismo archivo §5 «Worth (one sentence)».

**Texto fijo:** *sin tablero público mientras los derechos de datos estén abiertos*

*Citación audiencia:* mismo archivo §6 — public dashboard **No** (ownership OPEN, legal advice pending).

---

**Equipo:** Air4U (ilustrativo)  **Fecha:** 2026-11-21