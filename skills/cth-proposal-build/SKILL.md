---
name: cth-proposal-build
description: >
  Build, iterate, and deploy polished client-facing service proposals for CleantechHUB (CTH). Use this skill EVERY TIME Gideon asks to create a proposal, pitch document, service offering, or RFP response for any client or partner. Also trigger when asked to "build a proposal", "respond to an RFP", "write up a services doc", "create a pitch for [client]", "redo the HTML", or "update the proposal". This skill governs the full pipeline: research → HITL alignment gate → HTML proposal build → PDF export → Vercel deploy. It encodes all hard-won lessons from the Aliarse +PYMES proposal build (April 2026) including CTH brand application, SVG logo construction, animated components, PDF generation, and known failure modes.
---

# CleantechHUB Proposal Build Skill

Full pipeline for building client-facing CTH proposals: research → alignment analysis → HITL gate → branded HTML → PDF → deploy.

---

## Pipeline Overview

```
1. Read RFP / brief carefully
2. Run research agent (client + CTH alignment)
3. HITL gate — present analysis + GO/NO GO, wait for approval
4. Gather team + pricing inputs (ask_user_input_v0)
5. Build HTML proposal (CTH brand, interactive)
6. Generate PDF (Playwright)
7. Deploy to Vercel (if requested)
```

Always complete Steps 1–4 before writing any HTML. Never skip the HITL gate.

---

## Step 1 — RFP Analysis

Read the document carefully. Extract:

- **Client name, mission, founded**
- **Role/scope** — is this hiring, consulting, partnership, or implementation?
- **Exact requirements** — list every function, competency, and experience requirement
- **Geography** — countries, modality (remote/hybrid/on-site)
- **Deadline** — note urgency, highlight if < 2 weeks
- **Contact / submission** — name, email, deadline

Flag any requirements CTH cannot fully meet — propose mitigation strategy.

---

## Step 2 — Research Agent

Run web searches in parallel:

```
- "[Client name] organización historia programas impacto"
- "[Client name] LinkedIn" → fetch for partners, donors, scale
- "[Client name] + CTH overlap keywords" (MIPYMES, cleantech, etc.)
- CTH references relevant to this RFP (P4G, REIN, UNDP-AFCIA, CLP, etc.)
```

Fetch URLs directly when found (LinkedIn, official site, news articles).

**CTH Reference Projects to cite** (pull whichever are relevant):

| Project | Donor | Amount | Relevance |
|---|---|---|---|
| MubOn – EV charging Colombia | P4G / Denmark | USD $338K grant | Non-reimbursable fund management |
| REIN Hubs | PVBLIC Foundation + Family Offices | Do NOT cite dollar amount | Regional hub network, 5 countries |
| UNDP-AFCIA Colombia | PNUD Adaptation Fund | Grant (amount varies) | Multilateral funding, climate startups |
| ClimateLaunchpad | EIT Climate-KIC | Program fees | Startup training, competition |
| Climathon | EIT Climate-KIC | Program fees | Hackathon/ideation |

⚠️ **Never cite the REIN Hubs dollar amount** — it is not confirmed public. Use "5 países · 1,000+ ventures" instead.

---

## Step 3 — HITL Alignment Gate

Present to Gideon before building anything:

### 3a. Client Intelligence Summary
- Who they are, scale, donors, reputation
- Key programs relevant to CTH
- Decision-makers and contacts

### 3b. Alignment Scorecard (table)
Score each RFP requirement: ✅ Strong / ⚡ Moderate / ⚠️ Gap

### 3c. GO / NO GO Recommendation
- State clearly: **GO**, **CONDITIONAL GO**, or **NO GO**
- For conditional: explain exactly what gaps exist and how to mitigate
- For gaps: always propose a named person or sub-contractor solution

### 3d. Ask pre-build questions via `ask_user_input_v0`
Required inputs before building:
- Delivery team members (names + roles)
- Pricing model preference
- Language (Spanish / English / Bilingual)
- Any additional context or constraints

