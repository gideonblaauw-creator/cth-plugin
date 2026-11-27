# Contrast check — Zidi MEG deck (Fix-5)

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
| Statement attr on statement | `#B2EEFA` | `#002855` | 11.50:1 | PASS AA |
| Closing body on navy | `#FFFFFF` | `#0C498A` | 8.99:1 | PASS AA |

## Fix-5 mitigations

- Frosted navy or white tiles (`fp-text-glass`, bleed `fp-head` / `fp-body` shells) behind text on photos; print uses solid `rgba(0,40,85,.88)` or `rgba(255,255,255,.92)`.
- Source lines use white glass + navy text on bleed slides (no cyan-on-navy footnotes).
- Q4 caption in its own glass row below the table (`max-height` on table body).
- Q1/Q3 print columns use filled navy cards at 26px body.
