# CHECK — REIN Hubs × Academic City — 20 Oct 2026

Verifier pass after the slides were built. This file does not change slide prose.

| Check | Result |
|---|---|
| Clipped sides | Pass. At 1920×1080, 1512×982, 1366×768, and 1280×800, text nodes on the active slide sit inside the slide box. Print mode: 24 slides, each 1920×1080, no text node outside the slide. |
| Minimum type | Pass. Direct text inside `.deck-stage` computes at 24px or more. `.nav-hint` is 14px, outside `.deck-stage`, and hidden in `body.print-all`. `#slide-dots button` is 14×14px and sets no `font-size`. |
| Citation per figure | Pass. Numeric callouts use `a.cite` on the same slide. The link is visible without `?review`. |
| SOURCES slide | Pass. Slide 24 `data-menu-title` is `SOURCES`. Its links match `SOURCES.md`. |
| No invented numbers | Pass for the figures this deck states. HTML figures cite the April 2026 proposal. The 3-year scale cites Gideon Blaauw via REIN Hubs desk, 20 Oct 2026. Checks: 75+8+20=103 and 103+75+50=228. PDF page 7 budget amounts are not copied. Open conflicts are `[PENDIENTE]` in `PENDIENTES.md`. |
| PDF | Pass. `render-deck.py` wrote 24 pages. The DOM has 24 `.slide` elements. |
| curl 200 | Pass locally. `http://127.0.0.1:8765/index.html` returned HTTP 200 `text/html`. `fonts/open-sans.woff2` returned HTTP 200 `font/woff2`. The public URL is not live. This check does not publish. |
| EN/ES | Pass for this ticket. The REIN desk approved English only on 20 Oct 2026. The Spanish chip is removed. The deck does not invent Spanish sentences. |
| Keyboard | Pass. ArrowRight moves forward. ArrowLeft moves back. On a tablist, ArrowRight changes the year and does not change the slide. On the asset map, a click or ArrowRight changes the stage and does not change the slide. Hash `#1` opens the cover. Escape closes the index. The index lists 24 titles. Year 2 tab shows the Year 2 panel and marks that bar. |
| Brand tokens | Pass. `shell/deck.css` contains `#335D4F`, `#FF6633`, `#222A27`, `#5F6663`, `#C9D6D1`, and `#F1F5F3`. It does not contain `#0C498A`, `#B2EEFA`, `#69B5FA`, `#9DC384`, `#669348`, `#2D6A4F`, `#95D5B2`, `#1B4332`, `#F1562A`, or `#FC987C`. No `Inter` in `font-family`. |

## Not done

- No deploy.
- No Vercel project.
- No merge.
- Slug after Gideon says yes: `rein-academic-city-ghana`.
- Future URL: `https://decks.cleantechhub.net/rein-academic-city-ghana/`.
