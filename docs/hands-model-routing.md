# Hands model routing (Gideon lock t1263u — 2026-09-13)

**BUILDING = Composer 2.5 Fast ON.**

Canonical lock for Cloud Hands model fill-in. Playbook surfaces: `skills/harness/SKILL.md` §5 (Token lock + BUILDING lock), `tickets/TEMPLATE.md`, desk comms skills §5.

**Supersedes** t1242u (2026-09-12) and the 2026-08-26 default that repo/code Hands must use `composer-2.5` with `fast=false`. Repo/code **builds** launch **Fast ON** only. No silent swap back to Fast off.

## Explicit build surfaces

Includes but is not limited to:

- Repo / code on Lane A (`lane: github-pr`)
- LangGraph lane (`langgraph: yes`) and Lane A product apps
- **Signal Radar**, **LexiScan**, **scanner** (e.g. `cth-data-room-scanner`)
- Harness code (`skills/harness/`, `tickets/`, desk routing in `*-comms` skills)
- Skill plant, app graph, infrastructure playbook edits on owning repos

## Fill-in table

| Job class | Ticket signal | Model | Empty `model:` fill-in |
|---|---|---|---|
| Mechanical / tiny | Pack writes, inventories, copy grind, research grind, unspecified mechanical | `gemini-3.7-flash` | Yes — empty **mechanical** ticket only |
| Repo / code / build | Lane A PR, app, graph, skill plant, `langgraph: yes`, Signal Radar, LexiScan, scanner, harness | `composer-2.5` (`fast=true`) | Yes — empty **build** ticket (do **not** default to Flash) |
| Review / eval / brand | No model named | — | **HOLD** — flag Gideon (no auto-Sonnet/Opus/Grok) |
| Private residency | Must stay on 127.0.0.1 | local Ollama `LFM2.5-VL-3B` | Private overrides Flash and Composer |

## Rules

1. **Mechanical/tiny stays Flash** when the Desk names it — or when the ticket is clearly mechanical and `model:` is empty.
2. **Builds use Composer Fast ON** — ticket `model: composer-2.5 (fast=true)` or omit `model:` on a repo/code/build ticket → launch Fast ON.
3. **No Flash-as-default for builds** — an empty Lane A / repo / graph ticket is a **build**, not mechanical. Do not fill Flash.
4. **Never silently launch a build with Fast off** — do not default builds to `fast=false`, omit Fast, or swap Fast ON → Fast off without Gideon/Infra approval. HITL: no silent model swap to Fast off.
5. **Composer Fast on pack writes is still a miss** — remap pack tickets that name Composer Fast to `gemini-3.7-flash`.
6. **High-tier HOLD** — Sonnet, Opus, Haiku, Fable, Sol, Grok, second cloud Kimi, Muse Spark 1.2 Contributor → HOLD and flag Gideon unless the ticket explicitly names an allowed model.
7. **Infisical unchanged** — secrets SoT stays Infisical; model routing does not change credential rules.

## Ticket `model` field

```
model: gemini-3.7-flash | composer-2.5 (fast=true)
```

| Written on ticket | Launch |
|---|---|
| `gemini-3.7-flash` | Flash (mechanical/tiny) |
| `composer-2.5 (fast=true)` or repo/code build with empty model | Composer 2.5 **Fast ON** |
| `composer-2.5 (fast=false)` on a **build** | **Miss** — remap to `fast=true` (t1263u) and flag |
| Silent Fast off on a build | **Miss** — remap to `fast=true` (t1263u) and flag |
| Review/eval/brand, no model | HOLD |

## Historical note

Token lock **2026-08-26** remains in `skills/harness/SKILL.md` for Grok coordination-only, mechanical Flash, and forbidden high-tier fill-in. **t1242u** (2026-09-12) first planted BUILDING = Fast ON. **t1263u** (2026-09-13) hardens the lock: explicit build surfaces (Signal Radar, LexiScan, scanner, harness), no silent Fast-off defaults, and remap + flag on any build miss.
