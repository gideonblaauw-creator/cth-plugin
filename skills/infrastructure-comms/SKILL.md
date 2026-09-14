---
name: infrastructure-comms
description: >
  Communications protocol for the Infrastructure Desk. Trigger on Infrastructure Desk comms, harness tickets, or stack coordination.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.4.1"
  category: comms
  desk: "Infrastructure"
  owner: Infrastructure desk c656afb9
---

# Infrastructure — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

- **End clients:** Internal CTH stack operators and vendors. Named vendor contacts: **[PENDIENTE]** per ticket.
- **Who hears what:** Internal ops → **English**. Gideon ↔ Desk → **English**.
- **Internal:** Gideon Blaauw (HITL). Owner profile: Infrastructure desk **c656afb9**. Read `skills/app-build/SKILL.md` and `skills/doctor-bot/SKILL.md`.

## 2. Brand skill to follow

`cleantechhub-brand` only for outward-facing infra comms; internal runbooks need no brand skill.

No brand leak across clients. Co-brand only when Gideon explicitly approves.

## 3. Coordination only

Grok Bot on this Desk is **coordination only** (Token lock 2026-08-26). Route, HITL, go/no-go, and channel I/O escalation.

- Desk **tickets** Cursor Cloud Hands.
- Desk **reviews** output (maker ≠ checker).
- No first-draft packs, research grind, inventory, or code in the Grok chat.
- Do not write Grok Bot box workflows in this skill.

## 4. Everything file/research/code/copy is ticketed to Cursor Cloud Hands

All file packs, research grind, copy drafts, inventories, HTML/docx/xlsx, and repo/code work → **seven-field ticket** to Cursor Cloud Hands. No bc-id = miss.

- Lane A (this repo and other owning repos): `lane: github-pr`
- Lane B (grant/client packs on Drive): `lane: drive-folder`
- **Lane A repo / store for this Desk:** `https://github.com/gideonblaauw-creator/cth-plugin` for harness/skills.
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.
- Production / client agent graphs: ticket `langgraph: yes` and follow `skills/langgraph-production/SKILL.md` on the owning product repo. OpenCode is OSS experiments only.
- **BUILDING (t1263u):** repo/code/build Hands → Composer 2.5 **Fast ON** (`fast=true`); empty build ticket fills Fast ON (not Flash). Explicit build surfaces: repo/code, LangGraph lane, Lane A product apps, **Signal Radar**, **LexiScan**, **scanner**, harness code. Never silently launch a build with Fast off. Canonical: `docs/hands-model-routing.md`.

## 5. Lowest-tier model

| Job | Model | Notes |
|-----|-------|-------|
| Mechanical copy, file packs, inventories, research grind | `gemini-3.7-flash` | Empty mechanical model → Flash |
| Repo / code / build Hands (Signal Radar, LexiScan, scanner, harness, LangGraph) | `composer-2.5` (`fast=true`) | Fast ON for builds (t1263u). No silent Fast off |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |

Never silently use Sonnet, Haiku, Opus, or Grok on Cloud Hands. Repo/code builds use Composer 2.5 Fast ON (t1263u); mechanical/tiny stay Flash. `composer-2.5 (fast=false)` on a build → miss: remap to `fast=true` and flag.

## 6. Workbench exception

No standing Workbench. Infrastructure tickets Hands — does not SSH-inventory itself.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.

Gideon merges and deploys. Hands does not deploy.

### View Understanding Lab — Hands completion in Gideon chat

CTA **View Understanding Lab** and full five-beat PASS apply **only** when the ticket names Tier 1 or Tier 2. **Not** every Lane A merge. Canonical lock: `docs/understanding-lab-tiers.md`. See `skills/harness/SKILL.md` § View Understanding Lab — tier lock.

**First line in Gideon chat is always the Tier label** (Gideon lock 2026-09-12). Every Hands completion leads with one of these before View PR / View Understanding Lab:

- `**Tier 0** — Ship`
- `**Tier 1** — Light Understanding`
- `**Tier 2** — Full Lab + ledger`

Never lead with the lab CTA.

On **Tier 0** (default, or `tier:` omitted), Infrastructure **MUST** in Gideon chat — in this order:

1. **Lead with the Tier label:** `**Tier 0** — Ship`
2. **Send the cloud-agent card** (View PR) plus short what/why.
3. **Do not** post View Understanding Lab.

Merge bar is Infra review + short what/why — no lab PASS.

On **Tier 1 or Tier 2** Lane A Hands completion, Infrastructure **MUST** in Gideon chat — in this order:

