#!/usr/bin/env python3
"""Deterministic Geist sans (600) text metrics for wire diagrams at 16px."""

from __future__ import annotations

# Per-character advance widths (px) at 16px / weight 600 — stable wire table.
_CHAR_ADVANCE_16: dict[str, float] = {}
for _ch in "il1!|:;.":
    _CHAR_ADVANCE_16[_ch] = 6.4
for _ch in "mwMWQ@%":
    _CHAR_ADVANCE_16[_ch] = 11.2
for _ch in "ABCDEFGHIJKLNOPRSTUVXYZ":
    _CHAR_ADVANCE_16[_ch] = 10.4
for _ch in "abcdefghknopqrstuvxyz":
    _CHAR_ADVANCE_16[_ch] = 9.2
for _ch in "0123456789":
    _CHAR_ADVANCE_16[_ch] = 9.6
_CHAR_ADVANCE_16[" "] = 4.8
_CHAR_ADVANCE_16["-"] = 6.4
_CHAR_ADVANCE_16["/"] = 6.4
_CHAR_ADVANCE_16["_"] = 8.0
_DEFAULT_ADVANCE_16 = 9.6


def advance_px(character: str, font_size: float = 16.0) -> float:
    if not character:
        return 0.0
    base = _CHAR_ADVANCE_16.get(character, _DEFAULT_ADVANCE_16)
    return base * (font_size / 16.0)


def text_width(label: str, font_size: float = 16.0) -> float:
    return sum(advance_px(ch, font_size) for ch in label)


def wrap_label(label: str, max_inner_width: float, *, max_lines: int = 2) -> list[str]:
    words = label.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if text_width(trial) <= max_inner_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if len(lines) <= max_lines:
        return lines
    merged = " ".join(lines[max_lines - 1 :])
    lines = lines[: max_lines - 1] + [merged]
    while text_width(lines[-1]) > max_inner_width and len(lines[-1]) > 1:
        lines[-1] = lines[-1][:-1]
    if text_width(lines[-1]) > max_inner_width:
        lines[-1] = lines[-1][: max(1, len(lines[-1]) - 2)] + "…"
    return lines


def label_metrics_for_spec(
    nodes: list[dict],
    *,
    node_w_min: int,
    pad_x: int,
    icon_gutter: int,
) -> tuple[int, int, dict[str, list[str]]]:
    """Return (node_w, node_h, label_lines_by_node_id)."""
    inner_at_min = float(node_w_min - pad_x - icon_gutter - 8)
    max_lines_needed = 1
    max_line_width = 0.0
    provisional: dict[str, list[str]] = {}
    for node in nodes:
        label = node["label"]
        single = text_width(label)
        if single <= inner_at_min:
            lines = [label]
        else:
            lines = wrap_label(label, inner_at_min)
        max_lines_needed = max(max_lines_needed, len(lines))
        provisional[node["id"]] = lines
        for line in lines:
            max_line_width = max(max_line_width, text_width(line))
    node_w = int(max(node_w_min, max_line_width + pad_x + icon_gutter + 8))
    node_w = int(round(node_w / 4) * 4)
    inner_final = float(node_w - pad_x - icon_gutter - 8)
    final_lines: dict[str, list[str]] = {}
    max_lines_needed = 1
    for node in nodes:
        label = node["label"]
        if text_width(label) <= inner_final:
            lines = [label]
        else:
            lines = wrap_label(label, inner_final)
        final_lines[node["id"]] = lines
        max_lines_needed = max(max_lines_needed, len(lines))
    has_note = any(node.get("note") for node in nodes)
    line_block = 36 if max_lines_needed == 1 else 52
    node_h = line_block + (14 if has_note else 0)
    node_h = int(round(node_h / 4) * 4)
    return node_w, node_h, final_lines
