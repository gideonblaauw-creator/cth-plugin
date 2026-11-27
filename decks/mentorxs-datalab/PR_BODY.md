## Entregables

- **Deck** `decks/mentorxs-datalab/`: 14 diapositivas reveal.js en español (FODESEP `fp-*`, `deck-meta.json` `gated: true`), control **Descargar PDF**, `mentorxs-datalab.pdf` (14 páginas).
- **Impresión** `decks/mentorxs-datalab/print/`: PDF A4 con membrete CTH (`part3-cuestionario-mentor.pdf`) y lista idéntica para Google Forms (`part3-google-forms-question-list.md`, 55 ítems). Sin formulario en vivo.

## Verificación de archivo metodología

| Comprobación | Resultado |
| --- | --- |
| `0cddef7d` en `cth-plugin` | **No existe** (no es commit git en este repo; Orchestrator usó una etiqueta de contenido, no SHA de git) |
| CHANGELOG VPS | **C17–C26** presentes en `/opt/claude-files/Clients/Air4U/datathon-questionnaires/CHANGELOG.md` |
| CHANGELOG Drive (`12mCsflPin2E-4h7nrISs4dxEysPed5Ha`) | Solo hasta **C21** al redactar el ticket |
| SHA256 tarball 11 archivos finals en VPS | `a10875fd7137eabfb0a6010d9e6c970334dd9c3273cf23f6660f384379ada8db` (**≠** `0cddef7d`) |

Fuente de contenido: bytes `.md` del VPS (no conversiones Google Docs).

## Flags / tensiones (abiertas)

1. **Honestidad 4/5** en ejemplo Air4U sin rung medallion para honestidad (slide 11); ejemplo ilustrativo.
2. **16:00** = boceto de un pantallazo, no producto; OSS/Gemini opcionales.
3. **Puerta 1** = elección de 1–2 flujos al cierre del Bloque 1; mapa Q1 etiqueta, no excluye (v0.3).
4. **Deploy / URL pública**: `gated: true`; sin Caddy/oauth2 hasta GO de Gideon.

## Pruebas (Hands)

- `tools/reveal/lint.sh --skip-overflow mentorxs-datalab`
- `tools/reveal/outline.sh --validate-only decks/mentorxs-datalab/deck.yaml`
- PDF deck: 14 páginas; cuestionario ~4 páginas; `pdffonts` Open Sans en cuestionario.

**Draft only** — no merge, deploy, ni Google Form en cuenta CTH.

## Proof paths

- VPS metodología: `/opt/claude-files/Clients/Air4U/datathon-questionnaires/`
- Letterhead: `/opt/claude-files/Projects/CTH-Brand/letterhead/`
- Ronda fix Datalab: logos `cleantechhub-color.png`, slide 13 `fp-stuck-grid`, alineación PDF/Forms 55 ítems