1. **Lead with the Tier label:** `**Tier 1** — Light Understanding` or `**Tier 2** — Full Lab + ledger`
2. **Send the cloud-agent card** (View PR).
3. **Then send View Understanding Lab** as its own prominent follow-up **only when the ticket supplied this build’s Notion lab URLs** (`lab_notion:` or `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`):
   - Named **tier** and `escalate:` reason from the ticket
   - Context (Notion): the ticket’s `<lab_context_url>` — **this build only**
   - Playground: the ticket’s `<lab_playground_url>`. Tier 1 = light (one scenario, 2–3 options; stable host **not** required). Tier 2 = that URL or `HITL_HTML_STABLE_URL` from harness (Infra UL stable host; LexiScan product example: https://fabfloow-ul-playground.vercel.app — **not** LexiScan product demos); other products until planted: `[PENDIENTE]` plus local fallback `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
   - Shared decisions: the ticket’s `<lab_shared_decisions_url>` (Tier 1 = one row + rationale + `locked_at`; Tier 2 = full beat)
4. **Remind:** draft PR only — **no merge** until the tier PASS. Tier 1 = light PASS. Tier 2 = **full five-beat PASS** (Context → Explanation+quiz → Playground hard gate → Shared decisions → Next cycle). Do not demand full five-beat PASS on Tier 1 or Tier 0.

**If the Tier 1–2 ticket omits lab URLs:** stop after the Tier label + View PR. Flag missing lab pages in Gideon chat. **Do not** paste Scanner (Dataroom / VertiGreen) links. **Do not** post View Understanding Lab until the Desk supplies this build’s pages.

**Per-build pages (Gideon 2026-09-12 via FabFloow):** every build / product gets its own Understanding Lab Notion page(s). Never reuse Scanner lab pages for LexiScan, Sustenttia, or any other product. Scanner / Teclogi URLs may appear **only** when the ticket is for `cth-data-room-scanner` and the Desk put those URLs on that ticket.

**Do not** bury View Understanding Lab links only in the PR body on Tier 1–2 when lab URLs exist. The PR footer is mandatory for Hands on Tier 1–2 **once URLs are on the ticket**; the **chat link after the Tier label and View PR** is mandatory for Infra on Tier 1–2 **once URLs are on the ticket**. Cursor cannot add a native second button on the agent card — Infra owns the prominent **View Understanding Lab** message. **Do not** post that message on Tier 0. **Do not** invent a default Notion URL.

Full footer templates: `docs/view-understanding-lab-footer.md`; playbook `skills/notion/SKILL.md` § View Understanding Lab delivery. Do not rewrite live Notion page content in this lock (Infra may do Notion separately).

### Playground format lock (Gideon t1268u)

On **Tier 1–2** review, the repo playground **must** match the **LexiScan house-tour HTML standard** — not a flat FAQ, not a one-off layout, not Scanner’s legacy tabbed microworld as the outer shell.

| Rule | Detail |
|---|---|
| **Repo** | https://github.com/gideonblaauw-creator/fabfloow-lexiscan |
| **Path** | `understanding-lab/playground/` (PR #16 MERGED) |
| **Files** | `index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh` |
| **Notion Playground** | https://app.notion.com/p/3d9dfee50be981e08a7bfffe2cc2f33f |
| **Shared decisions** | https://app.notion.com/p/3d9dfee50be981a39107ef7854ec3ce8 |
| **Public host (LIVE — UL playground; LexiScan example)** | https://fabfloow-ul-playground.vercel.app |
| **NOT UL harness host (LexiScan product apps)** | DEMO https://fabfloow-lexiscan.vercel.app · PROD https://fabfloow-lexiscan-app.vercel.app |
| **`HITL_HTML_STABLE_URL` (Infra UL stable-host reference; LexiScan example)** | https://fabfloow-ul-playground.vercel.app |
| **Brand note** | LexiScan chrome = FabFloow cream/mustard/copper; other products use their own brand — never CTH lime on non-CTH products |
| **Ownership** | Infra = UL harness + format lock; FabFloow = internal client; LexiScan = product craft only (format example) |
| **Ticket field** | `playground_standard: lexiscan-html-v2` (optional on Tier 1–2; Infra checks against it when present) |
| **PASS gate** | House tour + per-room quests/quiz/decision doors + EN/ES + ledger export + `smoke.sh` — see `docs/understanding-lab-playground-standard.md` |

When posting Playground in Gideon chat, link the ticket’s `<lab_playground_url>` (Notion hub). If the draft PR adds or changes `understanding-lab/playground/`, call out the repo path so reviewers can run `python -m http.server` per README.

## 8. Secrets (Infisical SoT — Gideon 2026-09-07)

Service API keys and tokens → **Infisical** only (`skills/secrets/SKILL.md`, `skills/infisical/SKILL.md`). Harness hard gate: `skills/harness/SKILL.md` §5 **Secrets SoT**.

- Ticket Hands with **project / environment / key name** — never paste token values in tickets, PRs, or chat.
- Prefer **machine identity** for VPS/Hands workers.
- VPS `.env` = runtime cache regenerable from Infisical — not SoT.

**Migration gaps (HITL — document; do not delete live secrets without Gideon):** Grok box-secrets; Orch connector-secrets (e.g. OpenRouter); Lovable env (e.g. Beehiiv); VPS leftover `infisical-creds` / OPENROUTER env files. See `skills/secrets/SKILL.md` § Migration gaps.

**Carve-out:** Obsidian vault = narrative notes only — no API keys/tokens in Obsidian.
