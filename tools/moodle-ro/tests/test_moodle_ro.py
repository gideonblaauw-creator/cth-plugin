"""Offline tests with mocked HTTP — no live Moodle calls."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import MagicMock, patch

import requests

# Import from parent directory
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import moodle_ro as mro  # noqa: E402


class TestAllowlist(unittest.TestCase):
    def test_refuses_unknown_function(self) -> None:
        client = mro.MoodleClient("https://example.edu", "secret-token-value")
        with self.assertRaises(mro.MoodleROError) as ctx:
            client.call("core_user_get_users")
        self.assertIn("Refused", str(ctx.exception))
        self.assertNotIn("secret-token-value", str(ctx.exception))


class TestRedaction(unittest.TestCase):
    def test_redact_token_in_text(self) -> None:
        text = "failed wstoken=abc123&wsfunction=x"
        out = mro.redact_secrets(text, "abc123")
        self.assertNotIn("abc123", out)
        self.assertIn("[REDACTED_TOKEN]", out)


class TestConfig(unittest.TestCase):
    def test_load_from_env(self) -> None:
        with patch.dict(
            os.environ,
            {"MOODLE_URL": "https://academy.example/", "MOODLE_WS_TOKEN": "tok"},
            clear=False,
        ):
            url, token = mro.load_config()
        self.assertEqual(url, "https://academy.example")
        self.assertEqual(token, "tok")

    @patch.dict(os.environ, {}, clear=True)
    @patch("moodle_ro._infisical_secret")
    def test_load_from_infisical_fallback(self, mock_get: MagicMock) -> None:
        def side_effect(name: str) -> str | None:
            return {"MOODLE_URL": "https://a.example", "MOODLE_WS_TOKEN": "t2"}.get(name)

        mock_get.side_effect = side_effect
        url, token = mro.load_config()
        self.assertEqual(url, "https://a.example")
        self.assertEqual(token, "t2")


class TestMoodleClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = mro.MoodleClient(
            "https://academy.example",
            "super-secret",
            rate_sleep_s=0,
            max_retries=1,
        )
        self.session = MagicMock()
        self.client.session = self.session

    def test_success_json(self) -> None:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"sitename": "Academy"}
        self.session.post.return_value = resp

        data = self.client.site_info()
        self.assertEqual(data["sitename"], "Academy")
        call_kwargs = self.session.post.call_args.kwargs
        self.assertIn("data", call_kwargs)
        self.assertEqual(call_kwargs["data"]["wsfunction"], "core_webservice_get_site_info")

    def test_moodle_exception_json(self) -> None:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "exception": "moodle_exception",
            "errorcode": "invalidtoken",
            "message": "Invalid token super-secret",
        }
        self.session.post.return_value = resp

        with self.assertRaises(mro.MoodleROError) as ctx:
            self.client.site_info()
        self.assertNotIn("super-secret", str(ctx.exception))

    def test_retry_on_500_then_success(self) -> None:
        bad = MagicMock(status_code=503, text="error")
        good = MagicMock(status_code=200)
        good.json.return_value = [{"id": 1}]
        self.session.post.side_effect = [bad, good]

        client = mro.MoodleClient(
            "https://academy.example",
            "tok",
            rate_sleep_s=0,
            max_retries=2,
        )
        client.session = self.session
        data = client.courses()
        self.assertEqual(data, [{"id": 1}])
        self.assertEqual(self.session.post.call_count, 2)

    def test_no_retry_on_400(self) -> None:
        resp = MagicMock(status_code=404, text="not found")
        self.session.post.return_value = resp
        with self.assertRaises(mro.MoodleROError):
            self.client.courses()

    def test_request_exception_redacts_token(self) -> None:
        self.session.post.side_effect = requests.Timeout("timeout with super-secret")
        with self.assertRaises(mro.MoodleROError) as ctx:
            self.client.courses()
        self.assertNotIn("super-secret", str(ctx.exception))


class TestAggregates(unittest.TestCase):
    def test_aggregate_enrolled(self) -> None:
        self.assertEqual(
            mro.aggregate_enrolled([{"id": 1}, {"id": 2}]),
            {"enrolled_user_count": 2},
        )

    def test_aggregate_completion(self) -> None:
        rows = [
            {"userid": 1, "completion": {"completed": True}},
            {"userid": 2, "completion": {"completed": False}},
        ]
        agg = mro.aggregate_completion(rows)
        self.assertEqual(agg["learners_marked_complete"], 1)
        self.assertEqual(agg["learners_with_completion_checked"], 2)


class TestSnapshotPermissions(unittest.TestCase):
    def test_include_pii_sets_mode_600(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "nested" / "enrolled.json"
            mro.write_json(path, [{"id": 1, "email": "a@b.co"}], include_pii=True)
            mode = path.stat().st_mode & 0o777
            self.assertEqual(mode, 0o600)


if __name__ == "__main__":
    unittest.main()
