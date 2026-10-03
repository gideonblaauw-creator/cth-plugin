---
name: wire-brief
description: >
  Converts loose EN/ES asks into an STE-80 English wire brief before diagrams,
  images, explainer video scripts, or derived MD. Use when: wire diagram,
  diagrama, explainer video, image from an ask, MD from voice or strategy input.
  Do not use when: final diagram render (diagram-design), grant prose (cth-grant),
  or client proposals (cth-proposal-build).
license: MIT
metadata:
  version: "1.0.0"
  category: operations
  owner: Infrastructure desk
---

# Wire brief (STE-80 intake)

**Gate:** Controlled-language intake runs **before** any CTH wire diagram, image, explainer video, or Markdown file derived from a loose ask.

**Reference standard:** ASD-STE100 *Simplified Technical English* (ASD). CTH uses a loose subset **STE-80** — not STE compliant. See `references/ste80.md`.

## When to use

| Trigger | Run wire-brief first |
|---------|----------------------|
| User says **wire diagram**, **diagrama**, or flow from an ask | Yes |
| Explainer video script from an ask | Yes |
| Image brief from an ask | Yes |
| MD explainer derived from voice or typed ask | Yes |

## Workflow

1. **Capture source** — Save the verbatim transcript (voice ASR or typed). Do not edit the source file.
2. **Draft brief** — Fill every section in the template below in **English**. Add the one-line **Spanish gloss** under each section heading.
3. **Lint** — `python3 skills/wire-brief/scripts/ste_lint.py path/to/brief.md`. Fix high-noise warnings; lint is warn-only.
4. **Fact check** — `python3 skills/wire-brief/scripts/fact_check.py source.txt brief.md`. Every number, date, URL, bc-id, and named entity from the source must appear in the brief or move to **UNKNOWN** with explicit “not stated”.
5. **G0 confirmation** — Show the brief to Gideon **only** when the ask is a **voice note** or a **strategy ask**. Paste **at most 10 lines** in chat (section headers count as lines). Wait for confirm or edits.
6. **Hand-off** — Emit `wire.yaml` for `skills/diagram-design/scripts/wire.py` (schema in parallel PR). The YAML carries GOAL, ACTORS, STEPS, STATUS, LOCKS, UNKNOWN, OUT OF SCOPE.

Done when: brief passes fact check, lint is run, G0 satisfied when required, and `wire.yaml` validates against the diagram-design schema.

## Brief template

Copy to `brief.md`. One English block per section; gloss line immediately under the heading.

```markdown
## GOAL
_Objetivo en una frase._
<One sentence: what artifact or outcome the ask requires.>

## ACTORS
_Quién participa._
- <Actor>: <role>

## STEPS
_Pasos numerados; sujeto-verbo-objeto._
1. <Actor> <verb> <object>.
2. <Actor> <verb> <object>.

## STATUS
_Estado actual conocido._
<Short factual status. Use UNKNOWN if not in source.>

## LOCKS
_Decisiones fijas._
- <Decision already locked>

## UNKNOWN
_Lo que el origen no dice; no inventar._
- <Gap explicitly not in transcript>

## OUT OF SCOPE
_Fuera de este brief._
- <Excluded work>
```

### STEPS rules

- Number each step.
- Pattern: **actor — verb — object**; **one action** per step.
- Max **20 words** per step sentence (STE-80 procedural limit).

## G0 rule

| Condition | G0 to Gideon |
|-----------|----------------|
| Voice note origin | **Required** |
| Strategy ask | **Required** |
| Typed tactical ask (non-strategy) | **Skip G0** — proceed after lint + fact check |

When G0 applies: show brief ≤ **10 lines** in chat; do not publish diagrams or MD until Gideon confirms.

## Hand-off: wire.yaml

After approval, map the brief to YAML for the diagram pipeline:

- Target script: `skills/diagram-design/scripts/wire.py`
- Schema: defined in the diagram-design skill (parallel PR); do not invent fields here.
- Keep STEPS order and actor names stable — the renderer uses them as node labels.

Example shape (illustrative only):

```yaml
goal: "<one sentence>"
actors:
  - name: Cloud Hands
    role: builds Lane A PR
steps:
  - actor: Gideon
    verb: confirm
    object: wire brief
status: draft
locks: []
unknown: []
out_of_scope: []
```

## Rules

- **Never invent** facts, URLs, repo names, or metrics. Put gaps in **UNKNOWN**.
- Brief body is **English**; gloss is **Spanish** (STE is English-only).
- Cite **ASD-STE100** as the upstream standard; label output **STE-80**, not certified STE.
- Do not merge grant or proposal playbooks into the brief.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ste_lint.py` | Warn-only STE-80 scores per sentence |
| `scripts/fact_check.py` | Source vs brief fact parity |

## Examples

| Path | Description |
|------|-------------|
| `examples/en-diagram-tool-source.txt` | Verbatim EN typed ask (diagram tool) |
| `examples/en-diagram-tool-brief.md` | Worked brief |
| `examples/es-voice-strategy-source.txt` | **Example data** — invented Spanish voice note |
| `examples/es-voice-strategy-brief.md` | Worked brief with G0 |

## Related skills

| Skill | When instead |
|-------|----------------|
| `diagram-design` | Render wire diagram from `wire.yaml` |
| `cleantechhub-brand` | Visual identity on exported artifacts |
| `harness` | Ticket, bc-id, Lane A/B routing |

## References

- `references/ste80.md` — STE-80 subset rules
- `references/cth-glossary.md` — Allowed technical names
