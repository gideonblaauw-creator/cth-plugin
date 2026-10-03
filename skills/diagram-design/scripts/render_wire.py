#!/usr/bin/env python3
"""Render a validated wire spec to deterministic HTML and SVG."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from validate_spec import DEFAULT_LANES, load_spec, validate_spec_dict
from wire_text import label_metrics_for_spec, node_label_baselines

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_FONTS_HREF = "./fonts/wire"
SPLIT_THRESHOLD = 12
TARGET_VIEW_WIDTH = 1280

# CTH palette (PR #43) + status-only amber/red
TOKENS = {
    "paper": "#F7FBFD",
    "lane_tint": "#B2EEFA",
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

NODE_W_MIN = 192
NODE_LABEL_SIZE = 18
LANE_LABEL_SIZE = 14
EDGE_LABEL_SIZE = 12
LANE_LABEL_W_MIN = 72
LANE_LABEL_W_MAX = 112
LANE_PAD = 12
LANE_BAND_EXTRA = 8
NODE_PAD_X = 12
ICON_GUTTER = 28
GRID = 4
COL_GAP = 24
ROW_GAP = 20
MARGIN = 24
CHANNEL = 20
ROUTE_CLEARANCE = 12
LEGEND_ITEM_H = 22
LEGEND_CLEARANCE = 16


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

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def right_mid(self) -> tuple[int, int]:
        return self.right, self.cy

    def left_mid(self) -> tuple[int, int]:
        return self.x, self.cy

    def bottom_mid(self) -> tuple[int, int]:
        return self.cx, self.bottom

    def top_mid(self) -> tuple[int, int]:
        return self.cx, self.y

    def inflated(self, pad: int) -> "Box":
        return Box(self.x - pad, self.y - pad, self.w + 2 * pad, self.h + 2 * pad)


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


def ensure_wire_layout(spec: dict[str, Any]) -> dict[str, Any]:
    if "_wire_metrics" in spec:
        return spec["_wire_metrics"]
    node_w, node_h, lines = label_metrics_for_spec(
        spec["nodes"],
        node_w_min=NODE_W_MIN,
        pad_x=NODE_PAD_X,
        icon_gutter=ICON_GUTTER,
    )
    metrics = {"node_w": node_w, "node_h": node_h, "lines": lines}
    spec["_wire_metrics"] = metrics
    return metrics


def node_w(spec: dict[str, Any]) -> int:
    return int(ensure_wire_layout(spec)["node_w"])


def node_h(spec: dict[str, Any]) -> int:
    return int(ensure_wire_layout(spec)["node_h"])


def lane_columns(count: int, *, compact: bool = False, extra_cols: int = 0) -> int:
    if not compact:
        if count <= 3:
            return count or 1
        if count <= 6:
            return 3
        return 4
    base = 4
    if count <= 4:
        base = count or 1
    elif count <= 8:
        base = 4
    elif count <= 12:
        base = 5
    else:
        base = 6
    return min(count, base + extra_cols)


def lane_label_gutter(spec: dict[str, Any]) -> int:
    lanes = normalize_lanes(spec)
    longest = max((len(lane) for lane in lanes), default=6)
    width = snap(longest * 9 + 24)
    return int(max(LANE_LABEL_W_MIN, min(LANE_LABEL_W_MAX, width)))


def layout_lane_row(
    spec: dict[str, Any],
    nodes: list[dict[str, Any]],
    y: int,
    x_start: int,
    *,
    compact: bool = False,
    extra_cols: int = 0,
) -> list[PlacedNode]:
    if not nodes:
        return []
    nw, nh = node_w(spec), node_h(spec)
    cols = lane_columns(len(nodes), compact=compact, extra_cols=extra_cols)
    placed: list[PlacedNode] = []
    for index, node in enumerate(nodes):
        col = index % cols
        row = index // cols
        x = snap(x_start + col * (nw + COL_GAP))
        ny = snap(y + row * (nh + ROW_GAP))
        placed.append(PlacedNode(node, Box(x, ny, nw, nh)))
    return placed


def layout_lanes(
    spec: dict[str, Any],
    *,
    compact: bool = False,
    extra_cols: int = 0,
) -> tuple[list[PlacedNode], int, int, list[Box]]:
    ensure_wire_layout(spec)
    grouped = nodes_by_lane(spec)
    lanes = normalize_lanes(spec)
    gutter = lane_label_gutter(spec)
    x_start = MARGIN + gutter + LANE_PAD
    y = MARGIN + 8
    all_nodes: list[PlacedNode] = []
    lane_bands: list[Box] = []
    max_x = x_start
    max_y = y
    for lane in lanes:
        row_nodes = grouped.get(lane, [])
        if not row_nodes:
            continue
        placed = layout_lane_row(
            spec, row_nodes, y, x_start, compact=compact, extra_cols=extra_cols
        )
        all_nodes.extend(placed)
        row_top = min(p.box.y for p in placed) - LANE_BAND_EXTRA
        row_bottom = max(p.box.y + p.box.h for p in placed) + LANE_BAND_EXTRA
        row_right = max(p.box.x + p.box.w for p in placed)
        lane_bands.append(
            Box(snap(MARGIN), snap(row_top), snap(row_right + LANE_PAD - MARGIN), snap(row_bottom - row_top))
        )
        max_y = max(max_y, row_bottom)
        max_x = max(max_x, row_right)
        y = snap(row_bottom + 28)
    width = snap(max_x + MARGIN)
    height = snap(max_y + MARGIN)
    return all_nodes, width, height, lane_bands


def layout_flow(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int, list[Box]]:
    ensure_wire_layout(spec)
    nw, nh = node_w(spec), node_h(spec)
    nodes = sorted(spec["nodes"], key=lambda n: n["id"])
    x = snap(MARGIN + lane_label_gutter(spec) + LANE_PAD)
    y = MARGIN + 8
    placed: list[PlacedNode] = []
    for node in nodes:
        placed.append(PlacedNode(node, Box(x, y, nw, nh)))
        y = snap(y + nh + ROW_GAP)
    width = snap(x + nw + MARGIN)
    content_bottom = y
    height = snap(content_bottom + MARGIN)
    band = Box(MARGIN, MARGIN, width - 2 * MARGIN, content_bottom - MARGIN) if placed else []
    return placed, width, height, [band] if placed else []


def layout_before_after(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int, list[Box]]:
    ensure_wire_layout(spec)
    nw, nh = node_w(spec), node_h(spec)
    before_lane = "before"
    after_lane = "after"
    lanes = normalize_lanes(spec)
    if before_lane not in lanes:
        before_lane = lanes[0]
    if after_lane not in lanes:
        after_lane = lanes[-1] if len(lanes) > 1 else lanes[0]
    left = sorted(
        [n for n in spec["nodes"] if n["lane"] == before_lane],
        key=lambda n: n["id"],
    )
    right = sorted(
        [n for n in spec["nodes"] if n["lane"] == after_lane],
        key=lambda n: n["id"],
    )
    left_x = snap(MARGIN + 8)
    right_x = snap(left_x + nw + 80)
    header_y = MARGIN + 20
    y0 = snap(MARGIN + 44)
    rows = max(len(left), len(right))
    placed: list[PlacedNode] = []
    for row in range(rows):
        y = snap(y0 + row * (nh + ROW_GAP))
        if row < len(left):
            placed.append(PlacedNode(left[row], Box(left_x, y, nw, nh)))
        if row < len(right):
            placed.append(PlacedNode(right[row], Box(right_x, y, nw, nh)))
    width = snap(right_x + nw + MARGIN)
    content_bottom = snap(y0 + rows * (nh + ROW_GAP))
    height = snap(content_bottom + MARGIN)
    band_h = content_bottom - y0 + 8
    bands = [
        Box(left_x - 8, y0 - 8, nw + 16, band_h),
        Box(right_x - 8, y0 - 8, nw + 16, band_h),
    ]
    spec["_before_after_meta"] = {
        "header_y": header_y,
        "left_x": left_x,
        "right_x": right_x,
        "y0": y0,
    }
    return placed, width, height, bands


def layout_spec(spec: dict[str, Any]) -> tuple[list[PlacedNode], int, int, list[Box]]:
    ensure_wire_layout(spec)
    layout = spec.get("layout", "lanes")
    if layout == "flow":
        return layout_flow(spec)
    if layout == "before-after":
        return layout_before_after(spec)
    compact = len(spec.get("nodes") or []) > SPLIT_THRESHOLD
    extra_cols = 0
    placed: list[PlacedNode]
    width: int
    height: int
    bands: list[Box]
    while True:
        placed, width, height, bands = layout_lanes(spec, compact=compact, extra_cols=extra_cols)
        if not compact or width <= TARGET_VIEW_WIDTH or extra_cols >= 4:
            break
        extra_cols += 1
    return placed, width, height, bands


def status_stroke(status: str) -> str:
    return {
        "done": TOKENS["status_done"],
        "waiting": TOKENS["status_waiting"],
        "blocked": TOKENS["status_blocked"],
        "hold": TOKENS["status_hold"],
    }[status]


def status_icon_at(status: str, cx: int, cy: int) -> str:
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
    return (
        f'<rect x="{cx-6}" y="{cy-6}" width="12" height="12" rx="2" fill="none" '
        f'stroke="{color}" stroke-width="1.2" stroke-dasharray="3 2"/>'
    )


def status_icon(status: str, box: Box) -> str:
    cx = box.right - ICON_GUTTER // 2
    cy = box.y + box.h // 2
    return status_icon_at(status, cx, cy)


def node_svg(pn: PlacedNode, slug: str, spec: dict[str, Any]) -> str:
    node = pn.spec
    box = pn.box
    status = node["status"]
    stroke = status_stroke(status)
    fill = "#FFFFFF"
    dash = ' stroke-dasharray="6 4"' if status == "hold" else ""
    nid = html.escape(node["id"])
    metrics = ensure_wire_layout(spec)
    lines = metrics["lines"].get(node["id"], [node["label"]])
    baselines = node_label_baselines(
        box.y,
        box.h,
        line_count=len(lines),
        reserve_note=bool(node.get("note")),
    )
    parts = [
        f'<g id="{slug}-node-{nid}" class="wire-node" data-status="{status}">',
        f'<rect x="{box.x}" y="{box.y}" width="{box.w}" height="{box.h}" rx="6" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"{dash}/>',
    ]
    for line, baseline in zip(lines, baselines):
        parts.append(
            f'<text x="{box.x + NODE_PAD_X}" y="{baseline}" class="wire-node-label" '
            f'font-family="Geist, sans-serif" font-size="{NODE_LABEL_SIZE}" font-weight="600" '
            f'fill="{TOKENS["ink"]}">{html.escape(line)}</text>'
        )
    parts.append(status_icon(status, box))
    if node.get("note"):
        note = html.escape(node["note"])
        parts.append(
            f'<text x="{box.x + NODE_PAD_X}" y="{box.bottom - 8}" font-family="Geist Mono, monospace" '
            f'font-size="10" fill="{TOKENS["muted"]}">{note}</text>'
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


def h_seg_hits_box(y: int, x1: int, x2: int, box: Box) -> bool:
    if y < box.y or y > box.bottom:
        return False
    lo, hi = min(x1, x2), max(x1, x2)
    return lo < box.right and hi > box.x


def v_seg_hits_box(x: int, y1: int, y2: int, box: Box) -> bool:
    if x < box.x or x > box.right:
        return False
    lo, hi = min(y1, y2), max(y1, y2)
    return lo < box.bottom and hi > box.y


def path_hits_obstacles(
    sx: int, sy: int, mid_x: int, ty: int, tx: int, obstacles: Iterable[Box]
) -> bool:
    for box in obstacles:
        if h_seg_hits_box(sy, sx, mid_x, box):
            return True
        if v_seg_hits_box(mid_x, sy, ty, box):
            return True
        if h_seg_hits_box(ty, mid_x, tx, box):
            return True
    return False


def segments_hit_obstacles(
    segments: list[tuple[int, int, int, int]], obstacles: Iterable[Box]
) -> bool:
    for x1, y1, x2, y2 in segments:
        if abs(y1 - y2) <= 1:
            if any(h_seg_hits_box(y1, x1, x2, box) for box in obstacles):
                return True
        elif abs(x1 - x2) <= 1:
            if any(v_seg_hits_box(x1, y1, y2, box) for box in obstacles):
                return True
    return False


def routing_obstacles(
    obstacles: list[Box], src: Box, dst: Box
) -> list[Box]:
    return [
        b.inflated(ROUTE_CLEARANCE)
        for b in obstacles
        if b is not src and b is not dst
    ]


def candidate_mid_x_values(
    sx: int, tx: int, obstacles: list[Box], src: Box, dst: Box
) -> list[int]:
    lo = min(sx, tx) - 120
    hi = max(sx, tx) + 120
    gaps: set[int] = set()
    gaps.add(snap(dst.x - ROUTE_CLEARANCE))
    gaps.add(snap(src.right + ROUTE_CLEARANCE))
    gaps.add(snap((sx + tx) // 2))
    sorted_obs = sorted(obstacles, key=lambda b: b.x)
    for index in range(len(sorted_obs) - 1):
        left, right = sorted_obs[index], sorted_obs[index + 1]
        if right.x - left.right >= ROUTE_CLEARANCE * 2:
            gap = (left.right + right.x) // 2
            gaps.add(snap(gap))
    if sorted_obs:
        gaps.add(snap(sorted_obs[0].x - ROUTE_CLEARANCE))
        gaps.add(snap(sorted_obs[-1].right + ROUTE_CLEARANCE))
    gaps.add(snap(lo))
    gaps.add(snap(hi))
    candidates = sorted(g for g in gaps if lo <= g <= hi)
    if not candidates:
        candidates = [snap((sx + tx) // 2)]
    return candidates


def pick_mid_x(
    sx: int,
    sy: int,
    tx: int,
    ty: int,
    obstacles: list[Box],
    src: Box,
    dst: Box,
    *,
    canvas_w: int | None,
) -> int:
    obs = routing_obstacles(obstacles, src, dst)
    candidates = candidate_mid_x_values(sx, tx, obs, src, dst)
    best: tuple[int, int] | None = None
    target = (sx + tx) // 2
    for candidate in candidates:
        mid_x = clamp_x(candidate, canvas_w)
        if path_hits_obstacles(sx, sy, mid_x, ty, tx, obs):
            continue
        score = abs(mid_x - target)
        if best is None or score < best[0]:
            best = (score, mid_x)
    if best:
        return best[1]
    return clamp_x(snap(target), canvas_w)


def lane_row_bounds(placed: dict[str, PlacedNode], spec: dict[str, Any]) -> dict[str, tuple[int, int]]:
    bounds: dict[str, tuple[int, int]] = {}
    for lane in normalize_lanes(spec):
        nodes = [pn for pn in placed.values() if pn.spec["lane"] == lane]
        if not nodes:
            continue
        top = min(pn.box.y for pn in nodes)
        bottom = max(pn.box.bottom for pn in nodes)
        bounds[lane] = (top, bottom)
    return bounds


def gutter_below_lane(
    lane: str,
    lane_bounds: dict[str, tuple[int, int]],
    lanes: list[str],
) -> int | None:
    if lane not in lane_bounds:
        return None
    try:
        index = lanes.index(lane)
    except ValueError:
        return None
    if index + 1 >= len(lanes):
        return snap(lane_bounds[lane][1] + ROW_GAP)
    next_lane = lanes[index + 1]
    if next_lane not in lane_bounds:
        return None
    bottom = lane_bounds[lane][1]
    top = lane_bounds[next_lane][0]
    if top <= bottom + ROUTE_CLEARANCE:
        return None
    return snap((bottom + top) // 2)


def gutter_above_lane(
    lane: str,
    lane_bounds: dict[str, tuple[int, int]],
    lanes: list[str],
) -> int | None:
    if lane not in lane_bounds:
        return None
    try:
        index = lanes.index(lane)
    except ValueError:
        return None
    if index <= 0:
        return snap(lane_bounds[lane][0] - ROW_GAP)
    prev_lane = lanes[index - 1]
    if prev_lane not in lane_bounds:
        return None
    bottom = lane_bounds[prev_lane][1]
    top = lane_bounds[lane][0]
    if top <= bottom + ROUTE_CLEARANCE:
        return None
    return snap((bottom + top) // 2)


def path_from_segments(segments: list[tuple[int, int, int, int]]) -> str:
    if not segments:
        return ""
    x0, y0, _, _ = segments[0]
    parts = [f"M {x0} {y0}"]
    for _, _, x1, y1 in segments:
        parts.append(f"L {x1} {y1}")
    return " ".join(parts)


def route_margin_bus(
    sx: int,
    sy: int,
    tx: int,
    ty: int,
    channel_y: int,
    obs: list[Box],
    *,
    canvas_h: int | None,
) -> str | None:
    bus_x = snap(MARGIN + 4)
    channel_y = clamp_y(channel_y, canvas_h)
    segment_sets = [
        [
            (sx, sy, sx, channel_y),
            (sx, channel_y, bus_x, channel_y),
            (bus_x, channel_y, tx, channel_y),
            (tx, channel_y, tx, ty),
        ],
        [
            (sx, sy, sx, channel_y),
            (sx, channel_y, bus_x, channel_y),
            (bus_x, channel_y, bus_x, ty),
            (bus_x, ty, tx, ty),
        ],
    ]
    for segments in segment_sets:
        if not segments_hit_obstacles(segments, obs):
            return path_from_segments(segments)
    return None


def route_u_below(
    sx: int,
    sy: int,
    tx: int,
    ty: int,
    gutter_y: int,
    obs: list[Box],
    *,
    canvas_h: int | None,
) -> str | None:
    gutter_y = clamp_y(gutter_y, canvas_h)
    segments = [
        (sx, sy, sx, gutter_y),
        (sx, gutter_y, tx, gutter_y),
        (tx, gutter_y, tx, ty),
    ]
    if segments_hit_obstacles(segments, obs):
        return None
    return path_from_segments(segments)


def canvas_bottom_gutter_y(obstacles: Iterable[Box]) -> int:
    boxes = list(obstacles)
    if not boxes:
        return snap(MARGIN + 2 * ROUTE_CLEARANCE)
    max_bottom = max(b.bottom for b in boxes)
    return snap(max_bottom + 2 * ROUTE_CLEARANCE)


def lane_channel_ys(
    src: Box,
    dst: Box,
    obstacles: list[Box],
    *,
    src_lane: str,
    dst_lane: str,
    lane_bounds: dict[str, tuple[int, int]],
) -> list[int]:
    """Horizontal gutter Y values in gaps between lane rows (src lane → dst lane)."""
    _ = (src, dst, obstacles)
    channel_ys: list[int] = []
    lanes = normalize_lanes({"lanes": list(lane_bounds.keys())})
    if src_lane not in lane_bounds or dst_lane not in lane_bounds:
        return channel_ys
    try:
        index_src = lanes.index(src_lane)
        index_dst = lanes.index(dst_lane)
    except ValueError:
        return channel_ys
    lo, hi = min(index_src, index_dst), max(index_src, index_dst)
    for index in range(lo, hi):
        left, right = lanes[index], lanes[index + 1]
        if left not in lane_bounds or right not in lane_bounds:
            continue
        bottom = lane_bounds[left][1]
        top = lane_bounds[right][0]
        if top > bottom + ROUTE_CLEARANCE:
            channel_ys.append(snap((bottom + top) // 2))
    seen: set[int] = set()
    ordered: list[int] = []
    for value in channel_ys:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def route_lanes_gutter(
    src: Box,
    dst: Box,
    obstacles: list[Box],
    *,
    src_lane: str,
    dst_lane: str,
    lane_bounds: dict[str, tuple[int, int]],
    canvas_w: int | None,
    canvas_h: int | None,
) -> str | None:
    """Route via left margin bus + destination column (avoids node rows)."""
    sx, sy = src.right_mid()
    tx, ty = dst.left_mid()
    if tx <= sx + 4:
        sx, sy = src.left_mid()
        tx, ty = dst.right_mid()
    obs = routing_obstacles(obstacles, src, dst)
    channel_ys = lane_channel_ys(
        src, dst, obstacles, src_lane=src_lane, dst_lane=dst_lane, lane_bounds=lane_bounds
    )
    for channel_y in channel_ys:
        path = route_margin_bus(sx, sy, tx, ty, channel_y, obs, canvas_h=canvas_h)
        if path:
            return path
    return None


def clamp_x(value: int, canvas_w: int | None) -> int:
    if canvas_w is None:
        return value
    lo = MARGIN + CHANNEL
    hi = canvas_w - MARGIN - CHANNEL
    return max(lo, min(hi, value))


def clamp_y(value: int, canvas_h: int | None) -> int:
    if canvas_h is None:
        return value
    lo = MARGIN + CHANNEL
    hi = canvas_h - MARGIN - CHANNEL
    return max(lo, min(hi, value))


def route_orthogonal(
    src: Box,
    dst: Box,
    layout: str,
    obstacles: list[Box],
    *,
    canvas_w: int | None = None,
    canvas_h: int | None = None,
    src_lane: str = "",
    dst_lane: str = "",
    lane_bounds: dict[str, tuple[int, int]] | None = None,
) -> str:
    if layout == "flow":
        sx, sy = src.bottom_mid()
        tx, ty = dst.top_mid()
        mid_y = snap(sy + (ty - sy) // 2)
        obs = routing_obstacles(obstacles, src, dst)
        for delta in (0, -CHANNEL, CHANNEL, -2 * CHANNEL, 2 * CHANNEL):
            candidate = clamp_y(snap(mid_y + delta), canvas_h)
            if not any(
                v_seg_hits_box(sx, sy, candidate, b) or h_seg_hits_box(candidate, sx, tx, b)
                for b in obs
            ):
                mid_y = candidate
                break
        mid_y = clamp_y(mid_y, canvas_h)
        return f"M {sx} {sy} L {sx} {mid_y} L {tx} {mid_y} L {tx} {ty}"

    if layout == "before-after":
        if src.x < dst.x:
            sx, sy = src.right_mid()
            tx, ty = dst.left_mid()
        else:
            sx, sy = src.left_mid()
            tx, ty = dst.right_mid()
        mid_x = pick_mid_x(sx, sy, tx, ty, obstacles, src, dst, canvas_w=canvas_w)
        return f"M {sx} {sy} L {mid_x} {sy} L {mid_x} {ty} L {tx} {ty}"

    sx, sy = src.right_mid()
    tx, ty = dst.left_mid()
    if tx <= sx + 4:
        sx, sy = src.left_mid()
        tx, ty = dst.right_mid()

    bounds = lane_bounds or {}
    obs = routing_obstacles(obstacles, src, dst)
    if src_lane and dst_lane and src_lane == dst_lane:
        lanes = normalize_lanes({"lanes": list(bounds.keys())})
        below_y = canvas_bottom_gutter_y(obstacles)
        path = route_u_below(sx, sy, tx, ty, below_y, obs, canvas_h=canvas_h)
        if path:
            return path
        for gutter_y in (
            gutter_below_lane(src_lane, bounds, lanes),
            gutter_above_lane(src_lane, bounds, lanes),
        ):
            if gutter_y is None:
                continue
            path = route_margin_bus(sx, sy, tx, ty, gutter_y, obs, canvas_h=canvas_h)
            if path:
                return path
        mid_x = pick_mid_x(sx, sy, tx, ty, obstacles, src, dst, canvas_w=canvas_w)
        candidate = f"M {sx} {sy} L {mid_x} {sy} L {mid_x} {ty} L {tx} {ty}"
        mid_segments = [
            (sx, sy, mid_x, sy),
            (mid_x, sy, mid_x, ty),
            (mid_x, ty, tx, ty),
        ]
        if not segments_hit_obstacles(mid_segments, obs):
            return candidate
        path = route_u_below(sx, sy, tx, ty, below_y + ROW_GAP, obs, canvas_h=canvas_h)
        if path:
            return path
        return candidate

    gutter_path = route_lanes_gutter(
        src,
        dst,
        obstacles,
        src_lane=src_lane,
        dst_lane=dst_lane,
        lane_bounds=bounds,
        canvas_w=canvas_w,
        canvas_h=canvas_h,
    )
    if gutter_path:
        return gutter_path

    below_y = canvas_bottom_gutter_y(obstacles)
    path = route_u_below(sx, sy, tx, ty, below_y, obs, canvas_h=canvas_h)
    if path:
        return path

    mid_x = pick_mid_x(sx, sy, tx, ty, obstacles, src, dst, canvas_w=canvas_w)
    return f"M {sx} {sy} L {mid_x} {sy} L {mid_x} {ty} L {tx} {ty}"


def segments_from_path(path_d: str) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    points = parse_orthogonal_path(path_d)
    return list(zip(points, points[1:]))


def segment_intersects_box(
    p1: tuple[float, float],
    p2: tuple[float, float],
    box: Box,
    *,
    inset: float = 1.0,
) -> bool:
    x1, y1 = p1
    x2, y2 = p2
    bx, by, bw, bh = float(box.x), float(box.y), float(box.w), float(box.h)
    left, right = bx + inset, bx + bw - inset
    top, bottom = by + inset, by + bh - inset
    if abs(y1 - y2) < 0.01:
        y = y1
        if y < top or y > bottom:
            return False
        xa, xb = min(x1, x2), max(x1, x2)
        return xa < right and xb > left
    if abs(x1 - x2) < 0.01:
        x = x1
        if x < left or x > right:
            return False
        ya, yb = min(y1, y2), max(y1, y2)
        return ya < bottom and yb > top
    return False


def parse_orthogonal_path(path_d: str) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    tokens = path_d.replace(",", " ").split()
    index = 0
    x = y = 0.0
    while index < len(tokens):
        token = tokens[index]
        if token == "M":
            x, y = float(tokens[index + 1]), float(tokens[index + 2])
            points.append((x, y))
            index += 3
            continue
        if token == "L":
            x, y = float(tokens[index + 1]), float(tokens[index + 2])
            points.append((x, y))
            index += 3
            continue
        index += 1
    return points


def path_within_canvas(path_d: str, width: int, height: int, *, pad: float = 1.0) -> bool:
    for x, y in parse_orthogonal_path(path_d):
        if x < pad or y < pad or x > width - pad or y > height - pad:
            return False
    return True


def edge_label_metrics(label: str) -> tuple[int, int, int]:
    width = snap(max(40, len(label) * 7 + 16))
    height = 18
    return width, height, EDGE_LABEL_SIZE


def edges_layers(
    spec: dict[str, Any],
    placed: dict[str, PlacedNode],
    slug: str,
    layout: str,
    *,
    canvas_w: int,
    canvas_h: int,
) -> tuple[str, str]:
    paths: list[str] = []
    labels: list[str] = []
    obstacles = [p.box for p in placed.values()]
    bounds = lane_row_bounds(placed, spec)
    edges = sorted(spec["edges"], key=lambda e: (e["from"], e["to"], e["kind"]))
    for index, edge in enumerate(edges):
        src = placed.get(edge["from"])
        dst = placed.get(edge["to"])
        if not src or not dst:
            continue
        stroke, width, dash = edge_style(edge["kind"])
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        path = route_orthogonal(
            src.box,
            dst.box,
            layout,
            obstacles,
            canvas_w=canvas_w,
            canvas_h=canvas_h,
            src_lane=src.spec["lane"],
            dst_lane=dst.spec["lane"],
            lane_bounds=bounds,
        )
        paths.append(
            f'<path id="{slug}-edge-{index}" data-from="{html.escape(edge["from"])}" '
            f'data-to="{html.escape(edge["to"])}" d="{path}" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}"{dash_attr} marker-end="url(#wire-arrow)"/>'
        )
        if edge.get("label"):
            raw = edge["label"]
            label = html.escape(raw)
            lw, lh, lsize = edge_label_metrics(raw)
            sx, sy = src.box.right_mid()
            tx, ty = dst.box.left_mid()
            if layout == "flow":
                lx = snap((sx + tx) // 2 - lw // 2)
                ly = snap((sy + ty) // 2)
            else:
                lx = snap((sx + tx) // 2 - lw // 2)
                ly = snap((sy + ty) // 2 - 4)
            labels.append(
                f'<rect x="{lx}" y="{ly - lh + 4}" width="{lw}" height="{lh}" '
                f'rx="3" fill="{TOKENS["paper"]}" stroke="{TOKENS["rule"]}" stroke-width="0.6" '
                f'stroke-opacity="0.35"/>'
            )
            labels.append(
                f'<text x="{lx + 8}" y="{ly}" font-family="Geist Mono, monospace" '
                f'font-size="{lsize}" fill="{TOKENS["ink"]}">{label}</text>'
            )
    return "\n".join(paths), "\n".join(labels)


def lane_labels_svg(spec: dict[str, Any], placed: dict[str, PlacedNode]) -> str:
    layout = spec.get("layout", "lanes")
    lines: list[str] = []
    if layout == "before-after":
        meta = spec.get("_before_after_meta") or {}
        hy = meta.get("header_y", MARGIN + 20)
        lx = meta.get("left_x", MARGIN)
        rx = meta.get("right_x", lx + node_w(spec) + 80)
        lines.append(
            f'<text x="{lx + 12}" y="{hy}" font-family="Geist Mono, monospace" font-size="{LANE_LABEL_SIZE}" '
            f'font-weight="600" letter-spacing="0.14em" fill="{TOKENS["ink"]}">BEFORE</text>'
        )
        lines.append(
            f'<text x="{rx + 12}" y="{hy}" font-family="Geist Mono, monospace" font-size="{LANE_LABEL_SIZE}" '
            f'font-weight="600" letter-spacing="0.14em" fill="{TOKENS["ink"]}">AFTER</text>'
        )
        return "\n".join(lines)
    if layout != "lanes":
        return ""
    lanes = normalize_lanes(spec)
    for lane in lanes:
        nodes = [p for p in placed.values() if p.spec["lane"] == lane]
        if not nodes:
            continue
        y = min(p.box.y for p in nodes) + 32
        label = html.escape(lane.replace("-", " ").upper())
        lines.append(
            f'<text x="{MARGIN}" y="{y}" font-family="Geist Mono, monospace" font-size="{LANE_LABEL_SIZE}" '
            f'font-weight="600" letter-spacing="0.12em" fill="{TOKENS["muted"]}">{label}</text>'
        )
    return "\n".join(lines)


def lane_bands_svg(bands: list[Box]) -> str:
    parts: list[str] = []
    for index, band in enumerate(bands):
        parts.append(
            f'<rect class="wire-lane-band" x="{band.x}" y="{band.y}" width="{band.w}" height="{band.h}" '
            f'fill="{TOKENS["lane_tint"]}" opacity="0.55" rx="4"/>'
        )
    return "\n".join(parts)


def used_statuses(spec: dict[str, Any]) -> list[str]:
    order = ["done", "waiting", "blocked", "hold"]
    present = {n["status"] for n in spec["nodes"]}
    return [s for s in order if s in present]


def legend_svg(spec: dict[str, Any], canvas_w: int, content_bottom: int) -> tuple[str, int]:
    statuses = used_statuses(spec)
    if not statuses:
        return "", 0
    labels = {
        "done": "Done",
        "waiting": "Waiting",
        "blocked": "Blocked",
        "hold": "Hold / HITL",
    }
    legend_w = 168
    legend_h = snap(12 + len(statuses) * LEGEND_ITEM_H + 8)
    x = snap(canvas_w - legend_w - MARGIN)
    y = snap(content_bottom + LEGEND_CLEARANCE)
    parts = [
        f'<g id="wire-legend">',
        f'<rect id="wire-legend-box" x="{x}" y="{y}" width="{legend_w}" height="{legend_h}" rx="6" '
        f'fill="{TOKENS["paper"]}" stroke="{TOKENS["rule"]}" stroke-width="0.8" stroke-opacity="0.5"/>',
        f'<text x="{x + 12}" y="{y + 16}" font-family="Geist Mono, monospace" font-size="10" '
        f'font-weight="600" letter-spacing="0.1em" fill="{TOKENS["muted"]}">STATUS</text>',
    ]
    for index, status in enumerate(statuses):
        baseline = y + 28 + index * LEGEND_ITEM_H
        icon_cx = x + 24
        parts.append(f'<g class="wire-legend-row">')
        parts.append(status_icon_at(status, icon_cx, baseline))
        parts.append(
            f'<text x="{x + 48}" y="{baseline}" font-family="Geist, sans-serif" font-size="12" '
            f'fill="{TOKENS["ink"]}">{labels[status]}</text>'
        )
        parts.append("</g>")
    parts.append("</g>")
    return "\n".join(parts), legend_h


def compose_scene(
    spec: dict[str, Any],
    placed_list: list[PlacedNode],
    width: int,
    height: int,
    lane_bands: list[Box],
    subtitle: str | None = None,
    *,
    include_legend: bool = True,
    legend_spec: dict[str, Any] | None = None,
) -> tuple[int, int, str]:
    placed = {p.spec["id"]: p for p in placed_list}
    layout = spec.get("layout", "lanes")
    legend_source = legend_spec or spec
    statuses = used_statuses(legend_source) if include_legend else []
    content_bottom = height
    slug = spec["id"]
    nodes_layer = "\n".join(
        node_svg(p, slug, spec) for p in sorted(placed_list, key=lambda p: p.spec["id"])
    )
    edge_paths, edge_labels = edges_layers(
        spec, placed, slug, layout, canvas_w=width, canvas_h=height
    )
    lanes_layer = lane_labels_svg(spec, placed)
    bands_layer = lane_bands_svg(lane_bands)
    sub = html.escape(subtitle) if subtitle else ""
    sub_text = (
        f'<text x="{MARGIN}" y="{MARGIN + 14}" font-family="Geist, sans-serif" font-size="12" '
        f'font-weight="600" fill="{TOKENS["ink"]}">{sub}</text>'
        if sub
        else ""
    )
    legend = ""
    if include_legend and statuses:
        legend, legend_h = legend_svg(legend_source, width, content_bottom)
        height = snap(content_bottom + LEGEND_CLEARANCE + legend_h + MARGIN)
    body = (
        f'{sub_text}{bands_layer}{lanes_layer}{edge_paths}{nodes_layer}{edge_labels}{legend}'
    )
    return width, height, body


def build_canvas_svg(
    spec: dict[str, Any],
    placed_list: list[PlacedNode],
    width: int,
    height: int,
    lane_bands: list[Box],
    slug: str,
    title: str,
    desc: str,
    subtitle: str | None = None,
) -> str:
    width, height, body = compose_scene(spec, placed_list, width, height, lane_bands, subtitle)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="{slug}-title {slug}-desc">
  <title id="{slug}-title">{html.escape(title)}</title>
  <desc id="{slug}-desc">{html.escape(desc)}</desc>
  <defs>
    <marker id="wire-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{TOKENS["muted"]}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="{TOKENS["paper"]}"/>
  {body}
</svg>"""


def render_svg_document(spec: dict[str, Any]) -> str:
    slug = spec["id"]
    title = spec["title"]
    desc = spec.get("source") or f"Wire diagram for {title}"
    placed, w, h, bands = layout_spec(spec)
    return build_canvas_svg(spec, placed, w, h, bands, slug, title, desc)


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
      padding: 1.25rem 1.5rem;
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
      font-size: clamp(1.25rem, 1.6vw + 0.5rem, 1.65rem);
      font-weight: 400;
      margin-bottom: 0.75rem;
    }}
    .diagram svg {{ width: auto; max-width: 100%; height: auto; display: block; }}
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
