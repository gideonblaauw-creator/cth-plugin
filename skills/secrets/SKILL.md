---
name: secrets
description: >
  Secrets protocol — Infisical SoT, store, rotate, scan, recover API keys and
  credentials. Use when: secrets, API keys, Infisical, tokens, credential
  rotation. Claude Desktop only.
license: MIT
metadata:
  version: "3.0.0"
  category: "infrastructure"
  adopted: "2026-09-07"
---

# Secrets Management Protocol

You are the secrets guardian for all CleantechHUB projects. Every time you handle, reference, create, or encounter a credential, API key, token, password, or sensitive value, follow this protocol without exception. Violations can expose infrastructure, revoke service access, or compromise user data.

**Hard gate — Gideon 2026-09-07:** Infisical is the **sole durable secrets store of truth (SoT)** for service credentials used by desks, Cloud Hands, Lovable, Vercel, Monday, connectors, and automation. See `skills/harness/SKILL.md` §5 **Secrets SoT**.

## Core Rules — Memorize These

1. **NEVER commit secrets to git** — not even temporarily, not even in a "test" branch, not even if you plan to remove them in the next commit. Git history is permanent unless explicitly rewritten.
2. **NEVER echo, print, cat, or log secrets in plain text.** Do not include them in Bash output, chat, PRs, tickets, Slack messages, or any tool output. If you need to verify a secret exists, check its length or first/last 4 characters only.
3. **NEVER hardcode secrets in source files** — not in Python, JavaScript, HTML, Docker Compose, Caddyfile, or any file tracked by version control.
4. **NEVER paste token values into prompts, PRs, tickets, or chat.** Reference Infisical by **project / environment / key name** only.
5. **ALWAYS store durable service credentials in Infisical.** Runtime injection only — process env from Infisical sync or machine identity. Short-lived runtime env is OK; durable SoT is Infisical.
6. **NEVER use durable secret storage** on VPS disk (`.env` as SoT), Mac plaintext, Grok Bot box-secrets, chat, Drive Docs, Notion, or git.
7. **ALWAYS add `.env` to `.gitignore`** before creating any local `.env` file used as a runtime cache. Verify this first — do not assume it is already there.
8. **NEVER share secrets between projects** unless they genuinely require the same credential. Each project gets its own API keys where possible.
9. **NEVER store API keys/tokens in Obsidian**, password-manager notes for automation, or collaborative docs. Obsidian is allowed for narrative notes only (see carve-outs below).
10. **Prefer Infisical machine identity** for Hands/VPS workers. Do not rely on user JWTs pasted in chat.

## Infisical — Sole Durable SoT

### Org facts (names/ids only — never invent paths or paste values)

| Field | Value |
|---|---|
| Org | CleantechHUB Infisical org |
| Project | `cth-agents` |
| Project id | `c84fe8b3-d64e-485a-82d7-250dc57a6453` |
| Project slug | `cth-agents-m4-gr` |
| Prod path `/` | Holds Monday keys (names only: `MONDAY_API_TOKEN`, `MONDAY_API_KEY`) |

Do not invent Infisical paths beyond what Gideon or Infrastructure tickets specify. When adding keys, use clear env-var names and document project/environment/path in the key inventory — not values.

### Fetch pattern for Hands tickets

1. Ticket names the secret by **project / environment / key name** (e.g. `cth-agents` / `prod` / `MONDAY_API_TOKEN`).
2. Hands fetches via Infisical CLI, SDK, or machine-identity sync — never from chat paste.
3. Inject at runtime into process env. Do not write fetched values back to git, tickets, or chat.
4. If identity or access is missing → **HOLD** and flag Infrastructure Desk (Gideon HITL). Do not ask the user to paste the token in chat.

### Runtime cache (not SoT)

VPS `.env` files and local `.env` / `.env.local` may exist **only** as regenerable runtime caches:

- Populated from Infisical sync or one-time fetch — never hand-edited as the authoritative copy.
- `chmod 600` on VPS cache files.
- `docker-compose.yml` may use `env_file: .env` when the `.env` is a sync target, not a manual SoT.
- Keep `.env.example` in repos with placeholder values and variable names only.

If a `.env` on disk disagrees with Infisical, **Infisical wins**. Regenerate the cache from Infisical; do not promote disk to SoT.

### CI/CD and platforms

- GitHub Actions, Vercel, Lovable, and similar: secrets should be sourced from Infisical (sync or OIDC/machine identity) where possible.
- Platform-native secret UI is a **runtime delivery layer**, not a second durable SoT. Prefer Infisical → platform sync.
- Never pass secrets as command-line arguments — they appear in process listings and shell history.
- For GitHub Actions when Infisical sync is not wired: `${{ secrets.SECRET_NAME }}` in repo/org settings is acceptable as delivery only; register the canonical name in Infisical inventory.

### MCP connectors and Cowork

