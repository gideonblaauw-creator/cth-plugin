# CleantechHUB Plugin · v1.2.0

Plugin oficial para el equipo CleantechHUB en Claude Team Plan. Reúne todas las skills internas de CTH (marcas, programas, operaciones) y los conectores MCP que el equipo usa para colaborar desde Cowork.

**Audiencia:** miembros del equipo CleantechHUB.

---

## Qué incluye este plugin

### 🎨 Skills de marca (3)
- `cleantechhub-brand` — marca matriz · paleta · tipografía · logos · tono
- `clp26-brand` — overlay ClimateLaunchpad 2026 · colores · plantillas · idioma por país
- `sustenttia-brand` — marca del cliente Sustenttia (CTH presta servicios)

### 🚀 Skills de programa (1)
- `social-media-campaign` — pipeline contenido → Buffer → publicación

### 🛠️ Skills operativas (9)
- `monday` · `gmail` · `google-drive` · `bookstack` · `buffer` · `canva`
- `doctor-bot` · `secrets` · `dual-desktop-macos`

> **Nota:** `social-media-campaign` pendiente de Pod schema retrofit — ver Pod W2.

### 🤖 MCP servers (2)
- `files-mcp` — SSOT de archivos Claude en el VPS (`/opt/claude-files/`)
- `doctor-bot` — salud de infraestructura (read-only)

### ⚡ Slash commands (3)
- `/cth-status` — estado de programa CLP26 + apps + agentes en una pantalla
- `/cth-handoff` — atajo a `delega: <outcome>`
- `/cth-newsletter-prep` — preparar la edición mensual de newsletter

---

## Instalación

### Pre-requisitos

Antes de instalar:
1. **Claude Desktop CTH** instalado (Mac o Windows · ≥ versión 1.0)
2. **Cowork mode activado** (Settings → Desktop app → Cowork)
3. **Cuenta CTH en Workspace** (invitación de Gideon)
4. **Tokens MCP**: Gideon te dará dos tokens secretos vía Infisical:
   - `files-mcp` token — para acceso a archivos Claude (formato `cthfm_...`)
   - `doctor-bot` token — para monitoreo de infra (read-only)
   
   Estos tokens son tuyos y solo tuyos. Si los pierdes o sospechas que se filtraron, escribe a Gideon en Telegram DM inmediato — rotamos en 5 min.

### Paso 1 · Agregar el marketplace desde GitHub

En Claude Desktop CTH (o Claude Code):
```
/plugin marketplace add gideonblaauw-creator/cth-plugin
```

### Paso 2 · Instalar el plugin

```
/plugin install cleantechhub@cleantechhub
```

Espera a que descarguen las 13 skills + 3 commands (≤30 seg).

### Paso 3 · Pegar tus tokens MCP en el config

> ⚠️ **Nota técnica:** la versión actual de Claude Desktop no resuelve `${env:VAR}` en `claude_desktop_config.json`. Los tokens deben estar literal en el archivo. Te asignaré tokens individuales vía Infisical — no los compartas con nadie, ni los pegues en chats.

Abre el archivo de config de Claude Desktop CTH:
```bash
open -e ~/Library/Application\ Support/Claude-CTH/claude_desktop_config.json
```

En la sección `mcpServers`, encuentra las dos entradas `files-mcp` y `doctor-bot` que el plugin instaló. Reemplaza los placeholders con tus tokens reales:

```json
"mcpServers": {
  "files-mcp": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote",
      "https://files-mcp.cleantechhub.net/mcp",
      "--header",
      "Authorization: Bearer cthfm_TU_TOKEN_AQUI"
    ]
  },
  "doctor-bot": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote",
      "https://doctor-mcp.apps.cleantechhub.net/mcp",
      "--header",
      "Authorization: Bearer TU_DOCTOR_BOT_TOKEN_AQUI"
    ]
  }
}
```

