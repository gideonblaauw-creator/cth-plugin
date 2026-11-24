# Hoja 2 — Flujo que genera datos y escalera Medallion (¿QUÉ?) · Bloque 2

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es |
| Fecha | 2026-11-21 |
| Quién diligencia | Fundador + operador del flujo |
| Tiempo | ~10–15 min por tarjeta + tiempo de subida |
| Entrada | Bloques elegidos del Bloque 1 (o tarjeta de arranque abajo) |

## Para qué sirve

En la mañana ubicó **dónde** están los datos. Ahora describe **qué flujo** los produce y **sube la escalera Medallion**: Bronce › Plata › Oro.

**Empezar por debajo de Bronce es normal.** La tarde es la siguiente grada, no un reproche.

## Parte A — Preguntas del flujo (una tarjeta por bloque elegido)

| # | Pregunta | Guía breve |
|---|---|---|
| A1 | Bloque(s) e ID de datos | Del Bloque 1 |
| A2 | Nombre del flujo | Verbo + objeto |
| A3 | Evento disparador | Lo que crea un registro nuevo |
| A4 | Pasos | 3–8 pasos numerados |
| A5 | Actores (roles, no nombres) | |
| A6 | Sistemas / dispositivos | |
| A7 | Campos que produce un registro | |
| A8 | Unidad y granularidad | |
| A9 | Frecuencia y volumen (U si no sabe) | |
| A10 | Controles de calidad / calibración | |
| A11 | Huecos y pasos manuales | |
| A12 | Propiedad, consentimiento, límites legales | Escriba **ABIERTO** si hay duda |
| A13 | Capa sandbox | Delta / Línea base / Paisaje |
| A14 | **Tarea + audiencia (obligatorio)** | «[tarea] para [audiencia]» |
| A15 | Desacuerdos fundador / operador | |

## Parte B — Escalera Medallion

Responda **S** o **N** en cada ítem. **U = N.** El nivel es el más alto donde **todo** es S y las gradas inferiores también.

### Grada 1 — Bronce (registro crudo, accesible)

| # | Verificación | S/N |
|---|---|---|
| B1 | Registros crudos sin alterar | |
| B2 | Fecha-hora en cada registro | |
| B3 | ID de origen | |
| B4 | Unidades en campos numéricos | |
| B5 | Almacenamiento nombrado y responsable (sin REO) | |
| B6 | Derechos por escrito (G ≥ 2) | |
| B7 | Exportación estructurada (A ≥ 2) | |

### Grada 2 — Plata (limpios, validados)

| # | Verificación | S/N |
|---|---|---|
| S1 | Reglas de limpieza escritas | |
| S2 | Validación contra referencia | |
| S3 | Unidades y zona horaria estandarizadas | |
| S4 | Completitud, duplicados y huecos medidos (Q = 3) | |
| S5 | Diccionario de datos | |
| S6 | Datos personales o confidenciales anonimizados | |

### Grada 3 — Oro (tarea y audiencia nombradas)

| # | Verificación | S/N |
|---|---|---|
| G1 | Tarea + audiencia en A14 | |
| G2 | Referencia o punto de comparación aplicado | |
| G3 | Nivel de agregación fijo | |
| G4 | Dueño aprobó compartir con esa audiencia | |
| G5 | Pasos documentados para repetir | |
| G6 | Capa sandbox etiquetada | |
| G7 | Sin asuntos legales ABIERTOS en A12 | |
| G8 | Sin tablero público si derechos abiertos | |
| G9 | Si combina capas: riesgo de reidentificación revisado | |

| Nivel alcanzado | Significado breve |
|---|---|
| Ninguno | Debajo de Bronce — común al inicio |
| Bronce | Guardado, accesible, derechos claros |
| Plata | Fiel: limpio y calidad conocida |
| Oro | Listo para la tarea de A14 |

## Parte C — Plantilla de tarjeta de flujo (bloque con datos del Bloque 1)

Use una tarjeta por bloque elegido. Esta plantilla va **con** la escalera Medallion (Parte B).

```
TARJETA DE FLUJO · Equipo: ______ · Fecha: ______
Bloque(s) / ID datos : ______________________
Flujo              : ______________________________
Disparador         : ______________________________
Línea de flujo de datos   : Disparador › Captura [sistema] › Almacén [Bronce]
                     › Limpiar [Plata] › Referencia [Oro] › Tarea + audiencia [A14]
Nivel alcanzado    : Ninguno / Bronce / Plata / Oro
Siguiente grada    : Los «N» de la siguiente grada: ______________
```

---

## Tarjeta de arranque de datos *(aparte de la escalera Medallion)*

> **Esto no es la escalera:** es una tarjeta de arranque para cuando aún no hay datos formales.

Use **solo** si en Bloque 1 **ningún** bloque quedó tibio/caliente con vínculo VP ≥ 2. No sustituye la Parte B; responda las mismas preguntas de flujo (Parte A) y marque honestamente su nivel en la escalera.

Elija el conjunto con **mayor L** en Propuestas de valor (si empata, el de mayor evidencia D).

```
TARJETA DE ARRANQUE · Equipo: ______ · Fecha: ______
Motivo: Sin bloque VP tibio en Bloque 1
[ID, mismos campos que arriba hasta MEDALLION]
```

Ayuda del mentor: **un** paso de captura mejorable esta semana (copia maestra, responsable o consentimiento), no rehacer toda la plataforma.

---

Después continúe con **Hoja 3 — De dato a valor**.