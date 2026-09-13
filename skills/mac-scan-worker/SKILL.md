---
name: mac-scan-worker
description: >
  Recreate and operate the mac-scan private Cursor worker on Gideon's MacBook Air.
  Trigger on "mac-scan worker", "recreate mac-scan", "My Machines mac-scan",
  "private worker mac-scan", Mac Scan Desk Hands environment, or when a Mac Scan
  ticket needs `{type: machine, name: mac-scan}`. Read before ticketing Hands on
  mac-scan or debugging a dead mac-scan worker.
metadata:
  version: "1.0.0"
  category: infrastructure
  owner: Infrastructure desk c656afb9
  adopted: "2026-08-28"
---

# mac-scan — Private worker runbook

**Owner:** Infrastructure desk c656afb9  
**Machine:** Gideon's MacBook Air only  
**Worker name:** exactly `mac-scan` (Cursor My Machines display name)  
**Desk:** Mac Scan (Grok) — tickets and reviews only  
**Sources:** [Cursor My Machines](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines), [CLI worker parameters](https://cursor.com/docs/cli/reference/parameters), CTH Harness locks in `skills/harness/SKILL.md`

This runbook recreates a **clean** `mac-scan` private worker. It is **not** a vault plant, **not** a Grok desk rewrite, and **not** a jump host to the VPS or Archive.

## 1. Why this runbook exists

The Cursor private worker named `mac-scan` on the Air was never set up correctly (environment problems).

**Evidence (do not invent extra causes):**

| bc-id | Outcome |
|---|---|
| `bc-f4ec4040` | Cloud Hands died — status error, no transcript |
| `bc-2d32a8a2` | Cloud Hands died — status error, no transcript |
| `bc-45cfd896` | Cloud Hands died — status error, no transcript |

Symptoms: no vault path, no hello test. Tickets launched against a missing or misconfigured worker fail silently or error with no usable transcript.

## 2. Hard locks (CTH)

| Lock | Rule |
|---|---|
| **Name** | Worker `--name` must be exactly `mac-scan`. |
| **Host** | Runs on the **Air only**. Not the VPS, not Box, not a cloud VM. |
| **Disk** | Worker executes on Air disk. Can read/write paths the Air user can reach. |
| **Local REST** | Worker can reach `127.0.0.1` — Obsidian Local REST API ports **27124** and **27123**. |
| **Not a jump host** | Do **not** use mac-scan to reach `/opt/claude-files`, VPS `gws`, or any remote host. Harness §5 Hands-shift lock. |
| **Not a vault clone target** | Do **not** copy the Obsidian vault into this repo or onto a cloud VM. |
| **Hands environment** | Mac Scan Hands tickets: `environment: {type: machine, name: mac-scan}`. |
| **Worker down** | **HOLD.** Flag Gideon. **No** cloud VM failover. **No** silent retry on default environment. |
| **Desk scope** | Mac Scan desk (Grok) **tickets and reviews only**. Grok = coordination (Token lock 2026-08-26). |
| **Obsidian plugins** | Out of scope for worker setup. Do not install or configure Obsidian plugins in this runbook. |

## 3. What mac-scan is for

mac-scan is a **My Machines** worker ([official docs](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines)):

- A process on the Air opens an **outbound** HTTPS connection to Cursor.
- The agent loop runs in Cursor's cloud; **tool calls** (terminal, file edits, browser, command-based MCP) run on the Air.
- No inbound ports or firewall changes are required.

Use mac-scan when a Mac Scan ticket needs Air-local disk or `127.0.0.1` services (Obsidian Local REST). Do **not** use it for Archive writes, VPS inventory, or Lane B Drive packs.

## 4. Prerequisites (Air)

Before starting the worker:

1. **Air is awake** and on a stable network (Harness gate: Mac often asleep at 10pm/2am — worker must be running when Hands is ticketed).
2. **Obsidian** is running on the Air with Local REST enabled on `127.0.0.1:27124` or `127.0.0.1:27123` [PENDIENTE — confirm active port in Obsidian settings; not in Cursor docs].
3. **Target checkout exists** on Air disk — the git repo Mac Scan tickets will use. Registered repo = git remote of the directory where you start the worker ([official docs](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#how-cursor-picks-your-machine)).
4. **Cursor CLI** installed (`agent --version` succeeds).

Outbound HTTPS required ([official networking table](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#networking)):

- `api2.cursor.sh`, `api2direct.cursor.sh`
- `cloud-agent-artifacts.s3.us-east-1.amazonaws.com` (artifact uploads; session works if blocked, artifacts won't upload)

## 5. Recreate the worker (clean env)

Run on the **Air**, in Terminal, **one command per line**. `agent login` is **not** `agent worker start` (Harness war story §10.3).

### Step 1 — Install CLI (if missing)

```bash
curl https://cursor.com/install -fsS | bash
agent --version
```

Source: [My Machines quickstart](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#1-install-the-cli).

### Step 2 — Sign in

```bash
agent login
```

Browser login is the recommended path for a personal machine ([official docs](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#2-sign-in)). Use the same Cursor account that launches Cloud Hands.

Alternative for headless/automation ([official docs](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#use-an-api-key)):

```bash
agent worker start --api-key "your-user-api-key"
```

Personal user API key from [Cursor Dashboard → API Keys](https://cursor.com/dashboard/api). Service account keys start pool workers only — not mac-scan.

### Step 3 — Preflight (recommended)

From the target checkout directory on the Air:

```bash
cd /path/to/target-checkout
agent worker debug
```

Checks authentication, privacy routing, repo labels, and whether Cursor can see matching workers ([official troubleshooting](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#troubleshooting)).

### Step 4 — Start the worker

From the **same checkout** Mac Scan tickets will target:

```bash
cd /path/to/target-checkout
agent worker start --name mac-scan
```

Official options ([My Machines](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#name-the-machine), [CLI parameters](https://cursor.com/docs/cli/reference/parameters)):

```bash
agent worker start --name mac-scan --worker-dir /path/to/target-checkout
agent worker start --name mac-scan --debug
```

**Keep this process running.** Default: long-lived until you stop it. Closing the terminal stops the worker.

`agent login` and `agent worker start` are separate steps. Do not paste them on one line.

### Step 5 — Confirm in Cursor

Official path ([My Machines quickstart §4](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines#4-run-an-agent)):

1. Go to [cursor.com/agents](https://cursor.com/agents).
2. The machine should appear in the **environment dropdown**.
3. Select `mac-scan` before sending a task.

Environment picker UI labels (e.g. "My Machines", "Remote Control", "Run on") — **[PENDIENTE]** exact label; confirm in your Cursor build. Official docs: "environment dropdown" at cursor.com/agents.

If `mac-scan` does not appear: worker is not running, wrong account, wrong checkout, or auth failed. Run `agent worker debug` on the Air. Do **not** ticket Hands until the machine is visible.

## 6. Hello test (mandatory before first ticket)

Run **on the Air** while the worker process from §5 is still running. This is a **manual smoke test**, not a Cloud Hands ticket.

```bash
hostname
curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:27124/ || true
curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:27123/ || true
```

Then verify Obsidian Local REST returns **vault note titles only** (no full vault export, no file copy):

```bash
curl -sS http://127.0.0.1:27124/vault/ 2>/dev/null | head -c 500
# or port 27123 if 27124 is closed
```

**Pass:** `hostname` prints the Air name; at least one Local REST port responds; title list is non-empty or matches expectation.  
**Fail:** connection refused, wrong host, empty vault path → **STOP**. Fix worker/checkout/Obsidian before ticketing Hands.

**Then STOP.** Do not proceed to Mac Scan file work until Gideon confirms hello pass.

## 7. Ticket mac-scan Hands

Mac Scan Desk writes seven-field tickets per `tickets/TEMPLATE.md`. Hands reads `skills/harness/SKILL.md` and `skills/mac-scan-comms/SKILL.md`.

**Environment field (required for mac-scan):**

```yaml
environment:
  type: machine
  name: mac-scan
```

Pattern matches Harness VPS worker reference: `{type: machine, name: vps}` → mac-scan uses `mac-scan`.

**Model (Token lock 2026-08-26):**

| Job | Model |
|---|---|
| Mechanical copy, inventories, hygiene scripts | `gemini-3.7-flash` |
| Repo / code / build on Lane A | `composer-2.5` (`fast=true`) | Fast ON (t1263u) |
| Review / eval / brand, no model | **HOLD** — flag Gideon |

**Lane:** `github-pr` on the owning repo, or local Air paths per ticket `folder:` — never Archive via mac-scan.

**No bc-id = miss.** Empty bc-id = miss.

## 8. When the worker is down

| Situation | Action |
|---|---|
| mac-scan not in environment dropdown | **HOLD.** Flag Gideon. Restart worker on Air (§5). |
| Hands ticket errors / no transcript | **HOLD.** Flag Gideon. Do not re-launch on default cloud VM. |
| Air asleep or offline | **HOLD.** Flag Gideon. No silent retry. |
| Need Archive or VPS | Ticket worker `vps` (when installed) or Lane A cloud VM — **not** mac-scan. |

## 9. What not to do

- Do **not** use mac-scan as a jump host to VPS, Archive, or `gws`.
- Do **not** clone the Obsidian vault into `cth-plugin` or a cloud VM.
- Do **not** failover Mac Scan tickets to the default cloud VM when mac-scan is down.
- Do **not** install Obsidian plugins as part of worker recreation.
- Do **not** conflate `agent login` with `agent worker start`.
- Do **not** ticket Hands until §6 hello test passes and `mac-scan` is visible at cursor.com/agents.

## 10. Related skills

| Skill | Role |
|---|---|
| `skills/mac-scan-comms/SKILL.md` | Mac Scan Desk comms protocol |
| `skills/harness/SKILL.md` | Harness locks, lanes, Token lock |
| `skills/infrastructure-comms/SKILL.md` | Infrastructure Desk coordination |
| `skills/doctor-bot/SKILL.md` | VPS health — not mac-scan |

## 11. Official references

- [My Machines](https://cursor.com/docs/cloud-agent/self-hosted-guides/my-machines)
- [Choose where Cloud Agents run](https://cursor.com/docs/cloud-agent/self-hosted-guides/choose-runtime)
- [CLI `worker` parameters](https://cursor.com/docs/cli/reference/parameters)
- [Cloud Agent setup](https://cursor.com/docs/cloud-agent/setup) (managed cloud VM — **not** mac-scan)
