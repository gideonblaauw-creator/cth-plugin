# View Understanding Lab — PR footer snippets (Tier 1–2 only)

Paste at the **end** of a **Tier 1 or Tier 2** Lane A draft PR body. Replace placeholders with **this build’s** Notion lab URLs from the ticket (`lab_notion:` or `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`).

**Per-build pages (Gideon 2026-09-12 via FabFloow):** every build / product gets its own Understanding Lab Notion page(s). Do **not** reuse Scanner (Dataroom / VertiGreen) lab pages for LexiScan, Sustenttia, or any other product. These snippets use placeholders — never treat Scanner page IDs as a default for all products.

**If the ticket omits lab URLs:** Hands opens the draft PR without a filled lab footer (or with a one-line “lab pages missing” note). Infra posts the Tier label + View PR only and flags missing lab pages. Infra **does not** paste Scanner VertiGreen / Dataroom links and **does not** post View Understanding Lab until the Desk supplies this build’s pages.

**Do not** paste either block on Tier 0 (default). CTA **View Understanding Lab** and full five-beat PASS apply **only** when the ticket names `tier: 1` or `tier: 2` (plus `escalate:` one-liner). Canonical lock: `docs/understanding-lab-tiers.md`.

Infra: in Gideon chat, **lead with the Tier label** (`**Tier 0** — Ship` / `**Tier 1** — Light Understanding` / `**Tier 2** — Full Lab + ledger`) before View PR / View Understanding Lab (Gideon lock 2026-09-12). Tier 0 announces `**Tier 0** — Ship` then View PR only — **no** lab CTA. Tier 1–2 announce the tier, then View PR, then **View Understanding Lab** as a prominent follow-up **only when this build’s lab URLs are on the ticket**. Do not lead with the lab CTA. Do not rely on PR body alone.

**Playground hard lock (Tier 1–2):** `scenario → consequences → options → choose` before Shared decisions — not scrub-only or single-suggestion override. Tier 1 = one scenario, 2–3 options. Tier 2 = full hard gate (2–4 option paths).

**Playground artifact (t1268u):** when the product repo includes a microworld, it **must** follow the LexiScan house-tour standard at `understanding-lab/playground/`. The ticket’s `<lab_playground_url>` is the Notion hub; the repo path is the runnable artifact Infra expects on Tier 1–2 review. Canonical checklist: `docs/understanding-lab-playground-standard.md`.

See `skills/notion/SKILL.md` § View Understanding Lab delivery and `skills/harness/SKILL.md` § View Understanding Lab — tier lock.

---

## Tier 1 — Light Understanding

Hands: plant Context ≤½ page, Playground light, and one Shared decision row / locks file (`rationale` + `locked_at`). Skip full Explanation essay, quiz, stable host requirement, and event-store projector.

```markdown
## View Understanding Lab
- **Tier:** 1 — Light Understanding
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion, ≤½ page):** <lab_context_url>
- **Playground (light):** <lab_playground_url> — LexiScan-format house tour (`understanding-lab/playground/`); one scenario room, 2–3 decision doors; host optional
- **Shared decisions:** one row + rationale + locked_at — <lab_shared_decisions_url>

**Gate:** Draft only. Infra reviews. Gideon merges after Tier 1 light PASS (Context ≤½ page → Playground light → one Shared decision row). Full five-beat PASS is Tier 2 only.
```

---

## Tier 2 — Full Lab + ledger

Hands: plant all five beats (`Context → Explanation (quiz) → Playground → Shared decisions → Next cycle`), append `events.jsonl` on the VPS Archive ledger path, Notion-promote, and attach the GH run artifact on close. Ticket MUST name Tier 2.

```markdown
## View Understanding Lab
- **Tier:** 2 — Full Lab + ledger
- **Escalate:** <one-line reason from the ticket>
- **Context (Notion):** <lab_context_url>
- **Playground (stable HTML):** <lab_playground_url or HITL_HTML_STABLE_URL> — LexiScan-format house tour artifact
- **Playground (repo path):** `understanding-lab/playground/` — run `python -m http.server` per README
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up (legacy Scanner only until remediated)
- **Shared decisions:** <lab_shared_decisions_url>
- **Ledger:** append events.jsonl (VPS Archive ledger path) + GH run artifact on close

**Gate:** Draft only. Infra reviews. Gideon merges after full five-beat PASS (Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle).
```

**Stable host:** Infra-planted UL stable-host `HITL_HTML_STABLE_URL` = https://fabfloow-ul-playground.vercel.app (exemplified by the LexiScan product example; planted in `skills/harness/SKILL.md`). **Not** LexiScan product apps: DEMO https://fabfloow-lexiscan.vercel.app · PROD https://fabfloow-lexiscan-app.vercel.app. Other products: Infra plants per-product host — do not invent URLs. Required for Tier 2; skip as a requirement on Tier 1. A Playground URL on the ticket (`lab_playground_url`) wins over the stable-host token.

**Ticket fields:** `tier: 0|1|2` and `escalate:` — omit `tier:` → default Tier 0 (no footer). `major: yes` without `tier:` is a miss. Tier 1–2 also need this build’s `lab_notion:` URLs (or the three flat `lab_*_url` fields).

## Scanner / Teclogi only

Dataroom Scanner (VertiGreen) lab pages exist for **`cth-data-room-scanner` tickets only**. The Desk may paste those URLs on a Scanner ticket. Never copy them onto LexiScan, Sustenttia, or another product as a fallback default.
