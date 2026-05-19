# Changelog · CleantechHUB Plugin

Versionado: [Semver](https://semver.org/lang/es/) · `MAJOR.MINOR.PATCH`
Convención de commits: `vX.Y.Z · <título>` para releases.

---

## [1.2.0] — 2026-05-19 · Marketplace publish + MCP servers

### Added
- **`files-mcp` MCP server** — SSOT de archivos en el VPS (`files-mcp.cleantechhub.net`). Cada instalación auto-registra el conector; el miembro solo necesita configurar `FILES_MCP_TOKEN` en su entorno
- **`doctor-bot` MCP server** — salud de infraestructura (read-only) en `doctor-mcp.cleantechhub.net`
- **`cth-delegation` skill** — encodes Gideon's delegation operating system (6-element packet, 3 verdicts, two-strike codify rule). Disparador: `delega: <outcome>`
- **Slash commands**: `/cth-status` · `/cth-handoff` · `/cth-newsletter-prep`
- **Brand assets** programmatic: `brand-assets/colors.json` for Claude-generated artifacts
- **Workspace defaults**: idioma español, system prompt pre-cargado, lista de Projects preferidos

### Changed
- **`cth-grant` skill description**: removido `Triple Jump, Expertise France` de los triggers de funder (no son donantes activos)
- **`cth-grant` §5d**: removida fila de `Expertise France` budget rules; `DGGF / Triple Jump` → solo `DGGF`
- **`cth-grant` §3a**: Sustenttia reframed de "CTH platform" a "client engagement we delivered" (refleja que Sustenttia es cliente, no marca propia)
- **`cth-grant` §10**: tabla strengths/gaps · Sustenttia row aclarado como engagement de cliente

### Removed
- `notion` skill **NO incluida** en el plugin del equipo (CTH no usa Notion · usa Confluence + BookStack). Skill sigue existiendo en personal-only para Gideon
- `slack` skill **NO incluida** (CTH usa Telegram)
- `tec-alianza-brand`, `dialogos-del-futuro-brand` **NO incluidas** (proyectos personales de Gideon, no son marcas CTH)
- `dps-dashboard`, `quickbooks`, `davivienda-monetizacion` **NO incluidas** (financieros / Run Up Holdings / Gideon-only)
- `composio`, `mac-storage-hygiene`, `ollama`, `google-workspace-cli` **NO incluidas** (experimental / Gideon machine-specific)

### Security
- Tokens migrados de `tokens.json` plaintext en VPS → Infisical project `086e5791-f415-41c2-ad5d-9ec0026792ed` path `/cth/files-mcp/tokens/`
- `auth.py` cache TTL 60 seg en prod (era 300 seg en dev) para que revocación de token propague rápido
- Caddy `rate_limit` agregado: 60 req/min/IP + 600 req/h/token

### Discovery — Transport limitation
Testeo local 2026-05-19 (`HANDOFF_indirection_test.md`) confirmó que **Claude Desktop CTH (versión actual) NO carga MCP servers con `transport: streamable-http` desde `claude_desktop_config.json`** — los ignora silenciosamente, sin logs ni intento de conexión. Solo loadea servers stdio (`command` + `args`).

**Implicación:** este plugin usa `mcp-remote` como bridge stdio (idéntico al patrón del existente `doctor-bot`), NO native streamable-http. Tokens van literales en `args` (no env vars). Cuando una futura versión de Claude Desktop soporte native streamable-http, podremos simplificar a la sintaxis directa — por ahora, el bridge funciona perfecto.

**Lecciones para v1.3.0+:**
- Re-testar transport native streamable-http en cada release menor de Claude Desktop
- Si soporta env-var indirection (`${env:VAR}`), migrar a tokens via Infisical-on-machine en lugar de hard-coded
- Documentar versión mínima de Claude Desktop que soporta cada modo

### Documentation
- README en español, install paso a paso
- Reference a `CTH_Identity.md` como SSOT canónico
- Reference a `CTH_Pod_Handoff_ClaudeCode.md` para la arquitectura de implementación

---

## [1.1.0] — antes del 2026-05-19 · estado pre-marketplace

(No publicado oficialmente. Distribución vía repo + install manual.)
- 30+ skills agrupadas
- Sin MCP servers
- Sin slash commands

---

## [1.0.0] — anterior · skills aisladas

(Pre-plugin. Skills se cargaban individualmente por usuario.)

---

## Roadmap

### [1.3.0] · planificado
- Pod-frontmatter retrofit aplicado a skills de workflow (`social-media-campaign`, `cth-grant`, `cth-proposal-build`, `cth-seo`, `cth-delegation`) — alinea con Pod W2
- Skill nueva: `confluence` MCP wrapper (cuando exista MCP oficial de Atlassian)
- Skill nueva: `jira` MCP wrapper
- Skill nueva: `telegram` MCP wrapper (HITL gates · digests)

### [1.4.0] · cuando llegue Pod W5
- Slash command `/cth-eval` — corre eval-runner local sobre un draft
- Slash command `/cth-recovery` — abre el playbook de recovery
- Logs de audit consultables vía `mcp__files-mcp__get_audit_log`

### [2.0.0] · post-CLP26
- Multi-pod support — el plugin sabe a qué client pod estás conectada (CTH, Sustenttia, etc.)
- Pod selector en commands
- Brand switching automático según Project activo
