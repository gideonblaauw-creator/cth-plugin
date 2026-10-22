#!/usr/bin/env python3
"""Simulate visible teaser copy and grep for internal/harness wording (not HTML meta)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAT = re.compile(
    r"shortfall|csoReady|checker|theme-only|déficit|"
    r"matches:\s*\d|dropped|not a startup|"
    r"journey step|paso del journey|\bjourney\b|"
    r"paso del recorrido|etapa del recorrido|"
    r"\bGTM\b|\bdraft\b|\bborrador\b|CSO delivery|entrega CSO|"
    r"\bAccessed\b|\bConsultado\b",
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
    for g in data.get("gaps") or []:
        lines.append(g.get("title", {}).get(lang, ""))
        lines.append(g.get("context", {}).get(lang, ""))
        ev = g.get("report_evidence") or {}
        if lang == "en" and ev.get("quote_en"):
            lines.append(ev["quote_en"])
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
    for p in sorted(ROOT.glob("*-teaser/data.json")):
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
