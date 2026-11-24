# Hoja 1 — Mapa de calor de datos (¿DÓNDE?) · Bloque 1

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es |
| Fecha | 2026-11-21 |
| Evento | Datatón Observatorio de la Tierra (24 nov 2026) |
| Quién diligencia | Equipo fundador; ideal: fundador **y** operador por separado |
| Tiempo | 20–30 minutos |
| Metodología | Fundación CleantechHUB — Datatón |

## Para qué sirve

Esta hoja ubica **dónde** ya hay datos en su Lienzo de Modelo de Negocio (9 bloques). El resultado es un **mapa de calor**: frío, tibio o caliente, con **etiquetas** que muestran qué falta por trabajar.

**Entrada abierta.** Cuenta cualquier dato, incluso lo que solo está en conversaciones o en la memoria (**reo**). No hay puertas de exclusión en la mañana. Las reglas estrictas llegan en el Bloque 2 (escalera medallion).

## Cómo responder

1. Empiece por **Propuestas de valor** (VP1, VP2…). Recorra los 9 bloques. Hasta **3 conjuntos de datos** por bloque.
2. Si no sabe dónde está guardado, igual nómbrelo: llevará la etiqueta **REO**.
3. Si no sabe una respuesta, escriba **U** (desconocido). **No invente números ni cifras.**
4. El mismo conjunto de datos (D1, D2…) puede aparecer en varios bloques.
5. Si un bloque no tiene datos, escriba «ninguno» y continúe.

## Claves de respuesta (iguales en todos los bloques)

### ¿Tiene almacenamiento nombrado? (S)

| Código | Significado |
|---|---|
| Y | Puede decir dónde están los registros hoy |
| N | Sabe que existen pero no dónde → **REO** |

### Confiabilidad (R) — ¿dónde está la copia maestra hoy?

| 0–3 | Significado (resumen) |
|---|---|
| 0 | No registrado |
| 1 | Disperso (chat, papel, memoria). Todo **REO** usa R = 1 |
| 2 | Hoja de cálculo o documento a mano |
| 3 | Sistema con campos fijos (ERP, CRM, facturación, sensores, etc.) |

**Copia maestra.** Si hay chat **y** plataforma, responda: *¿dónde reabriría el mes pasado?* Si no puede nombrar un solo lugar: R = 1, etiqueta **COPIA MAESTRA NO CLARA**.

**Tableros.** Un tablero en vivo **sí cuenta** como dato nombrado en Bloque 1; no sustituye por sí solo una exportación estructurada.

### Historia (H) — meses de registros que aún puede abrir

| 0 | &lt; 3 meses o U |
| 1 | 3–11 |
| 2 | 12–23 |
| 3 | 24 o más |

### Frecuencia (F) — nuevos registros (promedio últimos 3 meses)

| 0 | Ninguno en 12 meses, una sola vez, o U |
| 1 | Al menos una vez en 12 meses, menos que mensual |
| 2 | Al menos mensual, menos que diario |
| 3 | Diario o más (incluye tiempo real) |

### Acceso técnico (A)

| 0 | No recuperable en 1 semana, o U. **REO → A = 0** |
| 1 | Recuperable en 1 semana, pero no como tabla; o sin responsable nombrado |
| 2 | Archivo exportable (CSV, XLSX) **y** responsable nombrado |
| 3 | Exportación automática o API **y** responsable nombrado |

### Calidad (Q) — tres sí/no; Q = cantidad de «sí» (0–3)

- Q-a Completitud (9 de 10 registros con campos clave)
- Q-b Duplicados controlados o raros
- Q-c Sabe qué periodos o sitios faltan

U cuenta como No.

### Acceso legal / ético (G) — etiqueta, no suma al puntaje

| 0–3 | Desconocido / verbal / base escrita / propósito documentado |
| Para datos operativos propios no personales, si deja G en blanco el facilitador usa **G = 2** salvo que usted indique un límite. |

### Modo de captura (M) — etiqueta

IoT · chat · hoja de cálculo · otro

### Vínculo a VP (L) — 0–3

Qué tan directo mide el beneficio que promete una propuesta de valor.

## Tabla por bloque (copie en cada bloque)

| ID | Conjunto de datos | S | R | Meses (texto) | H | Frecuencia (texto) | F | Formato / ubicación | Responsable (rol) | A | Q-a | Q-b | Q-c | Q | G | M | L | ¿VP? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | | | | | | | | | | | | | | | | | | |
| D2 | | | | | | | | | | | | | | | | | | |
| D3 | | | | | | | | | | | | | | | | | | |

Escriba la respuesta en palabras **y** el código.

## Los 9 bloques (preguntas guía)

### 1. Propuestas de valor
Liste VP1, VP2… ¿Mide si el cliente recibe el beneficio prometido? ¿Guarda desempeño del producto/servicio?

### 2. Segmentos de clientes
¿Ventas por tipo de cliente? ¿Ubicación o sector? ¿Lista con campos de segmento?

### 3. Flujos de ingreso
¿Cada venta o factura? ¿Ingresos por producto? ¿Facturación electrónica?

### 4. Canales
¿Canal de cada venta? ¿Analítica web o redes? ¿Lugar de entrega?

### 5. Relaciones con clientes
¿Soporte, garantías, mantenimiento? ¿Reseñas o satisfacción? ¿Renovaciones?

### 6. Actividades clave
¿Producción, instalación, servicio con fechas y sitios? ¿Mediciones de equipos? ¿Control de calidad?

### 7. Recursos clave
¿Inventario, equipos en campo? ¿Datos propios (sensores)? ¿Tiempo de personal?

### 8. Socios clave
¿Órdenes y proveedores? ¿Datos que envían socios? ¿Contratos de propiedad de datos?

### 9. Estructura de costos
¿Costo por unidad o proyecto? ¿Categorías contables? ¿Margen bruto desde registros?

## Verificación de contexto (2 min, una vez)

| Pregunta | Respuesta |
|---|---|
| ¿Algún conjunto tiene datos personales (nombre, correo, teléfono)? | S / N / U |
| ¿Alguno describe un sitio confidencial de cliente? | S / N / U |
| ¿Alguno lo produce o guarda un socio? ¿Quién es dueño? | |
| ¿Contrato, asesoría o disputa que limite algún conjunto? | |

## Registro de desacuerdos (si fundador y operador respondieron por separado)

| Bloque | Conjunto | Ítem | Fundador | Operador | Nota |
|---|---|---|---|---|---|

---

**Equipo:** _______________  **Fecha:** _______________