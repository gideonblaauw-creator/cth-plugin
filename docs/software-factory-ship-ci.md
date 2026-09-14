# Software Factory Ship CI (Gideon lock t267u)

**One-liner:** Factory step 4 Ship runs **PR-Agent** (plain-English review) plus **visual before/after CI** (Playwright + Argos or Lost Pixel) on Lane A product repos — not org-wide from `cth-plugin` alone.

**Parent:** `docs/software-factory.md` § Ship  
**Templates:** `docs/examples/software-factory/` — copy into owning product repos on the next factory build  
**Skill:** `skills/software-factory/SKILL.md` § Ship auto-loop

---

## What Ship CI adds (step 4)

| Layer | Tool | What it proves |
|---|---|---|
| **PR-Agent** | [Codium-ai/pr-agent](https://github.com/Codium-ai/pr-agent) / [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) (Qodo) | `/describe`, plain-English walkthrough, `/ask` on PR comments. AI review loop on the PR. |
| **Visual before/after CI** | Playwright (screenshots/video) + [Argos CI](https://argos-ci.com) or [Lost Pixel](https://lost-pixel.com) | Pixel-level before/after diffs posted on the PR. AI reviewers do not see pixels — this is the **Mic Prove** surface in CI. |

**Eng Prove (step 3) unchanged:** pytest + smoke always. Hands **before/after** in the PR for UI/behavior PRs. Visual CI **supplements** Hands evidence — it does not replace pytest/smoke.

---

## Auto-loop (Hands)

On PR-Agent fail, visual CI fail, or open review comments:

1. Hands reads PR-Agent summary and visual diff comments.
2. Hands replies on the PR, fixes on the branch, pushes.
3. Re-runs **Prove(eng)** (pytest + smoke; refresh Hands before/after when UI changed).
4. Waits for PR-Agent + visual CI to go green and review threads to resolve.
5. **Only then** pings Infrastructure for step 4 **Infra PASS**.

Do **not** send Gideon to Understanding Lab (step 5) until the auto-loop clears **and** Infra PASS.

---

## Template placement (this repo)

`cth-plugin` ships **reference templates only**. Hands copies them into the **owning Lane A product repo** when that repo adopts factory Ship CI — typically on the first `factory: yes` build after t267u.

| Template | Copy to (product repo) |
|---|---|
| `docs/examples/software-factory/pr-agent.yml` | `.github/workflows/pr-agent.yml` |
| `docs/examples/software-factory/visual-ci.yml` | `.github/workflows/visual-ci.yml` |

**Do not** enable these workflows org-wide from `cth-plugin` alone. This harness repo is content-only — no product deploy surface.

**Non-goals for the planting PR:** do not install workflows on Signal Radar, scanner, or LexiScan in the same PR unless a separate ticket targets that repo. Templates + this doc are sufficient for the lock.

---

## Secrets (names only — never paste values)

Store provider keys in **Infisical**; sync to GitHub Actions secrets on the **product repo** (not in `cth-plugin`).

| Secret / var | Purpose |
|---|---|
| `OPENAI_API_KEY` | PR-Agent default provider (or equivalent — see PR-Agent docs for `ANTHROPIC_API_KEY`, Azure, etc.) |
| `GITHUB_TOKEN` | Provided by Actions; PR-Agent uses for PR comments |
| `ARGOS_TOKEN` | Argos CI upload (if using Argos) |
| `LOST_PIXEL_API_KEY` | Lost Pixel (if using Lost Pixel instead of Argos) |

Ticket Hands with **Infisical project / environment / key name** only. Never commit token values. See `skills/infisical/SKILL.md`.

---

## Per-product configuration **[PENDIENTE]**

Each Lane A product repo must plant its own preview/base URL before visual CI is meaningful:

| Variable | Purpose | Status |
|---|---|---|
| `BASE_URL` / `PREVIEW_URL` | Playwright target (Vercel preview, staging, or local server in CI) | **[PENDIENTE]** per product until Infra/Desk plants on that repo |
| Argos / Lost Pixel project id | Visual baseline project for that product | **[PENDIENTE]** per product |

Document the planted values in the product repo README or Infra runbook — not in this harness repo.

---

## Infrastructure PASS (step 4) — Ship CI checks

Before Infra PASS, confirm on the draft PR:

- [ ] PR-Agent ran and `/describe` (or equivalent) summary is present and addressed
- [ ] Open PR-Agent or review comments resolved (auto-loop complete)
- [ ] Visual CI green when the repo has UI surface (Playwright + Argos/Lost Pixel job passed or legitimately skipped with ticket note)
- [ ] pytest + smoke green (step 3)
- [ ] Hands before/after present on UI/behavior PRs (step 3 — not replaced by visual CI alone)

Full checklist: `skills/software-factory/SKILL.md` § Infrastructure PASS checklist.

---

## References

- PR-Agent: https://github.com/Codium-ai/pr-agent
- The-PR-Agent fork (Qodo): https://github.com/The-PR-Agent/pr-agent
- Playwright: https://playwright.dev
- Argos CI: https://argos-ci.com
- Lost Pixel: https://lost-pixel.com
- Factory conveyor: `docs/software-factory.md`
- Infra comms: `skills/infrastructure-comms/SKILL.md` § Software Factory
