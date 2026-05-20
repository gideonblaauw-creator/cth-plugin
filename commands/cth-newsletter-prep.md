---
name: cth-newsletter-prep
description: Prepara la edición mensual del newsletter CTH · jala highlights de CLP26 + ediciones recientes de Doctor_Bot + cambios en Identity. Genera un borrador en Confluence o Drive listo para revisión de Gideon antes de enviar vía Resend.
trigger: "/cth-newsletter-prep"
audience: team
---

# /cth-newsletter-prep

Newsletter CTH es responsabilidad del **Founder** temporalmente. CLP Lead es candidata a heredar.

Cuando el usuario invoca este comando, ejecuta este flujo:

## 1. Pregunta para qué mes

> "¿Qué edición estás preparando? Dame el mes (ej. 'junio 2026') o asume el mes próximo."

Si el usuario dice "el próximo" o no responde claramente, asume el mes próximo al actual.

## 2. Carga contexto de marca

Asegúrate de que `cleantechhub-brand` está activa. Si la skill no carga automáticamente en este Project, actívala manualmente.

## 3. Pull paralelo

Ejecuta en paralelo:

### 3a. Highlights CLP26 del mes
- Items Monday con `Marca = CLP26` y `Estado = Publicado` en los últimos 30 días
- Posts del social media campaign que tuvieron alto engagement
- Hitos del programa: bootcamps, finales, etc.

### 3b. Salud y crecimiento de programa
- Número de aplicantes CLP26 actuales (lee Drive → `Postulaciones_CLP_*` sheet)
- Países activos
- Mentores confirmados

### 3c. Stories de cliente
- Sustenttia: avances recientes (vía Confluence space si existe)
- Otros clientes activos

### 3d. Donante updates
- Conversaciones recientes con donantes vía Gmail (search por nombres de donantes activos, últimos 30d)
- Solo titulares · NO detalles financieros (Capital Raise es privado)

## 4. Estructura del borrador

Genera el borrador con esta estructura:

```
# CleantechHUB · Newsletter {Mes} {Año}

**Tagline:** Inspira · Actúa · Transforma

## 🌎 Lo que pasó este mes
- [Highlight 1: una frase punzante]
- [Highlight 2]
- [Highlight 3]

## 🚀 CLP26 · Estado del programa
[2-3 párrafos: dónde estamos en el ciclo, próximos hitos, números clave de aplicantes/mentores]

## 💡 Spotlight: {nombre de equipo / proyecto / cliente destacado}
[Story de 2-3 párrafos · un equipo/proyecto que vale la pena destacar]

## 🤝 Donantes & partners
[Agradecimientos · NO cifras · solo presencia: "gracias a [Donante] por su apoyo continuo en..."]

## 📅 Próximamente
- [Evento 1 · fecha]
- [Evento 2 · fecha]

## 👋 Únete
{CTA · LinkedIn / Instagram / web · invitación a la próxima cohorte CLP / a postular como mentor / etc.}

—
**CleantechHUB Foundation** · cleantechhub.net · {dirección breve}
[Unsubscribe link] · [Update preferences]
```

## 5. Guarda el borrador

Vía `files-mcp` (cuando esté listo):
```
mcp__files-mcp__write_file
  path: "Projects/Claude Infrastructure/newsletters/CTH_Newsletter_{YYYY-MM}_DRAFT.md"
  content: <el borrador>
```

O directamente en Confluence space "Newsletters CTH" cuando exista.

## 6. Reporta a Gideon

Después de guardar, responde:

```
✅ Newsletter {Mes} draft creado.
Archivo: Projects/Claude Infrastructure/newsletters/CTH_Newsletter_{YYYY-MM}_DRAFT.md

Antes de enviar vía Resend:
1. [Gideon] Revisa el borrador end-to-end (~10 min)
2. [Gideon] Aprueba el spotlight y la CTA
3. Imágenes: 1-2 fotos del mes (banner + 1 inline) · vía Canva con cleantechhub-brand activa
4. Aprobación de cifras financieras si aparecen: NO debe haber
5. Send window óptima: martes/miércoles 10:00 COT
```

## 7. Reglas duras

- NO menciones donantes retirados — consulta la lista activa interna antes de nombrar donantes
- NO trates a Sustenttia como marca CTH; es cliente
- NO incluyas a TecAlianza, Diálogos del Futuro, Run Up Holdings (proyectos personales de Gideon, NO CTH)
- NO incluyas cifras de capital raise · si surge tema financiero, escala a Gideon
- Idioma: español neutro. Si hay versión en inglés, hazla aparte (no bilingüe en un solo correo)

## 8. Si falla

Si no encuentras un mes con suficiente contenido (programa en pausa, sin highlights), reporta:
> "Mes {Mes} con baja actividad. Sugiero: (a) skip esta edición, (b) edición temática (recapitulación de Q anterior), (c) edición spotlight de donante o cliente. ¿Qué prefieres?"
