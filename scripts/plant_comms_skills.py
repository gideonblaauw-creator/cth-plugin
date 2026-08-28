#!/usr/bin/env python3
"""Plant desk comms skills for CTH Harness (Token lock 2026-08-26)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CURSOR = ROOT / ".cursor" / "skills"

SHARED_TAIL = """## 3. Coordination only

Grok Bot on this Desk is **coordination only** (Token lock 2026-08-26). Route, HITL, go/no-go, and channel I/O escalation.

- Desk **tickets** Cursor Cloud Hands.
- Desk **reviews** output (maker ≠ checker).
- No first-draft packs, research grind, inventory, or code in the Grok chat.
- Do not write Grok Bot box workflows in this skill.

## 4. Everything file/research/code/copy is ticketed to Cursor Cloud Hands

All file packs, research grind, copy drafts, inventories, HTML/docx/xlsx, and repo/code work → **seven-field ticket** to Cursor Cloud Hands. No bc-id = miss.

- Lane A (this repo and other owning repos): `lane: github-pr`
- Lane B (grant/client packs on Drive): `lane: drive-folder`
- **Lane A repo / store for this Desk:** {lane_a}
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.

## 5. Cloud Hands model routing

Token lock **2026-08-28** (supersedes 2026-08-26 Flash-default for fill-in). See `skills/harness/SKILL.md` and `skills/hands-model-routing/SKILL.md`.

| Job | Model | Notes |
|-----|-------|-------|
| Empty / unspecified / file / Drive / inventory / copy / research compile / repo | `composer-2.5` (`fast=false`) | Hands default. Never Fast |
| Tiny only (one artifact, mechanical transform: rename, format, JSON fix, short classify) | `gemini-3.7-flash` | Ticket must **name** Flash. Empty ticket must NOT fill Flash |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |
| Private residency (must not leave 127.0.0.1) | local Ollama `LFM2.5-VL-3B` | If it does not fit 3B, HOLD Gideon. Do not fill Flash |

Never silently use Sonnet, Haiku, Opus, Grok, Composer Fast, or second cloud Kimi on Cloud Hands.

## 6. Workbench exception

{workbench_section}

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay.

## 7. HITL

Nothing **sent**, **posted**, or **paid** without **Gideon Blaauw** yes in the owning chat.

{hitl_extra}
"""

DESKS: list[dict] = [
    {
        "name": "teclogi-comms",
        "desk": "Teclogi",
        "trigger": "Teclogi comms, dataroom client messages, or Teclogi Desk coordination",
        "section1": """- **End client:** Teclogi (logistics / dataroom client). Primary external contacts: **[PENDIENTE]**.
- **Who hears what:** Client-facing → **Spanish** unless the live thread is English. Gideon ↔ Desk chat → **English** unless the live thread is Spanish.
- **Internal:** Gideon Blaauw (HITL, Orchestrator escalation).""",
        "brand": "`[PENDIENTE]` — Teclogi client brand (not `cleantechhub-brand`). No CTH lime leak.",
        "lane_a": "`https://github.com/gideonblaauw-creator/cth-data-room-scanner` (Teclogi-only per Lane A repo lock).",
        "workbench": "This Desk has **no standing Workbench**. WhatsApp only via Orchestrator when Hands cannot reach the contact.",
        "hitl_extra": "Lane A repo lock: never launch non-Teclogi work on `cth-data-room-scanner`.",
    },
    {
        "name": "aic-comms",
        "desk": "AIC",
        "trigger": "AIC, Bravo Bridge, or Americas Innovation Council comms",
        "section1": """- **End client / partners:** Americas Innovation Council (AIC) / Bravo Bridge. Named contact: **Frank** (US-facing).
