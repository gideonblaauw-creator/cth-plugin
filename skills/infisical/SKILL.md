---
name: infisical
description: >
  Pointer to Infisical as CleantechHUB sole durable secrets SoT. Use when:
  Infisical, where to store API keys, fetch secrets for Hands, machine identity.
  Do not use when: full rotation/leak protocol (secrets skill).
license: MIT
metadata:
  version: "1.0.0"
  category: "infrastructure"
  adopted: "2026-09-07"
---

# Infisical — Secrets SoT Pointer

**Hard gate — Gideon 2026-09-07.** Infisical is the **only** durable store for service API keys and tokens. Full protocol: `skills/secrets/SKILL.md`. Harness gate: `skills/harness/SKILL.md` §5 **Secrets SoT**.

## Quick reference (names/ids only)

| Field | Value |
|---|---|
| Org | CleantechHUB Infisical org |
| Project | `cth-agents` (`c84fe8b3-d64e-485a-82d7-250dc57a6453`, slug `cth-agents-m4-gr`) |
| Example prod keys (names only) | `MONDAY_API_TOKEN`, `MONDAY_API_KEY` at path `/` |

## Rules

- Fetch by **project / environment / key name** — never paste values in chat, tickets, or PRs.
- Prefer **machine identity** for Hands and VPS workers.
- VPS `.env` and platform env vars are **runtime cache** only; regenerable from Infisical.
- Obsidian, box-secrets, Drive, Notion, and git are **not** secrets SoT.

## When blocked

Missing Infisical access or identity → HOLD; ticket Infrastructure Desk. Do not ask Gideon to paste tokens in chat.

## Related skills

| Skill | When |
|---|---|
| `secrets` | Store, rotate, scan, leak recovery |
| `harness` | Hard gate and Hands ticket contract |
| `infrastructure-comms` | Migration gaps and stack tickets |
