---
name: oss-stills
description: >
  OSS self-host stills path — ComfyUI + Flux.1-Dev + CTH LoRA on the named
  GPU host. Use when: OSS stills, ComfyUI still, Flux LoRA still, branded
  diffusion still, self-host image generate. Do not use when: throwaway mocks
  (OpenRouter FLUX HTTP), Canva brand layouts, presenter video (HeyGen), or
  VPS-4 weight installs.
license: MIT
metadata:
  version: "1.0.0"
  category: infrastructure
  owner: Infrastructure desk c656afb9
---

# OSS Stills — ComfyUI + Flux.1-Dev + CTH LoRA

**Owner:** Infrastructure desk c656afb9
**Status:** planted dryrun 2026-08-28 — no generation in this track until host is live
**Rulebook:** `skills/harness/SKILL.md` §5 Media generation routing

This skill is the **OSS self-host track** for branded stills. It does not replace the OpenRouter FLUX HTTP cloud bus (harness media-generation lock). It does not cover presenter video (HeyGen stays primary per harness).

## Stack

| Layer | Choice |
|---|---|
| Runtime | ComfyUI |
| Base model | Flux.1-Dev |
| Brand adapter | CTH LoRA (trained from `skills/cleantechhub-brand/brand_dna.yaml`) |
| Brand DNA | `skills/cleantechhub-brand/brand_dna.yaml` — Manual de Marca Jan 2024, five colors only |

## GPU host

```yaml
host: HOLD
```

**Repo evidence (2026-08-28):** No suitable GPU host is named on `main`.

| Machine | Worker | Role | Flux weights? |
|---|---|---|---|
| Gideon's MacBook Air | `mac-scan` | Private Cursor worker; often asleep | **Unconfirmed** — no NVIDIA assumed in harness |
| VPS-4 (`vps-4e96ec79`, `51.195.45.77`) | `vps` | CPU VPS; Archive / `gws` | **Forbidden** — never download Flux or video weights here |

**Gideon must stand up (pick one):**

1. **Dedicated GPU box** — Linux host with NVIDIA GPU (≥12 GB VRAM recommended for Flux.1-Dev + LoRA), disk for Flux.1-Dev weights + CTH LoRA, ComfyUI installed, reachable from Hands (Cursor worker or SSH ticket). Name the host in this skill (`host: <name>`) when live.
2. **Confirm MacBook Air** — If the Air has a usable NVIDIA GPU and enough disk, install ComfyUI + Flux.1-Dev + CTH LoRA locally and ticket Hands with `environment: {type: machine, name: mac-scan}`. If no usable GPU, use option 1.

Do **not** install Flux.1-Dev or LoRA weights on VPS-4.

### BFL / Flux license (informational — not a blocker)

Black Forest Labs Flux.1-Dev default license is **non-commercial (NC)**. Commercial self-hosting is a **paid BFL add-on**, not a veto on planting this stack. Gideon decides NC vs commercial before production stills ship.

## Queue — how a Desk tickets a still

Every still is a **seven-field Hands ticket** per `tickets/TEMPLATE.md`. No bc-id = miss. **This plant does not generate images** — tickets below are for when the host is live.

```
desk: Socials | Grants | Proposals | <owning Desk>
folder: /opt/claude-files/Projects/<project>/stills/ or repo path for Lane A assets
done-when: <N> branded still(s) exported to folder; public-ready URLs if for Buffer/Workbench
model: composer-2.5 (fast=false)
lane: github-pr | drive-folder
hitl: nothing sent/posted/paid; stills Awaiting Gideon's approval before publish
reviewer: <owning Desk> — maker ≠ checker
context:
  skill: oss-stills
  route: oss-self-host
  host: HOLD  # replace with named GPU host when live
  brand_dna: skills/cleantechhub-brand/brand_dna.yaml
  prompt: <Desk brief — subject, aspect ratio, EN/ES copy context>
  count: <integer>
```

**Model rule:** Default `composer-2.5` (`fast=false`) for ComfyUI workflow edits, LoRA wiring, and export packs on the GPU host. Use `gemini-3.7-flash` only when the ticket is a **tiny** mechanical rename/manifest with no workflow change — name that exception in `context:`.

**Route selection (Desk / Orchestrator):**

| Need | Route | Skill |
|---|---|---|
| Branded OSS still (on-brand diffusion) | OSS self-host | This skill — when `host` ≠ HOLD |
| Throwaway mock / quick AI still | OpenRouter cloud bus | Harness §5 — `POST /api/v1/images` (FLUX / Qwen-Image) |
| Template / layout still | Canva | `skills/canva/SKILL.md` |
| Presenter video | HeyGen | Harness §5 — not this skill |

Do not add fal.ai. Do not delete OpenRouter image rows from the harness lock.

## Do not

- Generate images or download weights in a plant/dryrun PR.
- Put Flux.1-Dev, CTH LoRA, or other diffusion weights on VPS-4.
- Invent a GPU host — use `host: HOLD` until Gideon stands one up.
- Add black, purple, red, or a sixth brand color to `brand_dna.yaml`.
- Rewrite HeyGen / video routing in the harness — only cross-link stills.

## Related skills

| Skill | When instead |
|---|---|
| `cleantechhub-brand` | HTML/CSS brand tokens (Inter palette) — diffusion uses `brand_dna.yaml` |
| `canva` | Brand layout stills, not diffusion |
| `socials-loop` | Weekly social pack — stills step may ticket OSS or OpenRouter |
| `harness` | Media-generation lock, OpenRouter bus, HeyGen presenter |
