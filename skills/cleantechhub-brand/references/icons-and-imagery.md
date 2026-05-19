# CleantechHUB Icons & Imagery Reference

## Brand Icon Library

CleantechHUB has a custom illustration library. All icons are rendered exclusively in brand colors. They give materials a "young and fresh" visual feel.

### Core Brand Icons (always available)
| Icon | Description | Color Context |
|------|-------------|---------------|
| Rocket Ship | CTH's "insignia ship" — represents innovation and launch | Green or blue tones |
| Globe / Earth | The world we protect | Blue (water fill) or green (land fill) |
| Spectacled Bear | Endangered Colombian fauna, brand mascot character | Deep blue or green |
| Mangrove Scene | Mangroves + heron/bird, wetland ecosystem | Blue/green landscape |
| Water Waves | Stylized wavy lines, water element | Deep blue + light blue/green |
| Plant / Frond | Endangered flora, nature motif | Green tones |
| Leaf | Simple leaf, sustainability symbol | Green or blue tones |

### Icon Presentation Style
- Square tiles with **rounded corners** as containers
- Background fill: one solid brand color per tile
- Icon: contrasting brand color inside the tile
- Tiles can be arranged in grids or mosaics (see digital business card)
- Never use white or black-only icon backgrounds — always a brand color

### Icon Color Logic
- **Blue-toned icons:** The "water/ocean" part of the globe gets the color fill; land is lighter
- **Green-toned icons:** The "land/earth" part of the globe gets the color fill; water is lighter
- Always use a single tone family per logo/icon — don't mix green icon with blue text in same logo

---

## Photography Guidelines

### Approved Subject Matter
- Nature environments: forests, mountains, lakes, rivers, wetlands
- Hands interacting with nature (holding plants, seedlings, soil)
- Aerial/drone nature shots (forests, coastlines)
- People presenting, collaborating, or working in green/outdoor contexts
- Children and youth in nature (inclusive, diverse)
- Clean technology and innovation contexts

### Photography Style
- Bright, vibrant, full-color nature photography
- High contrast, clear subjects
- Environmental and inspiring tone

### Logo Placement on Photos
- Top-left corner, 3 cm from all edges
- Only where background allows legibility (light area or with white logo)
- Use white version of logo on dark photo backgrounds
- Use dark blue version only on light/clear photo areas
- NEVER place logo where it blends into busy background

### What to Avoid in Photography
- Dark, gritty, industrial, or dystopian imagery
- Stock photos that feel generic or corporate
- Images without environmental or human connection
- Anything that contradicts the clean/green/hopeful brand message

---

## Layout Motifs

### The Geometric Block System
The primary layout motif is overlapping/adjacent color-filled rectangles:
- Blocks in Deep Blue, Light Cyan, Forest Green, Light Green, or Sky Blue
- No outlines/borders — blocks use flat fills only
- Blocks often overlap slightly (z-stacking) to create depth
- Large blocks carry headline text (white or contrasting brand color)
- Small blocks act as decorative anchors

### The Wave / Fluid Shape
Used exclusively on:
- Official letterhead headers (printed and digital)
- Envelope designs
- Digital document headers
This is NOT for general use on social posts or presentations.

### Section Numbering Style
Documents and presentations use this pattern at top-left of pages:
```
04  Usos internos
```
Small bold number (01, 02, 03...) in Forest Green, followed by section name in regular Deep Blue text.

### Two-Column Module
A recurring structural pattern:
- Left: Dark blue or green block with bold, large white heading (often 2-3 lines)
- Right: Body content on light background (cyan or white)
Proportions roughly 40/60 or 35/65.

---

## Digital & Web Color Usage

For HTML/React/digital artifacts, translate brand colors to CSS variables:

```css
:root {
  --cth-deep-blue: #0C498A;
  --cth-light-cyan: #B2EEFA;
  --cth-light-green: #9DC384;
  --cth-forest-green: #669348;
  --cth-sky-blue: #69B5FA;
  --cth-white: #FFFFFF;
}
```

**Typical digital page structure:**
```
Header: background #0C498A, logo white version, tagline in #B2EEFA
Hero/Banner: background #B2EEFA, large heading in #0C498A
Section accent: background #669348 or #9DC384
Body: background white or #B2EEFA, text #0C498A
CTA Buttons: background #0C498A, text white; hover: #669348
Footer: background #0C498A, text white + #B2EEFA
```

---

## Sub-Brand Logos (Programs)

Three programs, each with own logo variant:

| Program | Color Theme | Usage |
|---------|------------|-------|
| **Ideación** | Light Cyan `#B2EEFA` | Early-stage / ideation contexts |
| **Incubación** | Light Green `#9DC384` | Growth/incubation contexts |
| **Aceleración** | Forest Green `#669348` | Scale/acceleration contexts |

All three follow: CTH rocket+globe icon (in program color) + program name (large) + "Powered by CleantechHUB" (smaller, below).
Same size, spacing, and placement rules as main logo.
