# Cursor Projects ↔ Desk map (Infra lock)

**Owner:** Infrastructure (Orchestrator routes; Infra seeds map + Grok Bot project shards; Gideon creates/merges Cursor IDE Projects; Hands plants repo docs).

**One-liner:** One Cursor Project ≈ one durable workstream (desk / client / product), not one chat.

Canonical lock for desk → Project → workspace routing. Playbook surfaces: `skills/harness/SKILL.md` § Cursor Projects, `skills/infrastructure-comms/SKILL.md` § Cursor Projects, `tickets/TEMPLATE.md` (`cursor_project`, `cursor_workspace`).

## Principle

| Rule | Detail |
|---|---|
| **One Project ≈ one workstream** | Desk, client, or product — not one chat session. |
| **Orchestrator is not a Project** | Routing and HITL stay in Grok Bot Orchestrator chat. |
| **OpenCode is not a Project** | OpenCode Go is a Hands lane chat, not a Cursor IDE Project. |
| **No inbox/scratch Projects** | Inbox, Box scratch, and ephemeral chats do not get their own Project. |
| **Grant isolation** | Isolated grant desks (CTCN Suriname, GRP, TNS VerdeXcelerate) are **chats inside** CTH-Grants — not separate Projects. |

## Workspace rule (Lane A vs Lane B)

| Lane | Workspace | When |
|---|---|---|
| **A — GitHub PR** | Owning product repo on the Lane A allowlist | Code, skills, harness, repo-tracked assets |
| **B — Drive / Archive** | `https://github.com/gideonblaauw-creator/cth-matters` + Hands worker `{type: machine, name: vps}` | Grant packs, client packs, Drive/Archive writes |

**Lane A allowlist (product code):**

| Repo | Typical desk / subject |
|---|---|
| `https://github.com/gideonblaauw-creator/cth-plugin` | CTH-Infrastructure, harness, skills |
| `https://github.com/gideonblaauw-creator/signal-radar` | Signal Radar product |
| `https://github.com/gideonblaauw-creator/cth-data-room-scanner` | CTH-Teclogi / dataroom scanner **only** |
| `https://github.com/gideonblaauw-creator/fabfloow-lexiscan` | FabFlow / LexiScan |
| `https://github.com/gideonblaauw-creator/sustenttia-v2` | Sustenttia app |
| `https://github.com/gideonblaauw-creator/americas-innovation-hub` | RunUp-AIC / AIC |
| `https://github.com/gideonblaauw-creator/almendra` | RunUp-Almendra |

Match `repo_url` to subject before launch — wrong repo = miss (`skills/harness/SKILL.md` § Lane A repo lock).

**Create Project modal:** defaulting to `cth-matters` is **correct** for Lane B packs. It is **wrong** for product code — open or create the owning Lane A repo instead.

## Naming

- **Project name** = desk slug (kebab-case or `CTH-*` as in the tables below).
- Align with Grok Bot sidebar labels and VPS Archive paths under `/opt/claude-files/Projects/…` when present.
- Do not invent Eve trees on desks. Do not nest grant desks as separate Projects.

## Layer 0 — Pods (sidebar grouping)

Four pods group Projects in Cursor IDE:

| Pod | Scope |
|---|---|
| **CTH** | CleantechHUB foundation desks |
| **Run-Up** | Run Up parent + AIC + Almendra |
| **Sustenttia** | Client brand (separate identity) |
| **Personal** | Personal workstreams (e.g. Natalia Ariza) |

Orchestrator lives **outside** pods — it is not a Project.

## Layer 1 — CTH desks → Projects

| Desk | Cursor Project | Lane | Workspace |
|---|---|---|---|
| CTH-Infrastructure | `CTH-Infrastructure` | A | `cth-plugin` |
| CTH-Grants | `CTH-Grants` | B | `cth-matters` + VPS worker |
| CTH-Proposals | `CTH-Proposals` | B | `cth-matters` + VPS worker |
| CTH-Meetings | `CTH-Meetings` | B | `cth-matters` + VPS worker |
| CTH-Socials | `CTH-Socials` | B | `cth-matters` + VPS worker |
| CTH-Inbox | `CTH-Inbox` | B | `cth-matters` + VPS worker |
| CTH-Strategy | `CTH-Strategy` | B | `cth-matters` + VPS worker |
| CTH-Teclogi | `CTH-Teclogi` | A + B | A: `cth-data-room-scanner` · B: `cth-matters` + VPS worker |
| CTH-AURA | `CTH-AURA` | B | `cth-matters` + VPS worker |
| CTH-Energy-Coop | `CTH-Energy-Coop` | B | `cth-matters` + VPS worker |
| CTH-Chamber-Bucaramanga | `CTH-Chamber-Bucaramanga` | B | `cth-matters` + VPS worker |
| CTH-CCF | `CTH-CCF` | B | `cth-matters` + VPS worker |
| CTH-CEE-Externado | `CTH-CEE-Externado` | B | `cth-matters` + VPS worker |
| CTH-APC | `CTH-APC` | B | `cth-matters` + VPS worker |
| CTH-Legal | `CTH-Legal` | B | `cth-matters` + VPS worker |
| CTH-REIN | `CTH-REIN` | B | `cth-matters` + VPS worker |

