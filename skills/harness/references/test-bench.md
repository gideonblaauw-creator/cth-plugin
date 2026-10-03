# Harness test bench

**Script:** `skills/harness/test-bench.py`  
**Run:** `python3 skills/harness/test-bench.py`  
**Owner lock:** Gideon 2026-08-20 (lanes); aligned to **BUILDING t1263u** (Composer 2.5 **Fast ON**) on current `main`.

## What it checks

Dry/smoke PASS / FAIL / SKIP table across ten lanes. Maps to **`skills/harness/SKILL.md` §5** (Collaboration — Token lock, BUILDING model lock, OSS-first, media routing, private residency) and **§6** (machine-readable `skills/harness/references/skill-toolkit.json` inventory).

| Lane | §5 / §6 anchor |
|---|---|
| 1–4 | OpenRouter media bus (§5 media generation routing) |
| 5 | Private residency — local Ollama `LFM2.5-VL-3B` on 127.0.0.1 only |
| 6 | OSS-first coding default; OpenCode Go CF 1010 — no loop |
| 7 | **BUILDING lock:** repo/code/build Hands = `composer-2.5` (`fast=true`); not Fast off |
| 8–9 | Tools session (HeyGen presenter, Canva brand layouts) |
| 10 | Rulebook + `skill-toolkit.json` (§6) |

## Rules

- No client send/post/pay. No private payloads on cloud workers. No video weights download. No Muse Spark.
- `OPENROUTER_API_KEY` is not in cloud VMs by default — missing key → clean SKIPs, not invented tokens.
- Lane 5 on cloud VM: SKIP with instruction for worker `{type: machine, name: vps}`.

Canonical model fill-in: `docs/hands-model-routing.md`.
