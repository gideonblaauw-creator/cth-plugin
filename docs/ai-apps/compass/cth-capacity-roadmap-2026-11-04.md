# CleantechHUB — Compass capacity roadmap (2026-11-04)

**Source tool:** [Compass](https://aiappsforgood.org/compass.html) (Nonprofit Builder — organisational diagnostic, ~80 projects / 14 themes).

**How this document was produced:** The live Compass flows (5-minute game, Claude “three questions” roadmap, or browse-and-select) require an **interactive browser session** and optional submission of org narrative to **Claude (Anthropic)** on AI Apps for Good. This file is a **framework-aligned roadmap** for CleantechHUB using **public, non-confidential** context only. It is **not** a Compass app export. Gideon can run Compass interactively later and diff priorities.

## Public org snapshot (inputs)

| Dimension | Public posture |
| --- | --- |
| Entity | CleantechHUB Foundation — Colombian cleantech **accelerator / foundation** |
| Mission (public) | Cleantech acceleration, climate innovation, programs (e.g. ClimateLaunchpad national org, Nexus portfolio, wiki knowledge base) |
| Team | **Small core team**; heavy use of **agent automation** (Harness, Cloud Hands, n8n on OVH VPS) |
| Digital surface | `cleantechhub.net`, `wiki.cleantechhub.net`, `nexus.cleantechhub.net`; Google Workspace; secrets in Infisical |
| Known ops gap (non-secret) | **Backup restore path** (restic → B2) reported **failing** — treat as resilience priority |

## Simulated priority themes (Compass catalogue alignment)

Compass maps needs to capacity-building **projects**. For CTH, the highest-leverage themes match Nonprofit Builder’s recurring grantee demand (strategy, communications, fundraising, leadership, governance, **MEL**, **technology/AI policy**, financial management):

| Priority | Compass-style project | Why now (CTH) |
| --- | --- | --- |
| P1 | **AI tools assessment & policy development** | Many Desks already use AI; need explicit data-privacy and “never paste secrets” rules aligned with Infisical + Harness. |
| P2 | **Impact assessment & reporting (MEL)** | Grant portfolio and Nexus need consistent indicators; adopt **MEL Builder** in `skills/cth-grant/SKILL.md`. |
| P3 | **Internal workflow redesign** | Automations (n8n) and Hands tickets should reduce manual grind; document bottlenecks quarterly. |
| P4 | **Funding diversification & earned income** | Reduce single-funder concentration; tie to grant watch Desk. |
| P5 | **Data protection & backup recovery** | Fix backup/restore verification; pairs with SecureCheck baseline. |
| P6 | **Communications strategy** | Bilingual EN/ES, approval gate for public voice; Buffer/socials Desk. |
| P7 | **Board effectiveness & governance** | Decision rights for Harness gates, deploy authority, and HITL. |

## 18-month sequenced roadmap (reasoned)

### Phase 1 — Stabilize (months 1–3)

- Run **SecureCheck** Full Assessment in browser; execute top 3 fixes (especially **backups + MFA audit** on Workspace admin).
- Publish internal **AI use policy** (what may enter Pitch Builder, MEL Builder, Tough Conversations, external LLMs).
- **MEL:** one pilot grant results framework using MEL Builder output archived in Drive.

### Phase 2 — Scale programs (months 4–9)

- **Pitch Builder → HTML deck** standard on all major grant submissions (`pitch-builder-first-draft`).
- Nexus / Datalab: align 5 portfolio-level indicators with grant MEL sections.
- n8n: document critical workflows; failure alerts to Doctor_Bot / Infrastructure Desk.

### Phase 3 — Governance & growth (months 10–18)

- Board review of automation boundary (Hands vs Workbench vs HITL).
- Fundraising diversification plan with donor mapping workshop (Compass “Fundraising” theme).
- Optional: repeat Compass **as a team** game to reconcile leadership priorities.

## Success signals

- Backup **restore test** documented once per quarter.
- Every full grant proposal references a MEL approach and Pitch Builder narrative handoff.
- Sensitive meetings use Tough Conversations prep note in meeting ticket.
- Calendar color rules deployed (dry-run log reviewed).

---

*CleantechHUB internal planning. Public-voice adoption of third-party AI tools remains subject to approval.*
