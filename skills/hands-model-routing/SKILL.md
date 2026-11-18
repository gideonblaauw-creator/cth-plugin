---
name: hands-model-routing
description: >-
  Use when ticketing Cursor Cloud Hands or when Gideon asks which model to use.
  Default composer-2.5 with Fast OFF for every Hands launch.
---
# Hands model routing

Grok Bot coordinates. File, research, code and copy work goes to Cursor Cloud Hands.

## Emergency Token Mode: EXPIRED
Emergency Token Mode (Gideon GO 27 Oct 2026) ended at the Cursor Ultra reset on 13 Nov 2026. Its rules no longer apply, except the ones kept below as normal rules. Gideon confirmed this on 17 Nov 2026 after the protocol review. Its old line "Routines launch no Hands" is withdrawn.

## Model (HARD)
- Every Hands launch uses `composer-2.5` with Fast OFF (`model_params: {fast: false}`). This includes repo code builds. Put it in the launch template and do not rely on memory.
- Grok models are forbidden in Hands.
- Mechanical work can use a cheaper non-Cursor model only if Gideon approves it for that job.
- OpenCode Kimi only when Gideon says OSS.

## Hold
Sonnet, Opus, Grok, Fable, Sol, GPT high tiers, Auto-as-a-spend, Max mode, Fast ON and silent upgrades: HOLD and flag Gideon.

## Agent size (kept from Emergency mode)
- One job = one fresh, small agent with an exact file list and a read budget.
- Prefer a new small agent per revision over long resume chains. A resume re-reads the whole history. If one agent gets more than about 5 follow-ups, cancel it and ticket a fresh one.
- No nice-to-have builds without Gideon's GO when the Cursor Models bar is above about 85%.

## Lanes
- Lane A repo: allowlist repo, Cursor cloud VMs.
- Lane B packs: `{type: machine, name: vps}`, no `repo_url`. One writer at a time on the same VPS path.

## Parallel Hands
One Hands = one artifact + one acceptance check, with exclusive write targets. Run independent jobs in parallel, about 3-5 live per workstream. Cancel and re-ticket a Hands that runs more than 30 min with no shippable result.

## Routines

Target state (Gideon, 7 Nov 2026, ops channel lock **18 Nov 2026**): routines run as deterministic scripts or Hands. **Every run result** is written to the audited `run_log` through the n8n **`CTH-OPS · Core · log-run`** sub-workflow. **Alerts and approvals** go to the **CTH_OPS** Slack channel on the **existing CTH Slack workspace (Slack Free)** through **`CTH-OPS · Core · notify-ops`**. **Telegram** is on hold and is used only if Gideon reopens it. **n8n-li** is the system of record for schedules and execution logs.

Infrastructure owns the migration. **Cutover gate:** run old Grok routines side by side with the Slack replacements until you log **three good runs**, then get **Gideon's OK** before you remove Telegram from any workflow. Do not disable an old routine before its replacement is verified.