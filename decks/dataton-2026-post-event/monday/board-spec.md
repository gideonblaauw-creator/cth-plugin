# Especificación de tablero Monday — Datatón CTH (no crear en esta ola)

**Propósito:** Plantilla para replicar el protocolo interno (*Protocolo Datatón CTH*) como tablero de seguimiento.  
**Idioma:** Español.  
**Regla:** Este ticket **no** crea el tablero; solo entrega `board-spec.md` + `board-import.csv`.

## Grupos (fases)

| Grupo en Monday | Fase / hito |
|-----------------|-------------|
| T-8 semanas | Concepto y aliados |
| T-6 semanas | Sede y agenda |
| T-4 semanas | Luma y convocatoria |
| T-3 semanas | Reclutamiento y briefing de mentores |
| T-2 semanas | Paquete de equipos |
| T-1 semana | Drive, WhatsApp, run-of-show, certificados |
| Día D | Ejecución en vivo |
| T+1 | Agradecimientos, biblioteca de imágenes, informe |
| T+2 semanas | Seguimiento |

## Columnas

| Columna | Tipo sugerido | Descripción |
|---------|---------------|-------------|
| **Tarea** | Texto | Ítem de checklist (una fila por línea del protocolo). |
| **Fase** | Grupo | Debe coincidir con uno de los grupos anteriores. |
| **Responsable (rol)** | Texto | Rol operativo (sin nombres personales). |
| **Fecha relativa (T-x)** | Texto | Etiqueta T-8 … T+2 o «Día D». |
| **Fecha** | Fecha | Opcional; fecha absoluta cuando se fije. |
| **Estado** | Estado | Por hacer / En curso / Hecho / Bloqueado. |
| **Entregable/link** | Enlace o texto | Ruta en repo, carpeta Drive o artefacto. |
| **Dependencia** | Texto | Tarea o fase previa requerida. |
| **Notas** | Texto largo | Riesgos, [por validar], [pendiente Gideon]. |

## Importación

1. Crear tablero vacío con los grupos en el orden de la tabla.
2. Añadir columnas con los nombres exactos de la tabla (respetar mayúsculas y tildes donde aplica).
3. Importar `board-import.csv` (UTF-8, coma como separador).
4. Asignar **Fase** al grupo correspondiente tras la importación si Monday no mapea automáticamente.

## Fuente de ítems

Cada fila del CSV corresponde a una línea de checklist del documento `protocol/protocolo-dataton-cth.pdf` (misma redacción abreviada si el espacio lo exige).

## Alcance edición 24 nov 2026

Los ítems reflejan la primera edición (Observatorio de la Tierra + Datalab), Universidad Externado, 24 nov 2026. Resultados oficiales (finalistas, ganadores, puntajes) **no constan en las fuentes** al cierre de esta ola — marcar en Monday como [por validar] donde aplique.