- **Who hears what:** Client-facing → **English**. Gideon ↔ Desk chat → **English** unless the live thread is Spanish.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`[PENDIENTE]` — AIC / Bravo Bridge brand (isolated from `cleantechhub-brand`). Per `skills/app-build/SKILL.md`: do not mix CTH lime into AIC.",
        "lane_a": "`https://github.com/gideonblaauw-creator/americas-innovation-hub`",
        "workbench": "No standing Workbench. WhatsApp via Orchestrator only when Hands cannot do the step.",
        "hitl_extra": "Never local H3 / US-excluded video weights for US-facing AIC/Frank content (Harness media lock).",
    },
    {
        "name": "almendra-comms",
        "desk": "Almendra",
        "trigger": "Almendra, Run Up coffee, or house-of-brands comms",
        "section1": """- **End client:** Almendra / Run Up coffee / house of brands. Primary external contacts: **[PENDIENTE]**.
- **Who hears what:** Client-facing → **Spanish** unless the live thread is English. Gideon ↔ Desk chat → **English** unless the live thread is Spanish.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`[PENDIENTE]` — Almendra / Run Up brand (not `cleantechhub-brand`).",
        "lane_a": "`https://github.com/gideonblaauw-creator/almendra`",
        "workbench": "No standing Workbench. WhatsApp via Orchestrator only when Hands cannot do the step.",
        "hitl_extra": "Private QBO / staging payloads → local Ollama residency only; do not ticket to cloud Hands.",
    },
    {
        "name": "mubon-comms",
        "desk": "Mubon",
        "trigger": "Mubon or P4G/MubOn program comms",
        "section1": """- **End client / program:** Mubon (P4G/MubOn context in Archive). External contacts: **[PENDIENTE]**.
- **Who hears what:** Follow the live thread language. Default client-facing → **English** for P4G-facing comms unless thread is Spanish.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`[PENDIENTE]` — Mubon program brand. No `cleantechhub-brand` leak unless co-branding is explicit.",
        "lane_a": "Lane B Drive packs unless Gideon marked a repo row.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "aura-comms",
        "desk": "AURA",
        "trigger": "AuRA funder or AURA Desk comms",
        "section1": """- **End client / funder:** AuRA (listed in `skills/cth-grant/SKILL.md` funder set). Funder contacts: **[PENDIENTE]**.
- **Who hears what:** Donor-facing → language of the live thread (often **English** or **Spanish**). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Grants Desk reviews grant packs (maker ≠ checker).""",
        "brand": "`cleantechhub-brand` for CTH-signed donor comms. No client-brand leak.",
        "lane_a": "Grant packs → Lane B Drive. Harness/docs → `cth-plugin`.",
        "workbench": "Gmail ingest only via **Inbox Desk** Workbench; this Desk tickets Hands for drafts.",
        "hitl_extra": "",
    },
    {
        "name": "cth-grants-comms",
        "desk": "CTH Grants",
        "trigger": "CTH Grants Desk comms, donor messages, or grant coordination",
        "section1": """- **End clients / funders:** UNDP, P4G, GIZ, Climate KIC, Expertise France, BID/IDB, and other funders in `skills/cth-grant/SKILL.md`. Named funder contacts: **[PENDIENTE]** per live grant.
- **Who hears what:** Donor-facing follows funder thread language. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Isolated live drafts (CTCN Suriname, GRP, TNS VerdeXcelerate) have their own comms skills.""",
        "brand": "`cleantechhub-brand` for CTH institutional voice. Read `skills/cth-grant/SKILL.md` for grant copy rules.",
        "lane_a": "Grant packs → Lane B Drive (not `cth-plugin`). Specs/harness → `cth-plugin`.",
        "workbench": "Gmail/Calendar via **Inbox** and **Meetings** Desks; this Desk coordinates only.",
        "hitl_extra": "Two live grant drafts max. Nothing submitted without Gideon yes (N8).",
    },
    {
        "name": "cth-grant-ctcn-suriname-comms",
        "desk": "CTH Grant · CTCN Suriname",
        "trigger": "CTCN Suriname isolated grant draft comms",
        "section1": """- **End client / funder:** CTCN Suriname grant (isolated live draft). Funder/partner contacts: **[PENDIENTE]**.
- **Who hears what:** Donor-facing → language of live thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). CTH Grants Desk reviews; Hands writes packs.""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "Lane B Drive for grant pack. Do not open a grant repo unless Gideon marked a row.",
        "workbench": "No standing Workbench on this isolated draft Desk.",
        "hitl_extra": "Counts toward two live grant drafts cap.",
    },
    {
        "name": "cth-grant-grp-comms",
        "desk": "CTH Grant · GRP",
        "trigger": "GRP isolated grant draft comms",
        "section1": """- **End client / funder:** GRP grant (isolated live draft). Funder/partner contacts: **[PENDIENTE]**.
- **Who hears what:** Donor-facing → language of live thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). CTH Grants Desk reviews; Hands writes packs.""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "Lane B Drive for grant pack.",
        "workbench": "No standing Workbench on this isolated draft Desk.",
        "hitl_extra": "Counts toward two live grant drafts cap.",
    },
    {
        "name": "cth-grant-tns-verdexcelerate-comms",
        "desk": "CTH Grant · TNS VerdeXcelerate",
        "trigger": "TNS VerdeXcelerate (CANOA) grant comms",
        "section1": """- **End client / funder:** TNS VerdeXcelerate (CANOA). Named contact: **Juan Pablo Diaz** (joint-work / RFP context per `docs/grant-graph/spec.md`). Recipient org: **TechnoServe**.
- **Who hears what:** Donor/partner-facing → **Spanish** unless live thread is English. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). CTH Grants Desk reviews; Hands writes to TNS Drive folder.""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "Lane B Drive — TNS grant folder (see `docs/grant-graph/spec.md`). Not `cth-plugin` for packs.",
        "workbench": "No standing Workbench. Gmail ingest via Inbox Desk.",
        "hitl_extra": "Nothing sent to TechnoServe without Gideon yes. Counts toward two live grant drafts cap.",
    },
    {
        "name": "cth-proposals-comms",
        "desk": "CTH Proposals",
        "trigger": "CTH commercial proposal comms or RFP responses",
        "section1": """- **End clients:** CleantechHUB service proposal recipients. Named client contacts: **[PENDIENTE]** per live RFP.
- **Who hears what:** Client-facing → language of the RFP/thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Read `skills/cth-proposal-build/SKILL.md` for pipeline.""",
        "brand": "`cleantechhub-brand` for CTH proposals. Client brands stay separate unless co-branding is explicit.",
        "lane_a": "`cth-plugin` for harness; proposal HTML may live in Archive or repo per ticket.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "Mark public-voice CTH proposal copy **Awaiting Gideon's approval** before send.",
    },
    {
        "name": "cth-meetings-comms",
        "desk": "CTH Meetings",
        "trigger": "CTH Meetings Desk comms, calendar invites, or meeting coordination",
        "section1": """- **End clients:** Meeting attendees across CTH programs and clients. Named attendees: **[PENDIENTE]** per meeting.
- **Who hears what:** Invite/body language follows attendee locale. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`cleantechhub-brand` for CTH-hosted meetings.",
        "lane_a": "Calendar is Tool/Workbench — not a GitHub pack by default.",
        "workbench": "**Calendar** Workbench (this Desk only): create/move events when Hands cannot. HITL before create/move.",
        "hitl_extra": "HITL before any Calendar create, move, or external invite send.",
    },
    {
        "name": "cth-strategy-comms",
        "desk": "CTH Strategy",
        "trigger": "CTH Strategy Desk comms or high-level CTH messaging",
        "section1": """- **End clients:** CTH leadership, board, and strategic partners. Named contacts: **[PENDIENTE]** per thread.
- **Who hears what:** External strategy notes → language of live thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "`cth-plugin` or Archive per ticket.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "cth-gtm-strategy-comms",
        "desk": "CTH GTM Strategy",
        "trigger": "CTH go-to-market strategy comms",
        "section1": """- **End clients:** CTH GTM audiences (donors, partners, market segments). Named contacts: **[PENDIENTE]** per campaign.
- **Who hears what:** Market-facing → bilingual EN/ES as appropriate. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "`cth-plugin` or Archive per ticket.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "socials-comms",
        "desk": "Socials",
        "trigger": "CTH Socials Desk comms, social posts, or channel coordination",
        "section1": """- **End clients:** CleantechHUB and partner-brand audiences on social channels. Named partner contacts: **[PENDIENTE]** per campaign.
- **Who hears what:** Public posts → per `skills/social-media-campaign/SKILL.md` and brand skill (CTH, CLP26, etc.). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Workbench chats stay out of Gideon's daily sidebar — he talks to Socials Desk.""",
        "brand": "`cleantechhub-brand` default; `clp26-brand` for CLP26 campaign; partner brands per campaign — no cross-leak.",
        "lane_a": "`cth-plugin` for skills/playbooks; content calendar in Notion/Buffer (Tools).",
        "workbench": "**LinkedIn, Instagram, Facebook, Google Ads** Workbenches (this Desk only): post/DM/spend when Hands cannot. HITL before post/DM/spend/launch/pause.",
        "hitl_extra": "All public CTH social copy: **Awaiting Gideon's approval** before publish.",
    },
    {
        "name": "newsletter-comms",
        "desk": "Newsletter",
        "trigger": "CTH Newsletter System comms or newsletter drafts",
        "section1": """- **End clients:** CleantechHUB newsletter subscribers. Segment contacts: **[PENDIENTE]**.
- **Who hears what:** Newsletter → **bilingual EN/ES** or single-language per edition plan. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Archive project: `CTH Newsletter System`.""",
        "brand": "`cleantechhub-brand`",
        "lane_a": "Content in Archive/Drive or repo per ticket.",
        "workbench": "Gmail send only via **Inbox Desk** Workbench after HITL.",
        "hitl_extra": "Newsletter send = HITL. Mark draft **Awaiting Gideon's approval**.",
    },
    {
        "name": "inbox-comms",
        "desk": "Inbox",
        "trigger": "Inbox Desk comms or Gmail coordination",
        "section1": """- **End clients:** Email correspondents across CTH and client threads. Named contacts: **[PENDIENTE]** per thread.
- **Who hears what:** Reply language follows the live email thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "Follow brand of the owning Desk/thread (`cleantechhub-brand`, `sustenttia-comms` routing, etc.). No cross-client leak.",
        "lane_a": "Email drafts via Hands (`gemini-3.7-flash`); repo only when ticket says so.",
        "workbench": "**Gmail** Workbench (this Desk only): send when Hands cannot. HITL before send.",
        "hitl_extra": "HITL before every outbound email send.",
    },
    {
        "name": "investor-matching-comms",
        "desk": "Investor Matching",
        "trigger": "Investor Matching Desk comms",
        "section1": """- **End clients:** Investors and startup founders in matching flows. Named contacts: **[PENDIENTE]** per deal.
- **Who hears what:** Investor-facing → **English** default unless thread is Spanish. Founder-facing → bilingual EN/ES as needed.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`cleantechhub-brand` for CTH-facilitated intros. Startup materials follow Nexus/startup context — no client-brand leak.",
        "lane_a": "Archive or `cth-plugin` per ticket.",
        "workbench": "No standing Workbench. WhatsApp via Orchestrator when needed.",
        "hitl_extra": "No investor intro sent without Gideon yes.",
    },
    {
        "name": "budget-comms",
        "desk": "Budget",
        "trigger": "CTH 2026 Budget Desk comms",
        "section1": """- **End clients:** CTH internal finance stakeholders and funders requiring budget correspondence. Named contacts: **[PENDIENTE]**.
- **Who hears what:** Internal → **English** unless Spanish thread. Funder-facing follows thread language.
- **Internal:** Gideon Blaauw (HITL). Archive: `CTH - 2026 Budget`.""",
        "brand": "`cleantechhub-brand` for CTH institutional budget comms.",
        "lane_a": "Lane B Drive / Archive for xlsx packs.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "Do not share draft budgets externally without Gideon yes.",
    },
    {
        "name": "academy-comms",
        "desk": "Academy",
        "trigger": "CTH Academy or CLP 2026 program comms",
        "section1": """- **End clients:** Academy participants, trainers, and CLP26 cohorts. Named contacts: **[PENDIENTE]** per program.
- **Who hears what:** Participant-facing → **Spanish** in LATAM markets; **English** when thread requires. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Archive: `CTH - Academy`, `CTH - CLP 2026`.""",
        "brand": "`clp26-brand` for CLP26 campaign content; `cleantechhub-brand` for CTH Academy institutional voice.",
        "lane_a": "`cth-plugin` for skills; program packs in Archive/Drive.",
        "workbench": "Social posts route through **Socials Desk** Workbench after HITL.",
        "hitl_extra": "",
    },
    {
        "name": "nexus-origo-comms",
        "desk": "Nexus/Origo",
        "trigger": "Nexus portfolio or Origo/Climate Data Platform comms",
        "section1": """- **End clients:** Startup founders (Nexus), data partners (Origo / Climate Data Platform). Named contacts: **[PENDIENTE]** per startup/partner.
- **Who hears what:** Startup-facing → **bilingual EN/ES** per `skills/nexus-onepager/SKILL.md`. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Archive: `CTH - Climate_Data_Platform`, Nexus, WIKI.""",
        "brand": "`cleantechhub-brand` for Nexus/CTH platform voice. Startup pages at nexus.cleantechhub.net.",
        "lane_a": "Nexus deploys via `skills/nexus-onepager/SKILL.md`; Origo per Infrastructure classify.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "energy-coop-comms",
        "desk": "Energy Coop",
        "trigger": "Energy Coop Desk comms",
        "section1": """- **End clients:** Energy cooperative stakeholders. Named contacts: **[PENDIENTE]**.
- **Who hears what:** Community-facing → **Spanish** default (Colombia context). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`[PENDIENTE]` — Energy Coop program brand. No `cleantechhub-brand` leak unless co-branding is explicit.",
        "lane_a": "Archive/Drive per ticket unless Gideon marked a repo row.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "embassy-albert-kobus-comms",
        "desk": "Embassy · Albert Kobus",
        "trigger": "Embassy Desk comms with Albert Kobus",
        "section1": """- **End client:** **Albert Kobus** (Embassy Desk named contact). Institution: **[PENDIENTE]** (embassy / mission name not planted in repo).
- **Who hears what:** Diplomatic-facing → language of live thread (**English** / **Dutch** / **Spanish** as used). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "`cleantechhub-brand` for CTH institutional voice unless embassy co-branding is explicit.",
        "lane_a": "Archive per ticket.",
        "workbench": "No standing Workbench. WhatsApp via Orchestrator when needed.",
        "hitl_extra": "",
    },
    {
        "name": "chamber-bucaramanga-comms",
        "desk": "Chamber · Bucaramanga",
        "trigger": "Cámara de Comercio Bucaramanga comms (single Desk — not split)",
        "section1": """- **End client:** Cámara de Comercio de Bucaramanga. Named contacts: **[PENDIENTE]**.
- **Who hears what:** Chamber-facing → **Spanish**. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). One Desk — do not open a twin Chamber skill.""",
        "brand": "`cleantechhub-brand` for CTH voice in chamber partnership comms unless chamber co-branding is explicit.",
        "lane_a": "Archive/Drive per ticket.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "",
    },
    {
        "name": "infrastructure-comms",
        "desk": "Infrastructure",
        "trigger": "Infrastructure Desk comms, harness tickets, or stack coordination",
        "section1": """- **End clients:** Internal CTH stack operators and vendors. Named vendor contacts: **[PENDIENTE]** per ticket.
- **Who hears what:** Internal ops → **English**. Gideon ↔ Desk → **English**.
- **Internal:** Gideon Blaauw (HITL). Owner profile: Infrastructure desk **c656afb9**. Read `skills/app-build/SKILL.md` and `skills/doctor-bot/SKILL.md`.""",
        "brand": "`cleantechhub-brand` only for outward-facing infra comms; internal runbooks need no brand skill.",
        "lane_a": "`https://github.com/gideonblaauw-creator/cth-plugin` for harness/skills.",
        "workbench": "No standing Workbench. Infrastructure tickets Hands — does not SSH-inventory itself.",
        "hitl_extra": "Gideon merges and deploys. Hands does not deploy.",
    },
    {
        "name": "mac-scan-comms",
        "desk": "Mac Scan",
        "trigger": "Mac Scan Desk comms or Mac hygiene coordination",
        "section1": """- **End clients:** Internal — Mac mirror / hygiene only. No external client voice.
- **Who hears what:** Internal → **English**. Gideon ↔ Desk → **English**.
- **Internal:** Gideon Blaauw (HITL).""",
        "brand": "None — internal ops only.",
        "lane_a": "Hands ticket for hygiene scripts; not a jump host (Harness §5).",
        "workbench": "No Workbench. **mac-scan is not a jump host** for VPS or Archive.",
        "hitl_extra": "Do not use mac-scan to reach `/opt/claude-files` or VPS `gws`.",
    },
    {
        "name": "rein-hubs-comms",
        "desk": "REIN Hubs",
        "trigger": "REIN Hubs or Pvblic-related comms",
        "section1": """- **End clients:** REIN Hubs / Pvblic stakeholders. Named contacts: **Lucio** (REIN HOLD context per Harness). Other contacts: **[PENDIENTE]**.
- **Who hears what:** Donor-facing → language of live thread. Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). **REIN HOLD** — no outbound to REIN/Pvblic until Gideon clears HOLD.""",
        "brand": "`cleantechhub-brand` for CTH voice. **Never cite REIN Hubs dollar amounts.**",
        "lane_a": "Lane B Drive for packs unless Gideon marked a repo row.",
        "workbench": "No standing Workbench while REIN HOLD active.",
        "hitl_extra": "REIN HOLD: nothing outbound to REIN/Pvblic without explicit Gideon go. Never cite REIN Hubs dollar amounts.",
    },
    {
        "name": "sustenttia-comms",
        "desk": "Sustenttia",
        "trigger": "Sustenttia client comms or Sustenttia Desk coordination",
        "section1": """- **End client:** **Sustenttia** (sustainability consulting firm — CTH client). Client contacts: **[PENDIENTE]**.
- **Who hears what:** Client-facing → language of live thread (often **Spanish** in Colombia). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Do not launch a second Sustenttia instance (Harness §5).""",
        "brand": "`sustenttia-brand` — client brand managed separately from `cleantechhub-brand`. **No CTH lime leak** into Sustenttia materials (per `skills/app-build/SKILL.md`).",
        "lane_a": "`https://github.com/gideonblaauw-creator/sustenttia-v2` for app tree; comms packs may be Lane B Drive.",
        "workbench": "No standing Workbench.",
        "hitl_extra": "Sustenttia trees stay Sustenttia. Private client payloads → local Ollama residency if required.",
    },
]


