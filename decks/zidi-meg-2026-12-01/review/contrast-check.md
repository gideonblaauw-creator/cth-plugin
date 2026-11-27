# Contrast check — Zidi MEG deck (Fix-5b)

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

## Fix-5 / Fix-5b mitigations

- Frosted navy or white tiles (`fp-text-glass`, bleed `fp-head` / `fp-body` shells) behind text on photos; print uses solid `rgba(0,40,85,.88)` or `rgba(255,255,255,.92)`.
- Source lines use white glass + navy text on bleed slides (no cyan-on-navy footnotes).
- Q4 caption in its own glass row below the table (`max-height` on table body).
- Q1/Q3 print columns use filled navy cards at 26px body; Fix-5b vertically centers the print grid.
- Q5 and Q6 split across two slides; Q5 flip print pairs stack front/back on navy with cyan/green labels.
- Q6 investor lens uses navy tile at ≥26px body in PDF.

_(PDF per-page overlap + live contrast run appended by `review/pdf-layout-check.mjs` after build.)_


## Automated PDF layout check (Fix-5b)

Run: `node review/pdf-layout-check.mjs` · 2026-11-27 · 16 slides (decktape print mode)

| Slide | Overflow | Overlap pairs | Contrast fails |
|------:|:--------:|--------------:|---------------:|
| 1 | no | 1 | 0 |
| 2 | no | 0 | 0 |
| 3 | no | 0 | 0 |
| 4 | no | 5 | 1 |
| 5 | no | 0 | 0 |
| 6 | no | 3 | 3 |
| 7 | no | 0 | 0 |
| 8 | no | 1 | 4 |
| 9 | no | 0 | 1 |
| 10 | no | 0 | 0 |
| 11 | no | 0 | 0 |
| 12 | no | 0 | 10 |
| 13 | no | 0 | 8 |
| 14 | no | 0 | 0 |
| 15 | no | 0 | 1 |
| 16 | no | 0 | 0 |

### Overlap detail

**Slide 1**
- `fp-cover__main fp-text-glass fp-text-glass--cover` × `fp-foot fp-foot--dark` — ~38174 px²

**Slide 4**
- `fp-programme-grid` × `fp-programme-card is-active` — ~105036 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~105041 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~105041 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~105041 px²
- `fp-programme-grid` × `fp-programme-card is-active` — ~105041 px²

**Slide 6**
- `fp-stat__value` × `SPAN` — ~4381 px²
- `fp-stat__value` × `SPAN` — ~2921 px²
- `fp-stat__value` × `SPAN` — ~1461 px²

**Slide 8**
- `fp-stat__value` × `SPAN` — ~3733 px²

### Live contrast samples (failing only)

**Slide 4**
- “Ideation — workshops, mentoring, and pitching comp” — 1:1 (need 4.5:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.12)

**Slide 6**
- “Investor engagements” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “P4G sub-goals delivered” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Energy delivered — quarterly kWh” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 8**
- “Charging sessions” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “14,000 registered users · public page chart · 27 N” — 2.34:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “EV brand share · March 2026” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Colombia EV registrations” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 9**
- “Source: RUNT, UPME, Datos Abiertos Bogotá (via htt” — 1.63:1 (need 4.5:1) · fg rgb(12, 73, 138) on bg rgba(0, 40, 85, 0.88)

**Slide 12**
- “EV & charging” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: kWh throughput grows with fleet” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Distributed solar & efficiency” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: contracted savings or tariffs o” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Sustainable agri-food & agritech” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: off-take contracts and traceabi” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Circular economy & waste” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: tipping fees, recovered materia” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “Climate & fintech data tools” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)
- “What makes it pay: recurring SaaS or data subscrip” — 2.34:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 0, 0, 0)

**Slide 13**
- “Capex intensity” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “High
Land, inputs, cold chain — often lumpy.” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “Low
Mostly people and software; lighter asset base” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “High
Hardware-heavy upfront; financing structure d” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “Regulation & FX” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “High
Export rules, phytosanitary permits, commodit” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “High
Licensing, data privacy, partner-bank rules; ” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)
- “High
Grid codes, permits, tariff resets; equipment” — 1:1 (need 3:1) · fg rgb(255, 255, 255) on bg rgba(255, 255, 255, 0.22)

**Slide 15**
- “Investor lens ILLUSTRATIVE

Diaspora lens (Q6): I ” — 1.63:1 (need 3:1) · fg rgb(12, 73, 138) on bg rgba(0, 40, 85, 0.92)

**Summary:** REVIEW — see rows above
