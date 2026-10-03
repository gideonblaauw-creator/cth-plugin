# Wire diagram

**Harness lane map** — who asked, who routed, which desk owns work, where Cloud Hands runs, and which tools touch data. Wire specs are YAML; the callable renderer produces offline-safe HTML+SVG (no Google Fonts).

## When to use

- Team reports across **Gideon → Orchestrator → Desks → Hands → Tools**
- Automation/data-flow sketches (e.g. n8n on the VPS)
- **Before/after** policy or architecture shifts (`layout: before-after`)

Do **not** use wire for dense architecture (use **Architecture**), time-ordered messages (**Sequence**), or executive charts.

## Spec v1 (YAML)

| Field | Required | Notes |
|---|---|---|
| `wire` | yes | Must be `1` |
| `id` | yes | Slug for output files (`<id>-wire.*`) |
| `title` | yes | Page `<h1>` and SVG `<title>` |
| `lang` | yes | `en`, `es`, or `en+es` |
| `layout` | yes | `lanes` (default swimlanes), `flow`, or `before-after` |
| `source` | no | Provenance line in SVG `<desc>` |
| `lanes` | no | Defaults to `gideon`, `orchestrator`, `desks`, `hands`, `tools` |
| `nodes[]` | yes | `id`, `lane`, `label`, `status`, optional `ref`, `note` |
| `edges[]` | yes | `from`, `to`, `kind` (`ask`, `ticket`, `hitl`, `data`), optional `label` |

**Status** uses wire-only tokens in [`style-guide.md`](style-guide.md#wire-status-tokens-status-only) — always pair color with the shape cue.

**Split:** more than 12 nodes → one **overview** frame (counts per lane) plus one **detail** frame per lane that has nodes, stacked in a single SVG/HTML export.

## Callable tool

From the skill directory:

```bash
python3 scripts/wire.py fixtures/wire/team-report-wire.yaml --out /tmp/wire-out --html --svg --md --png
python3 scripts/validate_spec.py fixtures/wire/*.yaml
```

Outputs: `<id>-wire.html`, `<id>-wire.svg`, `<id>-wire.md`, `<id>-wire.png` (PNG via Playwright Chromium, scale 2, solid `#B2EEFA` paper).

Fonts ship under `assets/fonts/wire/` (OFL, vendored woff2) — wire HTML never links Google Fonts.

## Validation rules

- Unique node `id` values
- Every `edges[].from` / `to` resolves to a node
- Every `nodes[].lane` appears in `lanes` (or the default lane list)

Schema: [`schemas/wire.schema.json`](../schemas/wire.schema.json).

## Layout notes

- **lanes:** default harness swimlanes; orthogonal connectors between nodes.
- **flow:** vertical stack (good for pipelines such as n8n).
- **before-after:** first/last lane columns (set `lanes: [before, after]`).

See [`assets/template-wire.html`](../assets/template-wire.html) for the static shell; the renderer fills the SVG body.
