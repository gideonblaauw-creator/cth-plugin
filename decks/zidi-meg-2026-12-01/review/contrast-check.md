# Contrast check — Zidi MEG deck (Fix-6b)

Generated for Gideon review · WCAG 2.x relative luminance · body ≥4.5:1 · large text ≥3:1.

| Style / pair | Foreground | Background | Ratio | Grade |
|--------------|------------|------------|------:|-------|
| Body on white card | `#0C498A` | `#FFFFFF` | 8.99:1 | PASS AA |
| Body on navy glass | `#FFFFFF` | `#002855` | 14.64:1 | PASS AA |
| Card title on white | `#0C498A` | `#FFFFFF` | 8.99:1 | PASS AA |
| Eyebrow green on navy glass | `#9DC384` | `#002855` | 7.37:1 | PASS AA |
| Title white on navy glass | `#FFFFFF` | `#002855` | 14.64:1 | PASS AA |
| Source on white glass | `#0C498A` | `#FFFFFF` | 8.99:1 | PASS AA |
| Source cyan on bleed (legacy) | `#B2EEFA` | `#0C498A` | 7.07:1 | PASS AA |
| Foot label on bleed | `#E8F8FC` | `#0C498A` | 8.25:1 | PASS AA |
| Conf label on bleed | `#9DC384` | `#0C498A` | 4.53:1 | PASS AA |
| KPI label on navy stat | `#FFFFFF` | `#0C498A` | 8.99:1 | PASS AA |
| KPI value cyan on navy | `#B2EEFA` | `#0C498A` | 7.07:1 | PASS AA |
| KPI label on white stat | `#0C498A` | `#FFFFFF` | 8.99:1 | PASS AA |
| KPI value green on white | `#669348` | `#FFFFFF` | 3.60:1 | PASS AA |
| Risk header on navy | `#FFFFFF` | `#0C498A` | 8.99:1 | PASS AA |
| Risk body on navy cell | `#FFFFFF` | `#0C498A` | 8.99:1 | PASS AA |
| Rate pill low | `#0C498A` | `#9DC384` | 4.53:1 | PASS AA |
| Rate pill med | `#0C498A` | `#B2EEFA` | 7.07:1 | PASS AA |
| Rate pill high | `#3A1A08` | `#F4A574` | 7.87:1 | PASS AA |
| Flip back on cyan tint | `#0C498A` | `#E8FAFE` | 8.36:1 | PASS AA |
| Flip print body on navy (Fix-5b) | `#FFFFFF` | `#002855` | 14.64:1 | PASS AA |
| Flip print front label on navy | `#B2EEFA` | `#002855` | 11.50:1 | PASS AA |
| Flip print back label on navy | `#9DC384` | `#002855` | 7.37:1 | PASS AA |
| Q6 lens body on navy (Fix-5b) | `#FFFFFF` | `#002855` | 14.64:1 | PASS AA |
| Q6 lens heading green on navy | `#9DC384` | `#002855` | 7.37:1 | PASS AA |
| Statement attr on statement | `#B2EEFA` | `#002855` | 11.50:1 | PASS AA |
| Closing body on navy | `#FFFFFF` | `#0C498A` | 8.99:1 | PASS AA |

## Fix-6 mitigations

- Full-bleed photo backgrounds and scrims removed; flat navy or white slides per FODESEP `deck.css`.
- Unblocked hero image rails (`fp-hero-rail`) beside content — thematic assets only, no people.
- Programme cards show photo unblocked with solid navy caption bar (no gradient scrim).
- Type scale ×1.5 vs Fix-5 v5 floors; source lines ≥22px.
- GIZ growth slides after CTH programmes; umbrella facts cited to giz.de (8 countries, 90 ventures, verified 27 Nov 2026).

_(PDF per-page overlap + live contrast run appended by `review/pdf-layout-check.mjs` after build.)_

