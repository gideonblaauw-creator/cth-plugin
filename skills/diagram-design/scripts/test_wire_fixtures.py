#!/usr/bin/env python3
"""Geometry checks for wire fixture SVG output."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_wire import (  # noqa: E402
    ICON_GUTTER,
    NODE_LABEL_SIZE,
    NODE_PAD_X,
    path_within_canvas,
    render_spec_path,
)
from wire_text import NODE_LABEL_LINE_HEIGHT, text_width  # noqa: E402

FIXTURES = SCRIPT_DIR.parent / "fixtures" / "wire"
LEGEND_CLEARANCE = 16
SVG_NS = {"svg": "http://www.w3.org/2000/svg"}
SPLIT_FIXTURE = FIXTURES / "split-cross-lane-synthetic.yaml"


def _float(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    return float(value)


def parse_rect(element: ET.Element) -> tuple[float, float, float, float]:
    return (
        _float(element.get("x")),
        _float(element.get("y")),
        _float(element.get("width")),
        _float(element.get("height")),
    )


def verify_svg(svg_source: str) -> list[str]:
    errors: list[str] = []
    root = ET.fromstring(svg_source)
    legend_rect = None
    for el in root.iter():
        if el.get("id") == "wire-legend-box":
            legend_rect = el
            break
    legend_box: tuple[float, float, float, float] | None = None
    if legend_rect is not None:
        legend_box = parse_rect(legend_rect)

    band_bottoms: list[float] = []
    for band in root.iter():
        if band.tag.endswith("rect") and "wire-lane-band" in (band.get("class") or ""):
            _x, y, _w, h = parse_rect(band)
            band_bottoms.append(y + h)

    for group in root.iter():
        if not group.tag.endswith("g"):
            continue
        if "wire-node" not in (group.get("class") or ""):
            continue
        rect_el = None
        for child in group:
            if child.tag.endswith("rect"):
                rect_el = child
                break
        if rect_el is None:
            continue
        rx, ry, rw, rh = parse_rect(rect_el)
        inner_right = rx + rw - ICON_GUTTER
        for text_el in group.iter():
            if not text_el.tag.endswith("text"):
                continue
            classes = text_el.get("class") or ""
            if "wire-node-label" not in classes:
                continue
            tx = _float(text_el.get("x"))
            ty = _float(text_el.get("y"))
            label = "".join(text_el.itertext())
            width = text_width(label, NODE_LABEL_SIZE)
            if tx < rx + NODE_PAD_X - 1:
                errors.append(f"label {label!r} starts before node padding")
            if tx + width > inner_right + 1:
                errors.append(
                    f"label {label!r} exceeds node inner width (text {tx + width:.1f} > {inner_right:.1f})"
                )
            text_top = ty - NODE_LABEL_SIZE * 0.85
            text_bottom = ty + NODE_LABEL_SIZE * 0.2
            if text_top < ry + 4:
                errors.append(f"label {label!r} extends above node top")
            if text_bottom > ry + rh - 4:
                errors.append(f"label {label!r} extends below node bottom")

    if legend_box and band_bottoms:
        _lx, ly, _lw, _lh = legend_box
        max_band = max(band_bottoms)
        if ly < max_band + LEGEND_CLEARANCE - 1:
            errors.append(
                f"legend overlaps lane bands (legend y={ly}, band bottom={max_band}, need {LEGEND_CLEARANCE}px)"
            )

    if legend_box:
        _lx, ly, lw, lh = legend_box
        for group in root.iter():
            if group.get("id") != "wire-legend":
                continue
            for row in group:
                if not row.tag.endswith("g"):
                    continue
                if "wire-legend-row" not in (row.get("class") or ""):
                    continue
                text_el = None
                icon_cy = None
                for child in row:
                    tag = child.tag.rsplit("}", 1)[-1]
                    if tag == "text":
                        text_el = child
                    if child.get("cy") is not None:
                        icon_cy = _float(child.get("cy"))
                if text_el is None or icon_cy is None:
                    continue
                ty = _float(text_el.get("y"))
                if abs(icon_cy - ty) > 2:
                    errors.append("legend icon cy misaligned with text baseline")

    for group in root.iter():
        if not group.tag.endswith("g"):
            continue
        if "wire-node" not in (group.get("class") or ""):
            continue
        label_ys: list[float] = []
        for text_el in group.iter():
            if not text_el.tag.endswith("text"):
                continue
            if "wire-node-label" not in (text_el.get("class") or ""):
                continue
            label_ys.append(_float(text_el.get("y")))
        if len(label_ys) == 2:
            label_ys.sort()
            gap = label_ys[1] - label_ys[0]
            if abs(gap - NODE_LABEL_LINE_HEIGHT) > 0.01:
                errors.append(
                    f"2-line label gap {gap}px != {NODE_LABEL_LINE_HEIGHT}px on {group.get('id')}"
                )

    width = _float(root.get("width"))
    height = _float(root.get("height"))
    if width <= 0 or height <= 0:
        view = root.get("viewBox", "0 0 0 0").split()
        if len(view) == 4:
            width, height = _float(view[2]), _float(view[3])
    edge_count = 0
    for el in root.iter():
        if not el.tag.endswith("path"):
            continue
        if el.get("marker-end") != "url(#wire-arrow)":
            continue
        edge_count += 1
        path_d = el.get("d") or ""
        if width and height and not path_within_canvas(path_d, int(width), int(height)):
            errors.append(f"edge {el.get('id')} exits canvas ({width}x{height})")

    return errors


def verify_split_cross_lane(spec_path: Path, svg_source: str) -> list[str]:
    errors: list[str] = []
    if spec_path.name != SPLIT_FIXTURE.name:
        return errors
    import yaml

    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    expected_edges = len(spec.get("edges") or [])
    root = ET.fromstring(svg_source)
    rendered = sum(
        1
        for el in root.iter()
        if el.tag.endswith("path") and el.get("marker-end") == "url(#wire-arrow)"
    )
    if rendered != expected_edges:
        errors.append(f"expected {expected_edges} edge paths, got {rendered}")
    if "overview-" in svg_source:
        errors.append("overview strip nodes must not appear in split layout")
    if "Lane:" in svg_source:
        errors.append("duplicate lane subtitle (Lane: ...) must not appear")
    return errors


def main() -> int:
    specs = sorted(FIXTURES.glob("*.yaml"))
    failed = False
    for spec_path in specs:
        _html, svg, _md = render_spec_path(spec_path)
        errors = verify_svg(svg)
        errors.extend(verify_split_cross_lane(spec_path, svg))
        if errors:
            failed = True
            print(f"FAIL {spec_path.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {spec_path.name} (labels in nodes, legend clear)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
