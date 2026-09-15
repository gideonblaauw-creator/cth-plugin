# Example legal eval memo

**EXAMPLE ONLY — illustrative structure, not counsel-approved text.**

---

# Legal eval memo — AURA-CONSULT-2026-001

- **review_mode:** moderate
- **fine_mode:** full_memo
- **doc_type:** Consulting agreement (draft v2)
- **entity:** CLEANTECHHUB INTERNATIONAL S.L. — party block matches canonical name
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