## Computed font sizes — print-pdf mode (Fix-6c)

Run: `node review/font-size-check.mjs` · 2026-11-27 · viewport 1920×1080

Values are **getComputedStyle** effective px (post-Reveal scale), not declared CSS.

### body / bullets (floor ≥36px)

| Slide | Computed (px) |
|------:|--------------:|
| 3 | 36 |
| 7 | 36 |
| 19 | 36 |

### card title (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 6 | 39 |
| 15 | 34 |
| 16 | 34 |
| 19 | 39 |

### card text (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 6 | 36 |
| 9 | 36 |
| 15 | 34 |
| 16 | 34 |

### flip print body (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 34 |
| 12 | 36 |
| 13 | 36 |
| 18 | 34 |

### flip print label (floor ≥24px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 26 |
| 12 | 26 |
| 13 | 26 |
| 18 | 26 |

### risk table td (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 17 | 34 |

### risk cell note (floor ≥22px)

| Slide | Computed (px) |
|------:|--------------:|
| 17 | 28 |

### Q6 lens body (floor ≥36px)

| Slide | Computed (px) |
|------:|--------------:|
| 19 | 36 |

### source line (floor ≥22px)

| Slide | Computed (px) |
|------:|--------------:|
| 4 | 22 |
| 5 | 22 |
| 6 | 22 |
| 7 | 22 |
| 8 | 22 |
| 9 | 22 |
| 10 | 22 |
| 11 | 22 |
| 12 | 22 |
| 13 | 22 |
| 14 | 22 |
| 15 | 22 |
| 16 | 22 |
| 17 | 22 |
| 18 | 22 |
| 19 | 22 |

### eyebrow (floor ≥24px)

| Slide | Computed (px) |
|------:|--------------:|
| 1 | 24 |
| 2 | 24 |
| 3 | 24 |
| 4 | 24 |
| 5 | 24 |
| 6 | 24 |
| 7 | 24 |
| 9 | 24 |
| 11 | 24 |
| 12 | 24 |
| 13 | 24 |
| 14 | 24 |
| 15 | 24 |
| 16 | 24 |
| 17 | 24 |
| 18 | 24 |
| 19 | 24 |

### giz action (floor ≥28px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 28 |



## Automated PDF layout check (Fix-5b)

Run: `node review/pdf-layout-check.mjs` · 2026-11-27 · 20 slides (decktape print mode)

| Slide | Overflow | Overlap pairs | Contrast fails |
|------:|:--------:|--------------:|---------------:|
| 1 | no | 8 | 0 |
| 2 | no | 0 | 0 |
| 3 | no | 0 | 6 |
| 4 | no | 10 | 7 |
| 5 | no | 0 | 3 |
| 6 | no | 0 | 6 |
| 7 | no | 0 | 4 |
| 8 | no | 11 | 5 |
| 9 | no | 0 | 9 |
| 10 | no | 2 | 6 |
| 11 | no | 0 | 0 |
| 12 | no | 0 | 2 |
| 13 | no | 0 | 2 |
| 14 | no | 0 | 14 |
| 15 | no | 13 | 8 |
| 16 | no | 4 | 6 |
| 17 | no | 20 | 5 |
| 18 | no | 0 | 2 |
| 19 | no | 0 | 6 |
| 20 | no | 0 | 0 |

### Overlap detail

**Slide 1**
- `fp-slide-shell` × `fp-cover__main` — ~834947 px²
- `fp-slide-shell` × `fp-cover__text` — ~310813 px²
- `fp-slide-shell` × `fp-cover__meta` — ~18270 px²
- `fp-cover__main` × `fp-foot fp-foot--dark` — ~31267 px²
- `fp-cover__text` × `fp-foot fp-foot--dark` — ~11752 px²
- `fp-cover__text` × `SPAN` — ~4493 px²
- `fp-cover__meta` × `fp-foot fp-foot--dark` — ~11752 px²
- `fp-cover__meta` × `SPAN` — ~4493 px²