def render_skill(d: dict) -> str:
    workbench = d["workbench"]
    hitl_extra = d.get("hitl_extra", "")
    if hitl_extra:
        hitl_extra = "\n" + hitl_extra
    tail = SHARED_TAIL.format(
        workbench_section=workbench,
        hitl_extra=hitl_extra,
        lane_a=d["lane_a"],
    )
    return f"""---
name: {d['name']}
description: >
  Communications protocol for the {d['desk']} Desk. Trigger on {d['trigger']}.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
metadata:
  version: "1.0.0"
  category: comms
  desk: "{d['desk']}"
  owner: Infrastructure desk c656afb9
---

# {d['desk']} — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

## 1. End client / who hears what

{d['section1']}

## 2. Brand skill to follow

{d['brand']}

No brand leak across clients. Co-brand only when Gideon explicitly approves.

{tail}
"""


def render_stub(name: str, desk: str, trigger: str) -> str:
    return f"""---
name: {name}
description: >
  Communications protocol for the {desk} Desk. Trigger on {trigger}.
  Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26).
---

# {name}

This file is a Cursor discovery stub. The playbook source of truth is `skills/{name}/SKILL.md`.

1. Read `skills/{name}/SKILL.md` before doing the work.
2. Follow that playbook. Do not invent a parallel workflow in this stub.
3. Grok Bot = coordination only. Ticket Cloud Hands for file/research/code/copy.
"""


