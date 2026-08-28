---
name: hands-model-routing
description: >
  Cloud Hands model routing lock for Cursor agents. Use when: ticketing Cloud Hands,
  choosing a Hands model, empty model fill-in, or desk comms section 5. Do not use when:
  Orchestrator/Grok coordination (not a Hands model slot).
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
---

# Cloud Hands model routing

**Owner:** Gideon Blaauw  
**Date:** 2026-08-28  
**Status:** hard gate — supersedes Token lock 2026-08-26 Flash-default for fill-in

Canonical rulebook: `skills/harness/SKILL.md` §5 (Token lock 2026-08-28).

## Routing

| Job | Model | Notes |
|-----|-------|-------|
| Empty / unspecified / file / Drive / inventory / copy / research compile / repo | `composer-2.5` (`fast=false`) | Hands default. Never Fast |
| Tiny only (one artifact, mechanical transform: rename, format, JSON fix, short classify) | `gemini-3.7-flash` | Ticket must **name** Flash. Empty ticket must NOT fill Flash |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |
| Private residency (must not leave 127.0.0.1) | local Ollama `LFM2.5-VL-3B` | If it does not fit 3B, HOLD Gideon. Do not fill Flash |

## High-tier (never silent fill)

Sonnet, Opus, Haiku as Hands, Fable, Sol, Grok, Composer Fast, second cloud Kimi, Auto-as-spend → **HOLD and flag Gideon.**

## Desk comms

Every `*-comms` desk skill section 5 points here. Grok Bot stays coordination only.
