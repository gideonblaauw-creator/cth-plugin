#!/usr/bin/env python3
"""STE-80 warn-only linter for wire brief markdown files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROCEDURAL_MAX = 20
DESCRIPTIVE_MAX = 25
MAX_NOUN_CLUSTER = 3
MAX_PARAGRAPH_SENTENCES = 6

# Common English stopwords / non-nouns for a light noun-stack heuristic
ARTICLES = {"a", "an", "the", "this", "that", "these", "those"}
PREPS = {
    "in", "on", "at", "to", "for", "of", "with", "from", "by", "as", "into",
    "via", "and", "or", "but", "if", "when", "after", "before",
}

PASSIVE_RE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+(\w+ed|built|done|shown|given|taken|made|used|hooked)\b",
    re.I,
)
PASSIVE_BY_RE = re.compile(r"\b\w+ed\s+by\b", re.I)
ING_NOUN_RE = re.compile(
    r"\b(\w+ing)\b", re.I
)  # flagged unless glossary or verb-like context
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
STEP_LINE_RE = re.compile(r"^\s*\d+\.\s+", re.M)
GLOSS_LINE_RE = re.compile(r"^\s*_(.+?)_\s*$|^\s*//.*español|^\s*\*.*glosa", re.I | re.M)


def repo_glossary_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "cth-glossary.md"


def load_glossary(path: Path | None = None) -> set[str]:
    path = path or repo_glossary_path()
    terms: set[str] = set()
    if not path.is_file():
        return terms
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and not line.startswith("| Term") and not line.startswith("|--"):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                terms.add(cells[0])
                for part in re.split(r"[/\s]+", cells[0]):
                    if part:
                        terms.add(part)
    return {t.lower() for t in terms if t}


def strip_front_matter_and_gloss(text: str) -> str:
    """Remove YAML front matter and italic gloss-only lines from scoring body."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    lines = []
    for line in text.splitlines():
        if GLOSS_LINE_RE.match(line.strip()):
            continue
        if line.strip().startswith("_") and line.strip().endswith("_"):
            continue
        lines.append(line)
    return "\n".join(lines)


def split_paragraphs(text: str) -> list[str]:
    paras: list[str] = []
    buf: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            if buf:
                paras.append("\n".join(buf).strip())
                buf = []
            continue
        if not line.strip():
            if buf:
                paras.append("\n".join(buf).strip())
                buf = []
            continue
        buf.append(line)
    if buf:
        paras.append("\n".join(buf).strip())
    return [p for p in paras if p]


def split_sentences(paragraph: str) -> list[str]:
    paragraph = re.sub(r"\n+", " ", paragraph.strip())
    # Do not treat the period in "1." as a sentence boundary.
    masked = re.sub(r"\b(\d+)\.", r"\1<ListDot>", paragraph)
    parts = SENTENCE_SPLIT_RE.split(masked)
    restored = [p.replace("<ListDot>", ".").strip() for p in parts if p.strip()]
    return restored


def is_procedural(sentence: str, in_steps: bool) -> bool:
    if in_steps:
        return True
    if STEP_LINE_RE.match(sentence):
        return True
    first = sentence.split()[0].lower() if sentence.split() else ""
    if first in {"you", "must", "do", "run", "add", "remove", "check", "confirm"}:
        return True
    return False


