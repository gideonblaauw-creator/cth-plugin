# Example legal eval memo

**EXAMPLE ONLY — illustrative structure, not counsel-approved text.**

---

# Legal eval memo — AURA-CONSULT-2026-001

- **review_mode:** moderate
- **fine_mode:** full_memo
- **doc_type:** Consulting agreement (draft v2)
- **cth_party:** sl
- **entity:** CLEANTECHHUB INTERNATIONAL S.L. (NIF B19439389) — party block matches canonical S.L. name for commercial consulting instrument
- **language:** ES (counterparty pack); EN fallback clauses noted

## Summary

[INTERNAL] First-pass review of AURA-related consulting agreement draft. Entity naming correct. Liability cap missing in §8 — route as blocker. Governing law cites Colombia with ES/CO multi-jurisdiction flag. Recommend HITL before any send.

## Findings

| Clause | Severity | Firewall | Recommendation |
|--------|----------|----------|----------------|
| §1 Parties | accept | EXTERNAL | Confirm signature blocks only — no text change |
| §3 Scope / SOW | negotiate | INTERNAL | Deliverables list vague vs playbook preferred — suggest fallback scope language in redline |
| §8 Liability | blocker | INTERNAL | Uncapped liability — hard stop; propose cap per playbook `liability_cap` fallback |
| §12 Governing law | negotiate | INTERNAL | ES/CO multi-jurisdiction — flag counsel matrix [PENDIENTE] |
| §15 Auto-renewal | accept | INTERNAL | 12-month term, 90-day notice — within playbook |

## Open questions

- [INTERNAL] Is AURA counterparty signing as funder entity or program vehicle?
- [INTERNAL] Confirm whether English annex is required for AuRA thread.

## HITL asks for Gideon

1. Approve proposed liability cap redline for [EXTERNAL] share?
2. Go/no-go on send pending counsel matrix for ES/CO?
3. Coordinate with AURA Desk on binding scope language?

---

## [EXTERNAL] redline excerpt (counterparty-safe)

> §8 Limitación de responsabilidad: [proposed cap language — no internal playbook reference]

Do not attach severity scores or YAML playbook to counterparty channels.

---

# Legal eval memo — GRANT-CONVENIO-2026-001 (Foundation example)

**EXAMPLE ONLY — illustrative structure, not counsel-approved text.**

- **review_mode:** moderate
- **fine_mode:** full_memo
- **doc_type:** Convenio (grant program)
- **cth_party:** foundation
- **entity:** CleantechHUB Foundation — party block matches canonical Foundation name for grant/convenio instrument
- **language:** ES

## Summary

[INTERNAL] First-pass review of donor convenio draft. Entity naming correct (Foundation, not S.L.). Scope references program deliverables — negotiate vs playbook preferred. Recommend HITL before any send.

## Findings

| Clause | Severity | Firewall | Recommendation |
|--------|----------|----------|----------------|
| §1 Parties | accept | EXTERNAL | Foundation party block correct — no text change |
| §2 Scope | negotiate | INTERNAL | Deliverables vague vs playbook preferred — suggest fallback scope language |
| §1 Parties (hypothetical) | blocker | INTERNAL | If S.L. named on grant/convenio → wrong entity hard stop |

## HITL asks for Gideon

1. Approve proposed scope redline for [EXTERNAL] share?
2. Coordinate with Grants Desk on program deliverables language?
