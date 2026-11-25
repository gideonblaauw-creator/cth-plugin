#!/usr/bin/env python3
"""Weekly token spend audit for CleantechHUB fleet governance (stdlib only)."""

from __future__ import annotations

import argparse
import csv
import heapq
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo("America/Bogota")
TOP_N_EVENTS = 15

TOKEN_KEYS = (
    "prompt-text-tokens",
    "cached-prompt-text-tokens",
    "cache-write-text-tokens",
    "completion-text-tokens",
)

REQUIRED_COLUMNS = ("Event Time", "Usage", "Product")

# North Star KPIs from build-plan §0 (target + hard enforcement where defined).
KPI = {
    "grok_share_weekly_alert_pct": 25.0,
    "grok_share_weekly_throttle_pct": 30.0,
    "grok_share_target_max_pct": 33.0,
    "cursor_share_target_min_pct": 67.0,
    "max_context_per_turn_tokens": 80_000,
    "rapid_fire_under_15s_max_pct": 20.0,
    "cua_share_max_pct": 2.0,
    "cached_prompt_baseline_pct": 92.6,
}


@dataclass
class ParseStats:
    rows_read: int = 0
    rows_parsed: int = 0
    skipped_missing_columns: int = 0
    skipped_bad_json: int = 0
    skipped_bad_timestamp: int = 0

    @property
    def rows_skipped(self) -> int:
        return (
            self.skipped_missing_columns
            + self.skipped_bad_json
            + self.skipped_bad_timestamp
        )

    def stderr_summary(self) -> str:
        return (
            f"parse: read {self.rows_read} rows, parsed {self.rows_parsed}, "
            f"skipped {self.rows_skipped} "
            f"(missing columns {self.skipped_missing_columns}, "
            f"bad JSON {self.skipped_bad_json}, "
            f"bad timestamp {self.skipped_bad_timestamp})"
        )


def parse_usage(usage_raw: str) -> dict[str, int]:
    data = json.loads(usage_raw)
    out: dict[str, int] = {}
    for key in TOKEN_KEYS:
        val = data.get(key, 0)
        out[key] = int(val) if val not in (None, "") else 0
    return out


def event_total_tokens(usage: dict[str, int]) -> int:
    return sum(usage[k] for k in TOKEN_KEYS)


def grok_model_bucket(model: str) -> str:
    low = model.lower()
    if "cua" in low:
        return "cua"
    if "automation" in low:
        return "automation"
    if "default" in low:
        return "default"
    return "other"


def parse_event_time(raw: str) -> datetime:
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    return datetime.fromisoformat(raw).astimezone(timezone.utc)


@dataclass
class GapStats:
    pairs: int = 0
    under_15s: int = 0
    under_5m: int = 0


def gap_stats_from_timestamps(timestamps: list[datetime]) -> GapStats:
    stats = GapStats()
    for i in range(1, len(timestamps)):
        gap = (timestamps[i] - timestamps[i - 1]).total_seconds()
        stats.pairs += 1
        if gap < 15:
            stats.under_15s += 1
        if gap < 300:
            stats.under_5m += 1
    return stats


@dataclass
class AuditResult:
    parse_stats: ParseStats = field(default_factory=ParseStats)
    event_count: int = 0
    window_start_utc: datetime | None = None
    window_end_utc: datetime | None = None
    total_tokens: int = 0
    product_tokens: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    daily_product_tokens: dict[str, dict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )
    grok_model_tokens: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    cached_prompt_tokens: int = 0
    prompt_plus_cached_tokens: int = 0
    hour_heatmap_tokens: list[int] = field(default_factory=lambda: [0] * 24)
    hour_heatmap_events: list[int] = field(default_factory=lambda: [0] * 24)
    rapid_fire_all_products: GapStats = field(default_factory=GapStats)
    rapid_fire_grok_only: GapStats = field(default_factory=GapStats)
    grok_turns_over_80k: int = 0
    max_single_turn_tokens: int = 0
    top_events: list[dict[str, Any]] = field(default_factory=list)
    kpi_checks: list[dict[str, Any]] = field(default_factory=list)


