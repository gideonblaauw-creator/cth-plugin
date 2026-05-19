---
name: sustenttia-brand
description: >
  Apply Sustenttia brand guidelines to any communication piece, artifact, or template.
  Use this skill EVERY TIME you create or edit anything that represents Sustenttia —
  including social media posts, presentations, documents, HTML artifacts, reports,
  proposals, email templates, landing pages, PDFs, or any visual/written content.
  Also trigger this skill when the user asks to "make it on brand", "brand this",
  "apply Sustenttia style", "use our colors/fonts", or mentions Sustenttia branding,
  identity, or visual guidelines. Also trigger for any content directed at PYMES,
  ASG diagnostics, sustainability consulting, or Sustenttia product marketing.
  If in doubt about whether something needs to be on brand — use this skill.
---

# Sustenttia Brand Communications Skill

This skill ensures all Sustenttia communications are consistent with the visual identity
observed across all official Sustenttia brand materials (social media, web, presentations,
product pages, and marketing collateral — April 2026).

---

## Brand Identity at a Glance

**Organization:** Sustenttia — sustainability consulting for Latin American SMEs (PYMES).
**Tagline:** *Sostenibilidad con Propósito*
**Brand Promise:** "Hacemos de la sostenibilidad una herramienta para mejorar la rentabilidad de las PYMES."
**Core Positioning:** Making sustainability a competitive advantage — accessible, structured, and actionable for Colombian and regional PYMES.
**Primary Audience:** Industrial and manufacturing PYMES, supplier PYMES to large companies, companies seeking ESG-compliant markets, business chambers, sustainability consultants.
**Products:** Evaluación Inicial ASG (free), Diagnóstico Estratégico ASG (paid), AI-assisted reports.
**Context:** Colombian market; content in Spanish; professional but approachable tone.

---

## Color Palette

Use ONLY these colors. Never introduce colors outside this set.

| Name | HEX | Role |
|------|-----|------|
| **Deep Teal** | `#1B6B74` | Primary — logo, headlines, dark backgrounds, icon fills, buttons |
| **Dark Navy Teal** | `#0D3D45` | Primary deep — darkest backgrounds (full-bleed sections), gradient dark anchor |
| **Medium Teal** | `#2E8B92` | Secondary — gradient mid-tone, active states, horizontal rules |
| **Light Teal / Sage** | `#5BA0A0` | Tertiary — softer icon outlines, lighter backgrounds |
| **Pale Sage Green** | `#B8D8C8` | Accent light — card icon circle backgrounds, soft fills, hover tints |
| **Mint Wash** | `#D9EDE8` | Background wash — page backgrounds, section dividers, subtle fills |
| **Warm White** | `#FFFFFF` | Primary text surface — card bodies, contrast text on dark |
| **Off-White** | `#F5F8F7` | Secondary background — alternating sections, clean panels |
| **Body Text Dark** | `#2C3E3A` | Primary body text on light backgrounds |
| **Body Text Muted** | `#5A7068` | Secondary body text, captions, supporting copy |
| **Gold / Amber Accent** | `#F5C842` | Sparingly — "Recomendado" badges, star ratings, CTA highlights |
| **Coral / Red** | `#E05A4A` | Sparingly — alerts, error states, urgency indicators only |

### Gradient Patterns
The signature Sustenttia background gradient transitions diagonally:
- **Top-left:** Pale Sage Green / Mint Wash (`#D9EDE8` → `#B8D8C8`)
- **Bottom-right:** Deep Teal / Dark Navy Teal (`#1B6B74` → `#0D3D45`)

Use: `background: linear-gradient(135deg, #D9EDE8 0%, #FFFFFF 40%, #B8D8C8 60%, #2E8B92 80%, #0D3D45 100%);`

For full-bleed dark sections (features, comparison tables): solid `#1B6B74` or `#0D3D45` with white text.

---

## Typography

### Fonts
| Role | Font | Weight | Use |
|------|------|--------|-----|
| **Headlines / Display** | `Nunito` or `Nunito Sans` | 700–800 (Bold/ExtraBold) | H1, H2, hero text, card titles |
| **Subheadings** | `Nunito` or `Nunito Sans` | 600–700 (SemiBold/Bold) | H3, H4, section labels |
| **Body Text** | `Inter` or `Open Sans` | 400–500 (Regular/Medium) | Paragraphs, descriptions, lists |
| **UI / Buttons / Tags** | `Inter` | 500–600 | Button labels, badges, nav items |

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

