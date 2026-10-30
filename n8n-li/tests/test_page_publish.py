#!/usr/bin/env python3
"""Unit tests for the WF1 organization publisher. HTTP is mocked. No LinkedIn calls."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cm" / "page-publish.py"

spec = importlib.util.spec_from_file_location("page_publish", SCRIPT)
assert spec is not None and spec.loader is not None
page_publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(page_publish)


ORG = "urn:li:organization:72031636"
PARENT = "urn:li:share:6957408550713184256"
TEXT = "CleantechHUB sample commentary"
TOKEN = "test-token-not-a-secret"


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _approval(directory: Path, text: str = TEXT, **overrides) -> str:
    approved_id = overrides.pop("id", "apr-test-001")
    record = {
        "id": approved_id,
        "approved_by": "gideon",
        "timestamp": "2026-10-30T16:00:00+00:00",
        "text_sha256": _sha(text),
        "reshare_parent": "",
    }
    record.update(overrides)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{approved_id}.json").write_text(
        json.dumps(record), encoding="utf-8"
    )
    return approved_id


class _Response:
    def __init__(self, status: int = 201, post_urn: str | None = "urn:li:share:6844785523593134080"):
        self.status = status
        self.headers = {"x-restli-id": post_urn} if post_urn else {}

    def read(self) -> bytes:
        return b""

    def getcode(self) -> int:
        return self.status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class PagePublishTests(unittest.TestCase):
    def setUp(self) -> None:
        self._env = patch.dict(os.environ, {}, clear=False)
        self._env.start()
        os.environ.pop("CM_LIVE", None)
        os.environ.pop("LINKEDIN_ACCESS_TOKEN", None)
        os.environ.pop("LINKEDIN_VERSION", None)
        self.addCleanup(self._env.stop)

    def _run(self, argv: list[str], urlopen=None):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            if urlopen is None:
                with patch("urllib.request.urlopen") as mocked:
                    code = page_publish.main(argv)
                    return code, stdout.getvalue(), stderr.getvalue(), mocked
            with patch("urllib.request.urlopen", urlopen):
                code = page_publish.main(argv)
                return code, stdout.getvalue(), stderr.getvalue(), urlopen

    def test_dry_run_is_default_and_skips_http(self) -> None:
        code, out, err, mocked = self._run(["--text", TEXT])
        self.assertEqual(code, 0, err)
        mocked.assert_not_called()
        payload = json.loads(out)
        self.assertEqual(payload["status"], "dry_run")
        self.assertFalse(payload["linkedin_api"])
        self.assertFalse(payload["http_called"])
        self.assertEqual(payload["payload"]["author"], ORG)
        self.assertEqual(payload["payload"]["commentary"], TEXT)
        self.assertEqual(payload["payload"]["lifecycleState"], "PUBLISHED")
        self.assertNotIn("reshareContext", payload["payload"])
        self.assertEqual(payload["text_sha256"], _sha(TEXT))
        self.assertNotIn(TOKEN, out)

    def test_dry_run_ignores_live_flag_and_token(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        code, out, err, mocked = self._run(["--text", TEXT, "--dry-run"])
        self.assertEqual(code, 0, err)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["status"], "dry_run")
        self.assertNotIn(TOKEN, out)

    def test_reshare_payload_shape(self) -> None:
        body = page_publish.build_post_body(TEXT, ORG, "PUBLIC", PARENT)
        self.assertEqual(body["reshareContext"], {"parent": PARENT})
        self.assertNotIn("root", body["reshareContext"])
        self.assertEqual(body["author"], ORG)
        self.assertEqual(body["distribution"]["feedDistribution"], "MAIN_FEED")
        text_only = page_publish.build_post_body(TEXT, ORG, "PUBLIC", None)
        self.assertNotIn("reshareContext", text_only)

    def test_dry_run_reshare_payload(self) -> None:
        code, out, err, mocked = self._run(
            ["--text", TEXT, "--reshare-parent", PARENT]
        )
        self.assertEqual(code, 0, err)
        mocked.assert_not_called()
        body = json.loads(out)["payload"]
        self.assertEqual(body["reshareContext"]["parent"], PARENT)
        self.assertNotIn("root", body["reshareContext"])

    def test_live_blocked_without_cm_live(self) -> None:
        code, out, err, mocked = self._run(
            ["--text", TEXT, "--no-dry-run", "--approved-id", "apr-test-001"]
        )
        self.assertEqual(code, 2)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["reason"], "cm_live_required")

    def test_live_blocked_without_approved_id(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        code, out, err, mocked = self._run(["--text", TEXT, "--no-dry-run"])
        self.assertEqual(code, 2)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["reason"], "approved_id_required")
        self.assertNotIn(TOKEN, out)
        self.assertNotIn(TOKEN, err)

    def test_live_blocked_when_approval_missing(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        missing = Path("/tmp/does-not-exist-n8n-li-approvals")
        code, out, err, mocked = self._run(
            [
                "--text",
                TEXT,
                "--no-dry-run",
                "--approved-id",
                "apr-missing",
                "--approvals-dir",
                str(missing),
            ]
        )
        self.assertEqual(code, 2)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["reason"], "approval_not_found")

    def test_approval_gate_rejects_wrong_approver(self) -> None:
        self._assert_gate_block({"approved_by": "someone-else"}, "approved_by_must_be_gideon")

    def test_approval_gate_rejects_missing_timestamp(self) -> None:
        self._assert_gate_block({"timestamp": ""}, "missing_timestamp")

    def test_approval_gate_rejects_naive_timestamp(self) -> None:
        self._assert_gate_block({"timestamp": "2026-10-30T16:00:00"}, "invalid_timestamp")

    def test_approval_gate_rejects_hash_mismatch(self) -> None:
        self._assert_gate_block({"text_sha256": "0" * 64}, "text_hash_mismatch")

    def test_approval_gate_rejects_reshare_swap(self) -> None:
        self._assert_gate_block(
            {"reshare_parent": PARENT},
            "reshare_parent_mismatch",
            extra_argv=["--reshare-parent", "urn:li:ugcPost:999"],
        )

    def _assert_gate_block(self, overrides: dict, reason: str, extra_argv: list[str] | None = None) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        with tempfile.TemporaryDirectory() as tmp:
            approved_id = _approval(Path(tmp), **overrides)
            argv = [
                "--text",
                TEXT,
                "--no-dry-run",
                "--approved-id",
                approved_id,
                "--approvals-dir",
                tmp,
            ]
            if extra_argv:
                argv.extend(extra_argv)
            code, out, err, mocked = self._run(argv)
        self.assertEqual(code, 2, err)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["reason"], reason)
        self.assertNotIn(TOKEN, out)
        self.assertNotIn(TOKEN, err)

    def test_live_blocked_without_token(self) -> None:
        os.environ["CM_LIVE"] = "1"
        with tempfile.TemporaryDirectory() as tmp:
            approved_id = _approval(Path(tmp))
            code, out, err, mocked = self._run(
                [
                    "--text",
                    TEXT,
                    "--no-dry-run",
                    "--approved-id",
                    approved_id,
                    "--approvals-dir",
                    tmp,
                ]
            )
        self.assertEqual(code, 2)
        mocked.assert_not_called()
        self.assertEqual(json.loads(out)["reason"], "access_token_required")

    def test_live_text_post_sends_posts_api_shape(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        captured = []

        def fake_urlopen(request, timeout=None):
            captured.append((request, timeout))
            return _Response()

        with tempfile.TemporaryDirectory() as tmp:
            approved_id = _approval(Path(tmp))
            code, out, err, _mocked = self._run(
                [
                    "--text",
                    TEXT,
                    "--no-dry-run",
                    "--approved-id",
                    approved_id,
                    "--approvals-dir",
                    tmp,
                ],
                urlopen=fake_urlopen,
            )
        self.assertEqual(code, 0, err)
        self.assertEqual(len(captured), 1)
        request, timeout = captured[0]
        self.assertEqual(timeout, 30)
        self.assertEqual(request.full_url, "https://api.linkedin.com/rest/posts")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Linkedin-version"), "202610")
        self.assertEqual(request.get_header("X-restli-protocol-version"), "2.0.0")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(request.get_header("Authorization"), f"Bearer {TOKEN}")
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["author"], ORG)
        self.assertEqual(body["commentary"], TEXT)
        self.assertEqual(body["visibility"], "PUBLIC")
        self.assertEqual(body["lifecycleState"], "PUBLISHED")
        self.assertNotIn("reshareContext", body)
        result = json.loads(out)
        self.assertEqual(result["status"], "published")
        self.assertTrue(result["linkedin_api"])
        self.assertEqual(result["post_urn"], "urn:li:share:6844785523593134080")
        self.assertEqual(result["approved_id"], approved_id)
        self.assertNotIn(TOKEN, out)
        self.assertNotIn(TOKEN, err)

    def test_live_reshare_parent_on_the_wire(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN
        captured = []

        def fake_urlopen(request, timeout=None):
            captured.append(request)
            return _Response(post_urn="urn:li:ugcPost:68447855235931240")

        with tempfile.TemporaryDirectory() as tmp:
            approved_id = _approval(Path(tmp), reshare_parent=PARENT)
            code, out, err, _mocked = self._run(
                [
                    "--text",
                    TEXT,
                    "--no-dry-run",
                    "--reshare-parent",
                    PARENT,
                    "--approved-id",
                    approved_id,
                    "--approvals-dir",
                    tmp,
                ],
                urlopen=fake_urlopen,
            )
        self.assertEqual(code, 0, err)
        body = json.loads(captured[0].data.decode("utf-8"))
        self.assertEqual(body["reshareContext"], {"parent": PARENT})
        self.assertNotIn("root", body["reshareContext"])
        self.assertEqual(json.loads(out)["post_urn"], "urn:li:ugcPost:68447855235931240")
        self.assertNotIn(TOKEN, out)

    def test_http_error_does_not_leak_token(self) -> None:
        os.environ["CM_LIVE"] = "1"
        os.environ["LINKEDIN_ACCESS_TOKEN"] = TOKEN

        def fake_urlopen(request, timeout=None):
            raise urllib.error.HTTPError(
                page_publish.POSTS_URL,
                403,
                "Forbidden",
                hdrs=None,
                fp=io.BytesIO(f"denied for {TOKEN}".encode("utf-8")),
            )

        with tempfile.TemporaryDirectory() as tmp:
            approved_id = _approval(Path(tmp))
            code, out, err, _mocked = self._run(
                [
                    "--text",
                    TEXT,
                    "--no-dry-run",
                    "--approved-id",
                    approved_id,
                    "--approvals-dir",
                    tmp,
                ],
                urlopen=fake_urlopen,
            )
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["reason"], "linkedin_http_error")
        self.assertIn("[redacted]", err)
        self.assertNotIn(TOKEN, out)
        self.assertNotIn(TOKEN, err)

    def test_source_has_no_secret_material(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("782xlck", source)
        self.assertNotIn("CLIENT_SECRET", source)
        self.assertNotIn("78cn54afhparm6", source)


class WorkflowContractTests(unittest.TestCase):
    def test_workflow_is_inactive_and_gated(self) -> None:
        path = ROOT / "workflows" / "wf1-org-publish-hitl.json"
        workflow = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(workflow["active"])
        types = [node["type"] for node in workflow["nodes"]]
        self.assertNotIn("n8n-nodes-base.scheduleTrigger", types)
        self.assertNotIn("n8n-nodes-base.cron", types)
        self.assertNotIn("n8n-nodes-base.webhook", types)
        self.assertIn("n8n-nodes-base.manualTrigger", types)
        self.assertIn("n8n-nodes-base.wait", types)

        by_name = {node["name"]: node for node in workflow["nodes"]}
        wait = by_name["Wait for Gideon"]
        self.assertEqual(wait["parameters"]["resume"], "webhook")
        self.assertNotIn("limitWaitTime", json.dumps(wait["parameters"]))

        linkedin = by_name["LinkedIn Create Org Post"]
        self.assertEqual(linkedin["parameters"]["url"], "https://api.linkedin.com/rest/posts")
        self.assertEqual(linkedin["parameters"]["method"], "POST")
        headers = {
            item["name"]: item["value"]
            for item in linkedin["parameters"]["headerParameters"]["parameters"]
        }
        self.assertEqual(headers["LinkedIn-Version"], "202610")
        self.assertEqual(headers["X-Restli-Protocol-Version"], "2.0.0")
        credential = linkedin["credentials"]["oAuth2Api"]
        self.assertEqual(credential["name"], "LinkedIn CleantechHUB n8n (78cn54)")
        self.assertEqual(credential["id"], "REPLACE_LINKEDIN_CREDENTIAL_ID")

        build = by_name["Build Org Post"]["parameters"]["jsCode"]
        self.assertIn("reshareContext", build)
        self.assertIn("parent", build)
        self.assertNotIn("root:", build)

        connections = workflow["connections"]
        true_branch = connections["IF Gideon Approved"]["main"][0]
        false_branch = connections["IF Gideon Approved"]["main"][1]
        self.assertEqual(true_branch[0]["node"], "Build Org Post")
        self.assertEqual(false_branch[0]["node"], "Log Not Approved")
        self.assertEqual(
            connections["Build Org Post"]["main"][0][0]["node"],
            "LinkedIn Create Org Post",
        )
        incoming = []
        for source, spec in connections.items():
            for outputs in spec.get("main", []):
                for edge in outputs:
                    if edge["node"] == "LinkedIn Create Org Post":
                        incoming.append(source)
        self.assertEqual(incoming, ["Build Org Post"])

        blob = path.read_text(encoding="utf-8")
        self.assertNotIn("782xlck", blob)
        self.assertNotIn("CLIENT_SECRET", blob)
        self.assertNotIn("Bearer ", blob)


if __name__ == "__main__":
    unittest.main()
