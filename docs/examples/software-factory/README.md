# Software Factory Ship CI — workflow templates

**Copy into Lane A product repos** on the next `factory: yes` build. Do not enable from `cth-plugin` alone.

Canonical doc: `docs/software-factory-ship-ci.md`

## Files

| File | Destination in product repo |
|---|---|
| `pr-agent.yml` | `.github/workflows/pr-agent.yml` |
| `visual-ci.yml` | `.github/workflows/visual-ci.yml` |

## Before first run

1. Plant GitHub Actions secrets from Infisical (names only in tickets): `OPENAI_API_KEY`, `ARGOS_TOKEN`.
2. Set per-product `BASE_URL` / preview URL — **[PENDIENTE]** until each repo defines it (repo variable or workflow input).
3. Add Playwright tests under `tests/` or `e2e/` in the product repo (this template assumes `npx playwright test`).

## Hands auto-loop

After opening the draft PR, wait for PR-Agent + visual CI. Fix and re-push until green and comments resolved, then ping Infra PASS.
