# CleantechHUB GTM — products & outreach (read-only findings)

**Date:** 2026-11-19 (UTC)  
**Scope:** READ-ONLY reconnaissance. No email sent, no DNS/deploy, no Resend settings changed.  
**Evidence roots:** `/opt/claude-files` → `/mnt/data/claude-files`, `/home/debian/src/cth-plugin`, `/home/debian/cth-nexus`, `/home/debian/cth-datalab`, `/home/debian/linkedin-connections-sync`

---

## 1. GreenTec / PREVEC project pages

### Where assets live

| Kind | Path / URL | Notes |
|------|------------|--------|
| **GreenTec one-pagers (2026-11)** | `/mnt/data/claude-files/Projects/CTH-Brochures/greentec-2026-11/` | Versions `v1`–`v4.1`; ticket `fix-ticket-onepagers-v2.md` states **client-agnostic** copy (no “GreenTec” in deliverables). |
| **Latest build** | `.../greentec-2026-11/v4.1/` | `pages/` (6× HTML), `assets/onepager.css`, `pdf/`, combined `cth-project-onepagers.pdf` (~1.49 MB). |
| **PREVEC III (GIZ)** | `/mnt/data/claude-files/Projects/GIZ-PREVEC3/` | CV/PDF outputs; **not** the same as the six CTH project one-pagers. |
| **GitHub `gideonblaauw-creator`** | `https://github.com/gideonblaauw-creator/cth-plugin` | No `greentec` code hits in repo search (`incomplete_results`). No dedicated `greentec` repo found via code search. **`gh repo list`:** not authenticated on VPS (`gh auth status` → not logged in). |
| **Live subdomains (curl -sI)** | `https://greentec.cleantechhub.net` | **PENDIENTE** — no HTTP response headers captured (likely NXDOMAIN / no route). |
| | `https://products.cleantechhub.net` | **PENDIENTE** — same. |
| **Analogue live pattern** | `https://decks.cleantechhub.net/<slug>/` | Caddy → Appwrite sites on VPS (`docs/infra/caddy/decks.cleantechhub.net.caddy`); OAuth on most slug paths (302 → `auth.cleantechhub.net`). |

### Style & layout (v4.1 sample: `pages/01-giz.html`)

- **Format:** Single-page **A4 print HTML** (`@page size: A4 portrait`), not reveal.js / not Next.js.
- **Structure:** Hero image band + scrim (project number, kicker, logo), eyebrow, H1, meta line, 4-tile stats row, two-column “What we did” / second column, footer source line.
- **Colours (onepager.css):** Primary text/header `#0C498A`, hero background `#0C498A`, body white — **blue brochure palette** (differs from `skills/cleantechhub-brand` green `#2D6A4F` / Inter).
- **Fonts:** `Open Sans` 10.5pt (Google-style stack in CSS).
- **PDF:** Yes — `v4.1/cth-project-onepagers.pdf` (combined, 6 pages).

### Stack & hosting

| Layer | Finding |
|-------|---------|
| Build | Static HTML + local CSS; no framework. |
| Deploy target (inferred) | Same family as **decks.cleantechhub.net** (Caddy + `/opt/cth-decks` / Appwrite upstream), or future **`products.cleantechhub.net`** — **not live in this pass**. |
| Vercel | Used for **datathon** demos (`*.vercel.app`), not for GreenTec one-pagers in tree. |

---

## 2. Email / contact base (~3,000+ claim)

### Summary

| Metric | Count | Status vs “3,000+ emails” |
|--------|------:|---------------------------|
| **Unique deliverable emails** (deduped across primary CSVs + SQLite) | **1,250** | **Below 3,000** — **PENDIENTE** larger master file not found on disk |
| **LinkedIn `li_connections` rows** | **9,838** | Explains “thousands” of **contacts**, not unique emails |
| **Rows with non-empty email in SQLite** | **365** | |
| **Distinct emails in SQLite** | **364** | |

### Files examined (paths, rows, unique emails, columns — no PII)

