---
name: cth-status
description: Vista consolidada del estado actual de CleantechHUB en una pantalla. Lee del Program Map artifact + Doctor_Bot + Monday board "CTH Team Delegation". Útil al inicio del día o cuando reapareces después de unos días fuera.
trigger: "/cth-status"
audience: team
---

# /cth-status

Cuando el usuario invoca `/cth-status`, ejecuta este flujo:

## 1. Cargar contexto base

Verifica que las siguientes referencias están disponibles:
- Project `CleantechHUB Identity` con `CTH_Identity.md` cargado
- MCP `files-mcp` registrado
- MCP `doctor-bot` registrado
- Acceso al board Monday `CTH Team Delegation` (id `18413506427`)

Si alguno falta, reporta el gap antes de continuar.

## 2. Pull paralelo de 4 fuentes

Ejecuta en paralelo (no secuencial):

### 2a. Estado CLP26 (programa estrella)
```
mcp__416f7430-0abf-417b-8b28-4afaa209d6a7__get_board_items_page
  boardId: 18413506427
  includeColumns: true
  filters: [{ columnId: "color_mm3d78pn", operator: "any_of", compareValue: ["Esperando aprobación", "Borrador"] }]
```

Cuenta:
- Items en "Esperando aprobación" (necesitan atención de Gideon hoy)
- Items en "Borrador" (en curso por Angelica/equipo)
- Items por marca: CLP26 / CleantechHUB / Sustenttia (cliente) / Interno
- Próximos hitos de cronograma (next 14 días)

### 2b. Salud de infraestructura
```
mcp__doctor-bot__get_latest_run
```

Reporta:
- Última corrida del Doctor_Bot (timestamp)
- Estado por capa: VPS · System · Cron · MCPs · HTTP
- Items en RED (acción inmediata)
- Items en AMBER (a vigilar)

### 2c. Cambios recientes en archivos SSOT
```
mcp__files-mcp__list_recent_changes
  since: <ahora menos 24h>
```

Reporta:
- Quién editó qué en las últimas 24h (vía audit log)
- Si Angie/Jenn están activas (writes recientes)

### 2d. Próximos hitos CLP26
Lee desde `files-mcp`:
```
mcp__files-mcp__read_file
  path: "Projects/Claude Infrastructure/CTH_Pod_Handoff_ClaudeCode.md"
```
(O del Cronograma 2026 HUBS sheet vía Drive MCP)

Identifica los próximos 3-5 hitos críticos.

## 3. Renderizar el dashboard

Construye una salida estructurada en este formato (markdown):

```markdown
# 📊 CTH · Estado actual · {timestamp Bogotá}

## 🚀 CLP26 · próximos 14 días
- **Próximo hito:** {nombre del hito · fecha · owner}
- **Bootcamps en:** {N días}
- **Final regional:** {N días}

## 📋 Tu queue de aprobación
- **Esperando tu aprobación:** {N items}
- {Item 1: nombre, marca, prioridad}
- {Item 2 ...}

## 💼 Trabajo en curso (equipo)
- **Angelica:** {N items en Borrador} · último write hace {X}
- **Jennifer:** {N items en Borrador} · último write hace {X}

## 🏥 Salud infra
- Doctor_Bot last run: {ts} · {RED count} RED · {AMBER count} AMBER
- files-mcp: {GREEN/AMBER/RED}
- CTH Pod: {W?/UNKNOWN}
- BookStack: {GREEN/AMBER/RED}

## 🎯 3 acciones que sugiero para hoy
1. {derivado del análisis arriba}
2. ...
3. ...
```

## 4. Sugerencias contextual

Después del dashboard, identifica 2-3 acciones específicas que el usuario podría tomar AHORA. Ejemplos:

- Si hay >3 items "Esperando aprobación" → "Bloquea 20 min para tu ventana de aprobación de las 10:30. Aquí están los 5 items."
- Si Doctor_Bot tiene RED → "files-mcp en RED por X. Investiga primero antes de cualquier handoff nuevo."
- Si Angie no ha escrito en 24h+ → "Angie sin actividad hoy. ¿Necesita un check-in?"

## 5. No

- NO listes TODOS los items del board — solo los de tu interés inmediato
- NO renderices artefactos pesados — esto es un comando rápido, no un dashboard interactivo
- NO repitas información que ya está en otros artefactos pinneados (Program Map, Delegation Cheat Sheet) — solo síntesis

## 6. Si fallas

Si cualquier MCP no responde, sigue con lo que sí funciona y reporta el gap explícitamente al final:

> ⚠️ No pude leer Monday board (timeout). El dashboard arriba refleja solo Doctor_Bot + files-mcp.
