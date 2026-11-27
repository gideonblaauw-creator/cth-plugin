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
| 9 | 36 |
| 18 | 36 |

### card title (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 6 | 39 |
| 15 | 34 |
| 18 | 39 |

### card text (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 6 | 36 |
| 9 | 36 |
| 15 | 34 |

### flip print body (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 34 |
| 12 | 36 |
| 13 | 34 |
| 17 | 34 |

### flip print label (floor ≥24px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 26 |
| 12 | 26 |
| 13 | 24 |
| 17 | 24 |

### risk table td (floor ≥34px)

| Slide | Computed (px) |
|------:|--------------:|
| 16 | 34 |

### risk cell note (floor ≥22px)

| Slide | Computed (px) |
|------:|--------------:|
| 16 | 28 |

### Q6 lens body (floor ≥36px)

| Slide | Computed (px) |
|------:|--------------:|
| 18 | 36 |

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

### giz action (floor ≥28px)

| Slide | Computed (px) |
|------:|--------------:|
| 5 | 28 |