**CSS variables:**
```css
--font-heading: 'Nunito', 'Nunito Sans', sans-serif;
--font-body: 'Inter', 'Open Sans', sans-serif;
```

### Type Scale
- **Hero H1:** 40–56px, Nunito Bold/ExtraBold, Deep Teal or White
- **Section H2:** 28–36px, Nunito Bold, Deep Teal or White
- **Card Title H3:** 18–22px, Nunito SemiBold/Bold, Deep Teal
- **Body:** 15–16px, Inter Regular, Body Text Dark
- **Small / Caption:** 12–13px, Inter Regular, Body Text Muted
- **Button:** 14–16px, Inter SemiBold, Uppercase or Title Case

---

## Logo

### Logotype
**SUSTENTTIA** — uppercase, Nunito ExtraBold or equivalent geometric sans, in Deep Teal (`#1B6B74`).
Paired with tagline: **"SOSTENIBILIDAD CON PROPÓSITO"** — small caps, tracked, lighter weight, same teal family.

### Logo Mark
Circular icon with two overlapping swoosh/leaf forms creating a stylized "S" or sustainability loop — rendered in Deep Teal on white, or white on Deep Teal.

### Logo Rules
- Always maintain clear space equal to the cap-height of the "S" on all sides
- On dark teal backgrounds: use white version
- On light/white backgrounds: use Deep Teal version
- Never distort, recolor outside palette, add drop shadows, or place on busy photographic backgrounds without a white/teal backing card
- Minimum digital size: 120px wide

---

## Layout & Design Principles

### Card Style
The primary UI component is a **rounded white card** floating on the gradient or teal background:
- Background: `#FFFFFF`
- Border radius: `16–24px`
- Box shadow: `0 8px 32px rgba(0,0,0,0.10)`
- Padding: `32–48px`
- Used for: product descriptions, pricing plans, feature callouts, testimonials

### Icon Treatment
- Icons inside **circular pale sage backgrounds** (`#B8D8C8` or `#D9EDE8`), Deep Teal icon color
- On dark teal backgrounds: white line icons, no fill background
- Icon style: rounded outline, 2px stroke — never solid flat fills outside the teal system
- Icon circles: `width/height: 80–100px; border-radius: 50%; background: #B8D8C8`

### Buttons / CTAs
- **Primary CTA:** Deep Teal background (`#1B6B74`), white text, border-radius `40px` (pill shape), with a right-facing arrow `>>` or chevron
- **Secondary CTA / Pill badge:** Pale Sage Green (`#B8D8C8`), Deep Teal text, same pill radius
- **"Recomendado" badge:** Gold (`#F5C842`) background, Deep Teal text, pill shape, small font
- Hover state: darken primary to `#0D3D45`

### Checkmark / Bullet Style
The brand uses a **teal circular checkmark** icon (✅ style, `#1B6B74`) for feature lists — not plain bullets or dashes.

### Divider / Progress Lines
Thin horizontal lines in Medium Teal (`#2E8B92`) or light sage; used as separators and progress indicators.

### Photo Treatment
- Photos appear inside **rounded rectangle frames** (border-radius `12–16px`)
- Accent border: Gold/Amber (`#F5C842`) left or bottom border `3–4px` on portrait/person photos
- No direct text overlay on photos — always use an adjacent white card or teal block for text
- Subject matter: Latin American business context, PYMES professionals, laptops showing dashboards, green/sustainable imagery

### Background Gradient Usage
Use the diagonal soft gradient (`#D9EDE8` → teal) for:
- Hero sections
- Full-page section backgrounds (landing pages, presentations)
- Email headers

Use solid Deep Teal (`#1B6B74` or `#0D3D45`) for:
- Feature comparison rows
- Full-bleed callout sections
- Footer areas

---

## Tone of Voice

| Dimension | Guidance |
|-----------|----------|
| **Language** | Spanish (Colombian market); formal but accessible |
| **Register** | Professional, credible, empowering — never bureaucratic |
| **Perspective** | Second person "tú/usted" — direct address to the PYME leader |
| **Key themes** | Rentabilidad, ventaja competitiva, claridad, acción, madurez ASG |
| **Key verbs** | Evalúa, convierte, transforma, prioriza, identifica, avanza |
| **Avoid** | Excessive jargon, greenwashing language, vague claims, fear-based framing |
| **Proof points** | Always back claims with structure (levels, percentages, frameworks: GRI, ISO 26000) |

