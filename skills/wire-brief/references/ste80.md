# STE-80 — CleantechHUB controlled-language subset

**Source:** ASD-STE100 *Simplified Technical English* (Issue 8, ASD). CleantechHUB uses a **loose subset** we call **STE-80**. It is **not** STE compliant and is **not** a certification claim.

**Why STE-80:** Karpathy’s post (Oct 2026) on applying aerospace controlled English to LLM output aligns with Gideon’s gate for wire artifacts. STE is **English-only**. Brief sections therefore include a **one-line Spanish gloss** for Gideon; the brief body stays in English.

## Sentence rules

| Rule | Limit |
|------|--------|
| Procedural sentence (instruction, step) | **Max 20 words** |
| Descriptive sentence (context, status) | **Max 25 words** |
| Instructions per sentence | **One** |
| Meanings per word | **One** (use the glossary for fixed terms) |
| Voice | **Active** — name the actor |
| `-ing` noun forms | Avoid where a verb works |
| Noun cluster | **Max 3** nouns in a row |
| Paragraph | **Max 6** sentences |

## Procedural vs descriptive

- **Procedural:** STEPS lines, imperatives, “You must…”, numbered actions.
- **Descriptive:** GOAL, ACTORS, STATUS, LOCKS, UNKNOWN, OUT OF SCOPE.

## Technical names

Use terms from `references/cth-glossary.md` verbatim. The linter **exempts** glossary tokens from noun-stack and `-ing` checks where they are fixed names.

## Do not invent

If the source transcript does not state a fact, put it under **UNKNOWN**. Never fill gaps with plausible detail.

## Lint

Run `python3 skills/wire-brief/scripts/ste_lint.py path/to/brief.md` before hand-off. Output is **warn-only**; fix high warnings before G0 when the gate applies.
