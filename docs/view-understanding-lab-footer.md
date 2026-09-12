# View Understanding Lab — PR footer snippets (lead with tier)

**HARD:** Every Hands completion and harness footer copy **leads with** the tier label. Never surface the Understanding Lab box/CTA without naming Tier 1 or 2 in the **same** message. Tier 0 never gets the lab popup. If the ticket omits `tier:` → treat as Tier 0 and **say so**. Canonical lock: `docs/understanding-lab-tiers.md`.

First line, before any `## View Understanding Lab` heading:

- `**Tier 0** — ship (no Understanding Lab)`
- `**Tier 1** — Light Understanding` + lab links
- `**Tier 2** — Full Lab + ledger` + full lab links

Infra: same first line in Gideon chat beside the cloud-agent card. Do not start the chat follow-up with “View Understanding Lab”. See `skills/infrastructure-comms/SKILL.md` §7 and `skills/harness/SKILL.md` § View Understanding Lab — tier lock.

**Playground hard lock (Tier 1–2):** `scenario → consequences → options → choose` before Shared decisions — not scrub-only or single-suggestion override. Tier 1 = one scenario, 2–3 options. Tier 2 = full hard gate (2–4 option paths).

---

## Tier 0 — ship (no Understanding Lab)

Hands: no lab. Short what/why only. **Say so** — do not stay silent, and do **not** paste a View Understanding Lab box.

```markdown
**Tier 0** — ship (no Understanding Lab)
Ticket omitted `tier:` (or named 0). No lab. No CTA.
```

Drop the “Ticket omitted `tier:`” clause when the ticket named `tier: 0`.

---

## Tier 1 — Light Understanding

Hands: plant Context ≤½ page, Playground light, and one Shared decision row / locks file (`rationale` + `locked_at`). Skip full Explanation essay, quiz, stable host requirement, and event-store projector.

```markdown
**Tier 1** — Light Understanding

## View Understanding Lab
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion, ≤½ page):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (light):** one scenario, 2–3 options with tradeoffs — host optional
- **Shared decisions:** one row + rationale + locked_at — https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after Tier 1 light PASS (Context ≤½ page → Playground light → one Shared decision row). Full five-beat PASS is Tier 2 only.
```

---

## Tier 2 — Full Lab + ledger

Hands: plant all five beats (`Context → Explanation (quiz) → Playground → Shared decisions → Next cycle`), append `events.jsonl` on the VPS Archive ledger path, Notion-promote, and attach the GH run artifact on close. Ticket MUST name Tier 2.

```markdown
**Tier 2** — Full Lab + ledger

## View Understanding Lab
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (stable HTML):** HITL_HTML_STABLE_URL
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b
- **Ledger:** append events.jsonl (VPS Archive ledger path) + GH run artifact on close

**Gate:** Draft only. Infra reviews. Gideon merges after full five-beat PASS (Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle).
```

**Stable host:** Replace `HITL_HTML_STABLE_URL` with the value Infra plants in harness after Vercel/Tailscale deploy. Do not invent a fake URL. Required for Tier 2; skip as a requirement on Tier 1.

**Ticket fields:** `tier: 0|1|2` and `escalate:` — omit `tier:` → treat as Tier 0 and say so. `major: yes` without `tier:` is a miss.