**Wait for explicit GO confirmation before proceeding.**

---

## Step 4 — Team Setup

### Standard CTH Team (as of April 2026)
| Name | Role | Default focus |
|---|---|---|
| Gideon Blaauw | Regional Lead / CEO | Strategy, multilateral relations, representation |
| Angélica Díaz | Tech Lead | Curriculum, M&E, technical delivery |
| Jennifer González | Growth Lead | Fundraising, proposals, institutional partnerships |
| [Advisor TBD] | Domain Specialist | Cover gaps specific to client (e.g., SBD Costa Rica) |

Add/remove team members based on Gideon's input in Step 3d.

### Contact Details (always use these)
- **Phone / WhatsApp:** +57 313 715 5965
- **Email:** gideon.blaauw@cleantechhub.net
- **Address:** CL 90 # 19–41, Oficina 801, Bogotá D.C., Colombia
- **Web:** cleantechhub.net

---

## Step 5 — HTML Proposal Build

### 5a. Required Sections
All proposals include these sections in order:

1. **Hero / Cover** — client name, program, eyebrow label, pills, hero stats
2. **Sticky Nav** — with section links and contact CTA button
3. **Alineación estratégica** — CTH intro, fit scorecard, animated bar chart
4. **Alcance del trabajo** — scope cards grid with color-coded left borders
5. **Oferta de servicios** — accordion (S1–Sn), each with Retainer/Milestone tag
6. **Entregables** — tabbed panels by phase
7. **Experiencia y referencias** — 3 reference cards + animated counters
8. **Precios** — 2 pricing cards + donut chart + total box
9. **Cronograma** — vertical timeline with hover effects
10. **Fuera de alcance** — warning grid
11. **Términos y condiciones** — 2-col grid
12. **Equipo** — team cards with SVG avatars
13. **CTA final** — email + WhatsApp buttons
14. **Footer** — logo, contact, references, legal

### 5b. CTH Brand Rules (non-negotiable)
See `cleantechhub-brand` skill for full details. Key rules:

**Colors — ONLY these 5:**
```
--deep:   #0C498A  (primary, formal, headers)
--cyan:   #B2EEFA  (primary, light fills, water)
--lgreen: #9DC384  (primary, earth, creative)
--fgreen: #669348  (secondary, earth, accents)
--sky:    #69B5FA  (secondary, water, supporting)
```
No other colors. No purple, no black backgrounds with dark blue logo.

**Fonts:**
```
Titillium Web 900 → headlines, numbers, logo wordmark
Open Sans → body text, labels, UI
PT Sans → supporting copy
```
Load from Google Fonts: `Titillium+Web:wght@300;400;600;700;900` + `Open+Sans:wght@300;400;600;700;800`

**Logo (CRITICAL — see known failure modes below):**
Always build the CTH logo as inline SVG. NEVER use `<img>` tags with base64 PNG — they fail silently on dark backgrounds. See Section 6 for the exact SVG template.

### 5c. Interactive Components

#### Scroll Progress Bar
```css
#progress-bar { position:fixed;top:0;left:0;height:3px;
  background:linear-gradient(90deg,var(--fgreen),var(--sky));
  width:0%;z-index:9999; }
```
```js
window.addEventListener('scroll',()=>{
  const pct = (doc.scrollTop) / (doc.scrollHeight - doc.clientHeight) * 100;
  document.getElementById('progress-bar').style.width = pct + '%';
});
```

#### Reveal on Scroll (IntersectionObserver)
Add `class="reveal"` to sections. CSS: `opacity:0; transform:translateY(30px); transition: opacity .6s, transform .6s`.
On intersection: add `class="visible"` → `opacity:1; transform:none`.
Also trigger fit-bar animations and counter animations inside the observer callback.

