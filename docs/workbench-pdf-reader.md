# Workbench PDF reader — operator runbook

Short runbook for Desks and Cloud Hands. Skill: `skills/workbench-pdf-reader/SKILL.md`. CLI: `scripts/workbench-pdf-read.sh`.

## Install pdfgrep

Hands **document only** — Gideon installs on VPS/box after merge. No deploy from agent runs.

### Debian / Ubuntu (OVH VPS, Linux boxes)

```bash
sudo apt update
sudo apt install -y pdfgrep poppler-utils
pdfgrep --version
pdftotext -v
```

- **pdfgrep** — keyword search inside PDFs  
- **poppler-utils** — provides **pdftotext** for full extract and `--context` fallback

### macOS (Gideon's Air / dev box)

```bash
brew install pdfgrep poppler
pdfgrep --version
pdftotext -v
```

## Quick check

From repo root after install:

```bash
chmod +x scripts/workbench-pdf-read.sh
./scripts/workbench-pdf-read.sh scripts/fixtures/sample-grant-fixture.pdf "CleantechHUB"
```

Expected: exit `0`, header `mode: search (pdfgrep)`, snippet containing `CleantechHUB grant research fixture`.

## Example invocations

### Archive PDF on VPS

```bash
cd /path/to/cth-plugin   # or use absolute script path
./scripts/workbench-pdf-read.sh \
  "/opt/claude-files/Projects/Nexus/blended-finance-colombia-un/2026-09-23/<file>.pdf" \
  "blended finance"
```

If that folder is not present yet, use the repo fixture for smoke only — do not invent Nexus pack files.

### Case-insensitive search with context

```bash
./scripts/workbench-pdf-read.sh grant.pdf --pattern "theory of change" -i -C 2
```

`--context` uses **pdftotext + grep** (pdfgrep has no `-C`).

### Full-text extract

```bash
./scripts/workbench-pdf-read.sh grant.pdf --extract /tmp/grant.txt
wc -l /tmp/grant.txt
```

Extract method: **pdftotext -layout** (documented fallback; search prefers **pdfgrep**).

## Smoke (CI / agent acceptance)

```bash
./scripts/workbench-pdf-read.sh scripts/fixtures/sample-grant-fixture.pdf "blended finance"
```

Sample output:

```
=== workbench-pdf-read v1.0.0 ===
file: scripts/fixtures/sample-grant-fixture.pdf
mode: search (pdfgrep)
pattern: blended finance
---
1:Keyword: blended finance Colombia UN
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pdfgrep not found` | Install packages above |
| `PDF not found` | Check Archive path; quote paths with spaces |
| No matches, exit 1 | Pattern typo or scanned PDF (no text layer) |
| `Output directory does not exist` | Create parent dir before `--extract` |

## Related

- Harness tool — not a Workbench channel (`skills/harness/SKILL.md`)
- Do not merge/deploy from Hands tickets; open PR on `cth-plugin` Lane A
