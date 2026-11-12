#!/usr/bin/env python3
"""Estimate visible copy and count stored Spanish verbatim fields (pre-template)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERNAL = re.compile(
    r"shortfall|csoReady|checker|theme-only|theme match|graph relation|"
    r"déficit|Déficit|hipótesis GTM|draft GTM",
    re.I,
)

SPANISH_MARKERS = re.compile(r"[áéíóúñÁÉÍÓÚÑ¿¡]|(\b(de|la|el|en|que|por|con)\b)", re.I)


def count_stored_verbatim(data: dict) -> dict:
    n_gap_es = n_match_es = 0
    for g in data.get("gaps") or []:
        ev = g.get("report_evidence") or {}
        if ev.get("quote_es"):
            n_gap_es += 1
        for m in g.get("matches") or []:
            if m.get("public_quote"):
                n_match_es += 1
    snap = (data.get("snapshot") or {}).get("report_evidence") or {}
    n_snap = 1 if snap.get("quote_es") else 0
    return {
        "gap_report_quote_es": n_gap_es,
        "match_public_quote_es": n_match_es,
        "snapshot_quote_es": n_snap,
        "total_stored_es_verbatim": n_gap_es + n_match_es + n_snap,
    }


def visible_ui(data: dict, lang: str) -> str:
    parts = []
    ui = data.get("ui", {}).get(lang) or {}
    for k, v in ui.items():
        if k in ("snap.shortfall", "snap.themeNote"):
            continue
        parts.append(str(v))
    for g in data.get("gaps") or []:
        parts.append(g.get("title", {}).get(lang, ""))
        parts.append(g.get("context", {}).get(lang, ""))
        ev = g.get("report_evidence") or {}
        if lang == "en" and ev.get("quote_en"):
            parts.append(ev["quote_en"])
        for m in g.get("matches") or []:
            parts.append(m.get("why_es" if lang == "es" else "why", "") or "")
            if lang == "en" and m.get("public_quote_en"):
                parts.append(m["public_quote_en"])
    return "\n".join(parts)


def main() -> None:
    rows = []
    celsia = None
    for p in sorted(ROOT.glob("*-snapshot/data.json")):
        slug = p.parent.name.replace("-snapshot", "")
        data = json.loads(p.read_text())
        counts = count_stored_verbatim(data)
        vis_en = visible_ui(data, "en")
        vis_es = visible_ui(data, "es")
        hits_en = INTERNAL.findall(vis_en)
        hits_es = INTERNAL.findall(vis_es)
        row = {
            "slug": slug,
            **counts,
            "internal_hits_en": len(hits_en),
            "internal_hits_es": len(hits_es),
        }
        rows.append(row)
        if slug == "celsia":
            celsia = row
    print(json.dumps({"pages": rows, "celsia": celsia}, indent=2))


if __name__ == "__main__":
    main()
