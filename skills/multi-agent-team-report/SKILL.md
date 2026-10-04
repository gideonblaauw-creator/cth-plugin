---
name: multi-agent-team-report
description: >
  Writes harness multi-agent team reports (Markdown) with a Wire diagram section.
  Use when: team report, weekly harness report, Orchestrator desk status, or
  Gideon → Desks → Hands routing summary. Do not use when: loose wire-diagram
  asks (wire-brief first), grant packs (cth-grant), or hand-drawn architecture
  figures (diagram-design HTML+SVG types).
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
  owner: Infrastructure desk
---

# Multi-agent team report

**Output:** one Markdown report plus a **wire spec YAML** and renderer exports in the **same folder**.

**Do not** draw wire maps with PIL, Matplotlib, or ad-hoc canvas scripts. The **Wire diagram** section is always produced by `skills/diagram-design/scripts/wire.py`.

## Workflow

1. **Collect facts** — Tickets, desk owners, Hands status, tool touchpoints. No invented bc-ids or URLs; mark gaps explicitly.
2. **Draft report MD** — Use `references/report-template.md`. Include all required sections; the **Wire diagram** section links to rendered assets (see step 4).
3. **Write wire spec** — Save `spec.yaml` in the **same directory** as the report MD (sibling file). Schema: `skills/diagram-design/schemas/wire.schema.json`. Map actors to harness lanes (`gideon`, `orchestrator`, `desks`, `hands`, `tools`). Example shape: `skills/diagram-design/fixtures/wire/team-report-wire.yaml`.
4. **Render wire diagram** — From repo root:

```bash
python3 skills/diagram-design/scripts/validate_spec.py path/to/spec.yaml
python3 skills/diagram-design/scripts/wire.py path/to/spec.yaml \
  --out path/to/ \
  --png --svg --html --md
```

Replace `path/to/` with the report folder. Outputs land beside the report: `<id>-wire.png`, `<id>-wire.svg`, `<id>-wire.html`, `<id>-wire.md` (id from spec `id:` field).

5. **Wire diagram section** — In the team report MD, link the PNG (and optional SVG) relative to the report path. State the spec path: `` `spec.yaml` `` (or the actual filename if the ticket names a different stem).

Done when: report MD is complete, `spec.yaml` validates, `wire.py` exports exist, and the **Wire diagram** section references them.

## Rules

- **Amber and red** in wire output are **status-only** (see `skills/diagram-design/references/style-guide.md`).
- Tier **0** by default — no Understanding Lab CTA unless the ticket sets `tier: 1` or `tier: 2`.
- Public-voice excerpts inside the report: mark **Awaiting Gideon's approval** per `CLAUDE.md`.

## Related skills

| Skill | When instead |
|-------|----------------|
| `wire-brief` | Loose EN/ES ask before any diagram or derived MD |
| `diagram-design` | Non-wire presentation diagrams (architecture, data-flow HTML+SVG) |
| `harness` | Ticket contract, lanes, Hands routing |

## References

- `references/report-template.md` — Report MD skeleton including **Wire diagram**
- `skills/diagram-design/references/type-wire.md` — Wire spec fields and layouts
