"""
Dormant evaluator for daily usage threshold alerts (prep only).

No network calls. Inputs are normalized percentage points of the shared weekly
included allowance for one America/Bogota calendar day — see docs/daily-usage-alerts.md.

Metric definition version bumps invalidate prior idempotency keys for the same (app, day).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, Iterable, List, Literal, Optional, Set, Tuple
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo("America/Bogota")

THRESHOLD_PP: Dict[str, Decimal] = {
    "grok_bot": Decimal("10"),
    "cursor": Decimal("4"),
}

AppId = Literal["grok_bot", "cursor"]


class Coverage(str, Enum):
    """Per-app source coverage."""

    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class UsageReading:
    """One normalized reading for an app on one Bogota calendar day."""

    app: AppId
    day: date
    metric_pp: Decimal
    """Percentage points of weekly included allowance (partial or total for tests)."""

    sample_id: str
    source_ts: Optional[datetime] = None
    observation_ts: Optional[datetime] = None
    is_correction: bool = False

    def __post_init__(self) -> None:
        if self.app not in THRESHOLD_PP:
            raise ValueError(f"unknown app {self.app!r}")


@dataclass
class AlertDecision:
    """Output of one evaluate() call (may emit 0+ threshold alerts — at most one per app/day/call)."""

    threshold_alerts: List[str] = field(default_factory=list)
    data_quality_warnings: List[str] = field(default_factory=list)
    blocked_skips: List[str] = field(default_factory=list)


def strict_above(value: Decimal, threshold: Decimal) -> bool:
    """Strict `>` — boundary values do not trigger."""
    return value > threshold


def _alert_key(app: AppId, day: date, metric_version: str) -> Tuple[str, str, str]:
    return (app, day.isoformat(), metric_version)


@dataclass
class DailyUsageEvaluator:
    """
    In-memory state for tests / dormant dry-run.

    Contributions with the same sample_id are de-duplicated; the last stored value wins
    (corrections set is_correction=True and overwrite the same sample_id).

    At most one threshold alert per app per local day per metric_definition_version.
    """

    metric_definition_version: str = "v0-prep"
    coverage: Dict[AppId, Coverage] = field(
        default_factory=lambda: {"grok_bot": Coverage.BLOCKED, "cursor": Coverage.BLOCKED}
    )
    _contributions: Dict[Tuple[AppId, date], Dict[str, Decimal]] = field(default_factory=dict)
    _seen_sample_ids: Set[str] = field(default_factory=set)
    _sent_keys: Set[Tuple[str, str, str]] = field(default_factory=set)
    _alert_already_issued: Set[Tuple[AppId, date]] = field(default_factory=set)

    def _day_total(self, app: AppId, day: date) -> Decimal:
        bucket = self._contributions.get((app, day), {})
        return sum(bucket.values(), start=Decimal("0"))

    def new_subscription_cycle(self) -> None:
        """
        Clear rolling counters when the weekly included allowance pool resets.

        Idempotency keys for a *new* cycle should use a new metric_definition_version
        or an external store keyed by allowance period; this helper models a reset for tests.
        """
        self._contributions.clear()
        self._seen_sample_ids.clear()
        self._sent_keys.clear()
        self._alert_already_issued.clear()

    def evaluate(
        self,
        readings: Iterable[UsageReading],
        *,
        now: datetime,
        incomplete_baseline: bool = False,
    ) -> AlertDecision:
        """
        Process readings (possibly out of order). `now` must be timezone-aware.

        If incomplete_baseline is True, never emit a spend-threshold alert (data quality only).
        """
        out = AlertDecision()

        for r in readings:
            cov = self.coverage.get(r.app, Coverage.BLOCKED)
            if cov is Coverage.BLOCKED:
                out.blocked_skips.append(
                    f"{r.app}:{r.day.isoformat()} blocked — missing proven source"
                )
                continue

            if r.sample_id in self._seen_sample_ids and not r.is_correction:
                out.data_quality_warnings.append(
                    f"duplicate sample_id ignored {r.sample_id!r} {r.app} {r.day}"
                )
                continue

            self._seen_sample_ids.add(r.sample_id)
            per_day = self._contributions.setdefault((r.app, r.day), {})
            per_day[r.sample_id] = r.metric_pp

        if incomplete_baseline:
            out.data_quality_warnings.append(
                "incomplete intraday baseline — no spend threshold alert"
            )
            return out

        seen_apps_days: Set[Tuple[AppId, date]] = set()
        for r in readings:
            if self.coverage.get(r.app, Coverage.BLOCKED) is Coverage.BLOCKED:
                continue
            seen_apps_days.add((r.app, r.day))

        for app, day in sorted(seen_apps_days):
            thr = THRESHOLD_PP[app]
            total = self._day_total(app, day)
            key = _alert_key(app, day, self.metric_definition_version)

            if strict_above(total, thr):
                if key in self._sent_keys:
                    continue
                self._sent_keys.add(key)
                self._alert_already_issued.add((app, day))
                out.threshold_alerts.append(
                    f"{app} {day.isoformat()} metric_pp={total} > {thr} "
                    f"(metric_def={self.metric_definition_version})"
                )

        # Correction pass: readings flagged as corrections that arrive after an alert
        for r in readings:
            if self.coverage.get(r.app, Coverage.BLOCKED) is Coverage.BLOCKED:
                continue
            if not r.is_correction:
                continue
            if (r.app, r.day) in self._alert_already_issued:
                out.data_quality_warnings.append(
                    f"correction after alert for {r.app} {r.day.isoformat()} — no resend"
                )

        return out


def infer_cursor_from_total_minus_grok(
    total_pp: Decimal,
    grok_pp: Decimal,
) -> Decimal:
    """
    **FORBIDDEN** for production coverage — raises to catch mistaken use.

    Ticket: never derive Cursor usage by subtracting Grok Bot from a shared total.
    """
    raise RuntimeError(
        "unsupported: Cursor must not be inferred from total minus Grok Bot"
    )


def local_day_from_utc(ts_utc: datetime, zone: ZoneInfo = BOGOTA) -> date:
    """Map an instant to calendar date in America/Bogota."""
    if ts_utc.tzinfo is None:
        raise ValueError("ts_utc must be timezone-aware")
    return ts_utc.astimezone(zone).date()
