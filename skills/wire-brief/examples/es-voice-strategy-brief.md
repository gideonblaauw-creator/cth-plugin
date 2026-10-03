# Wire brief — Origo strategy voice (example data)

## GOAL
_Objetivo._
Define a Workbench flow for Origo strategy audio that ends in a wire diagram Lane A PR.

## ACTORS
_Participantes._
- Gideon: confirms the brief at gate G0.
- Orchestrator: routes the strategy audio into wire-brief.
- Cloud Hands: renders the diagram and returns bc-id bc_a1b2c3d4e5.

## STEPS
_Pasos._
1. Orchestrator receives Origo strategy audio on the Workbench.
2. Cloud Hands transcribe the audio and draft an STE-80 English brief.
3. Gideon confirms the brief in at most ten chat lines at G0.
4. Cloud Hands generate the wire diagram in the owning GitHub repo.
5. Cloud Hands ready-ping with bc-id bc_a1b2c3d4e5.

## STATUS
_Estado._
Strategy flow is not documented yet for Origo.

## LOCKS
_Fijos._
- G0 applies to this voice strategy ask.
- Target date 15 Oct 2026.

## UNKNOWN
_Sin inventar._
- Exact Origo repo URL (not stated in source).

## OUT OF SCOPE
_Fuera._
- REIN Hubs budget figures.
