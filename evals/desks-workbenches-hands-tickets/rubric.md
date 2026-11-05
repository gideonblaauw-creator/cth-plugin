# Rubric — desks-workbenches-hands-tickets (harness)

Score each criterion **0** / **1** / **2**. Max **16**.

| ID | Criterion | Source |
|----|-----------|--------|
| H1 | Correctly separates **Desk** (subject, tickets, review), **Workbench** (channel I/O), **Cloud Hands** (writes files), **Tools** (not chats) | harness §2 |
| H2 | Ticket includes required fields: `desk`, `folder`, `done-when`, `model`, `files`, `read-budget`, `lane`, `hitl`, `reviewer` | harness §2 Tickets |
| H3 | First-draft file packs route to Cloud Hands with bc-id — not local Grok grind | hands-ticket-hard |
| H4 | Workbench used only for channel I/O when Hands cannot; not for research/crawl/pack grind | Workbench exception |
| H5 | HITL before send/post/pay; ready-ping carries PR/URL/bc-id/paths | harness §5 |
| H6 | Maker ≠ checker on high-risk; Token budget protocol respected (`composer-2.5`, `fast=true`) | Token budget protocol |
| H7 | Scoped reads: named paths, read budget, no whole-repo crawl; big-file rule (200 KB) | Token budget protocol §3–4 |
| H8 | Drive/GitHub/Buffer/Monday/Notion classified as Tools, not Workbenches | harness §2 |

**Pass threshold:** ≥12/16 and no must-not violation.
