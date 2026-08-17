# Grant Graph — CTH Harness spec

**Owner:** Infrastructure + Grants Desk
**Date:** 2026-08-17
**Status:** spec (analog — do not upgrade to live until gates A–C clear)
**PR:** cursor/blaauw-harness-v3-b285

Spine stays N1–N9. No new nodes. The NEW BAND (Tools / Repos / Backends) is the layer added 2026-08-17. Every later CTH graph (App-build, Commercial, Meetings) must reuse this band.

---

## Spine (N1–N9) — unchanged

| Node | Label | Notes |
|------|-------|-------|
| N1 | Call | Entry point. Gmail ingest + Calendar deadline card. |
| N2 | RFP | Funder doc retrieved; go/no-go max = 1. |
| N3 | SOI | Statement of interest. Hands writes; Desk reviews. |
| N4 | Full Proposal | Hands writes; Grants Desk reviews. |
| N5 | Budget | Hands writes; Grants Desk reviews. |
| N6 | Supporting Docs | Attachments, CVs, annexes. Hands writes. |
| N7 | Verify | Read-back from Drive. Hands reads; Desk checks. |
| N8 | HITL | Gideon signs off. Nothing submitted without this. |
| N9 | Park | Declined / deferred / on-hold. |

---

## NEW BAND: Tools / Repos / Backends

This band maps the layer below the spine — where data lands, which connectors move it, and which backend analogs exist. Label each backend: **live**, **coded-analog**, or **absent**.

### Tools

| Tool | Spine attachment | Role | Constraint |
|------|-----------------|------|------------|
| Drive | N3–N6 write; N7 read | Submit SoT. Hands writes. Verify reads. TNS folder: https://drive.google.com/drive/folders/1saTASGx9VPyG7auRjNu5SkzAP3e34vEA | All Drive writes via Hands (bc-id required). Desks do not write Drive. |
| Gmail | N1 only | Call ingest. Deadline forwarded to Calendar. | Do not send from Gmail via grant flow. |
| Calendar | N1 parallel | Deadline card on N1. Parallel with Gmail. | Read-only from grant graph perspective. |
| Box | Scratch | Scratch only. Never SoT. | Not a Workbench. Do not persist grant artefacts here. |

### Repos

| Repo | Role | Constraint |
|------|------|------------|
| `gideonblaauw-creator/cth-plugin` | Harness skill + this graph. Lane A Hands → GitHub PR. | No grant packs here. Docs/specs only. |
| `gideonblaauw-creator/sustenttia-v2` @ `1fc2dfb` | Analog only — shows how ingest + enrich run under a live app. | NOT the grant pack. No new grant repo. Reference pattern only. |

No new GitHub repo for grant packs. Grant packs go to Drive (Lane B).

### Backends (Sustenttia analog — label: live / coded-analog / absent)

| Backend | Status | Role in analog | Grant graph constraint |
|---------|--------|---------------|------------------------|
| Cognee | **live** (analog) | 9 datasets; Kùzu inside Cognee. | NOT a grant store. Pattern reference only. |
| FalkorDB + Graphiti | **coded-analog** | Container up, 0 nodes. Temporal graph pattern. | Do not claim grant facts stored here. Falkor is the graph DB (not Neo4j). |
| R2R | **absent** (crash-loop) | Retrieval analog. | Do not claim hits. Do not draw as a live path. |
| Gold LanceDB | **coded-analog** | Vector store analog. | Pattern reference only. |
| Chroma | **coded-analog** (leftover gate) | Legacy vector gate. | Do not stop. Do not copy as a second grant path. |
| Neo4j | **absent** | Graphify can emit Neo4j Cypher; no Neo4j container running. | Do not draw Neo4j as a CTH store. Falkor is the graph DB. |

---

## Gates before 65% target

Do not launch Grant Graph live or TNS packs until all three clear:

| Gate | Description | Status |
|------|-------------|--------|
| A | Drive MCP auth | Path 1 live — test file confirmed. Monitor needsAuth / cursor:// OAuth bug. |
| B | VPS Archive worker | Not installed. Archive writes blocked. |
| C | Cloud Agent healthy | Verify with bc-id on next Hands ticket. |

---

---

## DATA FLOW band — TNS VerdeXcelerate (CANOA) example

**Input example:** Juan Pablo Diaz RFP / joint-work points for TNS VerdeXcelerate (CANOA).
**PNG:** `docs/grant-graph/grant-dataflow.png`

