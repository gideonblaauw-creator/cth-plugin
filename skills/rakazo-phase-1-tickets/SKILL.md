---
name: rakazo-phase-1-tickets
description: >
  Use when launching Rakazo Plan B Phase 1 Hands after Orchestrator GO and blockers
  clear. Prep P1-1..P1-4 tickets; craft always stays on Cursor Cloud Hands (t1465u).
metadata:
  version: "2.0.0"
  category: infrastructure
---

# Rakazo Phase 1 tickets

Canonical merge of `rakazo-phase-1-tickets` + `rakazo-phase-1-tickets-2`. Plan B emergency only.

## Do not launch until GO

Use only after Orchestrator **GO Phase 1** with OpenRouter key + VPS-4 Tailscale `{type: machine, name: vps}`.

Phase 1 Hands tickets are prepped at `/workspace/rakazo-phase1/TICKETS.md` and mirror merged `rakazo-plan-b` docs. See `docs/rakazo-plan-b-pointer.md` and `skills/rakazo-failover-comms/SKILL.md`.

## t1465u lock (2026-09-17)

Rakazo = Orch + Desks only (coordination / Babo channels). **Craft ALWAYS → Cursor Cloud Hands** (Lane A/B). Never SF craft on Rakazo computers.

## Ticket order

1. **P1-1** compose up Rakazo+Babo Tailscale-only  
2. **P1-2** seed Orch twin + Infra twin only (route craft to Hands)  
3. **P1-3** OpenRouter mini/Flash + budget cap + spend receipt  
4. **P1-4** Babo WA/Google smoke READ only (HITL on; no send; LinkedIn **[PENDIENTE]**)

## Locks

Sonnet HOLD. No public ports. No dual-primary.

## READY to Orchestrator

Report: twin alive · spend receipt · standby confirmed · bc-ids.