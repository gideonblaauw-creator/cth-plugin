---
name: cleantechhub-brand
description: >
  Applies CleantechHUB brand — colors, typography, tone, HTML/CSS tokens. Use
  when: external CTH content, on-brand artifacts, proposals, social, reports. Do
  not use when: CLP26 campaign (clp26-brand) or client-only brands.
license: MIT
metadata:
  version: "2.1.0"
  category: "brand"
---

# CleantechHUB Brand Guidelines

Apply these rules to every piece of content you create or edit for CleantechHUB. Do not deviate from the color palette, typography, or tone without explicit user override.

## Visual Identity

### Color Palette

Use these exact hex values. Map them to CSS custom properties when building HTML artifacts.

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | CTH Green | #2D6A4F | Headers, primary buttons, key accents |
| Secondary | CTH Dark | #1B4332 | Text on light backgrounds, footer bars |
| Accent | CTH Lime | #95D5B2 | Highlights, secondary buttons, badges |
| Background | CTH Light | #D8F3DC | Section backgrounds, cards |
| Neutral | CTH White | #FFFFFF | Page backgrounds |
| Text | CTH Charcoal | #333333 | Body text |

Never introduce off-brand colors for primary UI elements. If a design calls for additional shades, derive them by adjusting opacity of the existing palette — do not invent new hues.

### CSS Custom Properties

When building any HTML artifact, always define these at the root:

```css
:root {
  --cth-primary: #2D6A4F;
  --cth-dark: #1B4332;
  --cth-accent: #95D5B2;
  --cth-light: #D8F3DC;
  --cth-white: #FFFFFF;
  --cth-text: #333333;
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

Reference these variables throughout your CSS instead of hardcoding hex values.

### Typography

- **Headlines:** Inter Bold. If Inter is unavailable, fall back to system sans-serif.
- **Body text:** Inter Regular, 16px base size, 1.6 line-height.
- **Accent text:** Inter Medium for labels, navigation items, metadata, and captions.
- Never use serif fonts in CleantechHUB materials.
- Minimum body text size is 14px; prefer 16px.

### Logo Usage

- The full logo is the "CleantechHUB" wordmark — "Cleantech" in regular weight, "HUB" in bold.
- Maintain minimum clear space of 1x the height of the "H" in HUB on all sides.
- Never stretch, rotate, add effects to, or recolor the logo.
- On dark backgrounds, use the white variant of the wordmark.
- When the logo cannot be embedded (plain text contexts), write "CleantechHUB" as one word with capital H-U-B.

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
2. Typography uses Inter (or system sans-serif fallback) — no serif fonts.
3. Tone follows the five principles — expert, accessible, action-oriented, collaborative, climate-positive.
4. Logo or wordmark is present where the format allows.
5. Standard footer or signature is included where appropriate.
6. "CleantechHUB" is spelled correctly everywhere (one word, capital H-U-B).
7. For HTML artifacts: CSS custom properties are defined and used for all brand colors.
8. For bilingual content: Spanish is Latin American neutral.
## Brand DNA for diffusion (OSS stills)

For ComfyUI / Flux LoRA stills, use the five-color Manual de Marca Jan 2024 palette in `skills/cleantechhub-brand/brand_dna.yaml` (not the Inter/CSS palette above). Routed by `skills/oss-stills/SKILL.md`.

## Related skills

| Skill | When instead |
|---|---|
| `oss-stills` | OSS self-host branded stills (ComfyUI + Flux.1-Dev + CTH LoRA) |
| `clp26-brand` | CLP26 / ClimateLaunchpad campaign content |
| `cth-proposal-build` | Proposal HTML structure (still apply CTH brand here first) |
| `nexus-onepager` | Startup profile pages on Nexus |