This band is a detailed data-flow wire. It does not add N-nodes to the spine. It maps what happens between raw notes and Drive outputs, using existing stages (ingest-before-N4). Analog ≠ live. Do not claim live grant facts in Falkor today.

### Stage 1 — INPUT (raw)

| Source | What lands | Where it goes first |
|--------|-----------|---------------------|
| JP Diaz notes / joint-work points | Raw text, bullet points, verbal commitments | TNS grant Drive folder |
| Gmail Call (N1) | RFP email, deadline, funder contact | TNS grant Drive folder |
| Supporting docs already in Drive | Prior CTH work, partner CVs, budgets | TNS Drive folder already present |
| Drive folder | `https://drive.google.com/drive/folders/1saTASGx9VPyG7auRjNu5SkzAP3e34vEA` | Source of truth for this grant |

All raw input lands in Drive first. Hands writes to Drive (Lane B). Desks do not write Drive.

### Stage 2 — ORGANIZE (graph layer, maps onto ingest-before-N4)

| Component | Role | Status today |
|-----------|------|-------------|
| FalkorDB + Graphiti | Fact store — "what JP said / what the RFP requires". Entities: funder, requirement, deliverable, partner, deadline, budget-line. Relations: requires, supports, blocks. | **EMPTY — 0 nodes.** Path is drawn; do not claim live grant facts. |
| Graphiti temporal layer | Tracks when facts were stated / updated (JP call date, RFP version). | **EMPTY** — coded, not populated. |
| Neo4j | NOT running. Graphify can emit Cypher but no Neo4j container. | **ABSENT** — Falkor is the graph DB. Do not draw Neo4j as the store. |

Hands receives an "organize" ticket (Haiku/Flash lane). Input = raw Drive docs. Output = Falkor write + bc-id.

### Stage 3 — RETRIEVE / ANALYZE

Query only sources that are currently up. Isolated bot tickets Hands; Grants Desk reviews. Maker ≠ checker.

| Source | Query type | Status | Constraint |
|--------|-----------|--------|------------|
| Nexus / idea-browser (Chroma RAG) | Startup matches for the call | **live analog** | For startup context only — not a grant SoT. |
| Drive / Archive (prior CTH packs) | UNDP, P4G/MubOn, other funded proposals | **live** | Hands reads; path: Drive MCP → Composio Drive → VPS `gws`. |
| Cognee (Sustenttia analog) | 9-dataset graph query pattern | **live analog** | Sustenttia datasets only. NOT a grant SoT. Pattern reference. |
| R2R | Retrieval hits | **ABSENT (crash-loop)** | Do not claim hits. Do not draw as a live path. |
| FalkorDB (Stage 2 output) | Structured grant facts | **EMPTY today** | Query path ready; no facts until Stage 2 populates. |

"What CTH can do" = this analysis context. It feeds N3/N4. It is not a new Gideon stage.

### Stage 4 — OUTPUT (Hands → Drive, Lane B)

All outputs written by Cloud Hands. Must return a bc-id. Include Drive URL in the report. Verify (N7) reads Drive only. HITL (N8) before any send.

| Output | Format | Spine node | Drive destination |
|--------|--------|------------|------------------|
| Draft narrative | Unformatted `.docx` | N3 SOI / N4 Full Proposal | TNS grant folder |
| Structured proposal | Donor/template format `.docx` | N4 | TNS grant folder |
| Budget | `.xlsx` | N5 | TNS grant folder |
| Annexes / CVs / supporting docs | Various | N6 | TNS grant folder |

Verify reads Drive. HITL. Nothing sent to TechnoServe without Gideon's yes.

---

## Wire summary (for PNG)

```
SPINE (top band):
N1:Call → N2:RFP → N3:SOI → N4:Full Proposal → N5:Budget → N6:Supporting Docs → N7:Verify → N8:HITL → N9:Park

TOOLS band (below spine):
Drive ──────────────────── N3,N4,N5,N6 (write) + N7 (read)
Gmail ──── N1 (ingest)
Calendar ─ N1 (deadline, parallel)
Box ─────── scratch (no spine attachment)

REPOS band (below tools):
cth-plugin ─────────────── Lane A (spec + harness)
sustenttia-v2@1fc2dfb ──── analog pattern only

BACKENDS band (below repos):
Cognee (live analog) ──── pattern
FalkorDB+Graphiti (coded) ─ pattern / temporal
R2R (absent) ────────────── do not draw as live
Gold LanceDB (coded) ─────── pattern
Chroma (coded/leftover) ──── do not replicate
Neo4j (absent) ──────────── not a CTH store; Falkor is graph DB
```