#### Animated Counters
```html
<span class="count" data-target="1000" data-decimal="0">0</span>
```
```js
function animateCount(el) {
  const target = parseFloat(el.dataset.target);
  const decimal = parseInt(el.dataset.decimal || 0);
  let v = 0; const dur = 1600, step = 16, inc = target/(dur/step);
  const t = setInterval(() => {
    v = Math.min(v+inc, target);
    el.textContent = decimal ? v.toFixed(decimal) : Math.floor(v);
    if (v >= target) clearInterval(t);
  }, step);
}
```

#### Fit-Score Bar Chart
```html
<div class="fit-bar-fill green" data-w="95"></div>
```
Trigger in IntersectionObserver: `bar.style.width = bar.dataset.w + '%'`
CSS transition: `width 1.2s cubic-bezier(.25,.46,.45,.94)`

#### Services Accordion
Each `.srv` div has a header (onclick toggleSrv) and a body with `max-height:0` → `max-height:300px` via `.open` class.

#### Deliverables Tabs
`.tab-btn` + `.tab-panel` system. Active panel gets `display:grid`, inactive gets `display:none` with `fadeup` animation.

#### Donut Chart (CRITICAL — see known failure modes)
**Always use pure SVG `<path>` arcs. Never use JS `stroke-dasharray` on `<circle>` elements.** The JS approach fails silently in most browsers when inserted dynamically.

Use Python to pre-calculate the path geometry:
```python
import math
def donut_path(cx, cy, r, start_deg, end_deg, stroke_w=38):
    s = math.radians(start_deg - 90)
    e = math.radians(end_deg - 90)
    outer_r = r + stroke_w/2; inner_r = r - stroke_w/2
    ox1 = cx + outer_r*math.cos(s); oy1 = cy + outer_r*math.sin(s)
    ox2 = cx + outer_r*math.cos(e); oy2 = cy + outer_r*math.sin(e)
    ix1 = cx + inner_r*math.cos(e); iy1 = cy + inner_r*math.sin(e)
    ix2 = cx + inner_r*math.cos(s); iy2 = cy + inner_r*math.sin(s)
    large = 1 if (end_deg - start_deg) > 180 else 0
    return (f"M {ox1:.2f},{oy1:.2f} "
            f"A {outer_r:.2f},{outer_r:.2f} 0 {large},1 {ox2:.2f},{oy2:.2f} "
            f"L {ix1:.2f},{iy1:.2f} "
            f"A {inner_r:.2f},{inner_r:.2f} 0 {large},0 {ix2:.2f},{iy2:.2f} Z")

total = sum(vals); gap = 4; angle = 0
for i, (val, color) in enumerate(slices):
    frac = val/total
    end = angle + frac*360 - gap
    d = donut_path(100, 100, 62, angle+gap/2, end, 38)
    # embed d directly in SVG <path fill="{color}">
    angle += frac*360
```
Embed the paths as static SVG. Add `@keyframes fadeSlice { from{opacity:0} to{opacity:1} }` and inline `style="opacity:0;animation:fadeSlice 0.7s ease Xs forwards"` per slice.

#### Animated Rocket / Hero Illustration
Use a self-contained `<svg>` with embedded `<style>` and `@keyframes`. Required animations:

| Animation | Target | Timing |
|---|---|---|
| `rocketFloat` | Entire rocket group | 4s ease-in-out infinite, translateY(0→-16px) |
| `flameFlicker` | Flame ellipses | 0.18s ease-in-out infinite, scaleY(0.8→1.4) |
| `flameSpark` | 3 particle ellipses | 0.6s ease-out infinite, staggered 0/0.2/0.4s, translateY down + fadeout |
| `starTwinkle` | 6-8 star circles | 2–3.5s, varying delays, opacity 0.2→0.9 |
| `orbitDot` | Small circle | 8s linear infinite, rotate(0→360deg) translateX(88px) |
| `cloudDrift` | Background ellipses | 12–16s, translateX(-20px), opacity pulse |

The rocket SVG must be inside its own panel div (e.g., sky-blue background block), not embedded in the hero section body directly.

---

## Section 6 — SVG Logo Templates

### KNOWN FAILURE: Never use `<img>` with base64 PNG on dark backgrounds
The PNG logo has a black background. CSS filters (`brightness(0) invert(1)`) are unreliable across contexts. Always use the SVG version.

