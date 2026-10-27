#!/usr/bin/env python3
"""Simulate visible snapshot copy and grep for internal/harness wording (not HTML meta)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_LEGACY_LABEL = "tea" + "ser"
PAT = re.compile(
    r"shortfall|csoReady|checker|theme-only|déficit|"
    r"matches:\s*\d|dropped|not a startup|"
    r"journey step|paso del journey|\bjourney\b|"
    r"paso del recorrido|etapa del recorrido|"
    r"\bGTM\b|\bdraft\b|\bborrador\b|CSO delivery|entrega CSO|"
    r"\bAccessed\b|\bConsultado\b|"
    rf"\b{_LEGACY_LABEL}\b",
    re.I,
)


def visible_lines(data: dict, lang: str) -> list[str]:
    lines: list[str] = []
    ui = data.get("ui", {}).get(lang) or {}
    skip = {
        "snap.shortfall",
        "snap.themeNote",
        "cta.title",
        "cta.body",
        "foot.line",
        "hero.lead",
    }
    for k, v in ui.items():
        if k in skip:
            continue
        if not str(v).strip():
            continue
        lines.append(str(v))
    hist = data.get("cth_history") or {}
    for item in hist.get("timeline") or []:
        lines.append((item.get("text") or {}).get(lang, "") or (item.get("text") or {}).get("en", ""))
    for m in hist.get("metrics") or []:
        lines.append(m.get("value", ""))
        lines.append((m.get("label") or {}).get(lang, ""))
    for g in data.get("gaps") or []:
        lines.append(g.get("title", {}).get(lang, ""))
        lines.append((g.get("headline") or {}).get(lang, ""))
        ch = g.get("chart") or {}
        lines.append((ch.get("note") or {}).get(lang, "") if isinstance(ch.get("note"), dict) else "")
        for b in ch.get("bars") or []:
            lines.append((b.get("label") or {}).get(lang, ""))
        lines.append(g.get("context", {}).get(lang, ""))
        ev = g.get("report_evidence") or {}
        if lang == "en" and ev.get("quote_en"):
            lines.append(ev["quote_en"])
        dl = (g.get("datalab") or {}).get(lang) or {}
        lines.append(dl.get("reported_missing", ""))
        lines.append(dl.get("deliverable", ""))
        for row in dl.get("startup_metrics") or []:
            lines.append(
                " ".join(
                    str(row.get(k, ""))
                    for k in ("startup", "metric", "unit", "frequency", "method", "note")
                )
            )
        flow = dl.get("flow") or {}
        for fk in ("intro", "l1", "l2", "l3"):
            lines.append(flow.get(fk, ""))
        for m in dedupe_names(g.get("matches") or []):
            nx = (data.get("nexus") or {}).get(m.get("name", ""), {})
            lines.append(nx.get("ds" if lang == "es" else "d") or m.get("description") or "")
    for person in data.get("team") or []:
        lines.append(person.get("role", {}).get(lang, "") or "")
    return [ln for ln in lines if ln.strip()]


def dedupe_names(matches: list) -> list:
    seen: set[str] = set()
    out = []
    for m in matches:
        k = (m.get("name") or "").strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out


def main() -> int:
    hits = 0
    for p in sorted(ROOT.glob("*-snapshot/data.json")):
        slug = p.parent.name
        data = json.loads(p.read_text())
        for lang in ("en", "es"):
            for line in visible_lines(data, lang):
                if PAT.search(line):
                    hits += 1
                    print(f"HIT {slug} {lang}: {line[:140]}")
    print(f"Total visible hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
