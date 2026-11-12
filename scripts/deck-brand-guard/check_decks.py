#!/usr/bin/env python3
"""CI checker for decks/*/index.html — CleantechHUB house format and safety rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[2]
GUARD_DIR = Path(__file__).resolve().parent
DECKS_DIR = ROOT / "decks"


@dataclass(frozen=True)
class Finding:
    deck: str
    check: str
    message: str

    def key(self) -> tuple[str, str, str]:
        return (self.deck, self.check, self.message)


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_line_list(path: Path) -> list[str]:
    if not path.is_file():
        return []
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def discover_decks() -> list[tuple[str, Path]]:
    if not DECKS_DIR.is_dir():
        return []
    out: list[tuple[str, Path]] = []
    for child in sorted(DECKS_DIR.iterdir()):
        if not child.is_dir():
            continue
        index = child / "index.html"
        if index.is_file():
            out.append((child.name, index))
    return out


def deck_source(slug: Path, index: Path) -> str:
    """index.html plus shell/deck.css when present (assembled decks inline CSS anyway)."""
    parts = [index.read_text(encoding="utf-8", errors="replace")]
    css = slug / "shell" / "deck.css"
    if css.is_file():
        parts.append(css.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def check_cth_colors(slug: str, text: str, expected: dict) -> list[Finding]:
    findings: list[Finding] = []
    vars_map = expected.get("cth_css_variables") or {}
    for name, hex_val in vars_map.items():
        if name not in text:
            findings.append(
                Finding(slug, "cth.colors", f"missing CSS variable {name}")
            )
        hex_norm = str(hex_val).upper()
        if hex_norm not in text.upper() and hex_norm.lstrip("#") not in text.upper():
            findings.append(
                Finding(
                    slug,
                    "cth.colors",
                    f"missing hex {hex_val} for {name}",
                )
            )
    return findings


FONT_PATTERNS = {
    "Inter": re.compile(
        r"(?:font-family\s*:[^;]*['\"]Inter['\"]"
        r"|fonts\.googleapis\.com/css2[^\"']*family=Inter"
        r"|@font-face\s*\{[^}]*font-family\s*:\s*['\"]Inter['\"])",
        re.I | re.S,
    ),
}


def check_cth_fonts(slug: str, text: str, expected: dict) -> list[Finding]:
    findings: list[Finding] = []
    for font in expected.get("cth_fonts") or []:
        pat = FONT_PATTERNS.get(font)
        if pat is not None:
            if not pat.search(text):
                findings.append(
                    Finding(slug, "cth.fonts", f"missing font family {font!r}")
                )
        elif font not in text:
            findings.append(
                Finding(slug, "cth.fonts", f"missing font family {font!r}")
            )
    return findings


def check_cth_logo(slug: str, text: str, expected: dict) -> list[Finding]:
    basenames = expected.get("cth_logo_basenames") or []
    for base in basenames:
        if base in text:
            return []
    findings = [
        Finding(
            slug,
            "cth.logo",
            "no CTH logo reference (expected one of: "
            + ", ".join(basenames)
            + ")",
        )
    ]
    return findings


PRICE_PATTERNS = [
    re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:USD|usd|million|billion|M|K))?", re.I),
    re.compile(r"\bUSD\s?\d[\d,]*(?:\.\d+)?", re.I),
    re.compile(r"\bCOP\s?\d[\d,]*(?:\.\d+)?", re.I),
    re.compile(r"\b(?:precio|price)\s*:?\s*\d", re.I),
    re.compile(r"\bUS\$\s?\d[\d,]*", re.I),
]


def strip_html(html: str) -> str:
    no_script = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    no_style = re.sub(r"(?is)<style.*?>.*?</style>", " ", no_script)
    text = re.compile(r"(?s)<[^>]+>").sub(" ", no_style)
    return re.sub(r"\s+", " ", text)


def check_public_no_prices(
    slug: str,
    html: str,
    public_slugs: set[str],
    allowlist: list[re.Pattern[str]],
) -> list[Finding]:
    if slug not in public_slugs:
        return []
    plain = strip_html(html)
    findings: list[Finding] = []
    for pat in PRICE_PATTERNS:
        for m in pat.finditer(plain):
            span = m.group(0)
            if any(a.search(span) or a.search(plain[max(0, m.start() - 40) : m.end() + 40]) for a in allowlist):
                continue
            findings.append(
                Finding(
                    slug,
                    "public.no_prices",
                    f"currency or price pattern: {span.strip()!r}",
                )
            )
    return findings


def check_no_confidential(
    slug: str,
    html: str,
    conf_slugs: set[str],
    markers: list[str],
) -> list[Finding]:
    findings: list[Finding] = []
    if slug in conf_slugs:
        findings.append(
            Finding(
                slug,
                "repo.no_confidential",
                f"slug {slug!r} is listed server-only — remove from git",
            )
        )
    lower = html.lower()
    for marker in markers:
        if marker.lower() in lower:
            findings.append(
                Finding(
                    slug,
                    "repo.no_confidential",
                    f"confidential marker {marker!r} in index.html",
                )
            )
    return findings


def load_baseline(path: Path) -> set[tuple[str, str, str]]:
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    keys: set[tuple[str, str, str]] = set()
    for item in data.get("violations", []):
        keys.add((item["deck"], item["check"], item["message"]))
    return keys


def compile_allowlist(raw: list[str]) -> list[re.Pattern[str]]:
    out: list[re.Pattern[str]] = []
    for line in raw:
        try:
            out.append(re.compile(line, re.I))
        except re.error as e:
            raise SystemExit(f"Invalid allowlist regex {line!r}: {e}") from e
    return out


def run_checks(
    baseline_path: Path,
    update_baseline: bool = False,
) -> int:
    expected = load_yaml(GUARD_DIR / "expected.yaml")
    public_slugs = set(load_line_list(GUARD_DIR / "public_decks.txt"))
    conf_slugs = set(load_line_list(GUARD_DIR / "confidential_slugs.txt"))
    markers = load_line_list(GUARD_DIR / "confidential_markers.txt")
    allowlist = compile_allowlist(load_line_list(GUARD_DIR / "price_allowlist.txt"))

    all_findings: list[Finding] = []
    for slug, index in discover_decks():
        deck_path = index.parent
        text = deck_source(deck_path, index)
        html = index.read_text(encoding="utf-8", errors="replace")
        all_findings.extend(check_cth_colors(slug, text, expected))
        all_findings.extend(check_cth_fonts(slug, text, expected))
        all_findings.extend(check_cth_logo(slug, text, expected))
        all_findings.extend(check_public_no_prices(slug, html, public_slugs, allowlist))
        all_findings.extend(check_no_confidential(slug, html, conf_slugs, markers))

    baseline = load_baseline(baseline_path)
    new_failures: list[Finding] = []
    warnings: list[Finding] = []

    for f in all_findings:
        if f.key() in baseline:
            warnings.append(f)
        else:
            new_failures.append(f)

    if update_baseline:
        payload = {
            "violations": [
                {"deck": f.deck, "check": f.check, "message": f.message}
                for f in sorted(all_findings, key=lambda x: (x.deck, x.check, x.message))
            ]
        }
        baseline_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote baseline with {len(all_findings)} violation(s) to {baseline_path}")
        return 0

    for f in warnings:
        print(f"WARNING (baseline): [{f.deck}] {f.check}: {f.message}")
    for f in new_failures:
        print(f"ERROR: [{f.deck}] {f.check}: {f.message}")

    if new_failures:
        print(f"\n{len(new_failures)} new violation(s); {len(warnings)} baselined warning(s).")
        return 1
    print(f"OK — {len(warnings)} baselined warning(s), 0 new violations.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=GUARD_DIR / "baseline.json",
        help="JSON file listing known violations (warn only)",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Rewrite baseline from current deck scan (maintainer use)",
    )
    args = parser.parse_args()
    sys.exit(run_checks(args.baseline, update_baseline=args.update_baseline))


if __name__ == "__main__":
    main()
