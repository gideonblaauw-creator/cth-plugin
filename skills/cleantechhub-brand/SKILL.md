---
name: cleantechhub-brand
description: >
  Apply CleantechHUB brand guidelines to any communication piece, artifact, or
  template. Use this skill when creating or editing anything that will be seen
  externally or represents CleantechHUB — presentations, documents, social media
  posts, HTML artifacts, reports, proposals, flyers, email templates, or any
  visual/written content. Also trigger when the user asks to "make it on brand",
  "brand this", "apply our brand", "use our colors/fonts/style", or mentions
  CleantechHUB branding. If in doubt — use this skill.
metadata:
  version: "2.0.0"
  category: brand
---

# CleantechHUB Brand Guidelines

Apply these rules to every piece of content you create or edit for CleantechHUB. Do not deviate from the color palette, typography, or tone without explicit user override.

## Visual Identity

Source of truth: the CleantechHUB **Manual de Marca** (Brand Book, January 2024). Tagline: *Inspira · Actúa · Transforma*.

### Color Palette

Use ONLY these five official colors for primary elements. Map them to CSS custom properties when building HTML artifacts.

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Deep Blue | #0C498A | Official documents, formal comms, logo default, headers |
| Primary | Light Cyan | #B2EEFA | Backgrounds and light fills — the "water" element |
| Primary | Light Green | #9DC384 | Creative pieces, secondary emphasis — the "earth" element |
| Secondary | Forest Green | #669348 | Supporting earth tones, footer bars |
| Secondary | Sky Blue | #69B5FA | Supporting water tones |

**Color meaning:** blues represent water as a vital element and the human drive for change; greens represent the earth we belong to and must care for.

Neutrals: use white (#FFFFFF) for page backgrounds and a dark tone (Deep Blue #0C498A or near-black) for body text. Do not invent new hues — derive extra shades by adjusting the opacity of the palette.

**Forbidden:** black backgrounds combined with the dark blue logo (legibility conflict), purple or magenta backgrounds, and any color outside this palette.

### CSS Custom Properties

When building any HTML artifact, always define these at the root:

```css
:root {
  --cth-deep-blue: #0C498A;
  --cth-light-cyan: #B2EEFA;
  --cth-light-green: #9DC384;
  --cth-forest-green: #669348;
  --cth-sky-blue: #69B5FA;
  --cth-white: #FFFFFF;
  --font-primary: 'Open Sans', 'PT Sans', sans-serif;
  color-scheme: light;
}
```

Reference these variables throughout your CSS instead of hardcoding hex values.

### Typography

- **Wordmark:** Titilium Bold — used for the "CleantechHUB" wordmark only.
- **Primary:** Open Sans (Regular, SemiBold, Bold) — body text, headings, and main copy in all documents.
- **Secondary:** PT Sans — accompanying brand copy and supporting text.
- **Tertiary:** Hind Bold — extra artwork and modern variations.
- Web/digital fallback stack: `'Open Sans', 'PT Sans', sans-serif`. For HTML artifacts, load the fonts:
  `<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=PT+Sans:wght@400;700&display=swap" rel="stylesheet">`
- Never use serif fonts in CleantechHUB materials. Minimum body text size is 14px; prefer 16px.

### Logo Usage

- The full logo is the "CleantechHUB" wordmark — "Cleantech" in regular weight, "HUB" in bold. In plain-text contexts, write "CleantechHUB" as one word with capital H-U-B.
- Approved color versions: Deep Blue (#0C498A, default/official), Light Cyan (#B2EEFA, creative), Forest Green (#669348, semi-formal), Light Green (#9DC384, friendly/creative), and monochrome black-on-white or white-on-black for single-color reproduction.
- Maintain a clear-space exclusion zone on all sides (Manual de Marca: 3 cm in print; digitally, at least 1x the height of the "H" in HUB). Minimum print size is 4 cm wide.
- Never stretch, rotate, recolor, add shadows, or apply effects to the logo. Do not place it on busy photos without a solid-color shield, or on any background where it cannot be fully read.
- For co-branding and partnerships, use the dark blue horizontal logo and keep the same clear-space and minimum-size rules.

## Tone of Voice

Follow these five principles in every piece of copy:

1. **Expert but accessible** — Explain technical content clearly for non-specialists. Avoid jargon unless the audience is explicitly technical.
2. **Action-oriented** — Lead with impact, solutions, and next steps. Do not bury the value proposition.
3. **Bilingual-ready** — Use neutral English as default. When writing for Latin American audiences, use Latin American Spanish (not Peninsular Spanish).
4. **Collaborative** — Use "we" language and inclusive framing. CleantechHUB is a convener, not a gatekeeper.
5. **Climate-positive** — Be optimistic about solutions without greenwashing. Back claims with data when possible.

### Writing Rules

- Lead with the benefit or impact, not the process.
- Use active voice. Prefer short sentences (25 words maximum).
- Avoid jargon unless writing for a confirmed technical audience.
- Always capitalize "CleantechHUB" as one word with capital H-U-B. Never write "Cleantech Hub", "CleanTechHub", or "CTH" in external-facing content.
- Spell out acronyms on first use.
- Use the Oxford comma.
- Default to metric units.
- For Spanish content, use Latin American neutral Spanish. Avoid region-specific slang unless targeting a single country.

## Content Templates

### Social Media Post Structure

Follow this sequence for every social media post:

1. **Hook line** — A compelling problem statement, question, or insight.
2. **Body** — The solution, a supporting data point, or a brief story.
3. **Call to action** — Tell the reader exactly what to do next.
4. **Hashtags** — Always include `#CleantechHUB #ClimateAction #Cleantech` plus 2-3 topic-specific hashtags.

### Email Signature Block

Format signatures as:

```
[Name]
[Title] | CleantechHUB
[email] | cleantechhub.net
```

### Document Header/Footer

- **Header:** CleantechHUB logo (left-aligned) + document title (right-aligned).
- **Footer:** "© [Year] CleantechHUB Foundation" (left-aligned) + page number (right-aligned).
- Replace `[Year]` with the current year at time of creation.

## Application Checklist

Before delivering any CleantechHUB-branded content, verify:

1. Color palette is correct — no off-brand colors in primary elements.
2. Typography uses Open Sans / PT Sans (or system sans-serif fallback) — no serif fonts.
3. Tone follows the five principles — expert, accessible, action-oriented, collaborative, climate-positive.
4. Logo or wordmark is present where the format allows.
5. Standard footer or signature is included where appropriate.
6. "CleantechHUB" is spelled correctly everywhere (one word, capital H-U-B).
7. For HTML artifacts: CSS custom properties are defined and used for all brand colors.
8. For bilingual content: Spanish is Latin American neutral.
