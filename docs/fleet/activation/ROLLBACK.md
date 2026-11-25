# Fleet activation rollback (A–D)

Use this if the activation PR must be undone without touching secrets or live credentials.

## 1. Revert the merge commit

On `cth-plugin` default branch:

```bash
git revert -m 1 <merge-commit-sha-of-activation-pr>
```

Push a revert PR; Gideon merges. That restores pre-activation `FLEET_REGISTRY.yaml`, `PROTOCOLS.md`, and activation docs.

## 2. Restore Grok Bot profiles

**Source of truth:** `docs/fleet/activation/profile-snapshot-2026-11-25T1700.json` (rollback snapshot copied verbatim at activation).

For each object in the snapshot:

| Field | Action |
| :--- | :--- |
| `id` | Match Grok agent UUID |
| `name` | Restore `name` |
| `description` | Restore `description` (removes Fleet line from activation B) |
| `title` | Restore if non-empty in snapshot |

Apply via Grok admin / approved profile-sync ticket. **Do not** paste secrets. Profiles were not auto-applied in the activation PR.

## 3. Weekly audit routine

- **Pause or delete** the Control Tower · Infra Monday **07:00 America/Bogota** routine that launches the read-only Hands audit job.
- Confirm no job runs `weekly_token_audit.py` with `--enforce` or `ENFORCE_APPROVED`.

## 4. Verify

- `FLEET_REGISTRY.yaml` `enforcement_default` is no longer `report_only` if fully rolled back to pre-activation tree.
- `PROTOCOLS.md` header returns to DRAFT or pre-GO text.
- Conflicted profiles (`profile-diff-summary.md`) need manual check after restore.