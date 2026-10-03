#!/usr/bin/env python3
"""Render a validated wire spec to deterministic HTML and SVG."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from validate_spec import DEFAULT_LANES, load_spec, validate_spec_dict

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_FONTS_HREF = "./fonts/wire"
SPLIT_THRESHOLD = 12

# CTH palette (PR #43) + status-only amber/red
TOKENS = {
    "paper": "#B2EEFA",
    "ink": "#0C498A",
    "muted": "#669348",
    "accent": "#9DC384",
    "rule": "#69B5FA",
    "link": "#69B5FA",
    "status_done": "#669348",
    "status_waiting": "#E3A21A",
    "status_blocked": "#C0392B",
    "status_hold": "#8A97A6",
}

NODE_W = 168
NODE_H = 48
LANE_LABEL_W = 120
LANE_PAD = 16
GRID = 4
COL_GAP = 24
ROW_GAP = 20
MARGIN = 32


def snap(value: float) -> int:
    return int(round(value / GRID) * GRID)


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    w: int
    h: int

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    def right_mid(self) -> tuple[int, int]:
        return self.x + self.w, self.cy

    def left_mid(self) -> tuple[int, int]:
        return self.x, self.cy

    def bottom_mid(self) -> tuple[int, int]:
        return self.cx, self.y + self.h

    def top_mid(self) -> tuple[int, int]:
        return self.cx, self.y


@dataclass
class PlacedNode:
    spec: dict[str, Any]
    box: Box


def normalize_lanes(spec: dict[str, Any]) -> list[str]:
    return list(spec.get("lanes") or DEFAULT_LANES)


def nodes_by_lane(spec: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    lanes = normalize_lanes(spec)
    grouped: dict[str, list[dict[str, Any]]] = {lane: [] for lane in lanes}
    for node in sorted(spec["nodes"], key=lambda n: n["id"]):
        grouped.setdefault(node["lane"], []).append(node)
    return grouped


def lane_columns(count: int) -> int:
    if count <= 3:
        return count or 1
    if count <= 6:
        return 3
    return 4


def layout_lane_row(
    nodes: list[dict[str, Any]], y: int, x_start: int, max_width: int
) -> list[PlacedNode]:
    if not nodes:
        return []
    cols = lane_columns(len(nodes))
    placed: list[PlacedNode] = []
    for index, node in enumerate(nodes):
        col = index % cols
        row = index // cols
        x = snap(x_start + col * (NODE_W + COL_GAP))
        ny = snap(y + row * (NODE_H + ROW_GAP))
        placed.append(PlacedNode(node, Box(x, ny, NODE_W, NODE_H)))
    return placed


def layout_lanes(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int]:
    grouped = nodes_by_lane(spec)
    lanes = normalize_lanes(spec)
    x_start = MARGIN + LANE_LABEL_W + LANE_PAD
    y = MARGIN + 48
    all_nodes: list[PlacedNode] = []
    max_x = x_start
    max_y = y
    for lane in lanes:
        row_nodes = grouped.get(lane, [])
        if not row_nodes:
            continue
        placed = layout_lane_row(row_nodes, y, x_start, 1200)
        all_nodes.extend(placed)
        if placed:
            row_bottom = max(p.box.y + p.box.h for p in placed)
            row_right = max(p.box.x + p.box.w for p in placed)
            max_y = max(max_y, row_bottom)
            max_x = max(max_x, row_right)
        y = snap(y + NODE_H + ROW_GAP + 36)
    width = snap(max_x + MARGIN)
    height = snap(max_y + MARGIN)
    return all_nodes, width, height


def layout_flow(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int]:
    nodes = sorted(spec["nodes"], key=lambda n: n["id"])
    x = snap(MARGIN + LANE_LABEL_W)
    y = MARGIN + 48
    placed: list[PlacedNode] = []
    for node in nodes:
        placed.append(PlacedNode(node, Box(x, y, NODE_W, NODE_H)))
        y = snap(y + NODE_H + ROW_GAP)
    width = snap(x + NODE_W + MARGIN)
    height = snap(y + MARGIN)
    return placed, width, height


def layout_before_after(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int]:
    before_lane = "before"
    after_lane = "after"
    lanes = normalize_lanes(spec)
    if before_lane not in lanes:
        before_lane = lanes[0]
    if after_lane not in lanes:
        after_lane = lanes[-1] if len(lanes) > 1 else lanes[0]
    left = [n for n in sorted(spec["nodes"], key=lambda n: n["id"]) if n["lane"] == before_lane]
    right = [n for n in sorted(spec["nodes"], key=lambda n: n["id"]) if n["lane"] == after_lane]
    mid = snap(MARGIN + LANE_LABEL_W + 420)
    left_x = snap(MARGIN + LANE_LABEL_W)
    right_x = mid
    y0 = MARGIN + 48
    placed: list[PlacedNode] = []
    y_left = y0
    for node in left:
        placed.append(PlacedNode(node, Box(left_x, y_left, NODE_W, NODE_H)))
        y_left = snap(y_left + NODE_H + ROW_GAP)
    y_right = y0
    for node in right:
        placed.append(PlacedNode(node, Box(right_x, y_right, NODE_W, NODE_H)))
        y_right = snap(y_right + NODE_H + ROW_GAP)
    width = snap(right_x + NODE_W + MARGIN)
    height = snap(max(y_left, y_right) + MARGIN)
    return placed, width, height


def layout_spec(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int]:
    layout = spec.get("layout", "lanes")
    if layout == "flow":
        return layout_flow(spec)
    if layout == "before-after":
        return layout_before_after(spec)
    return layout_lanes(spec)


def status_stroke(status: str) -> str:
    return {
        "done": TOKENS["status_done"],
        "waiting": TOKENS["status_waiting"],
        "blocked": TOKENS["status_blocked"],
        "hold": TOKENS["status_hold"],
    }[status]


def status_icon(status: str, box: Box) -> str:
    cx, cy = box.x + box.w - 20, box.y + 16
    color = status_stroke(status)
    if status == "done":
        return (
            f'<path d="M{cx-6} {cy} l4 4 8-8" fill="none" stroke="{color}" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if status == "waiting":
        return (
            f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{color}" stroke-width="1.2"/>'
            f'<path d="M{cx} {cy-3} v3 l2 2" fill="none" stroke="{color}" stroke-width="1.2" stroke-linecap="round"/>'
        )
    if status == "blocked":
        return f'<rect x="{cx-7}" y="{cy-2}" width="14" height="4" rx="1" fill="{color}"/>'
    # hold — cue is dashed border on node; small dash glyph
    return (
        f'<rect x="{cx-6}" y="{cy-6}" width="12" height="12" rx="2" fill="none" '
        f'stroke="{color}" stroke-width="1.2" stroke-dasharray="3 2"/>'
    )


def node_svg(pn: PlacedNode, slug: str) -> str:
    node = pn.spec
    box = pn.box
    status = node["status"]
    stroke = status_stroke(status)
    fill = "#FFFFFF"
    dash = ' stroke-dasharray="6 4"' if status == "hold" else ""
    label = html.escape(node["label"])
    nid = html.escape(node["id"])
    parts = [
        f'<g id="{slug}-node-{nid}" class="wire-node" data-status="{status}">',
        f'<rect x="{box.x}" y="{box.y}" width="{box.w}" height="{box.h}" rx="6" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"{dash}/>',
        f'<text x="{box.x + 12}" y="{box.y + 28}" font-family="var(--font-sans)" '
        f'font-size="12" font-weight="600" fill="{TOKENS["ink"]}">{label}</text>',
        status_icon(status, box),
    ]
    if node.get("note"):
        note = html.escape(node["note"])
        parts.append(
            f'<text x="{box.x + 12}" y="{box.y + 40}" font-family="var(--font-mono)" '
            f'font-size="9" fill="{TOKENS["muted"]}">{note}</text>'
        )
    parts.append("</g>")
    return "\n".join(parts)


def edge_style(kind: str) -> tuple[str, str, str | None]:
    if kind == "data":
        return TOKENS["link"], "1.2", None
    if kind == "hitl":
        return TOKENS["status_hold"], "1.2", "6 4"
    if kind == "ask":
        return TOKENS["muted"], "1", "4 3"
    return TOKENS["ink"], "1.2", None


def route_orthogonal(src: Box, dst: Box, layout: str) -> str:
    if layout == "flow":
        sx, sy = src.bottom_mid()
        tx, ty = dst.top_mid()
        mid_y = snap(sy + (ty - sy) // 2)
        return f"M {sx} {sy} L {sx} {mid_y} L {tx} {mid_y} L {tx} {ty}"
    sx, sy = src.right_mid()
    tx, ty = dst.left_mid()
    if tx <= sx:
        sx, sy = src.left_mid()
        tx, ty = dst.right_mid()
        mid_x = snap(sx - (sx - tx) // 2)
        return f"M {sx} {sy} L {mid_x} {sy} L {mid_x} {ty} L {tx} {ty}"
    mid_x = snap(sx + (tx - sx) // 2)
    return f"M {sx} {sy} L {mid_x} {sy} L {mid_x} {ty} L {tx} {ty}"


def edges_svg(
    spec: dict[str, Any], placed: dict[str, PlacedNode], slug: str, layout: str
) -> str:
    lines: list[str] = []
    edges = sorted(spec["edges"], key=lambda e: (e["from"], e["to"], e["kind"]))
    for index, edge in enumerate(edges):
        src = placed.get(edge["from"])
        dst = placed.get(edge["to"])
        if not src or not dst:
            continue
        stroke, width, dash = edge_style(edge["kind"])
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        path = route_orthogonal(src.box, dst.box, layout)
        marker = "url(#wire-arrow)"
        lines.append(
            f'<path id="{slug}-edge-{index}" d="{path}" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}"{dash_attr} marker-end="{marker}"/>'
        )
        if edge.get("label"):
            # label at path midpoint (deterministic)
            sx, sy = src.box.right_mid()
            tx, ty = dst.box.left_mid()
            lx = snap((sx + tx) // 2)
            ly = snap((sy + ty) // 2 - 8)
            label = html.escape(edge["label"])
            lines.append(
                f'<rect x="{lx - 4}" y="{ly - 10}" width="{max(32, len(edge["label"]) * 6)}" '
                f'height="16" fill="{TOKENS["paper"]}"/>'
            )
            lines.append(
                f'<text x="{lx}" y="{ly}" font-family="var(--font-mono)" font-size="8" '
                f'fill="{TOKENS["ink"]}">{label}</text>'
            )
    return "\n".join(lines)


def lane_labels_svg(spec: dict[str, Any], placed: dict[str, PlacedNode], slug: str) -> str:
    layout = spec.get("layout", "lanes")
    if layout != "lanes":
        return ""
    lanes = normalize_lanes(spec)
    lines: list[str] = []
    for lane in lanes:
        nodes = [p for p in placed.values() if p.spec["lane"] == lane]
        if not nodes:
            continue
        y = min(p.box.y for p in nodes) + 28
        label = html.escape(lane.replace("-", " ").title())
        lines.append(
            f'<text x="{MARGIN}" y="{y}" font-family="var(--font-mono)" font-size="10" '
            f'font-weight="500" letter-spacing="0.12em" fill="{TOKENS["muted"]}">{label}</text>'
        )
    return "\n".join(lines)


def build_canvas_svg(
    spec: dict[str, Any],
    placed_list: list[PlacedNode],
    width: int,
    height: int,
    slug: str,
    title: str,
    desc: str,
    subtitle: str | None = None,
) -> str:
    placed = {p.spec["id"]: p for p in placed_list}
    layout = spec.get("layout", "lanes")
    nodes_layer = "\n".join(node_svg(p, slug) for p in sorted(placed_list, key=lambda p: p.spec["id"]))
    edges_layer = edges_svg(spec, placed, slug, layout)
    lanes_layer = lane_labels_svg(spec, placed, slug)
    sub = html.escape(subtitle) if subtitle else ""
    sub_text = (
        f'<text x="{MARGIN}" y="{MARGIN + 16}" font-family="var(--font-mono)" font-size="10" '
        f'fill="{TOKENS["muted"]}">{sub}</text>'
        if sub
        else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="{slug}-title {slug}-desc">
  <title id="{slug}-title">{html.escape(title)}</title>
  <desc id="{slug}-desc">{html.escape(desc)}</desc>
  <defs>
    <marker id="wire-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{TOKENS["muted"]}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="{TOKENS["paper"]}"/>
  {sub_text}
  {lanes_layer}
  {edges_layer}
  {nodes_layer}
</svg>"""


