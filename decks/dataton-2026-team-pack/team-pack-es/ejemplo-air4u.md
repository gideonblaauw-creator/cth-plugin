# Ejemplo trabajado — una clínica en Bogotá (piloto)

| Campo | Valor |
|---|---|
| Versión equipo | v0.3-es (ilustrativo) |
| Fecha | 2026-11-21 |
| Cliente | Solo «una clínica en Bogotá (piloto)» — sin nombre propio |
| Estado | Ejemplo de mesa; la empresa piloto no ha diligenciado las hojas |

Este ejemplo recorre Hojas 1–3 con datos **estimados** donde la escalera aún está en **Ninguno**.

---

## Hoja 1 (extracto) — conjunto principal D1

| Bloque | ID | Conjunto | S | R | H | F | A | Q | G | Etiquetas |
|---|---|---|---|---|---|---|---|---|---|---|
| Propuestas de valor | D1 | Lecturas de sensor indoor (PM, O₃) en sitio piloto | Y | 1 | U→0 | 2 | 1 | 0 | 0 | acceso legal, acceso técnico, calidad |

La copia maestra entre chat de operaciones y plataforma de monitoreo **no está clara** → R = 1.

---

## Hoja 2 — tarjeta de flujo (resumen)

```
TARJETA DE FLUJO · Equipo: [piloto aire interior] · Fecha: 2026-11-21
Bloque(s) / ID : Propuestas de valor, D1
Flujo          : Monitorear aire interior en sitio piloto
Disparador     : Lectura periódica del sensor en la clínica
Nivel alcanzado: Ninguno (debajo de Bronce)
Siguiente grada: B5 almacenamiento nombrado, B6 derechos escritos, B7 exportación
A12            : Propiedad del sitio piloto ABIERTO (pendiente Legal)
A14 (borrador) : «Mostrar PM₂.₅ indoor frente a referencia OMS para el gestor del sitio»
```

---

## Hoja 3 — tarjeta de valor (resumen)

**Usuario:** gestor de instalaciones de la clínica piloto.

**Decisión:** ¿Debe activar ventilación o revisión de filtros **esta semana** si el PM₂.₅ indoor podría superar la referencia?

| # | Métrica | Mostrar | Grada | Panel |
|---|---|---|---|---|
| N1 | PM₂.₅ indoor en sitio — valor no declarado en fuentes | **estimado** | Ninguno | Línea base |
| N2 | Brecha vs referencia OMS — no calculable sin N1 | **estimado** | Ninguno | Delta |
| N3 | PM₂.₅ exterior Bogotá — fuente paisaje por elegir | **estimado** | Ninguno | Paisaje |

**Tablero público:** **No** (derechos abiertos).

### Boceto

```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ LÍNEA BASE          │ DELTA               │ PAISAJE             │
│ PM2.5 indoor (est.) │ vs referencia (est.)│ PM2.5 exterior (est.)│
│ [Ninguno] D1        │ [Ninguno] D1        │ sin enlace aún      │
└─────────────────────┴─────────────────────┴─────────────────────┘
  Decisión: ¿ventilación extra esta semana?
  PÚBLICO: NO
```

---

## Lección para equipos

Se puede dibujar una pantalla **útil** con escalera en **Ninguno** si todos los números dicen **estimado** y la audiencia es **interna**.