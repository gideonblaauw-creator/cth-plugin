# Moodle read-only client (Academy)

Small Python CLI/library for **read-only** snapshots from `academy.cleantechhub.net` via Moodle REST web services. CleantechHUB Cloud Hands use this for reporting; merge and deploy are human-in-the-loop (Gideon).

## Requirements

- Python 3.11+
- `requests` (see `requirements.txt`)
- Infisical CLI authenticated for project **cth-agents** (`c84fe8b3-d64e-485a-82d7-250dc57a6453`)

## Configuration (no secrets in repo)

At runtime the client reads:

| Variable | Source |
|----------|--------|
| `MOODLE_URL` | Infisical `cth-agents` or process env when injected by `infisical run` |
| `MOODLE_WS_TOKEN` | Same |

Example:

```bash
cd tools/moodle-ro
pip install -r requirements.txt
infisical run --projectId=c84fe8b3-d64e-485a-82d7-250dc57a6453 -- \
  python moodle_ro.py site-info
```

Do **not** commit tokens, `.env` files, or paste secrets into logs, argv, or JSON output. Exceptions redact `wstoken` values.

## Allowlisted web service functions

Only these `wsfunction` names are permitted (hard-coded):

| Function | Purpose |
|----------|---------|
| `core_webservice_get_site_info` | Site metadata |
| `core_course_get_courses` | Course list |
| `core_course_get_courses_by_field` | Single course lookup |
| `core_enrol_get_enrolled_users` | Enrollees |
| `core_completion_get_course_completion_status` | Per-user course completion |
| `core_completion_get_activities_completion_status` | Activity completion (available on client; snapshot uses course completion loop) |
| `gradereport_user_get_grade_items` | Per-user grades |
| `mod_customcert_get_customcerts_by_courses` | **Unverified upstream** — not present in [mdjnelson/moodle-mod_customcert](https://github.com/mdjnelson/moodle-mod_customcert) `db/services.php` on `main`; kept for site-specific/mobile variants |
| `mod_customcert_list_issues` | Issued certificates (upstream `main`, PR #644) |

If `mod_customcert_list_issues` is unavailable on the external service, use Moodle admin **report export** for certificate issues (documented fallback in `certs` / `snapshot`).

## Commands

```bash
python moodle_ro.py site-info
python moodle_ro.py courses
python moodle_ro.py enrolled <courseid>            # counts by default
python moodle_ro.py enrolled <courseid> --include-pii
python moodle_ro.py completion <courseid>
python moodle_ro.py grades <courseid>
python moodle_ro.py certs <courseid>
python moodle_ro.py snapshot <courseid>              # out/<YYYY-MM-DD>/<courseid>/
python moodle_ro.py snapshot <courseid> --include-pii --no-aggregate-only
```

HTTP: `POST` to `<MOODLE_URL>/webservice/rest/server.php` with `wstoken`, `wsfunction`, `moodlewsrestformat=json`. Moodle exception JSON is surfaced as errors. Simple sleep between calls; timeouts; retries on HTTP 5xx only.

## Personal data (Ley 1581 / habeas data)

Colombia **Ley 1581 de 2012** treats personal data under habeas data rules. By default, **`snapshot` uses aggregate counts only** (`--aggregate-only`, default ON). Full user rows require **`--include-pii`**; those files are written with **`0600`** permissions. Treat exports as confidential; limit retention and access on the VPS.

## Tests (offline)

```bash
cd tools/moodle-ro
python -m unittest discover -s tests -v
```

Tests mock HTTP; they do **not** call the live Academy site.

## Sample config

See `config.example.yaml` (URL placeholder only).
