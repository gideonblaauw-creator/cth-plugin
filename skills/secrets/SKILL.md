---
name: secrets
description: >
  Secrets protocol — store, rotate, scan, recover API keys and credentials. Use
  when: secrets, API keys, .env, tokens, credential rotation. Claude Desktop
  only.
license: MIT
metadata:
  version: "2.1.0"
  category: "infrastructure"
---

# Secrets Management Protocol

You are the secrets guardian for all CleantechHUB projects. Every time you handle, reference, create, or encounter a credential, API key, token, password, or sensitive value, follow this protocol without exception. Violations can expose infrastructure, revoke service access, or compromise user data.

## Core Rules — Memorize These

1. NEVER commit secrets to git — not even temporarily, not even in a "test" branch, not even if you plan to remove them in the next commit. Git history is permanent unless explicitly rewritten.
2. NEVER echo, print, cat, or log secrets in plain text. Do not include them in Bash output, SendUserMessage calls, Slack messages, or any tool output. If you need to verify a secret exists, check its length or first/last 4 characters only.
3. NEVER hardcode secrets in source files — not in Python, JavaScript, HTML, Docker Compose, Caddyfile, or any other file that will be tracked by version control.
4. ALWAYS use environment variables or a secrets manager to inject secrets at runtime.
5. ALWAYS add `.env` to `.gitignore` before creating any `.env` file. Verify this first — do not assume it is already there.
6. NEVER share secrets between projects unless they genuinely require the same credential. Each project gets its own API keys where possible.
7. NEVER store secrets in project docs, Confluence pages, Notion databases, or any collaborative document. Use a dedicated secrets manager or encrypted storage only.

## Standard Secret Storage

### For VPS Projects (OVH Server)

The CleantechHUB VPS hosts multiple services via Docker Compose. Each service has its own `.env` file:

- Store secrets in `.env` files on the VPS filesystem, never in the git repository.
- Set file permissions immediately after creation: `chmod 600 .env` — this restricts read/write to the file owner only.
- Reference secrets in `docker-compose.yml` using `env_file: .env` or individual `environment:` entries that reference the `.env` file.
- For shell scripts that need secrets, source the `.env` file: `set -a; source .env; set +a`.
- Keep a `.env.example` file in the repository with placeholder values showing the expected variable names and format, but never actual values. Example:

```
# .env.example — copy to .env and fill in real values
BOOKSTACK_DB_PASSWORD=changeme
CADDY_CLOUDFLARE_API_TOKEN=your-cloudflare-token-here
CHROMA_AUTH_TOKEN=generate-a-random-token
```

### For Local Development

- Use `.env.local` files (gitignored by most frameworks by default — verify the entry exists).
- For team sharing, use a password manager (1Password, Bitwarden) with a shared vault. Never send secrets via Slack, email, or messaging.

### For CI/CD Pipelines

- Use the platform's built-in secret storage: GitHub Actions secrets, GitLab CI/CD variables, or equivalent.
- Never pass secrets as command-line arguments — they appear in process listings (`ps aux`) and shell history.
- Never encode secrets in CI/CD pipeline URLs or webhook payloads.
- For GitHub Actions specifically, use `${{ secrets.SECRET_NAME }}` syntax and ensure the secret is configured in the repository or organization settings.

### For MCP Connectors and Cowork

- MCP connector credentials are managed by the connector's OAuth flow — do not extract, store, or manually manage these tokens.
- If a connector's auth fails, guide the user through re-authentication via connector settings.

## Secret Rotation Checklist

When rotating a key, follow every step in order. Do not skip steps.

1. **Generate the new key/token** from the service provider's dashboard or API. Do not reuse old keys or derive new keys from old ones.
2. **Update the `.env` file** on all relevant systems (VPS, local dev environments, CI/CD). Use SSH to update VPS files directly; do not commit the change.
3. **Restart services** that use the rotated key. For Docker services: `docker compose restart <service>`. For systemd services: `systemctl restart <service>`.
4. **Verify services work** with the new key. Run a health check or manual test to confirm the service is operational. Use Doctor_Bot if available.
5. **Revoke the old key** at the service provider. Do this only after confirming the new key works — revoking first creates a window where nothing works.
6. **Update the `.env.example`** if the variable name or format changed.
7. **Update the key inventory** (see below) with the new rotation date.
8. **Notify affected team members** that the key was rotated, without sharing the new value in the notification.

## Leak Recovery Procedure

If a secret is exposed — committed to git, logged in output, posted in Slack, or otherwise visible to unauthorized parties — execute this procedure immediately. Speed matters; every minute of exposure increases risk.

1. **Immediately revoke** the exposed credential at the service provider. Do not wait to generate a replacement first — revoke now, fix later.
2. **Generate a replacement** credential and deploy it following the standard storage procedures above.
3. **Audit for unauthorized access** during the exposure window. Check the service provider's access logs, API call logs, and billing dashboard for unexpected activity.
4. **Clean git history** if the secret was committed. Use BFG Repo-Cleaner (preferred) or `git filter-branch` to remove the secret from all commits, then force-push and notify all collaborators to re-clone.
5. **Rotate any related credentials** that share the same access scope — if a database password leaked, also rotate application-level tokens that connect to that database.
6. **Document the incident** — record what was exposed, when, how, and what remediation was taken. Store in a private incident log, not a public repository.

## Key Inventory

Maintain an inventory of which secrets exist, where they are stored, and when they were last rotated — without recording actual values.

Track: secret name, service/provider, storage location, dependent projects, last rotation date, rotation frequency, and owner.

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

Before every commit, scan for accidentally included secrets:

- Use `git diff --cached` to review staged changes.
- Use `trufflehog`, `gitleaks`, or `detect-secrets` to scan repository history.
- If you find a secret in the codebase during any task, stop and execute leak recovery before continuing.

## When Creating New Projects

1. Create `.env.example` with required variable names and placeholder values.
2. Verify `.env` is in `.gitignore`.
3. Generate strong, unique credentials (minimum 32 chars for tokens, 20 for passwords).
4. Store in the appropriate `.env` file with correct permissions.
5. Add entries to the key inventory.
6. Test that the service authenticates correctly.

For secret categories, rotation schedules, and inventory templates, see references/.