def overview_placed(spec: dict[str, Any], y_offset: int) -> tuple[list[PlacedNode], int, int]:
    grouped = nodes_by_lane(spec)
    lanes = [lane for lane in normalize_lanes(spec) if grouped.get(lane)]
    x = snap(MARGIN + LANE_LABEL_W)
    y = snap(y_offset + MARGIN + 48)
    placed: list[PlacedNode] = []
    max_x = x + NODE_W
    for lane in lanes:
        count = len(grouped[lane])
        pseudo = {
            "id": f"overview-{lane}",
            "lane": lane,
            "label": f"{lane} ({count})",
            "status": "done",
        }
        box = Box(x, y, NODE_W + 40, NODE_H)
        placed.append(PlacedNode(pseudo, box))
        max_x = max(max_x, box.x + box.w)
        y = snap(y + NODE_H + ROW_GAP)
    width = snap(max_x + MARGIN)
    height = snap(y + MARGIN)
    return placed, width, height


def split_frames(spec: dict[str, Any]) -> list[tuple[str, list[PlacedNode], int, int, dict[str, Any]]]:
    """Overview plus one detail frame per lane that has nodes."""
    frames: list[tuple[str, list[PlacedNode], int, int, dict[str, Any]]] = []
    overview_nodes, ow, oh = overview_placed(spec, 0)
    frames.append(("Overview", overview_nodes, ow, oh, {"nodes": overview_nodes and [], "edges": []}))
    grouped = nodes_by_lane(spec)
    all_edges = spec.get("edges") or []
    for lane in normalize_lanes(spec):
        nodes = grouped.get(lane, [])
        if not nodes:
            continue
        node_ids = {n["id"] for n in nodes}
        lane_edges = [
            e
            for e in all_edges
            if e["from"] in node_ids or e["to"] in node_ids
        ]
        mini_spec = {**spec, "nodes": nodes, "edges": lane_edges, "layout": "lanes"}
        placed, w, h = layout_lanes(mini_spec)
        frames.append((f"Lane: {lane}", placed, w, h, mini_spec))
    return frames


