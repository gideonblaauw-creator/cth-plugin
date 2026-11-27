#!/usr/bin/env python3
"""Emit review/contrast-check.md — WCAG contrast ratios for Zidi MEG deck tokens (Fix-5)."""
from __future__ import annotations

from pathlib import Path


def srgb(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    r, g, b = srgb(r), srgb(g), srgb(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def grade(ratio: float, large: bool = False) -> str:
    need = 3.0 if large else 4.5
    return "PASS AA" if ratio >= need else "FAIL"


PAIRS = [
    ("Body on white card", "#0C498A", "#FFFFFF", False),
    ("Body on navy glass", "#FFFFFF", "#002855", False),  # ~rgba(0,40,85,.88)
    ("Card title on white", "#0C498A", "#FFFFFF", True),
    ("Eyebrow green on navy glass", "#9DC384", "#002855", False),
    ("Title white on navy glass", "#FFFFFF", "#002855", True),
    ("Source on white glass", "#0C498A", "#FFFFFF", False),
    ("Source cyan on bleed (legacy)", "#B2EEFA", "#0C498A", False),
    ("Foot label on bleed", "#E8F8FC", "#0C498A", False),
    ("Conf label on bleed", "#9DC384", "#0C498A", False),
    ("KPI label on navy stat", "#FFFFFF", "#0C498A", True),
    ("KPI value cyan on navy", "#B2EEFA", "#0C498A", True),
    ("KPI label on white stat", "#0C498A", "#FFFFFF", False),
    ("KPI value green on white", "#669348", "#FFFFFF", True),
    ("Risk header on navy", "#FFFFFF", "#0C498A", True),
    ("Risk body on navy cell", "#FFFFFF", "#0C498A", False),
    ("Rate pill low", "#0C498A", "#9DC384", True),
    ("Rate pill med", "#0C498A", "#B2EEFA", True),
    ("Rate pill high", "#3A1A08", "#F4A574", True),
    ("Flip back on cyan tint", "#0C498A", "#E8FAFE", False),
    ("Flip print body on navy (Fix-5b)", "#FFFFFF", "#002855", False),
    ("Flip print front label on navy", "#B2EEFA", "#002855", True),
    ("Flip print back label on navy", "#9DC384", "#002855", True),
    ("Q6 lens body on navy (Fix-5b)", "#FFFFFF", "#002855", False),
    ("Q6 lens heading green on navy", "#9DC384", "#002855", True),
    ("Statement attr on statement", "#B2EEFA", "#002855", False),
    ("Closing body on navy", "#FFFFFF", "#0C498A", True),
]

out = Path(__file__).resolve().parent / "contrast-check.md"
lines = [
    "# Contrast check — Zidi MEG deck (Fix-6)",
    "",
    "Generated for Gideon review · WCAG 2.x relative luminance · body ≥4.5:1 · large text ≥3:1.",
    "",
    "| Style / pair | Foreground | Background | Ratio | Grade |",
    "|--------------|------------|------------|------:|-------|",
]
for name, fg, bg, large in PAIRS:
    ratio = contrast(fg, bg)
    lines.append(
        f"| {name} | `{fg}` | `{bg}` | {ratio:.2f}:1 | {grade(ratio, large)} |"
    )
lines.extend(
    [
        "",
        "## Fix-6 mitigations",
        "",
        "- Full-bleed photo backgrounds and scrims removed; flat navy or white slides per FODESEP `deck.css`.",
        "- Unblocked hero image rails (`fp-hero-rail`) beside content — thematic assets only, no people.",
        "- Programme cards show photo unblocked with solid navy caption bar (no gradient scrim).",
        "- Type scale ×1.5 vs Fix-5 v5 floors; source lines ≥22px.",
        "- GIZ growth slides after CTH programmes; umbrella facts cited to giz.de (8 countries, 90 ventures, verified 27 Nov 2026).",
        "",
        "_(PDF per-page overlap + live contrast run appended by `review/pdf-layout-check.mjs` after build.)_",
        "",
    ]
)
out.write_text("\n".join(lines), encoding="utf-8")
print(out)