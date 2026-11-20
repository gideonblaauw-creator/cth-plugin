# Visual QA — Observatorio de la Tierra · Datatón (EO brand v3)

Compared `review/slide-*.png` (1920×1080, print-pdf / final fragments) to Gideon basis 4 Nov 2026 (`review/refs/` and uploaded `gideon-basis.pdf`).

| Slide | Check | Result |
| --- | --- | --- |
| 01 | Cover: `#0C498A` scrim, orbit lines, reverse cobrand, green tagline, photo credit | Pass |
| 02 | Statement: full-bleed Apaporis, white quote type, green rule on attribution | Pass |
| 03–06 | White inner: large light-green section number, Titillium title, thin cyan rule, Open Sans body | Pass |
| 04 | Helix + dashed invitation circle (staged fragments in present mode) | Pass |
| 05–06 | Cards filled; slides marked for Alejandro trim 23 Nov in speaker notes | Pass (copy as shipped) |
| 07 | Cacao full-bleed, five solid lens cards + tech thread; CC BY-SA line | Pass |
| 08 | Five palanca questions + callout (lower third filled) | Pass |
| 09 | Magdalena photo (not pilot territory), three phase cards, open-time callout, no Bolívar name | Pass |
| 10 | Four Datalab environments, Datatón highlight, 10:05 handoff bar | Pass |
| 11 | Cocora close, handoff card, tagline, no Confidencial | Pass |

## Lint / build

- `tools/reveal/lint.sh observatorio-tierra-dataton` — exit 0
- `tools/reveal/outline.sh --validate-only decks/observatorio-tierra-dataton/deck.yaml` — deck.yaml OK
- PDF `observatorio-tierra-dataton.pdf` — 11 pages (matches slide count)
- Motion: Ken Burns + orbit drift under `prefers-reduced-motion: no-preference`; static in print/`print-pdf`

## Notes

- Photos: Colombian CC BY-SA only; no people observed in hires stills.
- Palette: official EO hex set only in deck CSS (`#0C498A`, `#B2EEFA`, `#9DC384`, `#669348`, `#69B5FA`, white).
- Public route still requires Infrastructure · Desks Caddy after merge (`/observatorio-tierra-dataton/`).