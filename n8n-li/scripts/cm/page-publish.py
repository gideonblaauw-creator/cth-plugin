#!/usr/bin/env python3
"""Publish a CleantechHUB LinkedIn post via the Posts API.

Organization author is the default. Personal-profile author is opt-in.
Dry-run is the default. A live POST needs CM_LIVE=1, --no-dry-run, and
--approved-id. The approval record must have approved_by=gideon, a
timezone-aware timestamp, and the sha256 of the exact commentary.

The access token is read from the LINKEDIN_ACCESS_TOKEN environment variable.
This file must not contain secrets.

Posts API (Microsoft Learn, version view li-lms-2026-10):
  POST https://api.linkedin.com/rest/posts
  LinkedIn-Version: YYYYMM (default 202610, override with LINKEDIN_VERSION)
  X-Restli-Protocol-Version: 2.0.0
  Organization author: urn:li:organization:72031636
  Organization scope: w_organization_social
  Person author: urn:li:person:<id>
  Person id: LINKEDIN_PERSON_ID, or GET https://api.linkedin.com/v2/userinfo
  field sub on a live run. Person scope: w_member_social.
  userinfo also needs openid and profile. Dry-run does not call userinfo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

POSTS_URL = "https://api.linkedin.com/rest/posts"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
DEFAULT_ORG_URN = "urn:li:organization:72031636"
DEFAULT_LINKEDIN_VERSION = "202610"
TOKEN_ENV = "LINKEDIN_ACCESS_TOKEN"
PERSON_ID_ENV = "LINKEDIN_PERSON_ID"
VERSION_ENV = "LINKEDIN_VERSION"
RESTLI_PROTOCOL_VERSION = "2.0.0"
APPROVED_BY = "gideon"
USER_AGENT = "CleantechHUB-n8n-li-page-publish"
AUTHOR_ORG = "org"
AUTHOR_PERSON = "person"

_ORG_URN_RE = re.compile(r"^urn:li:organization:\d+$")
_PERSON_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
_PARENT_URN_RE = re.compile(r"^urn:li:(?:share|ugcPost|groupPost):[A-Za-z0-9._:-]+$")
_APPROVED_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_VERSION_RE = re.compile(r"^\d{6}$")
_VISIBILITY = frozenset({"PUBLIC", "LOGGED_IN"})
_AUTHORS = frozenset({AUTHOR_ORG, AUTHOR_PERSON})


class ApprovalError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class PublishError(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(code)


def cm_live_enabled() -> bool:
    return os.environ.get("CM_LIVE", "0").strip().lower() in ("1", "true", "yes")


def linkedin_version() -> str:
    raw = os.environ.get(VERSION_ENV, DEFAULT_LINKEDIN_VERSION).strip()
    if not _VERSION_RE.fullmatch(raw):
        raise PublishError("bad_linkedin_version")
    return raw


def text_sha256(text: str) -> str:
    """SHA-256 hex of the exact UTF-8 text. No trim and no little-text escaping."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def default_approvals_dir() -> Path:
    root = Path(os.environ.get("N8N_LI_ROOT", "/opt/n8n-li"))
    return root / "data" / "cm" / "approvals"


def approval_path(directory: Path, approved_id: str) -> Path:
    if not _APPROVED_ID_RE.fullmatch(approved_id):
        raise ApprovalError("bad_approved_id")
    root = directory.resolve()
    path = (root / f"{approved_id}.json").resolve()
    if path.parent != root:
        raise ApprovalError("bad_approved_id")
    return path


def load_approval(directory: Path, approved_id: str) -> dict:
    path = approval_path(directory, approved_id)
    if not path.is_file():
        raise ApprovalError("approval_not_found")
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ApprovalError("approval_invalid_json") from exc
    if not isinstance(record, dict):
        raise ApprovalError("approval_invalid_json")
    return record


