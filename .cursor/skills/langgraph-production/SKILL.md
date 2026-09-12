---
name: langgraph-production
description: >
  Builds production LangGraph agent graphs with HITL interrupt, Notion
  Understanding Lab, and LangSmith. Use when: langgraph: yes, production
  agent graph, client agent graph, HITL interrupt. Do not use when:
  OpenCode OSS experiments or grant packs.
---

# langgraph-production

This file is a Cursor discovery stub. The playbook source of truth is `skills/langgraph-production/SKILL.md`.

1. Read `skills/langgraph-production/SKILL.md` before building a production or client agent graph.
2. Follow that playbook. Do not invent parallel rules in this stub.
3. Require `langgraph: yes` on the ticket. Launch Composer 2.5 Fast ON for builds (t1242u). OpenCode is OSS experiments only.
4. Copy per-build `lab_notion:` URLs only. Never reuse Scanner pages for other products.
5. No secrets in the repo or chat. HITL before any client deploy.