### Power Phrases (use naturally in copy)
- *"Sostenibilidad con propósito"* — tagline, always available
- *"Convierte la sostenibilidad en tu ventaja competitiva."*
- *"Evalúa de forma ejecutiva tu nivel de madurez ASG."*
- *"Hacemos de la sostenibilidad una herramienta para mejorar la rentabilidad."*
- *"Diagnóstico Estratégico ASG para PYMES"*
- *"Análisis estructurado por eje Ambiental, Social y Gobernanza"*
- *"Evaluación inicial sin costo."*

### ASG Axis Labels (always capitalize, use consistently)
- **Ambiental** (Environmental)
- **Social**
- **Gobernanza** (Governance)

### Maturity Level Language (4-level scale)
| Level | Range | Label |
|-------|-------|-------|
| Nivel 1 | 0–25% | Básico |
| Nivel 2 | 26–50% | Enfoque en cumplimiento |
| Nivel 3 | 51–75% | Enfoque en eficiencia |
| Nivel 4 | 76–100% | Proactividad estratégica |

---

## Content Templates by Format

### Social Media Post (LinkedIn / Instagram — landscape 16:9)
```
Structure:
- Background: gradient or soft teal wash
- White rounded card overlay (80% width, centered)
- Sustenttia logo: top-left of card
- Headline: Nunito Bold, 28–36px, Deep Teal — punchy, max 10 words
- Supporting text: Inter 15px, body dark — 1–2 lines
- Feature list: teal checkmarks + Inter 14px
- CTA pill or visual element: bottom of card
- Right side or inset: product screenshot, laptop mockup, or icon grid
```

### Feature Cards (5-column grid, dark teal background)
```
- Background: #1B6B74 full bleed
- Cards: slightly lighter teal surface (#2E8B92 or 8% opacity white)
- Icon: white outline, centered top
- Title: white, Nunito Bold, 16–18px, centered
- Body: white 80% opacity, Inter 13px, centered
```

### Pricing Plan Cards
```
- Background: white card, border-radius 20px
- Recommended badge: Gold pill top center
- Plan header: Deep Teal pill with "PLAN X" in white Nunito Bold
- Contents: teal checkmarks + feature list
- Price: Nunito ExtraBold 32px, Deep Teal
- CTA: Deep Teal pill button + >> arrow
```

### Presentation Slides
```
- Title slide: diagonal gradient background, white card center-left with logo and title
- Section header slides: solid Deep Teal, large white Nunito headline
- Content slides: white background, Deep Teal headings, body text dark
- Feature slides: icon + title + 2-line description in white card grid
- Always logo: top-left or bottom-left, teal version on white, white version on teal
```

### Email / HTML Document
```
- Header: Deep Teal bar with white Sustenttia logo
- Body: white, Inter 15px, body text dark
- Headings: Nunito Bold, Deep Teal
- CTA button: teal pill, white text
- Footer: mint wash background, muted text, logo small
```

---

## Quick Checklist — Before Producing Any Output

- [ ] Only palette colors used? (Deep Teal `#1B6B74`, Dark Navy `#0D3D45`, Medium Teal `#2E8B92`, Sage `#B8D8C8`, Mint `#D9EDE8`, White, Gold `#F5C842` sparingly)
- [ ] Fonts: Nunito for headings, Inter/Open Sans for body?
- [ ] Cards have correct border-radius (16–24px) and shadow?
- [ ] Icons in pale sage circles (light bg) or white outlines (dark bg)?
- [ ] CTA buttons are pill-shaped (40px radius), Deep Teal primary?
- [ ] Teal checkmarks used in feature lists (not plain bullets)?
- [ ] Language is Spanish, direct "tú/usted" address, professional-but-clear tone?
- [ ] ASG axes always written: Ambiental, Social, Gobernanza?
- [ ] Tagline or power phrase included where appropriate?
- [ ] No text directly on top of busy photos — always on card/block?

---

## Related Skills

- `cleantechhub-brand` — CleantechHUB is the parent ecosystem; Sustenttia is a partner/product built within the CTH context
- `social-media-campaign` — orchestration for multi-platform social posts using the Sustenttia brand
- `canva` — primary tool for producing Sustenttia visuals
- `buffer` — publishing Sustenttia posts; Sustenttia tone and image specs apply
- `bookstack` — Sustenttia knowledge base at wiki.cleantechhub.net uses teal brand styling

---

*Brand guidelines derived from Sustenttia official marketing materials, social media, and web assets — April 2026.*
