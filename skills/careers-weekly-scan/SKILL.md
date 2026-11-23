---
name: careers-weekly-scan
description: >
  Run the Careers desk weekly job-opening scan for Gideon Blaauw. Use when Careers
  schedules the scan, refreshes boards, or writes /workspace/careers-scan output.
  Never apply, send email, or contact recruiters (HITL).
metadata:
  version: "1.0.0"
  category: operations
  desk: Careers
  owner: Orchestrator 5dc64ea4
---

# Careers weekly scan

Gideon Blaauw Careers desk. Reports to Orchestrator. Scan only; never submit applications or outbound contact.

## When to run

- Run weekly on Hands (protocol-review 17 Nov 2026).
- Ticket craft to Cursor Cloud Hands. One job per wave; about 60 steps.

## Target boards

Check these sources each pass (add only with Gideon GO):

| Source | URL / ID | Notes |
| --- | --- | --- |
| Impactpool | impactpool.org job pages | Listing search may be dynamic; verify individual job IDs |
| UN careers | careers.un.org | Public postings |
| GGGI | Greenhouse job-boards | Colombia / LAC roles |
| WRI | wri.org/careers | Alianzas / LATAM when listed |
| New Energy Nexus | Workable jobs.md | Usually non-LATAM |
| Climate-KIC | climatekic.recruitee.com | Often empty board |
| Halcyon | halcyonaccelerator.org/careers | Usually US-based |
| NDC Partnership | ndcpartnership.org | Partial LATAM signal |
| RELP | relp.ngo/careers | Partial parse |
| Devex, ReliefWeb, Idealist, UNGM, CAF, IDB/IDB Lab, Climatebase, RMI, Acumen, Village Capital | Per prior scans | Mark **Not confirmed** when blocked (403, Cloudflare, 404) |

Do not use LinkedIn login or box browser for LinkedIn. Use the 20 Oct 2026 connections export or public pages only.

## Filters and scoring

Use Gideon profile: climate finance, cleantech ecosystems, LATAM, innovation/venture building, engagement/partnership leadership; Dutch passport; Colombian residency; US roles need visa sponsorship.

Score each role 0–5 on:

1. Sector fit  
2. Region (LATAM or remote-LATAM)  
3. Seniority  
4. Role type  
5. CTH conflict risk (5 = no conflict)

**Qualify:** posting still open; deadline in the future or rolling; total at least 15/25.

**Picks:** at most 5 qualified roles per scan.

Skip rows already on the applications tracker unless status or deadline changed.

## Output path and format

Write:

`/workspace/careers-scan/scan-YYYY-MM-DD.md`

Use this structure:

1. Title line with scan date (America/Bogota).  
2. Profile and scoring rules (short).  
3. **Not done** line: no application, email, or contact.  
4. **Sources checked** table: source, result (OK / Partial / Not confirmed).  
5. **Picks** table: role, org, location, five scores, total, deadline, URL, fit flags.  
6. **Near-misses** bullets.  
7. **Tracker deadlines** window table when relevant.

Archive copies: `/opt/claude-files/Projects/Careers/` plus Drive. GitHub-first for code only; CV and references stay out of public repos.

## HITL

- Never submit an application.  
- Never send email or message to recruiters or hiring teams.  
- Never contact a candidate channel without Gideon explicit yes.  
- Desk drafts answers in Gideon's voice only inside HITL review.

## Escalation

Escalate to Gideon when:

- A pick scores 20/25 or higher and deadline is within 72 hours.  
- A source stays **Not confirmed** for three consecutive scans and blocks picks.  
- CTH conflict risk is unclear (score below 5 on conflict column).

Use inline GO / NO GO widgets per `HARNESS.md` (22 Nov 2026). Log bc-ids to Orchestrator.