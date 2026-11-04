# CLP26 one-page report shell (sanitized)

Neutral template extracted from a CTH programme report page. All content, names, figures, links and data were removed; only layout, styling, JS components and CTH brand assets remain. Text shows placeholders ("Slide title", "Lorem ipsum", "Partner name", "Lorem stat", 0).

## Files
- `index.html` – single page: sticky topbar (logo, anchor nav, EN/ES toggle, burger), sections: Hero (eyebrow, title, leads, 3 animated stat counters `data-count`, 2 CTAs), Sponsors/partner logo groups + host grid + role cards, Journey timeline with detail panel, Stories (tabs + story card), Built grid + video gallery with filter, Mentors & Jury people groups (drawer bios), Bot/assistant card with modules and stats, CTA block with benefits list, Explorer (filters: selects, range slider, toggles, reset; map; 3 Chart.js charts; impact cards; searchable/sortable table; downloads card), footer, drawer and video modal.
- `styles.css` – CTH palette via CSS vars (green #335D4F, orange #FF6633, ink, gray), Open Sans/Poppins (Google Fonts), responsive grid.
- `app.js` – bilingual i18n dictionary `T` (keys used by `data-i18n` / `data-i18n-ph`), counter animation, timeline/story/gallery renderers, role cards, drawer/modal, explorer filtering, d3+topojson map, Chart.js charts. Inline data arrays were trimmed to 1–2 placeholder entries.
- `lib/` – chart.umd.js, d3.min.js, topojson-client.min.js (vendored, unmodified).
- `logos/cleantechhub.png` – CTH brand logo.
- `data/` – placeholder JSON with the expected shapes; `countries-110m.json` is the public world-atlas topojson.

## Use
1. Copy the folder, edit `T.en` / `T.es` strings in `app.js` and the arrays near the timeline/stories/built sections.
2. Fill `data/*.json` following the placeholder shapes (people, mentor_cards, jury_cards, hub_cards, startups).
3. Serve statically (`python3 -m http.server`) — `fetch()` needs http, not file://.
4. Set real `href`s (CTA mailto, downloads, footer links) — they are `#` here.
5. **Download PDF (HARD 4 Nov 2026):** add `../pdf-download.css` rules + `../pdf-download.html` fragment to `index.html`, run `../export-deck-pdf.py --pdf <basename>.pdf`, commit PDF beside HTML. See `../README.md` and `docs/html-deck-protocol.md`.

This folder also includes `pdf-download.css` and `pdf-download.html` copies for convenience when forking the shell.
