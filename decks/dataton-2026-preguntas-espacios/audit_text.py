#!/usr/bin/env python3
"""Banned-word audit on rendered PDF text."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "dataton-preguntas-espacios.pdf"

BANNED = [
    r"\bPR\b",
    r"\bHands\b",
    r"\bOrchestrator\b",
    r"\bOrch\b",
    r"\bCursor\b",
    r"\bdesk\b",
    r"\bGO\b",
    r"\bticket\b",
    r"\bgithub\b",
    r"decks/",
    r"\.md\b",
    r"gratis",
    r"gratuito",
    r"drive\.google",
    r"->",
    r"\bdos\s+mil\b",
    r"\bloop\b",
    r"cit-able",
    r"sin\s+costo",
]

RUN7_TOOL = [
    r"\btablero",
    r"\blienzo",
    r"\bmapa",
    r"\bflujo",
    r"\bhoja",
    r"\bgrada",
    r"\bETL",
    r"\bcapa\b",
    r"\balmac[eé]n",
    r"\bbodega",
    r"\bcitable",
    r"\btrazabilidad",
    r"\bmotor",
    r"\bpaisaje",
    r"\br[eé]gimen",
    r"\bnicho",
    r"\bh[eé]lice",
    r"\bdashboard",
    r"\bheatmap",
    r"\bcanvas",
]

RUN8_JARGON = [
    r"Carapulica",
    r"pregunta\s+núcleo",
    r"\bsandbox",
    r"\bsandboxes",
    r"dato\s+crudo",
    r"datos\s+crudos",
    r"archivo\s+muerto",
    r"vacíos\s+honestos",
    r"\bcohorte",
    r"citar\s+fuentes\s+oficiales",
    r"aguanta\s+una\s+conclusión",
    r"consorcio",
]

MOD_IN_Q = [
    r"sin\s+prometer",
    r"sin\s+inventar",
    r"sin\s+fijar",
    r"sin\s+confundir",
]

INSIDER = [
    r"armar\s+el\s+modelo",
    r"\bescalera\b",
    r"\bentornos\b",
    r"relato\s+sigue\s+vivo",
    r"\bhuecos\b",
]

MAX_ANSWER_WORDS = 25


def strip_excluded_blocks(text: str) -> str:
    """Remove page titles and VIENE DE / LLEVA A strips for jargon grep."""
    lines = text.splitlines()
    out: list[str] = []
    skip = False
    for ln in lines:
        if ln.strip() in ("V IE NE DE", "LLEVA A", "VIENE DE", "LLEVA A"):
            skip = True
            continue
        if skip:
            if ln.strip().startswith("Pregunta:"):
                skip = False
            else:
                continue
        out.append(ln)
    return "\n".join(out)


def conversation_lines(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        if ln.strip().startswith(("Pregunta:", "Repregunta:")):
            lines.append(ln)
    return "\n".join(lines)


def anticipated_answers(text: str) -> list[str]:
    answers: list[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("[") and s.endswith("]"):
            answers.append(s[1:-1].strip())
    return answers


def main() -> int:
    if not PDF.is_file():
        print("PDF missing", file=sys.stderr)
        return 1
    text = subprocess.check_output(["pdftotext", str(PDF), "-"], text=True, errors="replace")
    hits = []
    for pat in BANNED:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line = text[max(0, text.rfind("\n", 0, m.start()) + 1) : text.find("\n", m.start())]
            hits.append((pat, line.strip()[:120]))
    jargon_body = strip_excluded_blocks(text)
    title_allow = re.compile(r"Data sandbox de innovación", re.I)
    for pat in RUN7_TOOL + RUN8_JARGON:
        for m in re.finditer(pat, jargon_body, re.IGNORECASE):
            line = jargon_body[max(0, jargon_body.rfind("\n", 0, m.start()) + 1) : jargon_body.find("\n", m.start())]
            if pat == r"\bsandbox" and title_allow.search(line):
                continue
            hits.append((pat, line.strip()[:120]))
    conv = conversation_lines(text)
    for pat in MOD_IN_Q:
        for m in re.finditer(pat, conv, re.IGNORECASE):
            line = conv[max(0, conv.rfind("\n", 0, m.start()) + 1) : conv.find("\n", m.start())]
            hits.append((pat + " (Q/R)", line.strip()[:120]))
    for pat in INSIDER:
        for m in re.finditer(pat, jargon_body, re.IGNORECASE):
            line = jargon_body[max(0, jargon_body.rfind("\n", 0, m.start()) + 1) : jargon_body.find("\n", m.start())]
            hits.append((pat + " (insider)", line.strip()[:120]))
    for i, ans in enumerate(anticipated_answers(text), 1):
        wc = len(ans.split())
        if wc > MAX_ANSWER_WORDS:
            hits.append((f">{MAX_ANSWER_WORDS} words", f"answer#{i}: {wc} — {ans[:80]}"))
        if ";" in ans and "cooperación financia alertas" not in ans:
            hits.append(("semicolon (answer)", f"answer#{i}: {ans[:80]}"))
    if hits:
        print(f"BANNED HITS: {len(hits)}")
        for pat, line in hits:
            print(f"  [{pat}] {line}")
        return 2
    print("BANNED HITS: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())