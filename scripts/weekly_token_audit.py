#!/usr/bin/env python3
"""Weekly token spend audit for CleantechHUB fleet governance (stdlib only)."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo("America/Bogota")

TOKEN_KEYS = (
    "prompt-text-tokens",
    "cached-prompt-text-tokens",
    "cache-write-text-tokens",
    "completion-text-tokens",
)

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
class ParsedEvent:
    event_time_utc: datetime
    product: str
    model: str
    usage: dict[str, int]
    total_tokens: int
    billing_item_id: str = ""
    user_email: str = ""

    @property
    def bogota(self) -> datetime:
        return self.event_time_utc.astimezone(BOGOTA)


@dataclass
class AuditResult:
    events: list[ParsedEvent] = field(default_factory=list)
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
    gaps_under_15s: int = 0
    gaps_under_5m: int = 0
    gap_pairs: int = 0
    grok_turns_over_80k: int = 0
    max_single_turn_tokens: int = 0
    top_events: list[dict[str, Any]] = field(default_factory=list)
    kpi_checks: list[dict[str, Any]] = field(default_factory=list)


def load_csv(path: Path) -> list[ParsedEvent]:
    events: list[ParsedEvent] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            usage = parse_usage(row["Usage"])
            total = event_total_tokens(usage)
            ts = parse_event_time(row["Event Time"])
            events.append(
                ParsedEvent(
                    event_time_utc=ts,
                    product=row.get("Product", "").strip() or "unknown",
                    model=row.get("Model", "").strip() or "unknown",
                    usage=usage,
                    total_tokens=total,
                    billing_item_id=row.get("Billing Item ID", ""),
                    user_email=row.get("User Email", ""),
                )
            )
    events.sort(key=lambda e: e.event_time_utc)
    return events


def compute_audit(events: list[ParsedEvent]) -> AuditResult:
    result = AuditResult(events=events)
    if not events:
        return result

    result.window_start_utc = events[0].event_time_utc
    result.window_end_utc = events[-1].event_time_utc

    for ev in events:
        result.total_tokens += ev.total_tokens
        result.product_tokens[ev.product] += ev.total_tokens
        day_key = ev.event_time_utc.date().isoformat()
        result.daily_product_tokens[day_key][ev.product] += ev.total_tokens

        cached = ev.usage["cached-prompt-text-tokens"]
        prompt = ev.usage["prompt-text-tokens"]
        result.cached_prompt_tokens += cached
        result.prompt_plus_cached_tokens += prompt + cached

        if ev.product == "grok-bot":
            bucket = grok_model_bucket(ev.model)
            result.grok_model_tokens[bucket] += ev.total_tokens
            if ev.total_tokens > KPI["max_context_per_turn_tokens"]:
                result.grok_turns_over_80k += 1
            result.max_single_turn_tokens = max(result.max_single_turn_tokens, ev.total_tokens)

        hour = ev.bogota.hour
        result.hour_heatmap_tokens[hour] += ev.total_tokens
        result.hour_heatmap_events[hour] += 1

    for i in range(1, len(events)):
        gap = (events[i].event_time_utc - events[i - 1].event_time_utc).total_seconds()
        result.gap_pairs += 1
        if gap < 15:
            result.gaps_under_15s += 1
        if gap < 300:
            result.gaps_under_5m += 1

    ranked = sorted(events, key=lambda e: e.total_tokens, reverse=True)[:15]
    for ev in ranked:
        result.top_events.append(
            {
                "event_time_utc": ev.event_time_utc.isoformat(),
                "product": ev.product,
                "model": ev.model,
                "total_tokens": ev.total_tokens,
                "cached_prompt_tokens": ev.usage["cached-prompt-text-tokens"],
                "prompt_tokens": ev.usage["prompt-text-tokens"],
                "billing_item_id": ev.billing_item_id,
            }
        )

    result.kpi_checks = evaluate_kpis(result)
    return result


def pct(part: float, whole: float) -> float:
    if whole <= 0:
        return 0.0
    return 100.0 * part / whole


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

    if result.gap_pairs:
        rf15 = pct(result.gaps_under_15s, result.gap_pairs)
        add(
            "rapid_fire_under_15s_share",
            rf15,
            KPI["rapid_fire_under_15s_max_pct"],
            "lte",
            note="Share of consecutive event pairs with gap <15s",
        )
        rf5m = pct(result.gaps_under_5m, result.gap_pairs)
        checks.append(
            {
                "kpi": "rapid_fire_under_5m_share",
                "observed": round(rf5m, 4),
                "threshold": None,
                "comparator": "info",
                "unit": "%",
                "status": "info",
                "note": "Informational: gap <5 minutes",
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
        "window": {
            "start_utc": result.window_start_utc.isoformat() if result.window_start_utc else None,
            "end_utc": result.window_end_utc.isoformat() if result.window_end_utc else None,
            "duration_days": round(window_days(result), 4),
            "event_count": len(result.events),
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
            "pairs": result.gap_pairs,
            "under_15s": result.gaps_under_15s,
            "under_15s_share_pct": round(pct(result.gaps_under_15s, result.gap_pairs), 4),
            "under_5m": result.gaps_under_5m,
            "under_5m_share_pct": round(pct(result.gaps_under_5m, result.gap_pairs), 4),
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
    lines: list[str] = [
        "# Weekly token audit report",
        "",
        f"- **Source CSV:** `{source_csv}`",
        f"- **Events:** {len(result.events):,}",
        f"- **Window (UTC):** {result.window_start_utc} → {result.window_end_utc}",
        f"- **Duration:** {window_days(result):.2f} days",
        "",
        "## Baseline statement",
        "",
        baseline_note,
        "",
        "## Product share (whole window)",
        "",
        f"| Product | Tokens | Share |",
        f"| :--- | ---: | ---: |",
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
            f"- Event pairs: {result.gap_pairs:,}",
            f"- Gap &lt;15s: {result.gaps_under_15s:,} ({pct(result.gaps_under_15s, result.gap_pairs):.2f}%)",
            f"- Gap &lt;5m: {result.gaps_under_5m:,} ({pct(result.gaps_under_5m, result.gap_pairs):.2f}%)",
            "",
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

    lines.extend(["", "## KPI comparison (plan §0)", "", "| KPI | Observed | Threshold | Status |", "| :--- | ---: | ---: | :--- |"])
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
    rf15 = pct(result.gaps_under_15s, result.gap_pairs) if result.gap_pairs else 0.0

    if grok_share > KPI["grok_share_target_max_pct"]:
        logs.append(
            "[WOULD] Tighten max_context_tokens on top offending desks "
            f"(Grok share {grok_share:.2f}% > {KPI['grok_share_target_max_pct']}%)"
        )
        logs.append("[WOULD] Open PR to PROTOCOLS.md with mandatory Cursor dispatch rules")

    if rf15 > KPI["rapid_fire_under_15s_max_pct"]:
        logs.append(
            f"[WOULD] Flag rapid-fire desks (under-15s share {rf15:.2f}% > "
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

    events = load_csv(args.csv)
    result = compute_audit(events)
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
        print(f"audited {len(events)} events, {result.total_tokens:,} tokens", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())