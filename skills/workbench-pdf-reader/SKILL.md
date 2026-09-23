---
name: workbench-pdf-reader
description: >
  Dedicated PDF keyword search and snippet extract for grants and research via
  pdfgrep. Use when: PDF keyword search, PDF snippet extract, grant PDF grep,
  research PDF search, Archive PDF path search. Do not use when: ad-hoc pdfgrep
  one-liners in chat, HTML-to-PDF export (html-to-pdf), or OCR/scanned PDFs
  without a text layer.
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
  owner: Infrastructure desk
  adopted: "2026-09-23"
compatibility: Requires pdfgrep and poppler-utils (pdftotext) on the host running the script.
---

# Workbench PDF reader (pdfgrep)

**Owner:** Infrastructure desk  
**Tool type:** Harness script (not a Workbench channel)  
**Entry point:** `scripts/workbench-pdf-read.sh`  
**Runbook:** `docs/workbench-pdf-reader.md`

Desks and Cloud Hands use this skill to search PDFs on the VPS Archive (`/opt/claude-files/…`) or local checkouts. **Never** run ad-hoc `pdfgrep` one-liners as the protocol — invoke the script.

## When to use

| Need | Action |
|---|---|
| Find a keyword or regex in a grant PDF | Search mode with `--pattern` or positional pattern |
| Pull surrounding lines for a hit | Search with `--context N` (pdftotext + grep fallback) |
| Dump full text to a writable path | `--extract /path/out.txt` (pdftotext) |
| Smoke / CI | Fixture at `scripts/fixtures/sample-grant-fixture.pdf` |

## Workflow

1. **Resolve path** — VPS Archive path from ticket `folder:` or absolute path on box. Do not copy Archive PDFs into this repo unless the ticket says so.
2. **Invoke the script** — from repo root or with absolute path to the script:

```bash
./scripts/workbench-pdf-read.sh "/path/to/document.pdf" "search pattern"
```

3. **Read structured output** — header (`file`, `mode`, `pattern`) then matches as `page:line` (pdfgrep) or grep line numbers (context mode).
4. **Ticket back** — paste match snippets and page numbers into the Desk pack or PR; do not paraphrase missing pages as found.

Done when: operator has page-scoped snippets or an extract file, and exit code reflects match/no-match.

## Script reference

```bash
# Keyword search (default)
./scripts/workbench-pdf-read.sh report.pdf "blended finance"

# Case-insensitive + context (fallback path)
./scripts/workbench-pdf-read.sh report.pdf --pattern "grant" -i -C 2

# Full-text extract
./scripts/workbench-pdf-read.sh report.pdf --extract /tmp/report.txt

# Fixture smoke
./scripts/workbench-pdf-read.sh scripts/fixtures/sample-grant-fixture.pdf "CleantechHUB"
```

### Flags (pass-through to pdfgrep unless noted)

| Flag | Effect |
|---|---|
| `-i`, `--ignore-case` | Case-insensitive |
| `-n`, `--page-number` | Page prefix on matches |
| `-H`, `--with-filename` | File name prefix |
| `-c`, `--count` | Match count only |
| `-m NUM`, `--max-count` | Cap matches per file |
| `-P`, `--perl-regexp` | PCRE regex |
| `-C NUM`, `--context` | **Fallback:** pdftotext + grep (pdfgrep has no native context) |
| `--extract PATH` | Full text via **pdftotext** (search flags ignored) |

## Errors

| Exit | Cause |
|---|---|
| Non-zero | `pdfgrep`/`pdftotext` missing, bad PDF path, no matches (search), or grep/pdfgrep failure |
| Message | Script prints `workbench-pdf-read: …` on stderr with install pointer to runbook |

## Install (operators — not deployed by Hands)

Document only. Gideon installs on VPS/box after merge. See `docs/workbench-pdf-reader.md`.

## Do not use when

- **HTML → PDF** → `skills/html-to-pdf/SKILL.md`
- **Scanned PDFs / no text layer** → OCR pipeline (out of scope; flag Desk)
- **Raw pdfgrep in chat** → use this script
- **Nexus/Datalab pack content** → separate tickets; this skill is tooling only

## Related skills

| Skill | When instead |
|---|---|
| `harness` | Ticket lanes, Hands routing, Archive SoT |
| `html-to-pdf` | Create PDFs from HTML artifacts |
| `cth-grant` | Grant lifecycle content — use this skill only to search source PDFs |
| `google-drive` | Fetch PDF from Drive before local search |

## References

- `docs/workbench-pdf-reader.md` — install, VPS examples, smoke command
- `scripts/workbench-pdf-read.sh` — CLI implementation
- `scripts/fixtures/sample-grant-fixture.pdf` — CI/box smoke PDF