def word_tokens(sentence: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9'-]+", sentence)


def count_noun_cluster(sentence: str, glossary: set[str]) -> int:
    tokens = word_tokens(sentence)
    cluster = 0
    max_cluster = 0
    for raw in tokens:
        low = raw.lower()
        if low in ARTICLES or low in PREPS or low in glossary:
            cluster = 0
            continue
        if raw[0].isupper() or low.endswith("tion") or low.endswith("ment"):
            cluster += 1
            max_cluster = max(max_cluster, cluster)
        else:
            cluster = 0
    return max_cluster


def score_sentence(
    sentence: str,
    *,
    procedural: bool,
    glossary: set[str],
) -> dict:
    tokens = word_tokens(sentence)
    words = len(tokens)
    limit = PROCEDURAL_MAX if procedural else DESCRIPTIVE_MAX
    warnings: list[str] = []
    scores = {
        "length": max(0, words - limit),
        "passive": 0,
        "ing": 0,
        "noun_stack": 0,
    }

    if words > limit:
        warnings.append(f"length:{words}>{limit}")

    if PASSIVE_RE.search(sentence) or PASSIVE_BY_RE.search(sentence):
        scores["passive"] = 1
        warnings.append("passive_voice")

    for m in ING_NOUN_RE.finditer(sentence):
        word = m.group(1)
        if word.lower() in glossary:
            continue
        # allow common participles in "is running"
        if re.search(rf"\b(is|are|was|were)\s+{re.escape(word)}\b", sentence, re.I):
            continue
        scores["ing"] += 1
        warnings.append(f"ing_form:{word}")

    stack = count_noun_cluster(sentence, glossary)
    if stack > MAX_NOUN_CLUSTER:
        scores["noun_stack"] = stack - MAX_NOUN_CLUSTER
        warnings.append(f"noun_stack:{stack}>{MAX_NOUN_CLUSTER}")

    return {
        "text": sentence,
        "procedural": procedural,
        "word_count": words,
        "scores": scores,
        "warnings": warnings,
    }


def lint_text(text: str, glossary: set[str] | None = None) -> dict:
    glossary = glossary or load_glossary()
    body = strip_front_matter_and_gloss(text)
    sentence_results: list[dict] = []
    paragraph_results: list[dict] = []

    current_section = ""
    buf: list[str] = []

    def flush_buf() -> None:
        nonlocal buf
        if not buf:
            return
        para = "\n".join(buf).strip()
        buf = []
        if not para:
            return
        in_steps = current_section.startswith("STEPS")
        sents = split_sentences(para)
        para_warnings: list[str] = []
        if len(sents) > MAX_PARAGRAPH_SENTENCES:
            para_warnings.append(
                f"paragraph_sentences:{len(sents)}>{MAX_PARAGRAPH_SENTENCES}"
            )
        paragraph_results.append(
            {"sentence_count": len(sents), "warnings": para_warnings}
        )
        for sent in sents:
            proc = is_procedural(sent, in_steps)
            sentence_results.append(
                score_sentence(sent, procedural=proc, glossary=glossary)
            )

    for line in body.splitlines():
        if line.strip().startswith("## "):
            flush_buf()
            current_section = line.strip().lstrip("#").strip().upper()
            continue
        if not line.strip():
            flush_buf()
            continue
        buf.append(line)
    flush_buf()

    total_warnings = sum(len(s["warnings"]) for s in sentence_results) + sum(
        len(p["warnings"]) for p in paragraph_results
    )

    return {
        "sentences": sentence_results,
        "paragraphs": paragraph_results,
        "summary": {
            "sentence_count": len(sentence_results),
            "warning_count": total_warnings,
        },
    }


def human_report(report: dict) -> str:
    lines = [
        f"STE-80 lint (warn-only): {report['summary']['sentence_count']} sentences, "
        f"{report['summary']['warning_count']} warnings",
        "",
    ]
    for i, s in enumerate(report["sentences"], 1):
        flag = ", ".join(s["warnings"]) if s["warnings"] else "ok"
        kind = "proc" if s["procedural"] else "desc"
        lines.append(f"{i}. [{kind} w={s['word_count']}] {flag}")
        lines.append(f"   {s['text'][:120]}{'…' if len(s['text']) > 120 else ''}")
    for j, p in enumerate(report["paragraphs"], 1):
        if p["warnings"]:
            lines.append(f"Paragraph {j}: {', '.join(p['warnings'])}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="STE-80 warn-only linter for brief.md")
    parser.add_argument("brief", type=Path, help="Path to brief markdown")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument(
        "--glossary",
        type=Path,
        default=None,
        help="Optional glossary markdown path",
    )
    args = parser.parse_args()
    text = args.brief.read_text(encoding="utf-8")
    glossary = load_glossary(args.glossary) if args.glossary else load_glossary()
    report = lint_text(text, glossary)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(human_report(report))
        print("\n--- JSON ---")
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
