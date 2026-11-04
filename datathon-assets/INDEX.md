# Datathon / Earth Observatory — comms kit index

**Marca:** Datalab powered by CleantechHUB (`Datalab` una palabra).
**Evento ancla:** martes 24 de noviembre de 2026.
**Estado:** borrador PR — NO publicar.

## Streams (5)

| Carpeta | Tema |
|---------|------|
| `01-agenda/` | Agenda del evento |
| `02-earth-observatory/` | Lanzamiento Observatorio de la Tierra |
| `03-datalab/` | Datalab soft launch |
| `04-datathon/` | Datathon |
| `05-air4u-demo/` | Demo en vivo Air4U |

## Canales y tamaños (cada stream)

Por canal: `svg/`, `png/`, `jpg/` (+ `carousel.pdf` en carruseles). HTML fuente en la raíz del canal.

| Canal | Tamaños (stem) |
|-------|----------------|
| `linkedin/` | 1200x627, 1080x1080 |
| `facebook/` | 1200x630, 1920x1005 |
| `instagram/` | 1080x1080, 1080x1350 |
| `story/` | 1080x1920 |
| `x/` | 1600x900 |
| `whatsapp/` | 1080x1080, 1080x1920 |
| `email/` | 1200x400 |
| `web/` | 1920x600 |
| `linkedin-carousel/` | 1080×1350 · 4 slides + PDF |
| `instagram-carousel/` | 1080×1080 · 4 slides + PDF |

## Copy por stream

`posts.md` — LinkedIn (largo/corto), Facebook, Instagram (caption, hashtags, alt), X, WhatsApp, email, CTAs.
`copy.txt` — texto plano legacy.
`copy-es.md` — borrador extendido.

## Fotos stock (LatAm cleantech)

`06-fotos/` — JPG + `credits.txt`. Integradas en **03-datalab** y **04-datathon** (overlays).

## Agenda impresa

`01-agenda/agenda-print-a4.html` → PNG/PDF vía `render-comms.sh`. En el zip: `agenda-evento.pdf`.

## WhatsApp kit (`datathon-kit.zip`)

~12–15 MB (JPG + SVG + PNG si cabe; repack sin PNG si supera 15 MB). Tope duro 100 MB.

Regenerar: `fetch-stock-photos.sh` → `python3 build_assets.py` → `render-comms.sh` → `build-kit-zip.sh`.

**Logo:** Option A grid — `brand/datalab-logo-2026-11/archive/logo/option-a.*`.

## PENDIENTE (global)

- Hora de inicio del evento
- Sede / venue
- Enlace RSVP / registro
- Panelistas del panel de apertura
- Reglas y premios del datathon
- Logos finales CleantechHUB, Air4U, Externado
- Mapa o foto de sede
- Contacto / CTA final
- Tercera fecha de pre-evento (si aplica fuera de este pack)

## Reglas aplicadas

- Copy CTH en español latinoamericano.
- Sin ángulo cannabis; sin precios Phase 2; sin nombre Comapán.
- Capas de datos en lenguaje llano (no bronze/silver/gold).
- Air4U = socio de innovación; CleantechHUB = custodio.
- Placeholders de logo hasta archivo aprobado.
