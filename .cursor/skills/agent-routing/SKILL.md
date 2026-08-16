---
name: agent-routing
description: >
  Decide whether a task stays with the Grok Bot fleet (Chief-of-Staff Bot
  routing to specialist Bots on a shared cloud computer) or gets mirrored
  to a Cursor IDE background agent running Sonnet for cheap, high-volume
  daily execution. Trigger on "which bot should handle this", "route this
  task", "save Grok Bot quota/usage", "run this in Cursor instead",
  "mirror this bot to Cursor", "daily tasks vs high thinking", or whenever
  Grok Bot's weekly usage is running low.
---

# agent-routing

This file is a Cursor discovery stub. The playbook source of truth is `skills/agent-routing/SKILL.md`.

1. Read `skills/agent-routing/SKILL.md` and `skills/agent-routing/references/wire-diagram.md` before doing the work.
2. Follow that playbook. Do not invent a parallel routing policy in this stub.
3. Do not mirror `skills/secrets` into Cursor under any circumstances — see the hard boundary in the canonical playbook.
