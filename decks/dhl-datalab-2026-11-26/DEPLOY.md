# DEPLOY — capa reunión AGV × Air4U (sin ejecutar en este run)

**Ventana:** validar antes de **07:00 COT** del 26 nov 2026. Este documento es solo instrucción; Hands no corre estos pasos aquí.

## Alcance

| Repo | Qué despliega |
| --- | --- |
| `gideonblaauw-creator/cth-plugin` | Pack `decks/dhl-datalab-2026-11-26/` (métricas, eval, preview estático) — opcional en VPS `/opt/sites/decks` si se sirve el HTML |
| `gideonblaauw-creator/cth-datalab` | `app/app/js/meeting-air4u-agv-dhl-2026-11-26.js`, `app/app/css/meeting-layer-2026-11-26.css`, entradas en `index.html` |

**No** mezclar etiquetas: en UI y datos, **source: AGV Open Market Informe de Sostenibilidad 2025** vs **source: DHL Group 2025 public report**.

## 1. Respaldo (VPS, como `debian` o usuario deploy)

```bash
TS=$(date -u +%Y%m%d-%H%M%S)
sudo mkdir -p /var/backups/cth-datalab
sudo tar -czf "/var/backups/cth-datalab/datalab-app-pre-meeting-agv-${TS}.tgz" \
  -C /opt/sites/datalab app/app/index.html \
  app/app/js/meeting-air4u-agv-dhl-2026-11-26.js \
  app/app/css/meeting-layer-2026-11-26.css 2>/dev/null || true
# Respaldo completo si no existían los archivos nuevos:
sudo tar -czf "/var/backups/cth-datalab/datalab-app-full-${TS}.tgz" -C /opt/sites/datalab app
```

## 2. Actualizar `cth-datalab` en el servidor

```bash
cd /opt/sites/datalab
git fetch origin
git checkout cursor/dhl-datalab-2026-11-26-fa08   # o el commit tras merge
git pull --ff-only origin cursor/dhl-datalab-2026-11-26-fa08
# Verificar archivos:
test -f app/app/js/meeting-air4u-agv-dhl-2026-11-26.js
test -f app/app/css/meeting-layer-2026-11-26.css
grep -q meeting-air4u-agv-dhl app/app/index.html
```

No reiniciar API salvo que el diff toque `api/` (este cambio es solo estático en `app/app/`).

## 3. Cache bust (si Caddy sirve estáticos con query `?v=`)

Incrementar sufijos `?v=` en `index.html` para los dos assets nuevos tras desplegar, o purgar CDN si aplica.

## 4. Verificación humana

1. Abrir `https://datalab.cleantechhub.net/app/#/lab`
2. Rol con acceso Air4U (token gated si aplica).
3. Confirmar bloque **«Capa reunión 26 nov · AGV + referencia DHL Group»** bajo el living lab.
4. Etiquetas de fuente visibles en cada tarjeta.
5. Mapa y capas A1/A2/A3 existentes siguen cargando.

## 5. Rollback

```bash
TS=<timestamp-del-backup>
sudo tar -xzf "/var/backups/cth-datalab/datalab-app-pre-meeting-agv-${TS}.tgz" -C /opt/sites/datalab
# o restaurar full:
sudo tar -xzf "/var/backups/cth-datalab/datalab-app-full-${TS}.tgz" -C /opt/sites/datalab
```

Validar de nuevo `#/lab` y descartar caché del navegador.

## 6. Pack cth-plugin (opcional)

Si se publica `preview.html` en decks:

```bash
rsync -av /path/to/cth-plugin/decks/dhl-datalab-2026-11-26/ \
  /opt/sites/decks/dhl-datalab-2026-11-26/
```

No copiar PDFs AGV/DHL al repo ni al VPS público; solo CSV/MD/HTML extraídos.