#!/usr/bin/env python3
"""Add per-gap Datalab detail blocks to all *-snapshot/data.json (EN + ES)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEX = json.loads((Path(__file__).resolve().parent / "datalab-lexicon.json").read_text())
UNSOURCED: list[str] = []

UNIT_PAT = re.compile(
    r"(µg/m³|ug/m3|mg/m³|tCO2e|kWh|MWh|GWh|%/|por ciento|percent|ppm|m³|hectares|ha\b|trees|árboles|colonias|complaints)",
    re.I,
)
FREQ_PAT = re.compile(
    r"(hourly|daily|weekly|monthly|real[- ]time|tiempo real|semanal|mensual|diario|intervalo)",
    re.I,
)
GRI_PAT = re.compile(
    r"GRI\s[\d]+[^.]*?(?:\([^)]+\))?|IFRS[^.]*|SASB[^.]*|TCFD[^.]*|TNFD[^.]*|GHG Protocol[^.]*",
    re.I,
)


def log_unsourced(slug: str, gap: int, startup: str, field: str, note: str) -> None:
    UNSOURCED.append(f"{slug} gap{gap} {startup}: {field} — {note}")


def standards_from_context(ctx: str) -> str:
    found = GRI_PAT.findall(ctx or "")
    if not found:
        return "the sustainability standards cited in the gap context"
    # dedupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for s in found:
        k = s.strip().lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(s.strip().rstrip("."))
    return "; ".join(out[:3])


def reported_vs_missing(gap: dict, lang: str) -> str:
    ctx = (gap.get("context") or {}).get(lang, "")
    ev = gap.get("report_evidence") or {}
    page = ev.get("page")
    parts: list[str] = []
    if ctx.strip():
        parts.append(ctx.strip())
    if page:
        ref = (
            f"Report evidence is on PDF page {page} (see link above)."
            if lang == "en"
            else f"La evidencia del reporte está en la página {page} del PDF (ver enlace arriba)."
        )
        parts.append(ref)
    if lang == "en":
        parts.append(
            "Missing data: quantities the report says are still being completed, audited, or not yet published for this indicator."
        )
    else:
        parts.append(
            "Dato faltante: cantidades que el reporte señala como aún en completación, auditoría o sin publicar para este indicador."
        )
    return " ".join(parts)


def metric_type_from_text(text: str, lang: str) -> str:
    t = text or ""
    tl = t.lower()
    if re.search(r"alcances?\s*1|scope\s*1", tl):
        return "Scope 1–3 greenhouse gas emissions" if lang == "en" else "Emisiones GEI alcances 1–3"
    if "pm2.5" in tl or "pm10" in tl or "calidad del aire" in tl or "air quality" in tl:
        return "Air pollutant concentrations" if lang == "en" else "Concentraciones de contaminantes del aire"
    if "agua" in tl or "water" in tl or "embalse" in tl or "reservoir" in tl:
        return "Water movement or stress indicators" if lang == "en" else "Indicadores de movimiento o estrés hídrico"
    if "solar" in tl or "renovable" in tl or "renewable" in tl or "energía" in tl:
        return "Non-conventional renewable generation or capacity share" if lang == "en" else "Generación o participación de renovables no convencionales"
    if "empaque" in tl or "packaging" in tl or "residuo" in tl or "waste" in tl:
        return "Packaging or waste circularity indicators" if lang == "en" else "Indicadores de empaque o circularidad de residuos"
    if "abeja" in tl or "bee" in tl or "biodivers" in tl:
        return "Biodiversity or species relocation indicators" if lang == "en" else "Indicadores de biodiversidad o reubicación de especies"
    if "financ" in tl or "fondo" in tl or "fund" in tl:
        return "Clean energy finance or efficiency program indicators" if lang == "en" else "Indicadores de financiamiento o eficiencia energética"
    return "Environmental performance indicators named on the public page" if lang == "en" else "Indicadores de desempeño ambiental nombrados en la página pública"


def extract_units(text: str) -> str:
    m = UNIT_PAT.search(text or "")
    return m.group(1) if m else ""


def extract_frequency(text: str) -> str:
    m = FREQ_PAT.search(text or "")
    return m.group(1) if m else ""


def method_from_text(text: str, lang: str) -> str:
    tl = (text or "").lower()
    bits: list[str] = []
    if "sensor" in tl or "trazador" in tl or "tracer" in tl:
        bits.append("field sensors or tracers" if lang == "en" else "sensores o trazadores de campo")
    if "auditable" in tl or "auditable" in tl or "metodología" in tl:
        bits.append("auditable methodology" if lang == "en" else "metodología auditable")
    if "iot" in tl:
        bits.append("IoT" if lang == "en" else "IoT")
    if "consultor" in tl or "consulting" in tl:
        bits.append("consulting assessment" if lang == "en" else "evaluación de consultoría")
    return "; ".join(bits)


def startup_metrics(
    slug: str,
    gap_rank: int,
    match: dict,
    nexus: dict,
    lang: str,
) -> list[dict]:
    name = match.get("name") or "Startup"
    quote = match.get("public_quote") or ""
    nx = nexus.get(name) or {}
    desc = (nx.get("ds" if lang == "es" else "d") or "").strip()
    src_url = match.get("public_source_url") or match.get("website") or ""
    source = src_url or "public_quote in snapshot data.json"
    combined = " ".join(x for x in (quote, desc) if x)

    unit = extract_units(combined)
    freq = extract_frequency(combined)
    method = method_from_text(combined, lang)
    metric = metric_type_from_text(quote, lang) or metric_type_from_text(desc, lang)

    if not unit:
        log_unsourced(slug, gap_rank, name, "unit", "no unit on public page")
        unit = LEX["ui"][lang]["datalab.notStated"]
    if not freq:
        log_unsourced(slug, gap_rank, name, "frequency", "no frequency on public page")
        freq = LEX["ui"][lang]["datalab.notStated"]
    if not method:
        log_unsourced(slug, gap_rank, name, "method", "no method on public page")
        method = LEX["ui"][lang]["datalab.notStated"]

    # If quote names a metric concept but no numeric unit, keep type-only note
    type_note = ""
    if quote and not extract_units(quote):
        type_note = LEX["ui"][lang]["datalab.metricTypeOnly"]

    line = {
        "startup": name,
        "metric": metric,
        "unit": unit,
        "frequency": freq,
        "method": method,
        "source": source,
    }
    if type_note:
        line["note"] = type_note
    return [line]


def deliverable(gap: dict, standard: str, lang: str) -> str:
    title = (gap.get("title") or {}).get(lang, "")
    if lang == "en":
        return (
            f"A Datalab package for the end user: validated L2 tables and L3 disclosure lines for “{title.strip()}”, "
            f"mapped to {standard}, ready to paste into the next sustainability report with source links to field readings."
        )
    return (
        f"Paquete Datalab para el usuario final: tablas L2 validadas y líneas L3 de divulgación para «{title.strip()}», "
        f"mapeadas a {standard}, listas para el próximo reporte de sostenibilidad con enlaces a lecturas de campo."
    )


def flow_block(standard: str, lang: str) -> dict:
    ui = LEX["ui"][lang]
    l3 = ui["datalab.l3Template"].replace("{standard}", standard)
    return {
        "intro": ui["datalab.flowIntro"],
        "l1": ui["datalab.l1"],
        "l2": ui["datalab.l2"],
        "l3": l3,
    }


def enrich_gap(slug: str, gap: dict, nexus: dict) -> None:
    rank = int(gap.get("rank") or 0)
    block: dict = {"en": {}, "es": {}}
    for lang in ("en", "es"):
        ctx = (gap.get("context") or {}).get(lang, "")
        std = standards_from_context(ctx)
        block[lang] = {
            "reported_missing": reported_vs_missing(gap, lang),
            "startup_metrics": [],
            "flow": flow_block(std, lang),
            "deliverable": deliverable(gap, std, lang),
        }
        seen_names: set[str] = set()
        for m in gap.get("matches") or []:
            nk = (m.get("name") or "").strip().lower()
            if not nk or nk in seen_names:
                continue
            seen_names.add(nk)
            block[lang]["startup_metrics"].extend(
                startup_metrics(slug, rank, m, nexus, lang)
            )
    gap["datalab"] = block


def merge_ui(data: dict) -> None:
    for lang in ("en", "es"):
        ui = data.setdefault("ui", {}).setdefault(lang, {})
        for k, v in LEX["ui"][lang].items():
            ui[k] = v


def main() -> None:
    for path in sorted(ROOT.glob("*-snapshot/data.json")):
        slug = path.parent.name
        data = json.loads(path.read_text())
        merge_ui(data)
        nexus = data.get("nexus") or {}
        for gap in data.get("gaps") or []:
            enrich_gap(slug, gap, nexus)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("enriched", slug)

    log_path = Path(__file__).resolve().parent / "datalab-unsourced.log"
    log_path.write_text("\n".join(UNSOURCED) + ("\n" if UNSOURCED else ""))
    print(f"unsourced lines: {len(UNSOURCED)} -> {log_path}")


if __name__ == "__main__":
    main()