### Nav Logo (white, 40px height)
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 56" style="height:40px;width:auto">
  <g transform="translate(2,2)">
    <!-- Globe -->
    <circle cx="26" cy="24" r="20" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.8"/>
    <circle cx="26" cy="24" r="18" fill="rgba(255,255,255,0.12)"/>
    <!-- Continents (simplified) -->
    <path d="M16 16 Q22 11 29 13 Q36 15 38 22 Q40 30 36 36 Q30 42 23 38 Q16 34 14 26 Q12 19 16 16Z" fill="rgba(255,255,255,0.65)"/>
    <path d="M28 13 Q34 10 39 13 Q43 17 41 23 Q39 28 35 29 Q31 28 29 23 Q27 18 28 13Z" fill="rgba(255,255,255,0.45)"/>
    <!-- Equator -->
    <path d="M6 24 Q16 20 26 24 Q36 28 46 24" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="1"/>
    <!-- Rocket (upper-left, rotated -40deg) -->
    <g transform="translate(7,1) rotate(-40,13,15)">
      <ellipse cx="13" cy="14" rx="4" ry="9" fill="rgba(255,255,255,0.92)"/>
      <ellipse cx="13" cy="7" rx="2.8" ry="4" fill="rgba(255,255,255,0.75)"/>
      <circle cx="13" cy="14" r="2" fill="none" stroke="rgba(178,238,250,0.6)" stroke-width="1.2"/>
      <path d="M9 19 L6 26 L12 22Z" fill="rgba(255,255,255,0.6)"/>
      <path d="M17 19 L20 26 L14 22Z" fill="rgba(255,255,255,0.6)"/>
      <ellipse cx="13" cy="25" rx="2.5" ry="3.5" fill="rgba(178,238,250,0.55)"/>
    </g>
    <!-- Arc trail -->
    <path d="M12 38 Q6 28 10 16" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="3 2"/>
  </g>
  <text x="54" y="30" font-family="'Titillium Web','Open Sans',sans-serif" font-weight="900" font-size="22" fill="rgba(255,255,255,0.97)" letter-spacing="-0.3">CleantechHUB</text>
  <text x="55" y="46" font-family="'Open Sans',sans-serif" font-weight="300" font-size="10" fill="rgba(178,238,250,0.75)" letter-spacing="0.3">Inspira. Actúa. Transforma.</text>
</svg>
```

For the **hero section** (larger, 70px): scale up font-size to 36, icon group scale ~1.5x, adjust viewBox to `0 0 380 90`.

For the **footer** (dark bg, 48px): same as nav but `style="height:48px"`.

For **light backgrounds** (cyan/white): change all `rgba(255,255,255,x)` to `rgba(12,73,138,x)` and text fill to `#0C498A`.

---

## Step 7 — PDF Generation

### Use Playwright (NOT weasyprint)
weasyprint fails on complex CSS grid layouts and on Google Fonts subsetting. Always use Playwright Chromium:

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        with open('proposal.html','r') as f:
            html = f.read()
        await page.set_content(html, wait_until='networkidle')
        await page.wait_for_timeout(2000)  # let animations/fonts settle
        await page.pdf(
            path='proposal.pdf',
            format='A4',
            print_background=True,
            margin={'top':'10mm','bottom':'10mm','left':'0mm','right':'0mm'}
        )
        await browser.close()

