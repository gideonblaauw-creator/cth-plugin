#!/usr/bin/env python3
"""
Read-only Moodle web services client for CleantechHUB Academy snapshots.

Secrets: MOODLE_URL and MOODLE_WS_TOKEN from Infisical (cth-agents) or env when
injected by `infisical run`. No live calls in unit tests.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping, Sequence
from urllib.parse import urljoin

import requests

INFISICAL_PROJECT_ID = "c84fe8b3-d64e-485a-82d7-250dc57a6453"

ALLOWED_WS_FUNCTIONS: frozenset[str] = frozenset(
    {
        "core_webservice_get_site_info",
        "core_course_get_courses",
        "core_course_get_courses_by_field",
        "core_enrol_get_enrolled_users",
        "core_completion_get_course_completion_status",
        "core_completion_get_activities_completion_status",
        "gradereport_user_get_grade_items",
        "mod_customcert_get_customcerts_by_courses",
        "mod_customcert_list_issues",
    }
)

DEFAULT_RATE_SLEEP_S = 0.35
DEFAULT_TIMEOUT_S = 30
DEFAULT_MAX_RETRIES = 3
RETRY_BACKOFF_S = 1.0


class MoodleROError(Exception):
    """Base error with token redaction in messages."""


def redact_secrets(text: str, token: str | None) -> str:
    if not text:
        return text
    if token:
        text = text.replace(token, "[REDACTED_TOKEN]")
    text = re.sub(r"(wstoken=)[^&\s]+", r"\1[REDACTED_TOKEN]", text, flags=re.IGNORECASE)
    text = re.sub(r'("wstoken"\s*:\s*")[^"]+(")', r"\1[REDACTED_TOKEN]\2", text, flags=re.IGNORECASE)
    return text


def _infisical_secret(name: str) -> str | None:
    cmd = [
        "infisical",
        "secrets",
        "get",
        name,
        f"--projectId={INFISICAL_PROJECT_ID}",
        "--plain",
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    value = (proc.stdout or "").strip()
    return value or None


def load_config() -> tuple[str, str]:
    """Load MOODLE_URL and MOODLE_WS_TOKEN from env or Infisical CLI."""
    url = os.environ.get("MOODLE_URL", "").strip()
    token = os.environ.get("MOODLE_WS_TOKEN", "").strip()
    if not url:
        url = _infisical_secret("MOODLE_URL") or ""
    if not token:
        token = _infisical_secret("MOODLE_WS_TOKEN") or ""
    if not url or not token:
        raise MoodleROError(
            "MOODLE_URL and MOODLE_WS_TOKEN must be set in the environment "
            "(e.g. via `infisical run --projectId=... --`) or available through "
            "the Infisical CLI for project cth-agents."
        )
    return url.rstrip("/"), token


@dataclass
class MoodleClient:
    base_url: str
    token: str
    rate_sleep_s: float = DEFAULT_RATE_SLEEP_S
    timeout_s: float = DEFAULT_TIMEOUT_S
    max_retries: int = DEFAULT_MAX_RETRIES
    session: requests.Session | None = None

    def __post_init__(self) -> None:
        if self.session is None:
            self.session = requests.Session()

    @property
    def endpoint(self) -> str:
        return urljoin(self.base_url + "/", "webservice/rest/server.php")

    @staticmethod
    def _encode_params(params: Mapping[str, Any]) -> dict[str, Any]:
        encoded: dict[str, Any] = {}
        for key, value in params.items():
            if isinstance(value, (list, tuple)):
                for idx, item in enumerate(value):
                    encoded[f"{key}[{idx}]"] = item
            else:
                encoded[key] = value
        return encoded

    def call(self, wsfunction: str, **params: Any) -> Any:
        if wsfunction not in ALLOWED_WS_FUNCTIONS:
            raise MoodleROError(f"Refused disallowed webservice function: {wsfunction}")

        payload: MutableMapping[str, Any] = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "moodlewsrestformat": "json",
        }
        payload.update(self._encode_params(params))

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            if self.rate_sleep_s > 0 and attempt == 0:
                time.sleep(self.rate_sleep_s)
            elif attempt > 0:
                time.sleep(RETRY_BACKOFF_S * attempt)

            try:
                resp = self.session.post(
                    self.endpoint,
                    data=payload,
                    timeout=self.timeout_s,
                )
            except requests.RequestException as exc:
                last_error = exc
                msg = redact_secrets(str(exc), self.token)
                last_error = MoodleROError(msg)
                continue

            if resp.status_code >= 500:
                last_error = MoodleROError(
                    redact_secrets(
                        f"Moodle HTTP {resp.status_code} for {wsfunction}",
                        self.token,
                    )
                )
                continue

            if resp.status_code >= 400:
                raise MoodleROError(
                    redact_secrets(
                        f"Moodle HTTP {resp.status_code} for {wsfunction}: {resp.text[:500]}",
                        self.token,
                    )
                )

            try:
                data = resp.json()
            except json.JSONDecodeError as exc:
                raise MoodleROError(
                    redact_secrets(
                        f"Invalid JSON from Moodle for {wsfunction}: {exc}",
                        self.token,
                    )
                ) from exc

            if isinstance(data, dict) and data.get("exception"):
                message = str(data.get("message", "Moodle webservice exception"))
                errorcode = data.get("errorcode", "")
                raise MoodleROError(
                    redact_secrets(
                        f"Moodle exception ({errorcode}): {message}",
                        self.token,
                    )
                )

            if self.rate_sleep_s > 0:
                time.sleep(self.rate_sleep_s)
            return data

        assert last_error is not None
        raise last_error

    def site_info(self) -> Any:
        return self.call("core_webservice_get_site_info")

    def courses(self) -> Any:
        return self.call("core_course_get_courses")

    def course_by_id(self, courseid: int) -> Any:
        return self.call(
            "core_course_get_courses_by_field",
            field="id",
            value=str(courseid),
        )

    def enrolled_users(self, courseid: int) -> Any:
        return self.call("core_enrol_get_enrolled_users", courseid=courseid)

    def course_completion(self, courseid: int, userid: int) -> Any:
        return self.call(
            "core_completion_get_course_completion_status",
            courseid=courseid,
            userid=userid,
        )

    def activities_completion(self, courseid: int, userid: int) -> Any:
        return self.call(
            "core_completion_get_activities_completion_status",
            courseid=courseid,
            userid=userid,
        )

    def grade_items(self, courseid: int, userid: int) -> Any:
        return self.call(
            "gradereport_user_get_grade_items",
            courseid=courseid,
            userid=userid,
        )

    def customcerts_by_courses(self, courseids: Sequence[int]) -> Any:
        return self.call(
            "mod_customcert_get_customcerts_by_courses",
            courseids=[int(i) for i in courseids],
        )

    def list_cert_issues(
        self,
        *,
        customcertid: int | None = None,
        userid: int | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> Any:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if customcertid is not None:
            params["customcertid"] = customcertid
        if userid is not None:
            params["userid"] = userid
        return self.call("mod_customcert_list_issues", **params)


def aggregate_enrolled(data: Any) -> dict[str, Any]:
    users = data if isinstance(data, list) else []
    return {"enrolled_user_count": len(users)}


def aggregate_completion(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = 0
    for row in rows:
        status = row.get("completion", row)
        if isinstance(status, dict):
            if status.get("completed") or status.get("isoverallcomplete"):
                completed += 1
        elif row.get("completed"):
            completed += 1
    return {
        "learners_with_completion_checked": len(rows),
        "learners_marked_complete": completed,
    }


def aggregate_grades(rows: list[dict[str, Any]]) -> dict[str, Any]:
    with_grades = sum(1 for r in rows if r.get("gradeitems") or r.get("usergrades"))
    return {"learners_with_grade_payload": with_grades, "learners_total": len(rows)}


def aggregate_certs(data: Any) -> dict[str, Any]:
    if isinstance(data, list):
        return {"certificate_issue_count": len(data)}
    if isinstance(data, dict) and "issues" in data:
        issues = data["issues"]
        return {"certificate_issue_count": len(issues) if isinstance(issues, list) else 0}
    return {"certificate_issue_count": 0}


def write_json(path: Path, payload: Any, *, include_pii: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if include_pii:
        path.chmod(0o600)


def emit_stdout(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def collect_completion_for_course(client: MoodleClient, courseid: int) -> list[dict[str, Any]]:
    enrolled = client.enrolled_users(courseid)
    if not isinstance(enrolled, list):
        return []
    rows: list[dict[str, Any]] = []
    for user in enrolled:
        uid = user.get("id")
        if uid is None:
            continue
        try:
            status = client.course_completion(courseid, int(uid))
        except MoodleROError:
            status = {"error": "completion_unavailable"}
        rows.append({"userid": uid, "completion": status})
    return rows


def collect_grades_for_course(client: MoodleClient, courseid: int) -> list[dict[str, Any]]:
    enrolled = client.enrolled_users(courseid)
    if not isinstance(enrolled, list):
        return []
    rows: list[dict[str, Any]] = []
    for user in enrolled:
        uid = user.get("id")
        if uid is None:
            continue
        try:
            grades = client.grade_items(courseid, int(uid))
        except MoodleROError:
            grades = {"error": "grades_unavailable"}
        rows.append({"userid": uid, "grades": grades})
    return rows


def fetch_certs_for_course(client: MoodleClient, courseid: int) -> tuple[Any, str]:
    """
    Return certificate data and a note describing which WS path was used.
    """
    try:
        data = client.customcerts_by_courses([courseid])
        return data, "mod_customcert_get_customcerts_by_courses"
    except MoodleROError as exc:
        msg = str(exc).lower()
        if "invalid parameter" in msg or "invalidrecord" in msg or "function" in msg:
            pass
        else:
            raise

    issues: list[Any] = []
    try:
        page = client.list_cert_issues(limit=500, offset=0)
        if isinstance(page, list):
            issues.extend(page)
    except MoodleROError:
        return (
            {
                "error": "certificates_unavailable",
                "fallback": (
                    "Use Moodle admin report export for customcert issues if "
                    "mod_customcert_list_issues is not enabled on the service."
                ),
            },
            "fallback_documented",
        )
    return issues, "mod_customcert_list_issues"


def cmd_site_info(client: MoodleClient, _args: argparse.Namespace) -> int:
    emit_stdout(client.site_info())
    return 0


def cmd_courses(client: MoodleClient, _args: argparse.Namespace) -> int:
    emit_stdout(client.courses())
    return 0


def cmd_enrolled(client: MoodleClient, args: argparse.Namespace) -> int:
    data = client.enrolled_users(args.courseid)
    if args.aggregate_only:
        emit_stdout(aggregate_enrolled(data))
    else:
        emit_stdout(data)
    return 0


def cmd_completion(client: MoodleClient, args: argparse.Namespace) -> int:
    rows = collect_completion_for_course(client, args.courseid)
    if args.aggregate_only:
        emit_stdout(aggregate_completion(rows))
    else:
        emit_stdout(rows)
    return 0


def cmd_grades(client: MoodleClient, args: argparse.Namespace) -> int:
    rows = collect_grades_for_course(client, args.courseid)
    if args.aggregate_only:
        emit_stdout(aggregate_grades(rows))
    else:
        emit_stdout(rows)
    return 0


def cmd_certs(client: MoodleClient, args: argparse.Namespace) -> int:
    data, source = fetch_certs_for_course(client, args.courseid)
    if args.aggregate_only:
        payload = aggregate_certs(data)
        payload["source_function"] = source
        emit_stdout(payload)
    else:
        emit_stdout({"source_function": source, "data": data})
    return 0


def cmd_snapshot(client: MoodleClient, args: argparse.Namespace) -> int:
    courseid = args.courseid
    include_pii = args.include_pii
    aggregate_only = not include_pii if args.aggregate_only is None else args.aggregate_only

    stamp = date.today().isoformat()
    out_dir = Path(args.output_dir) / stamp / str(courseid)
    out_dir.mkdir(parents=True, exist_ok=True)

    site = client.site_info()
    courses = client.courses()
    course_field = client.course_by_id(courseid)
    enrolled = client.enrolled_users(courseid)
    completion_rows = collect_completion_for_course(client, courseid)
    grade_rows = collect_grades_for_course(client, courseid)
    certs, cert_source = fetch_certs_for_course(client, courseid)

    write_json(out_dir / "site_info.json", site, include_pii=False)
    write_json(out_dir / "courses.json", courses, include_pii=False)
    write_json(out_dir / "course.json", course_field, include_pii=False)

    if aggregate_only:
        write_json(out_dir / "enrolled.json", aggregate_enrolled(enrolled), include_pii=False)
        write_json(
            out_dir / "completion.json",
            aggregate_completion(completion_rows),
            include_pii=False,
        )
        write_json(out_dir / "grades.json", aggregate_grades(grade_rows), include_pii=False)
        write_json(
            out_dir / "certs.json",
            {**aggregate_certs(certs), "source_function": cert_source},
            include_pii=False,
        )
    else:
        write_json(out_dir / "enrolled.json", enrolled, include_pii=True)
        write_json(out_dir / "completion.json", completion_rows, include_pii=True)
        write_json(out_dir / "grades.json", grade_rows, include_pii=True)
        write_json(
            out_dir / "certs.json",
            {"source_function": cert_source, "data": certs},
            include_pii=True,
        )

    summary_path = out_dir / "summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        writer.writerow(["courseid", courseid])
        writer.writerow(["snapshot_date", stamp])
        writer.writerow(["aggregate_only", aggregate_only])
        writer.writerow(["enrolled_user_count", aggregate_enrolled(enrolled)["enrolled_user_count"]])
        comp = aggregate_completion(completion_rows)
        writer.writerow(["learners_marked_complete", comp["learners_marked_complete"]])
        writer.writerow(
            ["learners_with_completion_checked", comp["learners_with_completion_checked"]]
        )
        gr = aggregate_grades(grade_rows)
        writer.writerow(["learners_with_grade_payload", gr["learners_with_grade_payload"]])
        cert_agg = aggregate_certs(certs)
        writer.writerow(["certificate_issue_count", cert_agg["certificate_issue_count"]])
        writer.writerow(["certs_source_function", cert_source])

    emit_stdout({"written_to": str(out_dir), "aggregate_only": aggregate_only})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only Moodle web services client (CleantechHUB Academy)."
    )
    parser.add_argument(
        "--rate-sleep",
        type=float,
        default=DEFAULT_RATE_SLEEP_S,
        help="Seconds to sleep between API calls (default: %(default)s)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_S,
        help="HTTP timeout seconds (default: %(default)s)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("site-info", help="Call core_webservice_get_site_info")

    sub.add_parser("courses", help="Call core_course_get_courses")

    p_enrolled = sub.add_parser("enrolled", help="Enrolled users for a course")
    p_enrolled.add_argument("courseid", type=int)
    _add_pii_flags(p_enrolled)

    p_completion = sub.add_parser("completion", help="Completion status per enrolled user")
    p_completion.add_argument("courseid", type=int)
    _add_pii_flags(p_completion)

    p_grades = sub.add_parser("grades", help="Grade items per enrolled user")
    p_grades.add_argument("courseid", type=int)
    _add_pii_flags(p_grades)

    p_certs = sub.add_parser("certs", help="Certificate metadata/issues for a course")
    p_certs.add_argument("courseid", type=int)
    _add_pii_flags(p_certs)

    p_snap = sub.add_parser("snapshot", help="Write JSON/CSV bundle under out/<date>/<courseid>/")
    p_snap.add_argument("courseid", type=int)
    p_snap.add_argument(
        "--output-dir",
        default="out",
        help="Base output directory (default: out)",
    )
    p_snap.add_argument(
        "--aggregate-only",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write counts only (default: true). Use --no-aggregate-only with --include-pii for rows.",
    )
    p_snap.add_argument(
        "--include-pii",
        action="store_true",
        help="Include identifiable user rows in snapshot files (mode 0600).",
    )

    return parser


def _add_pii_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--include-pii",
        action="store_true",
        help="Emit full Moodle payloads (may contain personal data). Default is aggregate counts only.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "snapshot":
        args.aggregate_only = not args.include_pii if args.include_pii else args.aggregate_only
    else:
        args.aggregate_only = not getattr(args, "include_pii", False)

    try:
        base_url, token = load_config()
    except MoodleROError as exc:
        print(redact_secrets(str(exc), None), file=sys.stderr)
        return 2

    client = MoodleClient(
        base_url=base_url,
        token=token,
        rate_sleep_s=args.rate_sleep,
        timeout_s=args.timeout,
    )

    handlers: dict[str, Callable[[MoodleClient, argparse.Namespace], int]] = {
        "site-info": cmd_site_info,
        "courses": cmd_courses,
        "enrolled": cmd_enrolled,
        "completion": cmd_completion,
        "grades": cmd_grades,
        "certs": cmd_certs,
        "snapshot": cmd_snapshot,
    }

    try:
        return handlers[args.command](client, args)
    except MoodleROError as exc:
        print(redact_secrets(str(exc), token), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
