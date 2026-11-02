# Skill eval runner

Procedure for weekly (or ad-hoc) checks that Cloud Hands outputs still follow each skill playbook.

## Roles

| Role | Who | Job |
|------|-----|-----|
| **Maker** | Cloud Hands (or local agent with the target `skills/<name>/SKILL.md` loaded) | Runs each prompt in `prompts.jsonl` and saves raw outputs under `evals/results/raw/<date>/<skill>/`. |
| **Judge** | A **different** model from the maker (read-only; no file writes except the score file) | Scores each output against `rubric.md` (0–2 per criterion; sum and note fails). |
| **Recorder** | Human or Orchestrator | Appends the summary to `evals/results/<date>.md`. |

Maker ≠ judge. Do not score your own draft.

## One skill, one pass

1. Read the skill source named in that folder's `README.md` (canonical `skills/<name>/SKILL.md` on `main`, or the documented branch until merged).
2. Load `evals/<skill>/rubric.md` and `evals/<skill>/prompts.jsonl`.
3. For each JSONL row, run the maker with the row's `prompt` and the skill playbook in context.
4. Store each maker output as `evals/results/raw/<YYYY-MM-DD>/<skill>/<id>.md` (or `.html` when the prompt asks for HTML).
5. Pass the output + rubric + row `must_have` / `must_not` to the judge. Judge returns a short table: criterion id, score, one-line note.
6. Append to `evals/results/<YYYY-MM-DD>.md`:
   - skill name, prompt id, pass/fail on must-have/must-not gates, rubric total, judge model id, maker model id, link or path to raw output.

## Pass / fail gates

Before rubric scoring, the judge checks each prompt's `must_have` and `must_not` lists (binary). Any must-not hit or missing must-have → **FAIL** for that prompt regardless of rubric total.

## Weekly Monday run (proposal only — no scheduler in repo)

**Cron (UTC, adjust for Bogotá if the host uses local time):**

```cron
0 14 * * 1 cd /path/to/cth-plugin && ./evals/run-weekly.sh >> /var/log/cth-skill-evals.log 2>&1
```

`14:00 UTC Monday` ≈ `09:00 COT`. Change the path to the clone on the runner host.

**Manual steps (same as cron would invoke):**

1. `git fetch origin main && git checkout main && git pull --ff-only origin main`
2. Set `EVAL_DATE=$(date -u +%Y-%m-%d)` and `MAKER_MODEL=composer-2.5-fast` / `JUDGE_MODEL=<read-only checker model per harness>`
3. For each folder under `evals/` except `results/` and files at eval root: run the maker/judge loop above.
4. Write or append `evals/results/$EVAL_DATE.md` with a one-page executive summary (counts pass/fail per skill).
5. If any FAIL on a client-facing skill (`cleantechhub-brand`, `linkedin-posts`, `cth-html-deck-visual`), open a Desk ticket — do not auto-fix in the eval job.
6. Commit only `evals/results/<date>.md` (and raw outputs if policy allows); skill rubrics/prompts change via normal PR.

Optional helper script `evals/run-weekly.sh` is **not** included in this PR; operators can add it when wiring cron on the VPS or a CI worker.

## Constraints (harness-aligned)

- Do not read source files over **200 KB** inside a single eval job; use grep/hash for large decks.
- Cap each maker job at about **60 steps**; split long skills across weeks.
- No secrets, tokens, or live LinkedIn publish in eval runs — drafts only.
- REIN Hubs dollar amounts must never appear in deck eval fixtures.
