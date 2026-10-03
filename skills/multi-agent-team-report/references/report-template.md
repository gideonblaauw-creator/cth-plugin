# Team report template

Copy and fill. Keep filenames in one folder: `<report>.md`, `spec.yaml`, and wire exports from `wire.py`.

```markdown
# Multi-agent team report — <title>

**Date:** YYYY-MM-DD  
**Tier:** 0  
**Source:** <ticket or Orchestrator ask>

## Summary

<One short paragraph — routing and outcomes.>

## Desks and tickets

| Desk | Active tickets | Status |
| --- | --- | --- |
| <Desk> | <ticket ref> | done / waiting / hold |

## Hands and verifiers

- **Cloud Hands:** <branch or PR ref>
- **Verifiers:** <pytest, fixture, or n8n-li note>

## Wire diagram

Spec: `spec.yaml` (wire v1, validated with `validate_spec.py`).

![Harness wire map](./<id>-wire.png)

Rendered with:

`python3 skills/diagram-design/scripts/wire.py spec.yaml --out . --png --svg --html --md`

## Locks and unknowns

- **Locks:** <decisions already fixed>
- **Unknown:** <gaps not stated in source>
```

Replace `<id>` with the `id:` field from `spec.yaml`.
