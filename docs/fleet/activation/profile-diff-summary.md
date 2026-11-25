# Profile diff summary (activation B — not applied in Grok UI)

**Generated from:** `profile-snapshot-2026-11-25T1700.json` + `FLEET_REGISTRY.yaml`

## Counts

- Total profile changes: **93**
- Unchanged (skipped): **0**
- Conflicts (manual): **0**
- Registry bots missing from snapshot: **0**
- Snapshot ids not in registry: **0**

## Per batch

- Batch 1: 20 bots
- Batch 2: 20 bots
- Batch 3: 20 bots
- Batch 4: 20 bots
- Batch 5: 11 bots
- Batch 6: 2 bots

## Fleet line exceptions

- **`5dc64ea4` Orchestrator** — append-only line uses `parent Gideon Blaauw (HITL root)` (no `(null)`); registry `parent.id` is null / HITL.

## Conflicts

- None (resolved 25 Nov 2026): `fbc6f772` **Health** — parent **Control Tower · Infra** (`c656afb9`); registry aligned with profile Reports-to line; Fleet profile line appended 25 Nov.

**Last-batch pins:** `7ea170b4, d3d9dd60` share the final batch.

## Skipped unchanged

- None

## Snapshot ids not in registry

- None

## Byte-check

- All `new_description` values verified: `current.rstrip() + "\n" + fleet_line + "\n"`