def _parse_timestamp(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ApprovalError("missing_timestamp")
    raw = value.strip()
    candidate = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ApprovalError("invalid_timestamp") from exc
    if parsed.tzinfo is None:
        raise ApprovalError("invalid_timestamp")
    return raw


def validate_approval(record: dict, text: str, reshare_parent: str | None) -> None:
    if record.get("approved_by") != APPROVED_BY:
        raise ApprovalError("approved_by_must_be_gideon")
    _parse_timestamp(record.get("timestamp"))
    expected = text_sha256(text)
    recorded = record.get("text_sha256")
    if not isinstance(recorded, str) or recorded.strip().lower() != expected:
        raise ApprovalError("text_hash_mismatch")
    recorded_parent = record.get("reshare_parent", "")
    if recorded_parent is None:
        recorded_parent = ""
    if not isinstance(recorded_parent, str):
        raise ApprovalError("reshare_parent_mismatch")
    wanted = reshare_parent or ""
    if recorded_parent != wanted:
        raise ApprovalError("reshare_parent_mismatch")


def person_urn(person_id: str) -> str:
    if not _PERSON_ID_RE.fullmatch(person_id):
        raise PublishError("bad_person_id")
    return f"urn:li:person:{person_id}"


def configured_person_id() -> str | None:
    """Bare member id from LINKEDIN_PERSON_ID. Unset means resolve via userinfo."""
    raw = os.environ.get(PERSON_ID_ENV, "").strip()
    if not raw:
        return None
    if not _PERSON_ID_RE.fullmatch(raw):
        raise PublishError("bad_person_id")
    return raw


def build_post_body(
    text: str,
    author_urn: str,
    visibility: str,
    reshare_parent: str | None,
) -> dict:
    body = {
        "author": author_urn,
        "commentary": text,
        "visibility": visibility,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if reshare_parent:
        body["reshareContext"] = {"parent": reshare_parent}
    return body


def _header(headers: object, name: str) -> str | None:
    getter = getattr(headers, "get", None)
    if getter is None:
        return None
    for key in (name, name.lower()):
        found = getter(key)
        if found:
            return str(found).strip()
    return None


def _redact(text: str, token: str) -> str:
    if token:
        return text.replace(token, "[redacted]")
    return text


def _read_error_body(exc: urllib.error.HTTPError, token: str) -> str:
    detail = ""
    try:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
    except Exception:
        detail = ""
    return _redact(f"HTTP {exc.code}: {detail}", token)


def fetch_person_id(token: str) -> str:
    """GET /v2/userinfo and return the sub field. Does not return profile fields."""
    request = urllib.request.Request(USERINFO_URL, method="GET")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = getattr(response, "status", None) or response.getcode()
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise PublishError("userinfo_http_error", _read_error_body(exc, token)) from exc
    except urllib.error.URLError as exc:
        raise PublishError("linkedin_transport_error", "transport error") from exc

    if status != 200:
        raise PublishError("userinfo_http_error", f"HTTP {status}")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PublishError("userinfo_invalid_json") from exc
    sub = payload.get("sub") if isinstance(payload, dict) else None
    if not isinstance(sub, str):
        raise PublishError("userinfo_missing_sub")
    sub = sub.strip()
    if not _PERSON_ID_RE.fullmatch(sub):
        raise PublishError("userinfo_missing_sub")
    return sub


def post_to_linkedin(body: dict, token: str, version: str) -> dict:
    payload = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(POSTS_URL, data=payload, method="POST")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("LinkedIn-Version", version)
    request.add_header("X-Restli-Protocol-Version", RESTLI_PROTOCOL_VERSION)
    request.add_header("Content-Type", "application/json")
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = getattr(response, "status", None) or response.getcode()
            response.read()
            post_urn = _header(getattr(response, "headers", None), "x-restli-id")
    except urllib.error.HTTPError as exc:
        raise PublishError("linkedin_http_error", _read_error_body(exc, token)) from exc
    except urllib.error.URLError as exc:
        raise PublishError("linkedin_transport_error", "transport error") from exc

    if status not in (200, 201):
        raise PublishError("linkedin_http_error", f"HTTP {status}")
    result = {
        "status": "published",
        "linkedin_api": True,
        "http_called": True,
        "http_status": status,
        "post_urn": post_urn,
        "posts_url": POSTS_URL,
    }
    if not post_urn:
        result["warning"] = "missing_x_restli_id"
    return result


def _emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def blocked(code: str) -> int:
    print(f"BLOCKED: {code}", file=sys.stderr)
    _emit({"linkedin_api": False, "reason": code, "status": "blocked"})
    return 2


def _fail_publish(exc: PublishError) -> int:
    print(f"ERROR: {exc.code}", file=sys.stderr)
    if exc.detail:
        print(exc.detail, file=sys.stderr)
    _emit(
        {
            "linkedin_api": True,
            "reason": exc.code,
            "status": "error",
        }
    )
    return 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a CleantechHUB LinkedIn post (dry-run by default)."
    )
    parser.add_argument("--text", required=True, help="Exact post commentary")
    parser.add_argument(
        "--author",
        choices=sorted(_AUTHORS),
        default=AUTHOR_ORG,
        help="org (default) or person. person uses urn:li:person:<id>.",
    )
    parser.add_argument(
        "--visibility",
        default="PUBLIC",
        help="PUBLIC or LOGGED_IN (Posts API samples use PUBLIC)",
    )
    parser.add_argument(
        "--org-urn",
        default=DEFAULT_ORG_URN,
        help="Organization author URN. Used when --author org.",
    )
    parser.add_argument(
        "--reshare-parent",
        default=None,
        help="Post URN for reshareContext.parent (urn:li:share: or urn:li:ugcPost:)",
    )
    parser.add_argument(
        "--approved-id",
        default=None,
        help="Approval record id. Required for a live run.",
    )
    parser.add_argument(
        "--approvals-dir",
        default=None,
        help="Directory of <approved-id>.json records",
    )
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Default. --no-dry-run attempts a live POST when every gate passes.",
    )
    return parser.parse_args(argv)


