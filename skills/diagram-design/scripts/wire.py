#!/usr/bin/env python3
"""CTH wire diagram CLI — validate, render, and export wire specs."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from export_png import export_png  # noqa: E402
from render_wire import DEFAULT_FONTS_HREF, SKILL_DIR, render_spec_path  # noqa: E402
from validate_spec import load_spec, validate_spec_path  # noqa: E402


def copy_fonts(out_dir: Path) -> None:
    src = SKILL_DIR / "assets" / "fonts" / "wire"
    dest = out_dir / "fonts" / "wire"
    dest.mkdir(parents=True, exist_ok=True)
    for woff in sorted(src.glob("*.woff2")):
        (dest / woff.name).write_bytes(woff.read_bytes())


def write_outputs(
    spec_path: Path,
    out_dir: Path,
    *,
    html: bool,
    svg: bool,
    md: bool,
    png: bool,
) -> Path:
    errors = validate_spec_path(spec_path)
    if errors:
        raise SystemExit(f"Invalid spec:\n" + "\n".join(f"  - {e}" for e in errors))

    out_dir.mkdir(parents=True, exist_ok=True)
    copy_fonts(out_dir)
    html_doc, svg_doc, md_doc = render_spec_path(spec_path, fonts_href=DEFAULT_FONTS_HREF)
    spec_id = load_spec(spec_path)["id"]
    html_path = out_dir / f"{spec_id}-wire.html"
    svg_path = out_dir / f"{spec_id}-wire.svg"
    md_path = out_dir / f"{spec_id}-wire.md"
    png_path = out_dir / f"{spec_id}-wire.png"

    if html or png:
        html_path.write_text(html_doc, encoding="utf-8")
    if svg:
        svg_path.write_text(svg_doc, encoding="utf-8")
    if md:
        md_path.write_text(md_doc, encoding="utf-8")
    if png:
        if not html_path.is_file():
            html_path.write_text(html_doc, encoding="utf-8")
        export_png(html_path, png_path, scale=2)
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Wire YAML spec")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--svg", action="store_true")
    parser.add_argument("--md", action="store_true")
    parser.add_argument("--png", action="store_true")
    parser.add_argument(
        "--check-determinism",
        action="store_true",
        help="Render SVG twice and assert byte-identical output",
    )
    args = parser.parse_args()
    if not any((args.html, args.svg, args.md, args.png)):
        args.html = args.svg = args.md = args.png = True

    if args.check_determinism:
        _, svg_a, _ = render_spec_path(args.spec)
        _, svg_b, _ = render_spec_path(args.spec)
        da = hashlib.sha256(svg_a.encode()).hexdigest()
        db = hashlib.sha256(svg_b.encode()).hexdigest()
        if da != db:
            print("FAIL determinism: SVG hashes differ", file=sys.stderr)
            return 1
        print(f"OK determinism sha256={da}")

    write_outputs(
        args.spec,
        args.out,
        html=args.html,
        svg=args.svg,
        md=args.md,
        png=args.png,
    )
    print(f"OK wrote to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