def try_parse_row(row: dict[str, str] | None) -> tuple[dict[str, Any] | None, str | None]:
    if row is None:
        return None, "missing_columns"
    for col in REQUIRED_COLUMNS:
        if col not in row or row[col] is None or str(row[col]).strip() == "":
            return None, "missing_columns"
    try:
        usage = parse_usage(row["Usage"])
    except (json.JSONDecodeError, TypeError, ValueError):
        return None, "bad_json"
    try:
        ts = parse_event_time(row["Event Time"].strip())
    except (ValueError, TypeError):
        return None, "bad_timestamp"
    product = row.get("Product", "").strip() or "unknown"
    model = row.get("Model", "").strip() or "unknown"
    total = event_total_tokens(usage)
    return (
        {
            "event_time_utc": ts,
            "product": product,
            "model": model,
            "usage": usage,
            "total_tokens": total,
            "billing_item_id": row.get("Billing Item ID", ""),
            "user_email": row.get("User Email", ""),
        },
        None,
    )


def stream_csv(path: Path) -> tuple[AuditResult, list[datetime], list[datetime]]:
    """Stream CSV: aggregates in memory; timelines are sorted UTC timestamps only."""
    stats = ParseStats()
    result = AuditResult(parse_stats=stats)
    timeline_all: list[datetime] = []
    timeline_grok: list[datetime] = []
    # Min-heap of (total_tokens, seq, event_dict) — seq breaks ties deterministically.
    top_heap: list[tuple[int, int, dict[str, Any]]] = []
    seq = 0

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames:
            missing_headers = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
            if missing_headers:
                print(
                    f"warning: CSV missing header columns: {', '.join(missing_headers)}",
                    file=sys.stderr,
                )
        for row in reader:
            stats.rows_read += 1
            parsed, skip = try_parse_row(row)
            if skip:
                if skip == "missing_columns":
                    stats.skipped_missing_columns += 1
                elif skip == "bad_json":
                    stats.skipped_bad_json += 1
                elif skip == "bad_timestamp":
                    stats.skipped_bad_timestamp += 1
                continue
            assert parsed is not None
            stats.rows_parsed += 1
            seq += 1
            ev = parsed
            ts: datetime = ev["event_time_utc"]
            timeline_all.append(ts)
            if ev["product"] == "grok-bot":
                timeline_grok.append(ts)

            result.event_count += 1
            tok = ev["total_tokens"]
            result.total_tokens += tok
            product = ev["product"]
            result.product_tokens[product] += tok
            day_key = ts.date().isoformat()
            result.daily_product_tokens[day_key][product] += tok

            usage = ev["usage"]
            result.cached_prompt_tokens += usage["cached-prompt-text-tokens"]
            result.prompt_plus_cached_tokens += (
                usage["prompt-text-tokens"] + usage["cached-prompt-text-tokens"]
            )

            if product == "grok-bot":
                bucket = grok_model_bucket(ev["model"])
                result.grok_model_tokens[bucket] += tok
                if tok > KPI["max_context_per_turn_tokens"]:
                    result.grok_turns_over_80k += 1
            result.max_single_turn_tokens = max(result.max_single_turn_tokens, tok)

            hour = ts.astimezone(BOGOTA).hour
            result.hour_heatmap_tokens[hour] += tok
            result.hour_heatmap_events[hour] += 1

            if result.window_start_utc is None or ts < result.window_start_utc:
                result.window_start_utc = ts
            if result.window_end_utc is None or ts > result.window_end_utc:
                result.window_end_utc = ts

            heapq.heappush(top_heap, (tok, seq, ev))
            if len(top_heap) > TOP_N_EVENTS:
                heapq.heappop(top_heap)

    timeline_all.sort()
    timeline_grok.sort()
    result.rapid_fire_all_products = gap_stats_from_timestamps(timeline_all)
    result.rapid_fire_grok_only = gap_stats_from_timestamps(timeline_grok)

    ranked = sorted(top_heap, key=lambda x: (-x[0], x[1]))
    for tok, _, ev in ranked:
        result.top_events.append(
            {
                "event_time_utc": ev["event_time_utc"].isoformat(),
                "product": ev["product"],
                "model": ev["model"],
                "total_tokens": tok,
                "cached_prompt_tokens": ev["usage"]["cached-prompt-text-tokens"],
                "prompt_tokens": ev["usage"]["prompt-text-tokens"],
                "billing_item_id": ev["billing_item_id"],
            }
        )

    result.kpi_checks = evaluate_kpis(result)
    return result, timeline_all, timeline_grok