asyncio.run(main())
```

Install if needed: `pip install playwright --break-system-packages -q && python3 -m playwright install chromium`

Expected output size: 250–350 KB for a full proposal.

---

## Step 8 — Vercel Deploy

Read the `dual-desktop-macos` skill before deploying — CTH deploys go from Desktop 1 (CleantechHUB profile).

```bash
# From terminal on CTH desktop
cd /path/to/proposal/
npx vercel --prod
# Follow prompts: project name, no framework, public dir = ./
```

Share the resulting URL with Aliarse (or relevant client) via email + WhatsApp.

---

## Known Failure Modes & Fixes

### ❌ Logo not loading / appearing black
**Cause:** Using `<img src="data:image/png;base64,...">` — the PNG has a black background, CSS filters are unreliable.
**Fix:** Always use inline SVG logo. See Section 6 for templates.

### ❌ Donut chart not showing colors
**Cause:** JS-based `stroke-dasharray` on `<circle>` elements inserted dynamically into SVG. Browser rendering timing issues.
**Fix:** Pre-calculate arc paths in Python using `math.cos/sin`, embed as static `<path fill="COLOR">` elements. No JS needed.

### ❌ Rocket / animations static in PDF
**Cause:** PDF renders the page at a snapshot; CSS animations are not captured in motion.
**Fix:** This is expected. PDF will show the rocket at its starting position. For the live HTML, all animations work. Consider adding a `@media print { .rocket-group { transform: translateY(-8px); } }` to position it nicely in the PDF.

### ❌ weasyprint failing on CSS grids
**Cause:** weasyprint has known bugs with CSS `grid-template-columns` on complex layouts.
**Fix:** Always use Playwright for PDF generation.

### ❌ Fit bars not animating
**Cause:** IntersectionObserver callback not finding elements with `data-w` attribute.
**Fix:** Trigger bar fills inside the IO callback on the `.reveal` elements that contain them, not on the bars directly.

### ❌ Google Fonts not loading in PDF
**Cause:** Playwright default network settings may block external fonts.
**Fix:** Use `wait_until='networkidle'` + `wait_for_timeout(2000)` to ensure fonts load before PDF capture.

### ❌ REIN Hubs dollar amount cited incorrectly
**Cause:** The "USD $15M+" figure for REIN is not confirmed public.
**Fix:** Always use "5 países · 1,000+ ventures" or "Hubs activos: Colombia · CR · Guatemala · Perú · El Salvador" instead.

---

## Pricing Model Reference

### Standard Hybrid Model
- **Retainer:** USD $4,500–$6,500/month depending on scope and team size
- **Milestones:** USD $800–$3,500 per verified deliverable
- **Specialist advisor:** USD $1,000–$1,500/month add-on

### Milestone Pricing Reference (Aliarse +PYMES build)
| Deliverable | Price |
|---|---|
| Training cohort completed (≥40 MiPYMES) | USD $3,500 |
| 10 SBD expedientes elaborated | USD $2,800 |
| Funding proposal approved | USD $1,500 |
| Quarterly impact report | USD $800 |
| New Hub activated (new city) | USD $2,000 |
| SBD Senior Advisor (monthly) | USD $1,200 |

Adjust all figures based on client budget signals, geography, and scope.

---

## File Naming Convention

```
aliarse_propuesta_v{N}_CTH.html   # Interactive HTML
aliarse_propuesta_v{N}_CTH.pdf    # PDF export
```
Replace `aliarse` with client slug. Increment `vN` on each revision.
Output to `/mnt/user-data/outputs/` and use `present_files` to deliver.

---

## Iteration Workflow

When Gideon asks for changes:
1. Open the current HTML from `/home/claude/` working file
2. Make targeted edits (Python string replace or `str_replace` tool)
3. Verify changes with a checks list printed to stdout
4. Copy updated file to `/mnt/user-data/outputs/`
5. Regenerate PDF only if content has meaningfully changed
6. `present_files` both HTML and PDF

For significant redesigns ("redo the HTML", "start over"), build fresh from this skill rather than patching.

---

## Related Skills

- `cleantechhub-brand` — Full CTH brand guidelines, color palette, typography, asset library
- `frontend-design` — Design principles for HTML artifacts (bold choices, animations, typography)
- `dual-desktop-macos` — Which desktop/profile to use for Vercel deploy
- `pdf` — PDF generation reference (note: use Playwright, not weasyprint, for complex HTML)
- `gmail` — Sending the final proposal to the client
- `canva` — If client needs a visual one-pager in addition to the HTML proposal