| Path | Rows | Unique emails | Source (inferred) | Consent / opt-out columns |
|------|-----:|--------------:|-------------------|---------------------------|
| `/home/debian/linkedin-connections-sync/processed/Connections-2026-10-20.csv` | 9,863 | 364 | LinkedIn Connections export (Oct 2026) | **None** (`First Name`, `Last Name`, `URL`, `Email Address`, `Company`, `Position`, `Connected On`) |
| `/home/debian/linkedin-connections-sync/li_connections.sqlite` (`li_connections`) | 9,838 | 364 | Ingested connections DB | **No consent fields** |
| `/home/debian/cth-matters/enrichment/ccb-cluster-energia-2026-09-25/00-assemble/union.csv` | 2,029 | 654 | CCB cluster energía assembly (SECOP/CCB arms) | **None** (`email`, `email_type`, …) |
| `.../10-workshop-abc/monday_feed_universe.csv` | 2,113 | 804 | Monday.com feed export | **No marketing consent**; legal-rep columns only (`email_rep_legal`, `nombre_representante_legal`, …) |
| `/mnt/data/claude-files/Projects/CCB-Bucaramanga/exports/workshop-2026-10-08/monday_feed_universe.csv` | (mirror) | — | Same Monday export on claude-files | Same |
| `/home/debian/mail-finder/cth-teaser-2026-10-22/emails_v2.csv` | 58 | 66 | Enriched/guessed emails | `status`, `method`, `guess_status` — **not Ley 1581 authorization** |
| `/mnt/data/claude-files/Projects/CCB-Bucaramanga/CCB-Cluster-Energia-profile-fit-open-2026-09-25.csv` | 2,115 | 0 | Company profile fit | No email column in header set |

### Segments lacking documented consent (for outreach)

- **All LinkedIn-derived rows** (9,838 contacts; 364 emails) — connection export, **no autorización de tratamiento / marketing opt-in** field.
- **CCB / Monday universe (~2.1k rows)** — business/event pipeline; **no explicit consent column**.
- **SECOP/union enrich (~2k rows)** — **no consent**.
- **Mail-finder guessed addresses** — **high risk** without verified consent.
- **Resend audience segments** (names only, API): `General`, `Founders`, `Investors`, `ruta-verde-*`, `CCB Clúster Energía — *` — **consent provenance not documented on disk** (**PENDIENTE** per-segment contact counts without PII export).

---

## 3. Five product surfaces (existing work)

| Product | Live URL (curl -sI) | Repo / path | Stack / notes |
|---------|---------------------|-------------|---------------|
| **Datatón / Datathon** | `https://datathon.data.cleantechhub.net/` → **200** (Caddy, static) | `cth-datalab/app/dataton/` (draft; slug `/dataton` not approved deploy) | Static portal on VPS; Vercel: `https://ccb-datathon-energia.vercel.app/` **200**, `https://marlene-datathon-cth.vercel.app/` **200** |
| **Earth Observatory** | `https://decks.cleantechhub.net/earth-observatory/` → **302** OAuth | Brand spec: `src/cth-plugin/docs/html-deck-protocol.md`, `docs/brand-rules.md`; Caddy route in `docs/infra/caddy/decks.cleantechhub.net.caddy` | HTML deck / EO v3 palette (Titillium Web + Open Sans); **PDF brand book path referenced in docs** — `brand/earth-observatory/...` **PENDIENTE** in checked tree |
| **Programs** | `https://programs.cleantechhub.net/` → **302** → Docmost share; share URL **200** | Docmost (not in repo) | `server: Caddy`; public share id `01a1eb6a-528e-7fcb-8c55-e3fd7623306e` |
| **LMS** | `https://academy.cleantechhub.net/` → **200** (`server: openresty`, Moodle session cookie) | `src/cth-plugin/tools/moodle-ro/` (read-only API client) | Moodle at **academy** subdomain (not `lms.` / `moodle.` — **no response**) |
| **Nexus** | `https://nexus.cleantechhub.net/` → **301** `/p/home`; `/p/home` **200** | `cth-nexus/` (separate tree), skill `skills/nexus-onepager` in nexus repo | Static ecosystem + startup one-pagers; `decks/nexus-co2/` reveal deck in `cth-plugin` |
| **Datalab (related)** | `https://datalab.cleantechhub.net/` → **200** | `cth-datalab/` | Static HTML + CSP; datatón draft references Datalab lockup |
| **products.cleantechhub.net** | **PENDIENTE** (no headers) | **PENDIENTE** — no infra snippet in `cth-plugin/docs/infra` grep | Planned target in GTM brief, not provisioned in evidence |

**decks.cleantechhub.net:** root **302** → OAuth; dashboard path pattern documented in Caddy file.

---

## 4. Proposed sending setup (read-only)

### Resend (configured)

| Item | Finding |
|------|---------|
| Account domain | **`cleantechhub.net`** — status **verified**, region **sa-east-1**, sending **enabled** (Resend MCP `list-domains`, 2026-04-10 created) |
| Sending subdomain | **`send.cleantechhub.net`** — SPF (TXT + MX → amazonses.com) **verified** |
| DKIM | Host name **`resend._domainkey`** — **verified** (public key not reproduced here) |
| DMARC | `dig +short TXT _dmarc.cleantechhub.net` → **empty** — **PENDIENTE** publish/align |
| Tracking | Open/click tracking **off** on domain |
| Suppressions | List non-empty (bounce-origin entries present); **do not mass-mail until list reviewed** |
| Segments | 9 named segments (see §2) |
| Privacy policy draft | `src/cth-plugin/artifacts/cleantechhub-privacy-policy.md` — cites **Ley 1581 / Decreto 1377**, prior authorization, rights, newsletter |