def render_svg_document(spec: dict[str, Any]) -> str:
    slug = spec["id"]
    title = spec["title"]
    desc = spec.get("source") or f"Wire diagram for {title}"
    nodes = spec["nodes"]
    if len(nodes) > SPLIT_THRESHOLD:
        frames = split_frames(spec)
        total_w = max(w for _t, _p, w, _h, _s in frames)
        inner: list[str] = []
        y = 0
        for subtitle, placed, w, h, frame_spec in frames:
            placed_map = {p.spec["id"]: p for p in placed}
            layout = frame_spec.get("layout", "lanes")
            nodes_layer = "\n".join(
                node_svg(p, slug) for p in sorted(placed, key=lambda p: p.spec["id"])
            )
            edges_layer = edges_svg(frame_spec, placed_map, slug, layout)
            lanes_layer = lane_labels_svg(frame_spec, placed_map, slug)
            sub = html.escape(subtitle)
            body = (
                f'<rect width="{w}" height="{h}" fill="{TOKENS["paper"]}"/>'
                f'<text x="{MARGIN}" y="{MARGIN + 16}" font-family="var(--font-sans)" '
                f'font-size="11" font-weight="600" fill="{TOKENS["ink"]}">{sub}</text>'
                f"{lanes_layer}{edges_layer}{nodes_layer}"
            )
            inner.append(f'<g transform="translate(0,{y})">{body}</g>')
            y += h
        total_h = y
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}" role="img" aria-labelledby="{slug}-title {slug}-desc">
  <title id="{slug}-title">{html.escape(title)}</title>
  <desc id="{slug}-desc">{html.escape(desc)}</desc>
  <defs>
    <marker id="wire-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{TOKENS["muted"]}"/>
    </marker>
  </defs>
  {''.join(inner)}