def pct(part: float, whole: float) -> float:
    if whole <= 0:
        return 0.0
    return 100.0 * part / whole


def gap_section_json(label: str, stats: GapStats) -> dict[str, Any]:
    return {
        "label": label,
        "pairs": stats.pairs,
        "under_15s": stats.under_15s,
        "under_15s_share_pct": round(pct(stats.under_15s, stats.pairs), 4),
        "under_5m": stats.under_5m,
        "under_5m_share_pct": round(pct(stats.under_5m, stats.pairs), 4),
    }


def evaluate_kpis(result: AuditResult) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    total = result.total_tokens
    grok = result.product_tokens.get("grok-bot", 0)
    cursor = result.product_tokens.get("cursor", 0)
    grok_share = pct(grok, total)
    cursor_share = pct(cursor, total)

    def add(
        name: str,
        observed: float,
        threshold: float,
        comparator: str,
        unit: str = "%",
        note: str = "",
    ) -> None:
        if comparator == "lte":
            ok = observed <= threshold
        elif comparator == "gte":
            ok = observed >= threshold
        else:
            ok = observed < threshold
        checks.append(
            {
                "kpi": name,
                "observed": round(observed, 4),
                "threshold": threshold,
                "comparator": comparator,
                "unit": unit,
                "status": "pass" if ok else "fail",
                "note": note,
            }
        )

    add(
        "grok_share_of_spend",
        grok_share,
        KPI["grok_share_target_max_pct"],
        "lte",
        note="Target ≤33%; alert 25%, throttle 30% (enforcement OFF by default)",
    )
    add(
        "cursor_share_of_spend",
        cursor_share,
        KPI["cursor_share_target_min_pct"],
        "gte",
        note="Target ≥67% of total spend",
    )

    cached_share_total = pct(result.cached_prompt_tokens, total)
    checks.append(
        {
            "kpi": "cached_prompt_share_of_total_tokens",
            "observed": round(cached_share_total, 4),
            "threshold": KPI["cached_prompt_baseline_pct"],
            "comparator": "baseline_ref",
            "unit": "%",
            "status": "info",
            "note": "Baseline reference ~92.6% on full Nov window; not a hard cap",
        }
    )

    grok_rf = result.rapid_fire_grok_only
    if grok_rf.pairs:
        rf15_grok = pct(grok_rf.under_15s, grok_rf.pairs)
        add(
            "rapid_fire_grok_only_under_15s_share",
            rf15_grok,
            KPI["rapid_fire_under_15s_max_pct"],
            "lte",
            note="Plan §0: consecutive grok-bot call pairs with gap <15s (baseline ~82.1%)",
        )
        rf5m_grok = pct(grok_rf.under_5m, grok_rf.pairs)
        checks.append(
            {
                "kpi": "rapid_fire_grok_only_under_5m_share",
                "observed": round(rf5m_grok, 4),
                "threshold": None,
                "comparator": "info",
                "unit": "%",
                "status": "info",
                "note": "Consecutive grok-bot pairs with gap <5 minutes",
            }
        )

    all_rf = result.rapid_fire_all_products
    if all_rf.pairs:
        checks.append(
            {
                "kpi": "rapid_fire_all_products_under_15s_share",
                "observed": round(pct(all_rf.under_15s, all_rf.pairs), 4),
                "threshold": None,
                "comparator": "info",
                "unit": "%",
                "status": "info",
                "note": "All products in export order (informational, not plan §0 KPI)",
            }
        )
        checks.append(
            {
                "kpi": "rapid_fire_all_products_under_5m_share",
                "observed": round(pct(all_rf.under_5m, all_rf.pairs), 4),
                "threshold": None,
                "comparator": "info",
                "unit": "%",
                "status": "info",
                "note": "All products; gap <5 minutes (informational)",
            }
        )

    cua_tokens = result.grok_model_tokens.get("cua", 0)
    add(
        "grok_cua_share_of_total",
        pct(cua_tokens, total),
        KPI["cua_share_max_pct"],
        "lte",
    )

    checks.append(
        {
            "kpi": "grok_turns_over_80k",
            "observed": result.grok_turns_over_80k,
            "threshold": KPI["max_context_per_turn_tokens"],
            "comparator": "count_lte_zero_preferred",
            "unit": "events",
            "status": "fail" if result.grok_turns_over_80k else "pass",
            "note": "Grok events with total tokens >80k",
        }
    )
    return checks