**Slide 4**
- `fp-body` × `fp-programme-card is-active` — ~46003 px²
- `fp-body` × `fp-programme-card is-active` — ~46003 px²
- `fp-body` × `fp-programme-card is-active` — ~46003 px²
- `fp-body` × `fp-programme-card is-active` — ~46003 px²
- `fp-body` × `fp-programme-card is-active` — ~46003 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~46003 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~46003 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~46003 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~46003 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~46003 px²

**Slide 8**
- `fp-body` × `SPAN` — ~12481 px²
- `fp-body` × `SPAN` — ~4161 px²
- `fp-stats fp-stats--4 fp-stats--compact` × `SPAN` — ~12481 px²
- `fp-stats fp-stats--4 fp-stats--compact` × `SPAN` — ~4161 px²
- `fp-stat` × `SPAN` — ~12481 px²
- `fp-stat__value` × `SPAN` — ~8398 px²
- `SPAN` × `fp-stat__label` — ~2216 px²
- `fp-stat__value` × `SPAN` — ~5599 px²
- `SPAN` × `fp-stat__label` — ~1478 px²
- `fp-stat` × `SPAN` — ~4161 px²
- `fp-stat__value` × `SPAN` — ~2800 px²

**Slide 10**
- `fp-stat__value` × `SPAN` — ~8398 px²
- `SPAN` × `fp-stat__label` — ~2216 px²

**Slide 15**
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-trio` × `fp-sector-detail` — ~27340 px²
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-trio` × `EM` — ~19409 px²
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-trio` × `fp-sector-detail` — ~4152 px²
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-trio` × `fp-sector-detail` — ~15746 px²
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-trio` × `EM` — ~10224 px²
- `fp-card fp-sector-card is-open` × `fp-sector-detail` — ~27340 px²
- `fp-card fp-sector-card is-open` × `EM` — ~19409 px²
- `fp-sector-detail` × `cth-source` — ~7824 px²
- `fp-card fp-sector-card is-open` × `fp-sector-detail` — ~4152 px²
- `fp-sector-detail` × `cth-source` — ~16501 px²
- `fp-card fp-sector-card is-open` × `fp-sector-detail` — ~15746 px²
- `fp-card fp-sector-card is-open` × `EM` — ~10224 px²
- `fp-sector-detail` × `cth-source` — ~7051 px²

**Slide 16**
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-duo` × `fp-sector-detail` — ~43415 px²
- `fp-sector-grid fp-sector-grid--q2 fp-sector-grid--q2-duo` × `fp-sector-detail` — ~25004 px²
- `fp-card fp-sector-card is-open` × `fp-sector-detail` — ~43415 px²
- `fp-card fp-sector-card is-open` × `fp-sector-detail` — ~25004 px²

**Slide 17**
- `fp-risk-table fp-risk-table--q4-full` × `fp-foot` — ~27257 px²
- `fp-risk-table fp-risk-table--q4-full` × `fp-conf` — ~5458 px²
- `fp-risk-table fp-risk-table--q4-full` × `SPAN` — ~9991 px²
- `TBODY` × `cth-source` — ~57863 px²
- `TBODY` × `fp-foot` — ~24104 px²
- `TBODY` × `fp-conf` — ~4783 px²
- `TBODY` × `SPAN` — ~8889 px²
- `TR` × `cth-source` — ~57863 px²
- `TR` × `fp-foot` — ~24104 px²
- `TR` × `fp-conf` — ~4783 px²
- `TR` × `SPAN` — ~8889 px²
- `TD` × `cth-source` — ~12729 px²
- `TD` × `fp-foot` — ~5303 px²
- `TD` × `fp-conf` — ~4783 px²
- `rate-high` × `cth-source` — ~10542 px²
- `rate-high` × `fp-foot` — ~4392 px²
- `rate-high` × `SPAN` — ~4137 px²
- `rate-med` × `cth-source` — ~15723 px²
- `rate-med` × `fp-foot` — ~6550 px²
- `rate-med` × `SPAN` — ~4751 px²