**CTH-Grants note:** isolated live grant desks (CTCN Suriname, GRP, TNS VerdeXcelerate) stay as **chats inside** `CTH-Grants` — not separate Cursor Projects.

## Layer 2 — Run Up, Sustenttia, FabFlow

| Desk / product | Cursor Project | Lane | Workspace |
|---|---|---|---|
| RunUp-AIC | `RunUp-AIC` | A | `americas-innovation-hub` |
| RunUp-Almendra | `RunUp-Almendra` | A | `almendra` |
| Sustenttia | `Sustenttia` | A (+ B packs) | A: `sustenttia-v2` · B: `cth-matters` for comms packs |
| FabFlow / LexiScan | `FabFlow` | A | `fabfloow-lexiscan` |

Pod: RunUp-AIC and RunUp-Almendra under **Run-Up**; Sustenttia under **Sustenttia**; FabFlow under **CTH** or product pod per Gideon sidebar.

## Layer 3 — Bench (Hands utilities)

| Bench | Default | Exception |
|---|---|---|
| Bench-Research | `cth-matters` (B) | Lane A repo when ticket is code |
| Bench-Presentations | `cth-matters` (B) | Lane A repo when ticket is code |
| Bench-Video | `cth-matters` (B) | Lane A repo when ticket is code |
| Bench-Images | `cth-matters` (B) | Lane A repo when ticket is code |
| Bench-Scraper | `cth-matters` (B) | Lane A repo when ticket is code |

Bench work runs as Hands tickets — not extra Desks. No separate Cursor Project per bench unless Gideon promotes a durable workstream.

## Layer 4 — Personal

| Workstream | Cursor Project | Lane | Workspace |
|---|---|---|---|
| Personal-Natalia-Ariza | `Personal-Natalia-Ariza` | B | `cth-matters` + VPS worker |

Pod: **Personal**.

## Agents in a Project

Cloud agents launched from a Cursor Project inherit that desk’s scope:

- **Desk** + **Workbench children** for that subject only.
- Do not cross-pollinate agents across Projects (wrong repo / wrong pack lane = miss).
- Ticket `desk:` must match the Project’s desk slug when Hands is opened from that Project.

## Rollout (HITL)

Gideon creates and merges Cursor IDE Projects. Infra seeds the map and Grok Bot project shards. Hands plants this doc — **no Cursor Projects API from code**.

| Phase | Projects to stand up |
|---|---|
| **1 — Now** | 4 pods + `CTH-Infrastructure`, `Sustenttia`, `CTH-Teclogi`, `Personal-Natalia-Ariza`, `CTH-Grants` |
| **2 — Next** | Remaining Layer 1 CTH desks (Proposals, Meetings, Socials, Inbox, Strategy, AURA, Energy-Coop, Chamber-Bucaramanga, CCF, CEE-Externado, APC, Legal, REIN) |
| **3 — Later** | Run Up layer (`RunUp-AIC`, `RunUp-Almendra`, `FabFlow`) + Bench Projects as needed |

## Ticket fields (optional)

When opening Hands for a desk, name the Cursor Project and workspace lane on the ticket:

```
cursor_project: CTH-Infrastructure
cursor_workspace: cth-plugin
```

| Field | Values |
|---|---|
| `cursor_project` | Desk slug / Project name from tables above |
| `cursor_workspace` | Lane A repo slug (`cth-plugin`, `sustenttia-v2`, …) or `cth-matters` for Lane B |

See `tickets/TEMPLATE.md`.

## Non-goals

- Do not create Cursor IDE Projects from this repo (no Projects API).
- Do not invent Eve trees on desks.
- Do not nest isolated grant desks as separate Projects.