def daily_share_table(result: AuditResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for day in sorted(result.daily_product_tokens):
        by_prod = result.daily_product_tokens[day]
        day_total = sum(by_prod.values())
        grok = by_prod.get("grok-bot", 0)
        cursor = by_prod.get("cursor", 0)
        rows.append(
            {
                "date_utc": day,
                "total_tokens": day_total,
                "grok_tokens": grok,
                "cursor_tokens": cursor,
                "grok_share_pct": round(pct(grok, day_total), 2),
                "cursor_share_pct": round(pct(cursor, day_total), 2),
            }
        )
    return rows


def render_heatmap_ascii(tokens: list[int]) -> str:
    mx = max(tokens) if tokens else 1
    lines = ["```", "Hour (America/Bogota) | bar (token share)"]
    for hour, val in enumerate(tokens):
        width = int(40 * val / mx) if mx else 0
        lines.append(f"{hour:02d}:00  {'█' * width}  {val:,}")
    lines.append("```")
    return "\n".join(lines)


def render_rapid_fire_md(title: str, stats: GapStats) -> list[str]:
    if stats.pairs == 0:
        return [f"### {title}", "", "_No consecutive pairs in window._", ""]
    return [
        f"### {title}",
        "",
        f"- Consecutive pairs: {stats.pairs:,}",
        f"- Gap &lt;15s: {stats.under_15s:,} ({pct(stats.under_15s, stats.pairs):.2f}%)",
        f"- Gap &lt;5m: {stats.under_5m:,} ({pct(stats.under_5m, stats.pairs):.2f}%)",
        "",
    ]


def window_days(result: AuditResult) -> float:
    if not result.window_start_utc or not result.window_end_utc:
        return 0.0
    delta = result.window_end_utc - result.window_start_utc
    return delta.total_seconds() / 86400.0


def to_json_report(result: AuditResult, source_csv: str) -> dict[str, Any]:
    total = result.total_tokens
    grok = result.product_tokens.get("grok-bot", 0)
    cursor = result.product_tokens.get("cursor", 0)
    grok_total = grok or 1
    return {
        "source_csv": source_csv,
        "parse_stats": {
            "rows_read": result.parse_stats.rows_read,
            "rows_parsed": result.parse_stats.rows_parsed,
            "rows_skipped": result.parse_stats.rows_skipped,
            "skipped_missing_columns": result.parse_stats.skipped_missing_columns,
            "skipped_bad_json": result.parse_stats.skipped_bad_json,
            "skipped_bad_timestamp": result.parse_stats.skipped_bad_timestamp,
        },
        "window": {
            "start_utc": result.window_start_utc.isoformat() if result.window_start_utc else None,
            "end_utc": result.window_end_utc.isoformat() if result.window_end_utc else None,
            "duration_days": round(window_days(result), 4),
            "event_count": result.event_count,
        },
        "totals": {
            "all_tokens": total,
            "grok_bot_tokens": grok,
            "cursor_tokens": cursor,
            "grok_share_pct": round(pct(grok, total), 4),
            "cursor_share_pct": round(pct(cursor, total), 4),
        },
        "daily_shares": daily_share_table(result),
        "grok_model_shares_pct_of_grok": {
            k: round(pct(v, grok_total), 4) for k, v in sorted(result.grok_model_tokens.items())
        },
        "grok_model_tokens": dict(result.grok_model_tokens),
        "cached_prompt": {
            "cached_prompt_tokens": result.cached_prompt_tokens,
            "share_of_total_tokens_pct": round(pct(result.cached_prompt_tokens, total), 4),
            "share_of_prompt_plus_cached_pct": round(
                pct(result.cached_prompt_tokens, result.prompt_plus_cached_tokens), 4
            ),
        },
        "heatmap_america_bogota": {
            "tokens_by_hour": result.hour_heatmap_tokens,
            "events_by_hour": result.hour_heatmap_events,
        },
        "rapid_fire": {
            "grok_only_plan_kpi": gap_section_json(
                "Consecutive grok-bot calls (plan §0 KPI)", result.rapid_fire_grok_only
            ),
            "all_products_informational": gap_section_json(
                "All products in CSV time order (informational)", result.rapid_fire_all_products
            ),
        },
        "max_single_turn_tokens": result.max_single_turn_tokens,
        "grok_turns_over_80k": result.grok_turns_over_80k,
        "top_events": result.top_events,
        "kpi_checks": result.kpi_checks,
        "plan_figures_note": (
            "Master plan §0 cites ~6.13B tokens, 65.7% Grok monthly, 76.9% Grok weekly "
            "from the full Nov 1–25 export. This run only reflects the ingested CSV slice."
        ),
    }


def render_markdown(result: AuditResult, source_csv: str, baseline_note: str) -> str:
    total = result.total_tokens
    grok = result.product_tokens.get("grok-bot", 0)
    cursor = result.product_tokens.get("cursor", 0)
    ps = result.parse_stats
    lines: list[str] = [
        "# Weekly token audit report",
        "",
        f"- **Source CSV:** `{source_csv}`",
        f"- **Events parsed:** {result.event_count:,} "
        f"(skipped {ps.rows_skipped:,} of {ps.rows_read:,} rows)",
        f"- **Window (UTC):** {result.window_start_utc} → {result.window_end_utc}",
        f"- **Duration:** {window_days(result):.2f} days",
        "",
        "## Baseline statement",
        "",
        baseline_note,
        "",
        "## Product share (whole window)",
        "",
        "| Product | Tokens | Share |",
        "| :--- | ---: | ---: |",
        f"| grok-bot | {grok:,} | {pct(grok, total):.2f}% |",
        f"| cursor | {cursor:,} | {pct(cursor, total):.2f}% |",
        f"| **Total** | **{total:,}** | 100% |",
        "",
        "## Daily Grok vs Cursor share (UTC date)",
        "",
        "| Date | Total tokens | Grok % | Cursor % |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for row in daily_share_table(result):
        lines.append(
            f"| {row['date_utc']} | {row['total_tokens']:,} | "
            f"{row['grok_share_pct']:.2f}% | {row['cursor_share_pct']:.2f}% |"
        )

    lines.extend(
        [
            "",
            "## Grok model mix (share of Grok tokens)",
            "",
            "| Bucket | Tokens | Share of Grok |",
            "| :--- | ---: | ---: |",
        ]
    )
    for bucket, tok in sorted(result.grok_model_tokens.items(), key=lambda x: -x[1]):
        lines.append(f"| {bucket} | {tok:,} | {pct(tok, grok or 1):.2f}% |")

    cached_total_pct = pct(result.cached_prompt_tokens, total)
    cached_pc_pct = pct(result.cached_prompt_tokens, result.prompt_plus_cached_tokens)
    lines.extend(
        [
            "",
            "## Cached prompt",
            "",
            f"- Cached prompt tokens: **{result.cached_prompt_tokens:,}**",
            f"- Share of all tokens: **{cached_total_pct:.2f}%**",
            f"- Share of prompt + cached: **{cached_pc_pct:.2f}%**",
            "",
            "## Hour-of-day heatmap (America/Bogota)",
            "",
            render_heatmap_ascii(result.hour_heatmap_tokens),
            "",
            "## Rapid-fire intervals",
            "",
            "Plan §0 KPI uses **grok-bot-only** consecutive call pairs. The all-product "
            "metric is included for context but is not the governance threshold.",
            "",
        ]
    )
    lines.extend(
        render_rapid_fire_md(
            "Grok-bot only (plan §0 KPI — baseline ~82.1% under 15s)",
            result.rapid_fire_grok_only,
        )
    )
    lines.extend(
        render_rapid_fire_md(
            "All products in CSV time order (informational)",
            result.rapid_fire_all_products,
        )
    )

    lines.extend(
        [
            "## Top events by tokens",
            "",
            "| UTC time | Product | Model | Total tokens |",
            "| :--- | :--- | :--- | ---: |",
        ]
    )
    for ev in result.top_events[:10]:
        lines.append(
            f"| {ev['event_time_utc']} | {ev['product']} | {ev['model']} | {ev['total_tokens']:,} |"
        )

    lines.extend(
        [
            "",
            "## KPI comparison (plan §0)",
            "",
            "| KPI | Observed | Threshold | Status |",
            "| :--- | ---: | ---: | :--- |",
        ]
    )
    for chk in result.kpi_checks:
        thr = chk.get("threshold")
        thr_s = "—" if thr is None else f"{thr}{chk.get('unit', '')}"
        obs = chk["observed"]
        obs_s = f"{obs}{chk.get('unit', '')}" if chk.get("unit") != "events" else str(int(obs))
        if chk.get("unit") == "%" and isinstance(obs, (int, float)):
            obs_s = f"{obs:.2f}%"
        lines.append(f"| {chk['kpi']} | {obs_s} | {thr_s} | {chk['status']} |")

    lines.extend(
        [
            "",
            "## Plan vs this CSV",
            "",
            "The fleet redesign plan (25 Nov 2026) cites **6.13B tokens**, **65.7% Grok (monthly)**, "
            "**76.9% Grok (weekly active)**, and **92.6% cached reads** from the **full Nov 1–25** usage "
            "corpus. The staged `usage-events.csv` slice is **~5.7 days** and **~1.54B tokens**; it "
            "**cannot reproduce** the plan’s monthly/weekly headline percentages without the missing rows.",
            "",
            "_Enforcement actions (tighten max_context, PROTOCOLS.md PR, circuit breaker, auto-pause) "
            "are disabled unless `--enforce` and `ENFORCE_APPROVED` are set (Gideon GO required)._",
        ]
    )
    return "\n".join(lines) + "\n"


def run_enforcement(result: AuditResult, enforce: bool) -> list[str]:
    logs: list[str] = []
    if not enforce:
        logs.append("enforcement disabled (needs Gideon GO)")
        return logs

    if os.environ.get("ENFORCE_APPROVED") != "1":
        logs.append("enforcement disabled (needs Gideon GO)")
        return logs

    total = result.total_tokens
    grok_share = pct(result.product_tokens.get("grok-bot", 0), total)
    grok_rf = result.rapid_fire_grok_only
    rf15 = pct(grok_rf.under_15s, grok_rf.pairs) if grok_rf.pairs else 0.0

    if grok_share > KPI["grok_share_target_max_pct"]:
        logs.append(
            "[WOULD] Tighten max_context_tokens on top offending desks "
            f"(Grok share {grok_share:.2f}% > {KPI['grok_share_target_max_pct']}%)"
        )
        logs.append("[WOULD] Open PR to PROTOCOLS.md with mandatory Cursor dispatch rules")

    if rf15 > KPI["rapid_fire_under_15s_max_pct"]:
        logs.append(
            f"[WOULD] Flag rapid-fire desks (grok-only under-15s share {rf15:.2f}% > "
            f"{KPI['rapid_fire_under_15s_max_pct']}%)"
        )

    if grok_share >= KPI["grok_share_weekly_alert_pct"]:
        logs.append(
            "[WOULD] Circuit-breaker: pause non-critical tier-2 schedules "
            f"(Grok share {grok_share:.2f}% ≥ alert {KPI['grok_share_weekly_alert_pct']}%)"
        )
        logs.append("[WOULD] Auto-pause tier-2 until weekly reset")

    if not any(line.startswith("[WOULD]") for line in logs):
        logs.append("enforce: no remediation triggers fired; no actions queued")
    return logs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Weekly token audit (stdlib only)")
    parser.add_argument("csv", type=Path, help="Cursor usage export CSV")
    parser.add_argument(
        "--markdown",
        type=Path,
        help="Write human-readable markdown report",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Write machine-readable JSON report",
    )
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Run remediation hooks (requires ENFORCE_APPROVED=1)",
    )
    parser.add_argument(
        "--baseline-note",
        default="",
        help="Optional baseline reproduction note for markdown header",
    )
    args = parser.parse_args(argv)

    if not args.csv.is_file():
        print(f"error: CSV not found: {args.csv}", file=sys.stderr)
        return 1

    result, _tl, _gl = stream_csv(args.csv)
    print(result.parse_stats.stderr_summary(), file=sys.stderr)
    source = str(args.csv)

    baseline = args.baseline_note or (
        "This report reflects the ingested CSV only. Compare against the Nov 19–25 slice "
        "baseline (~56.2% Grok / ~43.8% Cursor, ~92.6% cached, ~5.7 days, ~1.54B tokens) "
        "when that file is used as input."
    )

    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(render_markdown(result, source, baseline), encoding="utf-8")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = to_json_report(result, source)
        payload["enforcement_log"] = run_enforcement(result, args.enforce)
        args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    for line in run_enforcement(result, args.enforce):
        print(line)

    if args.markdown or args.json:
        print(
            f"audited {result.event_count} events, {result.total_tokens:,} tokens",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())