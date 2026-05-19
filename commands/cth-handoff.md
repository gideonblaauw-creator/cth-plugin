---
name: cth-handoff
description: Atajo al disparador `delega: <outcome>` de la skill cth-delegation. Útil cuando estás en una conversación que no activó la skill automáticamente. Equivalente a tipear el disparador completo.
trigger: "/cth-handoff"
audience: team
---

# /cth-handoff

Cuando el usuario invoca `/cth-handoff` (con o sin argumentos), activa la skill `cth-delegation` y procede con su flujo de 5 pasos.

## Si hay argumentos

Si el usuario tipea `/cth-handoff prepara newsletter de junio`, trata el resto del mensaje como el outcome inicial y empieza directo en el Step 1 de la skill (acknowledge & gather missing elements).

## Si NO hay argumentos

Pregunta:
> "¿Qué quieres delegar? Dame el outcome en una línea. Ejemplo: '3 posts cierre convocatoria CLP26 para lunes 16:00 Bogotá'."

Luego procede normal con el flujo de la skill.

## Comportamiento idéntico al disparador `delega:`

Este comando NO duplica lógica — solo activa la skill `cth-delegation`. Toda la lógica del handoff packet (6 elementos), creación de item Monday, notificación Telegram, etc., vive en la skill misma.

## Por qué existe como comando separado

- Algunos usuarios prefieren slash commands sobre frases en lenguaje natural
- En conversaciones largas, escribir `/cth-handoff` es más rápido que `delega:`
- Aparece en el autocompletado de Cowork, facilita descubrimiento

## NO use cases

- No uses este comando para handoffs personales (TecAlianza, Diálogos, Run Up). Esos NO son CTH.
- No uses para handoffs RESERVED (capital raise, hiring, public crisis). La skill `cth-delegation` ya pushback en esos casos — confía en ella.