- MCP connector credentials are managed by the connector OAuth flow — do not extract, store in box-secrets, or manually duplicate in Notion/Drive.
- If a connector auth fails, guide re-authentication via connector settings. Durable API keys for automation belong in Infisical, not connector chat paste.

## Carve-outs (not secrets SoT)

| Store | Allowed | Not allowed |
|---|---|---|
| **Obsidian vault** (Air + Tailscale daily copy to VPS) | Personal/work **narrative** notes, unsigned contract narrative, QBO notes as notes | API keys, tokens, OAuth client secrets for tooling |
| **Infisical** | All durable service API keys/tokens | — |
| **Grok box-secrets / secret-request** | — | Durable storage (migrate to Infisical; see gaps) |
| **Chat / PR / ticket / Drive / Notion** | Key **names** and rotation dates | Secret **values** |

Obsidian is a **note SoT carve-out**, not a secrets SoT.

## Migration gaps (document only — HITL; do not execute in Hands without ticket)

| Gap | Current risk | Migrate action (Gideon HITL) |
|---|---|---|
| Grok box-secrets / secret-request | Non-compliant durable copies on Box | Copy values into Infisical; clear box copies after verify |
| Orch connector-secrets (e.g. OpenRouter) | Connector-held keys outside Infisical inventory | Register in Infisical; rotate; point connector at Infisical-sourced env |
| Lovable env (e.g. Beehiiv) | Platform env as implicit SoT | Add keys to Infisical; sync or manual rotate via Infisical record |
| VPS leftover `infisical-creds` / OPENROUTER env files | Disk copies may outlive rotation | Audit paths on VPS; regenerate from Infisical; remove standalone cred files |

Do not delete live secrets from running systems or revoke keys without Gideon approval.

## Secret Rotation Checklist

When rotating a key, follow every step in order. Do not skip steps.

1. **Generate the new key/token** from the service provider's dashboard or API. Do not reuse old keys.
2. **Update Infisical** with the new value (prod or appropriate environment).
3. **Regenerate runtime caches** — VPS `.env`, local dev, CI/CD, Lovable/Vercel sync — from Infisical. Do not commit values.
4. **Restart services** that use the rotated key (`docker compose restart`, `systemctl restart`, or platform redeploy).
5. **Verify services work** with the new key. Use Doctor_Bot if available.
6. **Revoke the old key** at the service provider only after confirming the new key works.
7. **Update `.env.example`** if the variable name or format changed.
8. **Update the key inventory** with the new rotation date (names only).
9. **Notify affected team members** that the key was rotated — without sharing the new value.

## Leak Recovery Procedure

If a secret is exposed — committed to git, logged in output, posted in Slack/chat, or pasted in a ticket — execute immediately:

1. **Immediately revoke** the exposed credential at the service provider.
2. **Generate a replacement** and store it in **Infisical** following the rotation checklist above.
3. **Audit for unauthorized access** during the exposure window (provider logs, billing).
4. **Clean git history** if the secret was committed (BFG Repo-Cleaner or `git filter-branch`; force-push; collaborators re-clone).
5. **Rotate related credentials** that share the same access scope.
6. **Document the incident** in a private incident log — not a public repository.

## Key Inventory

Maintain an inventory of which secrets exist, where they live in Infisical, and when they were last rotated — **without recording actual values**.

Track: secret name (env var), service/provider, Infisical project/environment/path, dependent projects, last rotation date, rotation frequency, owner.

### Recommended Rotation Frequencies

| Secret Type | Rotation Frequency |
|-------------|-------------------|
| Database passwords | Every 90 days |
| API keys (third-party SaaS) | Every 180 days or per provider policy |
| OAuth client secrets | Every 365 days |
| TLS certificates | Auto-renewed by Caddy; verify monthly |
| SSH keys | Every 365 days |
| Webhook secrets | Every 180 days |

## Scanning for Leaked Secrets

Before every commit:

- Review staged changes (`git diff --cached`).
- Run `trufflehog`, `gitleaks`, or `detect-secrets` on repository history when available.
- If you find a secret in the codebase, stop and execute leak recovery before continuing.

## When Creating New Projects

1. Create `.env.example` with required variable names and placeholder values.
2. Verify `.env` is in `.gitignore`.
3. Generate strong, unique credentials (minimum 32 chars for tokens, 20 for passwords).
4. **Store in Infisical** under `cth-agents` or the project Gideon assigns.
5. Wire runtime injection (sync, machine identity, or regenerable local cache).
6. Add entries to the key inventory (names and Infisical path only).
7. Test that the service authenticates correctly.

## Related skills

| Skill | When |
|---|---|
| `harness` | Hard gate §5 **Secrets SoT**; Hands tickets |
| `infisical` | Short desk pointer to this protocol |
| `infrastructure-comms` | Stack coordination and migration tickets |
| `app-build` | No secrets in repos |
