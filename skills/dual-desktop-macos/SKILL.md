---
name: dual-desktop-macos
description: >
  Gideon's personal workflow skill — covers (1) his dual-desktop macOS identity
  isolation (CleantechHUB Desktop 1 / Run Up Holdings Desktop 2 with separate
  Claude Desktop, Claude Code, and Chrome profiles) and (2) his CleantechHUB
  infrastructure deployment rule: every long-running thing Claude builds for
  CleantechHUB goes on the existing OVH VPS alongside the BookStack container,
  not a new host. Trigger when the user mentions Desktop 1, Desktop 2, Chrome CTH,
  Chrome Run_Up, dual-instance Claude Desktop / Code setup, profile 14 vs
  profile 9, `--user-data-dir` / `CLAUDE_CONFIG_DIR` isolation, or identity
  cross-contamination issues. ALSO trigger whenever Claude is about to propose or
  deploy infrastructure for CleantechHUB — databases, APIs, queues, schedulers,
  MCP servers, PDF renderers, webhooks, anything long-running — so the default is
  "put it on the CTH VPS" rather than "spin up something new." Personal to
  Gideon's machine.
---

# Dual-Desktop macOS Skill (Personal)

Two parts:

1. **Client-side identity isolation** — how Gideon separates CleantechHUB and Run Up work on one Mac (§§1–9).
2. **CleantechHUB infrastructure conventions** — where Claude-built deliverables get deployed (§10).

---

Gideon's MacBook Air runs **two fully isolated work environments** on one machine, mapped
to two macOS Desktops (Mission Control Spaces):

| Desktop | Identity | Anthropic Account | Chrome Profile |
|---|---|---|---|
| **Desktop 1** | CleantechHUB + Private | Personal / CleantechHUB | Profile 14 (`gideon.blaauw@cleantechhub.net`) |
| **Desktop 2** | Run Up Holdings | Run Up Holdings | Profile 9 (`gideon@runupholdings.com`) |

Inspired by the "how I forced my Mac to run 2 instances" pattern (helloai.substack.com),
adapted for Claude Desktop + Claude Code + Chrome.

---

## 1. What's isolated

Each desktop has its own:
- **Claude Desktop app instance** — separate `--user-data-dir`, separate sign-in,
  separate MCP server configurations, separate chat history
- **Claude Code CLI config** — separate `CLAUDE_CONFIG_DIR`, separate auth tokens,
  separate project histories
- **Chrome wrapper** — separate `--user-data-dir` + `--profile-directory`, launching
  straight into the right Google account
- **macOS Space** — Mission Control desktop; apps pinned to the right space via
  "Assign to This Desktop"

Not isolated (shared machine-wide):
- Filesystem (one home directory)
- Git identity (configured per-repo via `.gitconfig` includes)
- SSH keys (but per-host config in `~/.ssh/config`)
- Anthropic API keys (per-identity, but stored in one `~/.config/anthropic/` unless
  overridden per-session)

---

## 2. Launchers (one-click entry to each environment)

AppleScript wrappers compiled as `.app` bundles live in `/Applications/`:

**Desktop 1 (CleantechHUB)**
- `Claude CTH.app` — launches Claude Desktop with CTH user-data-dir
- `Code CTH.app` — launches Terminal with `CLAUDE_CONFIG_DIR` set for CTH
- `Chrome CTH.app` — launches Chrome Profile 14 directly

**Desktop 2 (Run Up)**
- `Claude Run_Up.app` — Claude Desktop with Run Up user-data-dir
- `Code Run_Up.app` — Terminal with Run Up Code config
- `Chrome Run_Up.app` — Chrome Profile 9 directly

Each `.app` is:
1. Dragged to the Dock
2. Swiped onto the correct Desktop (Mission Control)
3. Right-clicked → Options → **Assign to This Desktop**

This makes the dock icon appear only on the correct Desktop — zero-cognition identity
switching.

---

## 3. The Chrome wrappers (canonical form)

**Chrome CTH (Profile 14):**
```applescript
do shell script "open -na 'Google Chrome' --args \
  --user-data-dir='/Users/gideonblaauw/Library/Application Support/Google/Chrome' \
  --profile-directory='Profile 14'"
```

**Chrome Run_Up (Profile 9):**
```applescript
do shell script "open -na 'Google Chrome' --args \
  --user-data-dir='/Users/gideonblaauw/Library/Application Support/Google/Chrome' \
  --profile-directory='Profile 9'"
```

