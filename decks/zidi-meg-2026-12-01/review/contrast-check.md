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

## Computed font sizes (print mode, Fix-6b)

Run: `node review/font-size-check.mjs` · 2026-11-27

| Role | CSS declared (px) | Effective computed (px) | Floor |
|------|------------------:|------------------------:|------:|
| body / bullets | 36 | 36 | 36 | OK
| card title | 39 | 39 | 34 | OK
| card text | 36 | 36 | 34 | OK
| flip print body | 34 | 34 | 34 | OK
| GIZ print body | 34 | 34 | 34 | OK
| readiness print body | 36 | 36 | 36 | OK
| risk table td | 34 | 34 | 34 | OK
| Q6 lens body | 36 | 36 | 36 | OK
| source line | 22 | 22 | 22 | OK
| eyebrow | 24 | 24 | 24 | OK
| programme card text | 24 | 24 | 24 | OK
