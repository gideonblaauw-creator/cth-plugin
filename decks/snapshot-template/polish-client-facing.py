#!/usr/bin/env python3
"""Client-facing polish: team copy, CTA/footer/hero strings, Angélica role, no access dates."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACCESS_PAT = re.compile(
    r"\.\s*Accessed\s+\d{4}-\d{2}-\d{2}\.?|"
    r"Accessed\s+\d{4}-\d{2}-\d{2}\.?|"
    r"Consultado(\s+el)?\s+\d{2}-\d{2}-\d{4}\.?|"
    r"Consultado\s+\d{4}-\d{2}-\d{2}\.?",
    re.I,
)


def strip_access(text: str) -> str:
    if not text:
        return ""
    t = ACCESS_PAT.sub("", text)
    t = re.sub(r"\s{2,}", " ", t).strip()
    t = re.sub(r"\s+([,.])", r"\1", t)
    return t.strip(" .—–-")


def clean_html_report(text: str) -> str:
    t = strip_access(text)
    t = re.sub(r"\s*\.\s*\.", ".", t)
    return t.strip()


def polish_ui(block: dict, lang: str) -> None:
    block["team.title"] = (
        "Who shaped this snapshot"
        if lang == "en"
        else "Quién elaboró este snapshot"
    )
    block["hero.lead"] = ""
    block["cta.title"] = ""
    block["cta.body"] = ""
    block["foot.line"] = ""
    if "hero.report" in block:
        block["hero.report"] = clean_html_report(block["hero.report"])
    for key in list(block.keys()):
        if isinstance(block[key], str):
            block[key] = strip_access(block[key])
            block[key] = re.sub(r"\bdraft\b|\bGTM\b|\bborrador\b", "", block[key], flags=re.I)
            block[key] = re.sub(r"CSO delivery|entrega CSO", "", block[key], flags=re.I)
            block[key] = re.sub(r"\s{2,}", " ", block[key]).strip()


def polish_team(team: list) -> None:
    for person in team:
        if person.get("name") != "Angélica Díaz":
            continue
        person.setdefault("role", {})
        person["role"]["en"] = "Tech Lead"
        person["role"]["es"] = "Líder de Tecnología"


def main() -> None:
    for p in sorted(ROOT.glob("*-snapshot/data.json")):
        data = json.loads(p.read_text())
        for lang in ("en", "es"):
            ui = data.get("ui", {}).get(lang)
            if ui:
                polish_ui(ui, lang)
        polish_team(data.get("team") or [])
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("polished", p.parent.name)


if __name__ == "__main__":
    main()
