---
name: tec-alianza-brand
description: >
  Apply TecAlianza brand guidelines to any content representing TecAlianza —
  presentations, documents, social media posts, or proposals. Trigger on mentions
  of TecAlianza branding, education técnica y tecnológica in Colombia, Uniandes +
  Colsubsidio joint programs, or technical certifications.
metadata:
  version: "2.0.0"
  category: brand
  relationship: "CTH program"
---

# TecAlianza Brand Guidelines

Apply these rules to every piece of content created for TecAlianza. This is a joint initiative with multiple partner organizations — co-branding rules are critical. Follow them precisely.

## About TecAlianza

TecAlianza is a joint education initiative involving Universidad de los Andes (Uniandes) and Colsubsidio, facilitated by CleantechHUB. It focuses on technical and technological education (educación técnica y tecnológica) in Colombia, including post-media education, TIC (Information and Communications Technology) training, and technical certifications. The program bridges the gap between academic institutions and workforce needs.

## Visual Identity

### Color Palette

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | TA Blue | #003366 | Headers, primary buttons, key accents |
| Secondary | TA Red | #CC0000 | Accents, CTAs, emphasis elements |
| Accent | TA Gold | #FFB81C | Highlights, badges, achievement markers |
| Background | TA Light | #F0F5FA | Section backgrounds, cards |
| Text | TA Dark | #1A1A2E | Body copy |

### CSS Custom Properties

When building HTML artifacts for TecAlianza:

```css
:root {
  --ta-primary: #003366;
  --ta-secondary: #CC0000;
  --ta-accent: #FFB81C;
  --ta-light: #F0F5FA;
  --ta-text: #1A1A2E;
  --font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

### Typography

- **Headlines:** Roboto Bold.
- **Body:** Roboto Regular, 16px base size.
- **Accent text:** Roboto Medium for labels, navigation, and metadata.
- Roboto is available via Google Fonts. Fall back to system sans-serif if unavailable.

## Tone of Voice

Follow these four principles in all TecAlianza copy:

1. **Academic yet practical** — Bridge the gap between university rigor and workforce relevance. Content should feel credible to academics and useful to employers simultaneously.
2. **Institutional** — Use a formal register that respects all partner organizations. TecAlianza represents a collaboration between major institutions; the tone must reflect that gravity.
3. **Impact-driven** — Focus on employment outcomes, skills gap closure, and measurable workforce impact. Lead with results and data when available.
4. **Spanish default** — Use "usted" register for institutional audiences. English only when explicitly creating international-facing content.

### Writing Rules

- Always write "TecAlianza" as one word with capital T and capital A. Never write "Tec Alianza", "tecalianza", "TEC ALIANZA", or "Tech Alianza".
- Use full official names for partner organizations on first reference:
  - "Universidad de los Andes" (not "Uniandes" on first mention; "Uniandes" acceptable thereafter).
  - "Colsubsidio" (this is the full official name; no expansion needed).
  - "CleantechHUB" (one word, capital H-U-B).
- When referencing education types, use the official Colombian terminology: "educación técnica y tecnológica", "formación para el trabajo y el desarrollo humano", "educación post-media".
- When discussing certifications, specify the type: "certificación técnica", "certificación de competencias laborales", etc.
- Never position one partner as more important than another. The three organizations are equal collaborators.

## Co-branding Rules

### Partner Logo Placement

When format allows, include all three partner logos:

1. **TecAlianza** logo — center or primary position.
2. **Universidad de los Andes** logo — left or first position among partners.
3. **Colsubsidio** logo — right or second position among partners.

If space is limited, the TecAlianza logo takes priority. CleantechHUB attribution appears in the footer as "Facilitado por CleantechHUB".

### Attribution Hierarchy

- TecAlianza is the program brand — it appears most prominently.
- Uniandes and Colsubsidio are named as founding partners.
- CleantechHUB is the facilitating organization — mentioned in footer or "about" sections.
- Never imply that any single partner "owns" TecAlianza.

## Content Rules

### Documents and Presentations

- **Header:** TecAlianza logo (center or left) + partner logos (right) + document title.
- **Footer:** "© [Year] TecAlianza — Universidad de los Andes, Colsubsidio. Facilitado por CleantechHUB" + page number.
- Use the blue-red-gold palette for charts and data visualizations.
- Structure education-focused documents with context on the skills gap, program methodology, and outcomes/impact.

### Social Media

- Lead with workforce impact data or student success stories.
- Tag all three partner organizations in every post.
- Use professional imagery related to education, technology, and the Colombian workforce.
- Hashtags: #TecAlianza #EducaciónTécnica #Uniandes #Colsubsidio #CleantechHUB + topic-specific.

### Reports and Proposals

- Include an executive summary targeting institutional decision-makers.
- Present data in the blue-red-gold color scheme.
- Use gold (#FFB81C) for achievement and milestone highlights.
- Reference Colombian education policy frameworks (SNIES, CONACES, CNA) accurately.

## Quality Checklist

Before delivering any TecAlianza-branded content, verify:

1. "TecAlianza" is written as one word with capital T and A everywhere.
2. Colors are from the TA palette (blue/red/gold), not CleantechHUB or partner palettes.
3. Typography uses Roboto throughout.
4. All three partner organizations are credited appropriately.
5. No single partner is positioned as more important than the others.
6. Spanish uses "usted" register for institutional audiences.
7. Official Colombian education terminology is used correctly.
8. CleantechHUB is attributed as facilitator, not owner or lead.
