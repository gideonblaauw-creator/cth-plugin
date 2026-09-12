# View Understanding Lab — PR footer snippets (Tier 1–2 only)

Paste at the **end** of a **Tier 1 or Tier 2** Lane A draft PR body. Replace placeholders before opening the PR.

**Do not** paste either block on Tier 0 (default). CTA **View Understanding Lab** and full five-beat PASS apply **only** when the ticket names `tier: 1` or `tier: 2` (plus `escalate:` one-liner). Canonical lock: `docs/understanding-lab-tiers.md`.

Infra: also post **View Understanding Lab** as a prominent chat link beside the cloud-agent card on Tier 1–2 — do not rely on PR body alone, and do **not** post the CTA on Tier 0.

**Playground hard lock (Tier 1–2):** `scenario → consequences → options → choose` before Shared decisions — not scrub-only or single-suggestion override. Tier 1 = one scenario, 2–3 options. Tier 2 = full hard gate (2–4 option paths).

See `skills/notion/SKILL.md` § View Understanding Lab delivery and `skills/harness/SKILL.md` § View Understanding Lab — tier lock.

---

## Tier 1 — Light Understanding

Hands: plant Context ≤½ page, Playground light, and one Shared decision row / locks file (`rationale` + `locked_at`). Skip full Explanation essay, quiz, stable host requirement, and event-store projector.

```markdown
## View Understanding Lab
- **Tier:** 1 — Light Understanding
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
## View Understanding Lab
- **Tier:** 2 — Full Lab + ledger
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (stable HTML):** HITL_HTML_STABLE_URL
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b
- **Ledger:** append events.jsonl (VPS Archive ledger path) + GH run artifact on close

**Gate:** Draft only. Infra reviews. Gideon merges after full five-beat PASS (Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle).
```

**Stable host:** Replace `HITL_HTML_STABLE_URL` with the value Infra plants in harness after Vercel/Tailscale deploy. Do not invent a fake URL. Required for Tier 2; skip as a requirement on Tier 1.

**Ticket fields:** `tier: 0|1|2` and `escalate:` — omit `tier:` → default Tier 0 (no footer). `major: yes` without `tier:` is a miss.
