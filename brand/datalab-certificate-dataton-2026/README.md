# Datalab certificate · Datatón 2026

Spanish A4 landscape participation certificate for **Datatón · Lanzamiento del Observatorio de la Tierra** (24 Nov 2026, Universidad Externado de Colombia, Bogotá).

Print-ready HTML/CSS template, vendored logos and fonts, and a Python batch renderer. **Draft only** — not merged, not deployed, not for live attendee PII.

## Single render

```bash
cd brand/datalab-certificate-dataton-2026
python3 render.py --nombre "Tomás Hernández Quintero" --rol Participante --equipo "Equipo Andes Verdes" --fecha "24 de noviembre de 2026" --out review/nombre.pdf
```

`--equipo` is optional. `--rol` must be `Participante`, `Mentor`, or `Jurado`.

## Batch render

```bash
python3 render.py --csv examples/sample.csv --outdir review/batch/
```

UTF-8 CSV columns: `nombre`, `rol`, optional `equipo`, optional `fecha` (defaults to `24 de noviembre de 2026`).

Outputs one PDF per row plus `review/batch/all.pdf`.

## Dependencies

Playwright + Chromium (installed on first run). Optional: `pypdf` for batch merge, `pymupdf` + `pillow` for `review/make_contact_sheet.py`.

## Push back (summary)

- Landscape certificate, not CTH letterhead portrait wave.
- Datalab Option A datagrid vendored from draft PR #134 branch without merging that PR.
- CEE logo slot is labelled empty until an official light-ground file exists (`logos/GAPS.md`).
- Externado co-signer placeholders remain until confirmed.

See `SOURCES.md` and the Hands ticket for full provenance and acceptance checks.