### Alternatives (comparison, no action)

| Option | Pros | Cons vs current |
|--------|------|-----------------|
| **Resend (current)** | Domain verified, segments, API/MCP, CleantechHUB policy doc in repo | Needs DMARC, warm-up discipline, consent mapping |
| **Amazon SES direct** | Same SA-east spine as Resend SPF target | More ops; duplicate DNS if parallel |
| **SendGrid / Mailgun** | Mature warm-up tools | Second domain auth; migration cost |
| **Moodle / Gmail** | Already used for academy & inbox desks | Poor fit for 100+/day product campaigns; not bulk-marketing |

### Recommended operational pattern (proposal only)

1. **From:** `newsletter@send.cleantechhub.net` or product-specific local-part on **`send.`** subdomain (already in DNS).
2. **Warm-up:** Ramp **20 → 50 → 100+/day** over 2–3 weeks; segment by Resend segments with documented consent only.
3. **Compliance (CO):** Map each segment to purpose + **autorización** record; link **política de tratamiento** (privacy policy); honor **consulta/reclamo** flows (policy §).
4. **Headers:** `List-Unsubscribe` + one-click POST (RFC 8058); Resend supports unsubscribe headers per email-best-practices skill (plugin installed; not executed here).
5. **Suppression:** Sync bounces/complaints to Resend suppressions; threshold guard **&lt;2% bounce**, **&lt;0.1% complaint** (industry default — **PENDIENTE** formal CTH policy).
6. **HITL:** No cutover without Gideon GO (aligns `newsletter-comms` / Inbox desk).

### Segments without documented consent (outreach risk)

LinkedIn (all), CCB/Monday/SECOP CSVs, mail-finder guesses, and Resend **`General` / `Founders` / `Investors`** until provenance is filed (**PENDIENTE**).

---

## 5. Cloud Hands — product page build plan

**Target:** five public pages `products.cleantechhub.net/<slug>/` + PDF each (`dataton`, `earth-observatory`, `programs`, `lms`, `nexus` slugs TBD).

| Skill / route | Status |
|---------------|--------|
| `cleantechhub-brand` | `src/cth-plugin/skills/cleantechhub-brand/SKILL.md` |
| `reveal-deck-hands` | **PENDIENTE** — use `reveal-deck-build` for deck-like products only |
| `public-vercel-link` | **PENDIENTE** — prefer **OVH/Caddy** static path (cf. `decks.cleantechhub.net.caddy`) unless ticket specifies Vercel |
| Maker ≠ checker | `skills/harness/references/hands-ticket-hard.md` |
| Model (per GTM brief) | **`composer-2.5` with `fast=false`** on maker (note: harness default is `fast=true`) |

### Steps (HITL gated at DNS + deploy)

1. **Plan ticket** — slugs, SOURCES.md per product, acceptance URLs, read-budget 40 files / 400 KB.
2. **Maker job (1)** — static HTML/CSS from `cleantechhub-brand` (+ EO v3 rules where applicable); print CSS; output under `docs/gtm/products/<slug>/` or agreed repo path; **no secrets**.
3. **Checker job (1, read-only)** — different bc-id; verify brand tokens, no invented metrics, link checks `curl -sI`, PDF sha256, **no deploy**.
4. **PDF export (1)** — headless print or existing deck PDF pipeline; max 1.5 MB/single per GreenTec precedent.
5. **HITL — DNS + Caddy** — Gideon: `products.cleantechhub.net` vhost, TLS, `file_server` or upstream.
6. **HITL — deploy** — rsync to `/opt/...`; **no push to main** without merge GO.

**Estimated agent jobs:** **3** (maker + checker + PDF) + **2 human gates** (DNS, deploy) = **~5** tracked jobs. Optional **+5** if one maker/checker pair per product instead of batched wave (**~8–10** jobs).

---

## Evidence index

| Artifact | Value |
|----------|--------|
| Resend domain id | `9766debb-188a-4984-bbc4-ff73a8c8ccd9` (name: `cleantechhub.net` only) |
| programs Docmost share | `https://programs.cleantechhub.net/share/01a1eb6a-528e-7fcb-8c55-e3fd7623306e` |
| cth-plugin remote | `https://github.com/gideonblaauw-creator/cth-plugin.git` |
| LinkedIn ingest summary | `/home/debian/linkedin-connections-sync/2026-10-20/SUMMARY.md` |
| GreenTec PDF | `/mnt/data/claude-files/Projects/CTH-Brochures/greentec-2026-11/v4.1/cth-project-onepagers.pdf` |

---

*End of read-only findings.*