</svg>"""
    placed, w, h = layout_spec(spec)
    return build_canvas_svg(spec, placed, w, h, slug, title, desc)


def font_face_css(fonts_href: str = DEFAULT_FONTS_HREF) -> str:
    base = fonts_href.rstrip("/")
    return f"""
@font-face {{
  font-family: 'Geist';
  src: url('{base}/geist-sans-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Geist';
  src: url('{base}/geist-sans-500.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Geist';
  src: url('{base}/geist-sans-600.woff2') format('woff2');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Geist Mono';
  src: url('{base}/geist-mono-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Geist Mono';
  src: url('{base}/geist-mono-500.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Instrument Serif';
  src: url('{base}/instrument-serif-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
"""


def render_html(spec: dict[str, Any], svg: str, fonts_href: str = DEFAULT_FONTS_HREF) -> str:
    slug = spec["id"]
    title = html.escape(spec["title"])
    lang = spec.get("lang", "en")
    html_lang = "en" if lang.startswith("en") else "es"
    eyebrow = "Wire · CleantechHUB"
    return f"""<!DOCTYPE html>
<html lang="{html_lang}" data-cth-wire="1">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper: {TOKENS["paper"]};
      --color-ink: {TOKENS["ink"]};
      --color-muted: {TOKENS["muted"]};
      --font-sans: 'Geist', system-ui, sans-serif;
      --font-serif: 'Instrument Serif', serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
    }}
    {font_face_css(fonts_href)}
    body {{
      font-family: var(--font-sans);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100vh;
      padding: 2rem;
    }}
    .eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--color-muted);
      margin-bottom: 0.5rem;
    }}
    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(1.4rem, 2vw + 0.5rem, 1.85rem);
      font-weight: 400;
      margin-bottom: 1.25rem;
    }}
    .diagram svg {{ max-width: 100%; height: auto; display: block; }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <div class="diagram" id="{slug}-wire">
      {svg}
    </div>
  </div>
</body>
</html>
"""


def render_markdown(spec: dict[str, Any]) -> str:
    lines = [
        f"# {spec['title']}",
        "",
        f"- **id:** `{spec['id']}`",
        f"- **layout:** `{spec.get('layout', 'lanes')}`",
        f"- **lang:** `{spec.get('lang', 'en')}`",
        "",
        "## Nodes",
        "",
        "| id | lane | label | status | ref | note |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for node in sorted(spec["nodes"], key=lambda n: n["id"]):
        lines.append(
            "| {id} | {lane} | {label} | {status} | {ref} | {note} |".format(
                id=node["id"],
                lane=node["lane"],
                label=node["label"].replace("|", "\\|"),
                status=node["status"],
                ref=node.get("ref", ""),
                note=(node.get("note") or "").replace("|", "\\|"),
            )
        )
    lines.extend(["", "## Edges", "", "| from | to | kind | label |", "| --- | --- | --- | --- |"])
    for edge in sorted(spec["edges"], key=lambda e: (e["from"], e["to"])):
        lines.append(
            f"| {edge['from']} | {edge['to']} | {edge['kind']} | {edge.get('label', '')} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_spec_path(path: Path, fonts_href: str = DEFAULT_FONTS_HREF) -> tuple[str, str, str]:
    spec = load_spec(path)
    errors = validate_spec_dict(spec)
    if errors:
        raise ValueError("; ".join(errors))
    svg = render_svg_document(spec)
    html_doc = render_html(spec, svg, fonts_href=fonts_href)
    md = render_markdown(spec)
    return html_doc, svg, md


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Render wire spec to stdout (SVG)")
    parser.add_argument("spec", type=Path)
    parser.add_argument("--format", choices=("svg", "html", "md"), default="svg")
    args = parser.parse_args()
    html_doc, svg, md = render_spec_path(args.spec)
    if args.format == "html":
        print(html_doc)
    elif args.format == "md":
        print(md)
    else:
        print(svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
