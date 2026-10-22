#!/usr/bin/env python3
"""Strip internal GTM/checker wording from teaser data.json (client-facing copy)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMPANY_PATTERNS = [
    r"\.\s*Wave\s*1[^.]*",
    r"\.\s*Ola\s*1[^.]*",
    r"\s*Wave\s*1[^.]*\.?",
    r"\s*Ola\s*1[^.]*\.?",
    r"\s*\(\s*6\s*[–-]\s*10[^)]*\)",
    r"\s*Persona:\s*CSO\.?",
    r"\s*Persona:\s*CSO,?",
    r"\s*rank\s*\d+\.?",
    r"\s*rango\s*\d+\.?",
    r"\s*maker\s*[A-Z]\.?",
]

WHY_TRAIL_EN = re.compile(
    r"\s*(The quote does not name [^.]+\.|quote does not name [^.]+\.|FENOGE is a funder, so it has no startup stage\.)",
    re.I,
)
WHY_TRAIL_ES = re.compile(
    r"\s*(La cita no nombra [^.]+\.|FENOGE es financiador[^.]+\.)",
    re.I,
)


def clean_company(s: str) -> str:
    for pat in COMPANY_PATTERNS:
        s = re.sub(pat, "", s, flags=re.I)
    return re.sub(r"\s{2,}", " ", s).strip().rstrip(",")


def clean_why(s: str, lang: str) -> str:
    if not s:
        return s
    s = WHY_TRAIL_EN.sub("", s) if lang == "en" else WHY_TRAIL_ES.sub("", s)
    s = re.sub(r"\s*;\s*$", "", s).strip()
    return s


def clean_ui_block(block: dict, data: dict, lang: str) -> None:
    block.pop("snap.shortfall", None)
    block.pop("snap.themeNote", None)
    if "hero.lead" in block:
        block["hero.lead"] = ""
    if "hero.company" in block:
        block["hero.company"] = clean_company(block["hero.company"])
    if "cta.body" in block:
        block["cta.body"] = (
            "Book a short call with the CleantechHUB team to explore next steps."
            if lang == "en"
            else "Agende una llamada breve con el equipo CleantechHUB para explorar siguientes pasos."
        )
    for key in ("foot.line",):
        if key not in block:
            continue
        t = block[key]
        t = re.sub(r"\s*[—–-]\s*draft GTM hypothesis\.?", "", t, flags=re.I)
        t = re.sub(r"\s*draft GTM hypothesis\.?", "", t, flags=re.I)
        t = re.sub(r"\s*hipótesis GTM en borrador\.?", "", t, flags=re.I)
        t = re.sub(r"\bgap snapshot\b", "sustainability snapshot", t, flags=re.I)
        t = re.sub(r"\bpanorama de brechas\b", "panorama de sostenibilidad", t, flags=re.I)
        t = re.sub(r"\bThis page is a draft GTM hypothesis\.\s*", "", t, flags=re.I)
        t = re.sub(r"\bEsta página es una hipótesis GTM en borrador\.\s*", "", t, flags=re.I)
        t = re.sub(r"\bThis page is a Book\s*", "Book ", t, flags=re.I)
        t = re.sub(r"\bEsta página es una Agende\s*", "Agende ", t, flags=re.I)
        t = re.sub(r"borrador de la hipótesis GTM\.?", "", t, flags=re.I)
        t = re.sub(r"Instantánea de la brecha de", "Panorama de sostenibilidad —", t, flags=re.I)
        t = re.sub(r"\s{2,}", " ", t).strip()
        block[key] = t.strip()


def clean_nexus(data: dict) -> None:
    repl = (
        ("customer journey", "customer experience"),
        ("end-to-end customer experience", "digital customer experience"),
        ("viaje digital de extremo a extremo", "experiencia digital de extremo a extremo"),
    )
    for entry in (data.get("nexus") or {}).values():
        for field in ("d", "ds"):
            if not entry.get(field):
                continue
            entry[field] = re.sub(r";\s*quote does not name [^.]+\.?", "", entry[field], flags=re.I)
            entry[field] = re.sub(r";\s*La cita no nombra [^.]+\.?", "", entry[field], flags=re.I)
            for old, new in repl:
                entry[field] = re.sub(re.escape(old), new, entry[field], flags=re.I)
            entry[field] = entry[field].strip().rstrip(";")


def process(path: Path) -> None:
    data = json.loads(path.read_text())
    for lang in ("en", "es"):
        ui = data.get("ui", {}).get(lang)
        if ui:
            clean_ui_block(ui, data, lang)
    clean_nexus(data)
    data.pop("footer_note", None)
    for g in data.get("gaps") or []:
        g.pop("note", None)
        for m in g.get("matches") or []:
            if m.get("why"):
                m["why"] = clean_why(m["why"], "en")
            if m.get("why_es"):
                m["why_es"] = clean_why(m["why_es"], "es")
            for field in ("why", "why_es"):
                if not m.get(field):
                    continue
                m[field] = re.sub(
                    r"\s*(FENOGE is a funder[^.]*\.|not a startup[^.]*\.|no startup stage[^.]*\.)",
                    "",
                    m[field],
                    flags=re.I,
                ).strip()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    for p in sorted(ROOT.glob("*-teaser/data.json")):
        process(p)
        print("cleaned", p.parent.name)


if __name__ == "__main__":
    main()
