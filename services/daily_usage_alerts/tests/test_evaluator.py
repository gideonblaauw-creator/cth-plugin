"""Synthetic tests for dormant daily usage alert evaluator — no live I/O."""

from datetime import date, datetime, timezone
from decimal import Decimal
import unittest

from services.daily_usage_alerts.evaluator import (
    BOGOTA,
    Coverage,
    DailyUsageEvaluator,
    UsageReading,
    infer_cursor_from_total_minus_grok,
    local_day_from_utc,
    strict_above,
)


class TestStrictAbove(unittest.TestCase):
    def test_grok_boundary(self) -> None:
        self.assertFalse(strict_above(Decimal("10"), Decimal("10")))
        self.assertFalse(strict_above(Decimal("10.0"), Decimal("10")))
        self.assertTrue(strict_above(Decimal("10.0000001"), Decimal("10")))

    def test_cursor_boundary(self) -> None:
        self.assertFalse(strict_above(Decimal("4"), Decimal("4")))
        self.assertTrue(strict_above(Decimal("4.0000001"), Decimal("4")))


class TestThresholdAlerts(unittest.TestCase):
    def test_grok_ten_point_zero_no_alert_then_correction_triggers(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        a = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("10.0"), sample_id="s1")],
            now=now,
        )
        self.assertEqual(a.threshold_alerts, [])
        b = ev.evaluate(
            [
                UsageReading(
                    "grok_bot",
                    d,
                    Decimal("10.0000001"),
                    sample_id="s1",
                    is_correction=True,
                ),
            ],
            now=now,
        )
        self.assertEqual(len(b.threshold_alerts), 1)

    def test_cursor_four_no_alert_then_correction_triggers(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.BLOCKED, "cursor": Coverage.READY}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        self.assertEqual(
            ev.evaluate(
                [UsageReading("cursor", d, Decimal("4.0"), sample_id="c1")],
                now=now,
            ).threshold_alerts,
            [],
        )
        out = ev.evaluate(
            [
                UsageReading(
                    "cursor",
                    d,
                    Decimal("4.0000001"),
                    sample_id="c1",
                    is_correction=True,
                ),
            ],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)

    def test_apps_independent(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.READY}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [
                UsageReading("grok_bot", d, Decimal("11"), sample_id="g1"),
                UsageReading("cursor", d, Decimal("3"), sample_id="u1"),
            ],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)
        self.assertIn("grok_bot", out.threshold_alerts[0])

    def test_duplicate_sample_ignored(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [
                UsageReading("grok_bot", d, Decimal("5"), sample_id="dup"),
                UsageReading("grok_bot", d, Decimal("99"), sample_id="dup"),
            ],
            now=now,
        )
        self.assertTrue(any("duplicate" in w for w in out.data_quality_warnings))

    def test_correction_no_resend_after_alert(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        first = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("11"), sample_id="a")],
            now=now,
        )
        self.assertEqual(len(first.threshold_alerts), 1)
        second = ev.evaluate(
            [
                UsageReading(
                    "grok_bot",
                    d,
                    Decimal("-10"),
                    sample_id="a",
                    is_correction=True,
                ),
            ],
            now=now,
        )
        self.assertEqual(second.threshold_alerts, [])
        self.assertTrue(
            any("correction after alert" in w for w in second.data_quality_warnings)
        )

    def test_weekly_reset_subscription_cycle(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        ev.evaluate([UsageReading("grok_bot", d, Decimal("11"), sample_id="x")], now=now)
        ev.new_subscription_cycle()
        out = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("11"), sample_id="y")],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)

    def test_late_record_keeps_event_day(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        past_day = date(2026, 11, 5)
        now = datetime(2026, 11, 7, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [UsageReading("grok_bot", past_day, Decimal("11"), sample_id="late1")],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)
        self.assertIn("2026-11-05", out.threshold_alerts[0])

    def test_bogota_midnight_boundary_vs_utc(self) -> None:
        ts = datetime(2026, 11, 6, 4, 59, 0, tzinfo=timezone.utc)
        self.assertEqual(local_day_from_utc(ts), date(2026, 11, 5))
        ts2 = datetime(2026, 11, 6, 5, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(local_day_from_utc(ts2), date(2026, 11, 6))

    def test_out_of_order_samples_sum_same_day(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"cursor": Coverage.READY, "grok_bot": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [
                UsageReading("cursor", d, Decimal("3"), sample_id="p2"),
                UsageReading("cursor", d, Decimal("2"), sample_id="p1"),
            ],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)

    def test_blocked_no_zero_alert(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.BLOCKED, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("0"), sample_id="z")],
            now=now,
        )
        self.assertEqual(out.threshold_alerts, [])
        self.assertTrue(any("blocked" in b for b in out.blocked_skips))

    def test_incomplete_baseline_no_threshold_alert(self) -> None:
        ev = DailyUsageEvaluator(
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED}
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        out = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("50"), sample_id="q")],
            now=now,
            incomplete_baseline=True,
        )
        self.assertEqual(out.threshold_alerts, [])
        self.assertTrue(
            any("baseline" in w for w in out.data_quality_warnings)
        )

    def test_infer_cursor_subtraction_forbidden(self) -> None:
        with self.assertRaises(RuntimeError):
            infer_cursor_from_total_minus_grok(Decimal("100"), Decimal("60"))

    def test_metric_version_bumps_new_idempotency(self) -> None:
        ev = DailyUsageEvaluator(
            metric_definition_version="v1",
            coverage={"grok_bot": Coverage.READY, "cursor": Coverage.BLOCKED},
        )
        d = date(2026, 11, 6)
        now = datetime(2026, 11, 6, 12, 0, tzinfo=BOGOTA)
        ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("11"), sample_id="m")],
            now=now,
        )
        ev.metric_definition_version = "v2"
        out = ev.evaluate(
            [UsageReading("grok_bot", d, Decimal("11"), sample_id="m2")],
            now=now,
        )
        self.assertEqual(len(out.threshold_alerts), 1)


if __name__ == "__main__":
    unittest.main()