def _validate_request(args: argparse.Namespace) -> str | None:
    if args.author not in _AUTHORS:
        return "bad_author"
    if args.text == "" or args.text.strip() == "":
        return "empty_text"
    if args.visibility not in _VISIBILITY:
        return "bad_visibility"
    if args.author == AUTHOR_ORG and not _ORG_URN_RE.fullmatch(args.org_urn):
        return "bad_org_urn"
    if args.reshare_parent is not None and not _PARENT_URN_RE.fullmatch(args.reshare_parent):
        return "bad_reshare_parent"
    return None


def _check_approval(args: argparse.Namespace) -> dict:
    directory = Path(args.approvals_dir) if args.approvals_dir else default_approvals_dir()
    record = load_approval(directory, args.approved_id)
    validate_approval(record, args.text, args.reshare_parent)
    return record


def _author_fields(author_kind: str, author_urn: str, org_urn: str) -> dict:
    fields = {"author_kind": author_kind}
    if author_kind == AUTHOR_ORG:
        fields["organization_urn"] = org_urn
    else:
        fields["person_urn"] = author_urn
    return fields


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    problem = _validate_request(args)
    if problem:
        return blocked(problem)

    person_id = None
    if args.author == AUTHOR_PERSON:
        try:
            person_id = configured_person_id()
        except PublishError as exc:
            return blocked(exc.code)
        if person_id is None and args.dry_run:
            return blocked("person_id_required")

    author_urn = args.org_urn if args.author == AUTHOR_ORG else None
    if person_id is not None:
        author_urn = person_urn(person_id)
    digest = text_sha256(args.text)

    if args.dry_run:
        approval = None
        if args.approved_id:
            try:
                _check_approval(args)
            except ApprovalError as exc:
                return blocked(exc.code)
            approval = {"id": args.approved_id, "ok": True}
        body = build_post_body(args.text, author_urn, args.visibility, args.reshare_parent)
        payload = {
            "approval": approval,
            "cm_live": cm_live_enabled(),
            "http_called": False,
            "linkedin_api": False,
            "payload": body,
            "status": "dry_run",
            "text_sha256": digest,
        }
        payload.update(_author_fields(args.author, author_urn, args.org_urn))
        _emit(payload)
        return 0

    if not cm_live_enabled():
        return blocked("cm_live_required")
    if not args.approved_id:
        return blocked("approved_id_required")
    token = os.environ.get(TOKEN_ENV, "").strip()
    if not token:
        return blocked("access_token_required")
    try:
        _check_approval(args)
    except ApprovalError as exc:
        return blocked(exc.code)
    try:
        version = linkedin_version()
        if author_urn is None:
            author_urn = person_urn(fetch_person_id(token))
        body = build_post_body(args.text, author_urn, args.visibility, args.reshare_parent)
        result = post_to_linkedin(body, token, version)
    except PublishError as exc:
        return _fail_publish(exc)

    result["approved_id"] = args.approved_id
    result["cm_live"] = True
    result["text_sha256"] = digest
    result.update(_author_fields(args.author, author_urn, args.org_urn))
    _emit(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