### Live contrast samples (failing only)

**Slide 3**
- “I came from Dutch finance to Colombia — and I clos” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “I am Dutch and have lived and worked in Bogotá for” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Before Colombia, I spent more than 10 years in fin” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “For about 8 years I have helped climate startups m” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Today I tell that path through one public case: Mu” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 4**
- “CleantechHUB takes ventures from ideas to investor” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Ideation

Testable pitch from a climate idea.” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Incubation

MVP, model, first proof.

MUBON · DEEP” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Acceleration

Investor conversations open.

MUBON ” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Growth

Scale-up and follow-on capital.

MUBON · P” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Train-the-Trainer

Local partners run the pathway.” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 5**
- “GIZ CATAL1.5°T capital-raising accompaniment” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “We take climate SMEs from a four-area diagnosis to” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 6**
- “What each side gets from the accompaniment” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “For the SME” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Diagnosis, revised pitch, capital plan, investor s” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “For the investor” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “A company pre-examined on business, finance, impac” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 7**
- “MubOn is where that pathway meets grant-backed sca” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Colombian EV charging venture, originally incubate” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CleantechHUB was fiscal host and grant administrat” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 8**
- “In 18 months, MubOn reached investment-ready scale” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Investor engagements” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “P4G sub-goals delivered” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Energy delivered — quarterly kWh” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 9**
- “This model earns from usage, not from permanent gr” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SCALABLE (MUBON)

Comodato leases smart chargers; ” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SCALABLE (MUBON)” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Comodato leases smart chargers; recurring kWh reve” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SUBSIDY-DEPENDENT

Operations that stop when the g” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SUBSIDY-DEPENDENT” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Operations that stop when the grant ends, with no ” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “My test for any SME: does revenue continue if the ” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 10**
- “Investors can diligence network data a third party” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Charging sessions” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “14,000 registered users · public page chart · 27 N” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “EV brand share · March 2026” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Colombia EV registrations” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 12**
- “Readiness test — flip each card” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 13**
- “Unit economics and externalities” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 14**
- “I weigh regulated platforms against direct angel o” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SMALL ANGEL TICKET

Regulated crowdfunding or inve” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “SMALL ANGEL TICKET” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Regulated crowdfunding or investment platform — lo” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Trade-off: platform fees, standardised terms, limi” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “PLATFORM SYNDICATE

Blended path — platform syndic” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “PLATFORM SYNDICATE” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Blended path — platform syndicate plus a small dir” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Trade-off: more paperwork to align platform KYC wi” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “DIRECT EQUITY

Direct angel or private equity — yo” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “DIRECT EQUITY” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Direct angel or private equity — you set ticket si” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Trade-off: full diligence burden, FX, and governan” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 15**
- “Where I see impact SMEs that can earn revenue” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “EV & charging” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: kWh throughput grows with fleet” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Distributed solar & efficiency” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: contracted savings or tariffs o” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Sustainable agri-food & agritech” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: off-take contracts and traceabi” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 16**
- “More sectors with recurring revenue mechanics” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Circular economy & waste” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: tipping fees, recovered materia” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Climate & fintech data tools” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: recurring SaaS or data subscrip” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 17**
- “How I compare risk–return across agriculture, fint” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Revenue visibility” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Seasonality / weather” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Time to exit” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 18**
- “Political and regulatory diligence — flip each car” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 19**
- “What diaspora capital does differently” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Investor lens ILLUSTRATIVE” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Diaspora money often follows trust and cultural pr” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Institutions bring scale and standards — but rarel” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “MubOn shows both: grant-backed proof first, angel ” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “CONFIDENTIAL” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Summary:** REVIEW — see rows above
