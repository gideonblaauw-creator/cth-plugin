# Legal eval — severity rubric

Canonical enum for Hands findings: **`blocker` | `negotiate` | `accept` | `info` | `unknown`**

Do not invent alternate metrics or numeric scores in counterparty-facing output.

## Definitions

| Severity | When to use | Done when |
|---|---|---|
| `blocker` | Hard stop; withhold signature/send; counsel likely | Hard-stop rule cited; HITL ask explicit |
| `negotiate` | Material gap vs preferred playbook; needs redline or approved fallback | Named fallback or redline suggestion |
| `accept` | Matches preferred or approved fallback | One-line rationale |
| `info` | Desk awareness; no material block | `[INTERNAL]` unless externally safe |
| `unknown` | Text ambiguous or citation missing | No invented law; escalate question |

## Hard stops (always `blocker`)

1. **Uncapped liability** — no cap, or cap stated as unlimited.
2. **Preexisting IP assignment to counterparty** — background IP or tools assigned away without carve-out.
3. **Silent auto-renew >12 months without notice** — renewal without adequate notice period.
4. **Unknown governing law** — missing, contradictory, or not extractable with citation.
5. **Missing citation / no approved fallback** — cite-or-stop failure; cannot compare to library.

## Mode interaction

| review_mode | Typical routing |
|---|---|
| `strict` | Ambiguity → `negotiate` or `blocker`; prefer withhold/escalate |
| `moderate` | Material gaps → `negotiate`; minor → `accept` or `info` |
| `loose` | Exploratory only; never signature path |

## Desk coarse map (reporting only)

| Canonical | Coarse alias |
|---|---|
| `blocker` | `critical` |
| `negotiate` (material) | `high` |
| `negotiate` (minor) | `medium` |
| `accept` | `medium` (conditional) |
| `info` | `low` / `note` |
| `unknown` | `high` until resolved |

## Firewall by severity

- `blocker`, `negotiate`, `unknown` details → default **`[INTERNAL]`** in memo; external redlines state issue without playbook YAML or scores.
- `accept`, `info` → may appear **`[EXTERNAL]`** only when counterparty-safe.