def main() -> None:
    for d in DESKS:
        name = d["name"]
        skill_dir = SKILLS / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(render_skill(d), encoding="utf-8")

        stub_dir = CURSOR / name
        stub_dir.mkdir(parents=True, exist_ok=True)
        (stub_dir / "SKILL.md").write_text(
            render_stub(name, d["desk"], d["trigger"]), encoding="utf-8"
        )

    toolkit_path = ROOT / "skills" / "harness" / "references" / "skill-toolkit.json"
    toolkit = json.loads(toolkit_path.read_text(encoding="utf-8"))
    for d in DESKS:
        entry = {
            "name": d["name"],
            "category": "comms",
            "canonical": f"skills/{d['name']}/SKILL.md",
            "claude_desktop": True,
            "cursor": "stub",
            "description": (
                f"Communications protocol for the {d['desk']} Desk. "
                f"Trigger on {d['trigger']}. "
                "Grok Bot coordination only; file/copy/code → Cloud Hands (Token lock 2026-08-26)."
            ),
        }
        toolkit["skills"].append(entry)
    toolkit["inventory_date"] = "2026-08-27"
    toolkit["counts"]["canonical_on_main"] = len(toolkit["skills"])
    toolkit["counts"]["cursor_stubs"] = sum(
        1 for s in toolkit["skills"] if s.get("cursor") == "stub"
    )
    toolkit_path.write_text(
        json.dumps(toolkit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Planted {len(DESKS)} comms skills.")


if __name__ == "__main__":
    main()