> Si las entradas no aparecen tras instalar el plugin, copia el bloque de arriba dentro de `mcpServers` manualmente. (Algunas versiones de Claude Desktop no auto-instalan MCPs desde el manifest del plugin — depende del soporte de marketplace.)

Guarda el archivo. ⌘Q en Claude Desktop CTH. Relanza la app.

### Paso 4 · Verifica

En Claude Desktop CTH, en una conversación nueva, pregunta:
> "¿Qué skills tienes disponibles? Filtra a las que empiezan con `cleantechhub-` o `clp26-` o `cth-`."

Deberían aparecer al menos 8 skills CTH.

Luego prueba el MCP de archivos:
> "Usa `mcp__files-mcp__list_files` para listar el directorio raíz `/`."

Si responde con la estructura de `/opt/claude-files/`, todo está conectado.

---

## Uso del día a día

### Para CLP26 (CLP Lead)
1. Abre el Project **CLP26 — Campaña 2026** en tu sidebar
2. Las skills `clp26-brand` y `social-media-campaign` se activan automáticamente
3. Escribe handoffs como: `delega: <outcome>` para que Gideon apruebe
4. Lee/escribe archivos del programa directamente vía Claude (van al VPS, no a tu Mac)

### Para Hub Owners (REIN Coordinator)
1. Abre el Project **CTH Operaciones**
2. Activa `clp26-brand` cuando coordines países
3. `delega:` también funciona para ti cuando necesitas que Gideon apruebe algo

### Para revisión de salud de infraestructura
- En cualquier conversación: `mcp__doctor-bot__get_latest_run` te da el último digest
- O usa el comando `/cth-status` para una vista consolidada

---

## Lo que NO está en este plugin (intencionalmente)

Estos NO son parte del stack CTH del equipo. Si los necesitas para algo específico, habla con Gideon:

- `slack` (CTH usa Telegram, no Slack)
- `notion` (CTH usa Confluence + BookStack)
- `tec-alianza-brand`, `dialogos-del-futuro-brand` (proyectos personales de Gideon)
- `dps-dashboard`, `quickbooks`, `davivienda-monetizacion` (financieros · Gideon-only)
- `composio` (experimental)

---

## Documentación clave (vive en files-mcp)

Una vez instalado el plugin, estas referencias se cargan en tus Projects automáticamente:

- **`CTH_Identity.md`** — quiénes somos, marcas, clientes, stack, equipo
- **`CTH_Pod_Handoff_ClaudeCode.md`** — la arquitectura de implementación (6 pilares)
- **`Plan_Onboarding_Semana1.md`** — onboarding de equipo
- **`Protocolo_CLP26_Dos_Pilotos.md`** — protocolo CLP Lead ↔ Founder
- **`Guia_Delegacion_CTH.md`** — sistema operativo de delegación (Gideon)

---

## Soporte

- **Operativo:** grupo Telegram `CTH · Ops` con @Gideon
- **Bugs en el plugin:** issue en este repo
- **Token perdido o rotado:** Telegram DM directo a Gideon
- **Sospecha de compromiso de credencial:** Telegram DM inmediato + asunto `[URGENTE-SECURITY]`

---

## Para developers del plugin

Ver `CHANGELOG.md` para historial de versiones. PRs solo desde miembros del equipo CTH; review obligatorio de Gideon antes de merge a `main`. Cada release publica un tag `vX.Y.Z`.

Para correr en local antes de publicar:
```bash
git clone git@github.com:gideonblaauw-creator/cth-plugin.git
cd cth-plugin
# Instalar localmente (modo dev) en lugar de marketplace
claude plugin install ./
```

---

## Skills NOT in this public plugin (private to Founder)
`cth-grant` · `cth-proposal-build` · `cth-seo` — strategic playbooks, installed manually on Founder's machine only.

---

*v1.2.0 · 20 mayo 2026 · CleantechHUB Foundation · GitHub marketplace (migrated from VPS)*
