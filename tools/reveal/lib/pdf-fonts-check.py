#!/usr/bin/env python3
"""Return 0 if PDF embeds Open Sans (subset names like AAAAAA+OpenSans-Regular)."""
import sys

try:
    from pypdf import PdfReader
except ImportError:
    print("error: pypdf not installed", file=sys.stderr)
    sys.exit(2)

pdf_path = sys.argv[1]


def collect_fonts(obj, depth=0, found=None):
    if found is None:
        found = set()
    if depth > 10:
        return found
    if isinstance(obj, dict):
        font_map = obj.get("/Font")
        if font_map:
            for v in font_map.values():
                try:
                    f = v.get_object()
                    name = str(f.get("/BaseFont", f.get("/FontName", "")))
                    found.add(name)
                except Exception:
                    pass
        for v in obj.values():
            collect_fonts(v, depth + 1, found)
    elif isinstance(obj, list):
        for v in obj:
            collect_fonts(v, depth + 1, found)
    return found


def main():
    reader = PdfReader(pdf_path)
    fonts = set()
    for page in reader.pages:
        fonts |= collect_fonts(page)
    root = reader.trailer.get("/Root")
    if root:
        fonts |= collect_fonts(root.get_object())
    if any("OpenSans" in f or "Open Sans" in f for f in fonts):
        print("Open Sans embedded")
        sys.exit(0)
    print("error: Open Sans not embedded in PDF", file=sys.stderr)
    for f in sorted(fonts):
        print(f"  found: {f}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
