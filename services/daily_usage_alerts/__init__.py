"""Dormant daily usage alert evaluator (synthetic tests only; no live I/O)."""

from .evaluator import AlertDecision, AppId, Coverage, DailyUsageEvaluator

__all__ = ["AlertDecision", "AppId", "Coverage", "DailyUsageEvaluator"]
