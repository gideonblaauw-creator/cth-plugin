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