Both flags are required:
- `--user-data-dir` points to the shared Chrome data folder (where all signed-in
  profiles live)
- `--profile-directory` picks the specific one

Because both profiles are already authenticated, Chrome opens straight into the right
Google account with no login prompt.

**Do not** use `--profile-directory` alone — it will prompt for login. Don't use
separate user-data-dirs per profile — that requires re-authentication in each.

---

## 4. Claude Desktop isolation

Each instance launches with:
```bash
/Applications/Claude.app/Contents/MacOS/Claude \
  --user-data-dir="$HOME/Library/Application Support/Claude-<identity>"
```

where `<identity>` is `CTH` or `Run_Up`. Each has its own:
- `claude_desktop_config.json` (MCP servers, preferences)
- Chat history
- Signed-in Anthropic account
- Local cache

**Config file paths:**
- CTH: `~/Library/Application Support/Claude-CTH/claude_desktop_config.json`
- Run Up: `~/Library/Application Support/Claude-Run_Up/claude_desktop_config.json`

**Backup**: both configs are worth archiving into a private Git repo — MCP connection
setup is fiddly and a rebuild-from-scratch costs an hour.

---

## 5. Claude Code isolation

Each Code instance uses `CLAUDE_CONFIG_DIR`:
```bash
export CLAUDE_CONFIG_DIR="$HOME/.config/claude-cth"   # or claude-run-up
claude
```

The AppleScript wrappers wrap this in a Terminal launch:
```applescript
tell application "Terminal"
  do script "export CLAUDE_CONFIG_DIR=\"$HOME/.config/claude-cth\" && claude"
end tell
```

Per-identity directories contain:
- `auth.json` — Anthropic credentials
- `projects/` — project history
- `settings.json` — user preferences

---

## 6. Working across identities (when you have to)

Sometimes work legitimately crosses identities — e.g. CleantechHUB advising a Run Up
portfolio company. Rules:

1. **Start in the identity that owns the artifact** (if it's a CTH deliverable,
   start in Desktop 1).
2. **Export outputs** to a shared location (Downloads, a neutral Google Drive folder).
3. **Import into the other identity** explicitly — don't copy/paste between windows
   by habit.
4. **Document the handoff** in writing if anyone else is involved. Auditability matters.

---

## 7. Common pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Forgetting `--user-data-dir` on Chrome | Profile picker appears | Edit wrapper to include both flags |
| Only one flag set | Login prompt | See §3 — both `--user-data-dir` AND `--profile-directory` are mandatory |
| Dock icon appears on wrong desktop | Window comes up in the wrong space | Right-click dock icon → Options → "Assign to This Desktop" |
| `CLAUDE_CONFIG_DIR` not exported | Code auth from wrong identity | Always launch via the AppleScript wrapper, not `claude` bare |
| MCP config applied to wrong identity | Cross-contamination | Edit the right `claude_desktop_config.json` — read the path carefully |
| Git identity wrong | Commits as personal / wrong org | Use `.gitconfig` includeIf by directory: `[includeIf "gitdir:~/dev/runup/"]` |
| Same Anthropic account on both desktops | Data bleed | Sign out of the one that's wrong; sign into the right account |

---

## 8. Storage hygiene note

The dual-install doubles Claude Desktop's disk footprint (two user-data-dirs, two VM
bundles if Code is used). See the `mac-storage-hygiene` skill for the quarterly
cleanup routine.

---

## 9. Rebuild from scratch

If a config gets corrupted, the rebuild is roughly:

1. Back up working config from the healthy identity
2. Quit the broken Claude Desktop
3. `rm -rf ~/Library/Application\ Support/Claude-<identity>`
4. Relaunch via the wrapper
5. Sign in with the correct Anthropic account
6. Reinstall MCP servers from backed-up config or from scratch

Expect 30–60 minutes. Full dual-setup from zero is ~2 hours. See the Substack article
(helloai.substack.com/p/how-i-forced-my-mac-to-run-2-instances) for the generic
pattern; Gideon's specifics are in this skill.

---

## 10. CleantechHUB infrastructure — default to the VPS, always

**The rule:** every long-running thing Claude builds for CleantechHUB goes on the existing
OVH VPS, in or alongside the existing CTH container stack. Don't reach for a new hosting
provider by reflex.

This exists because:
- **One place to operate.** One VPS to patch, back up, monitor, pay for.
- **Shared ingress.** Caddy at `/etc/caddy/Caddyfile` handles TLS for every subdomain.
  Adding `rag.cleantechhub.net` is two lines; adding it on Vercel means a new DNS record,
  a new dashboard, a new bill.
- **Shared identity surface.** BookStack's user accounts, API tokens, and SSO already
  work. New services that integrate via API can reuse those tokens.
- **Predictable costs.** €30/mo OVH versus per-service SaaS creep.

### What "on the VPS" means concretely

The CTH deployment on OVH looks like this:

    /opt/bookstack/                 BookStack + MariaDB via docker compose
    /opt/sustenttia-rag/            Chroma DB (MB-0, Sustenttia project)
    /opt/sustenttia-rag/indexer/    one-shot indexer venv
    /opt/sustenttia/credentials.txt credentials vault for Sustenttia pipeline
    /etc/caddy/Caddyfile            single reverse proxy with auto-TLS
    /var/www/reportes/              static HTML copies of generated reports

New things Claude builds for CTH should sit in `/opt/<project-name>/` with their own
docker-compose.yml and their own `.env`, behind a Caddy block. That's the template.

### Decision tree for "where does this live?"

When Claude is about to propose deploying anything — a new MCP server, a queue, a
database, a scheduler, a webhook receiver, a cron job, a PDF renderer, an API gateway —
walk this:

1. **Is it long-running or stateful?** → VPS.
2. **Does it need a domain / TLS?** → VPS + Caddy block (five-line snippet).
3. **Is there an existing container that already does this?** → reuse it; don't
   introduce a duplicate. BookStack's MariaDB can host additional databases. Chroma's
   persistent volume lives at `/opt/sustenttia-rag/data` — one Chroma instance serves
   multiple collections for different projects.
4. **Would it force a second VPS?** → stop, tell Gideon, and discuss before going
   further. Don't quietly introduce a new host.
5. **Is it clearly better as SaaS** (Pipedream for orchestration, Supabase for managed
   Postgres, Buffer for scheduling social media)? → fine to propose, but flag the
   trade-off explicitly (cost, lock-in, data residency) and ask before committing.
6. **Is it serverless (one-off function, no state)?** → still prefer VPS as a small
   systemd unit or a `cron` entry; only reach for Vercel/Cloud Functions with explicit
   approval.

### What this rules out (without asking first)

- ❌ "Let's deploy this to Railway / Render / Fly / Vercel / AWS / GCP."
- ❌ "Let's create a new DigitalOcean droplet for just this."
- ❌ "Let's spin up a managed Postgres on Neon."
- ❌ "Let's use Cloudflare Workers for this little API."
- ❌ Kubernetes. Just no.

All of those are sometimes the right answer — but they require an explicit "yes, not on
the VPS this time" from Gideon first.

### What this actively encourages

- ✅ Add a new `docker compose` service under `/opt/<project>/`.
- ✅ Append a new site block to `/etc/caddy/Caddyfile` and reload Caddy.
- ✅ Reuse BookStack's MariaDB container for a small schema if Postgres overkill.
- ✅ Use `systemd --user` timers or root cron for scheduled tasks — the VPS is already
  running 24/7.
- ✅ Store secrets in `/opt/sustenttia/credentials.txt` pattern (root-owned, chmod 600)
  and pull into `.env` files at deploy time.
- ✅ Keep idempotent deploy scripts (`docker compose up -d` + `caddy reload`) so
  rebuilds from the `/opt/<project>/` folder are trivial.

### When Claude is generating deliverables

Any Claude-built deployment artifact for CTH — docker-compose.yml, Caddyfile snippet,
systemd unit, shell runbook — should assume `/opt/<project>/` layout and Caddy-fronted
TLS by default. If the deliverable targets a different host, call it out loudly in the
README so Gideon catches it in review.

The MB-0 Sustenttia infrastructure pack under `/Users/gideonblaauw/Documents/Claude/Projects/Sustenttia/mb-0-infra/`
is the canonical example of this pattern done right.

---

## 11. Related skills

- `claude-code` — per-identity project conventions
- `claude-cowork` — scheduled tasks live in the Desktop they were created in
- `claude-in-chrome` — use `switch_browser` when both Chrome wrappers are open
- `mac-storage-hygiene` — dual-install disk management
- `google-workspace-cli` — authed to Gideon's personal account; scopes span both identities
- `bookstack` — the anchor container on the CTH VPS; every new service sits next to it
- `dps-dashboard` — uses the Run Up VPS conventions (not CTH); good contrast example
