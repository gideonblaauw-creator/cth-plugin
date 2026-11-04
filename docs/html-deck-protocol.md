# HTML deck protocol

**Owner:** Presentations desk (Gideon 19 Oct 2026)  
**Canonical skills:** `skills/cth-html-deck/SKILL.md` when on `main` (replaces `cth-html-deck-visual` for the 1920×1080 stage shell); scroll-style REIN decks follow `skills/cth-html-deck-visual/SKILL.md` and `skills/rein-hubs-brand/SKILL.md`.  
**Harness:** `skills/harness/references/hands-ticket-hard.md` § HTML decks.

Context desks write the brief, sources, and ticket. They do not build the deck. Presentations tickets Cursor Hands. Hands builds in micro-parallel pieces with maker ≠ checker. HITL before deploy or send. Public URL: `https://decks.cleantechhub.net/<slug>/` (Infra deploy — not Hands).

## Interactive contract (summary)

- **Stage decks** (CleantechHUB, REIN slide shell, AIC): 1920×1080 stage, menu, arrows, dots, citations, SOURCES slide + `SOURCES.md`, EN/ES, `?print`. See `skills/cth-html-deck/SKILL.md` on branch `cursor/cth-html-deck-skill-3ac4` until merged.
- **Scroll decks** (long-page REIN partner decks): section `.slide` or `.reveal`, fixed nav optional. Same sourcing and HITL rules.

## Download PDF (HARD — Gideon 4 Nov 2026)

Every HTML deck ships a **print-ready PDF** beside `index.html` and **two identical Download PDF controls** in the HTML:

| Requirement | Detail |
|---|---|
| Footer control | Inside `<footer>` (or deck footer region): wrapper `.pdf-dl-footer` with `<a class="pdf-dl-btn" href="<basename>.pdf" download="<basename>.pdf">Download PDF</a>`. |
| Fixed control | Same `href` / `download` on `<a class="pdf-dl-btn pdf-dl-fixed" … aria-label="Download PDF">Download PDF</a>` fixed bottom-right (`right: ~22px`, `bottom: ~22px`, `z-index` below modals, above content). |
| Print | `@media print { .pdf-dl-btn, .pdf-dl-fixed, .pdf-dl-footer { display: none !important; } }` — buttons never appear on printed output or in the exported PDF. |
| PDF file | Same folder as `index.html`. Name `<slug-or-topic>.pdf` (stable basename; no query strings). Regenerate when HTML changes. |
| PDF content | **A4 landscape**, `printBackground: true`. All `.reveal` (or equivalent) in final visible state. All `[data-count]` counters at final numeric values. No chrome that screen mode hides unless `?print` / `print-all` already exposes it for stage decks. |
| Reference | Live pattern: `https://decks.cleantechhub.net/rein/externado-ncuk/` (footer + fixed orange pill; PDF co-located). Repo templates: `decks/_templates/pdf-download.*`, `decks/_templates/export-deck-pdf.py`. |

Hands add the snippet and run the export script in the deck folder. Do not commit confidential REIN figures; public repo decks stay sanitized.

## Build artifacts

| Artifact | Purpose |
|---|---|
| `decks/_templates/pdf-download.css` | Shared button + print-hide styles (brand tokens via CSS vars). |
| `decks/_templates/pdf-download.html` | HTML fragment to paste (replace `DECK_BASENAME.pdf`). |
| `decks/_templates/export-deck-pdf.py` | Headless Chromium (Playwright) PDF export with reveal/counter finalization. |
| `decks/_templates/README.md` | Usage for new decks and backfill. |

## Acceptance (verifier)

Record in `CHECK.md`:

- Footer and fixed Download PDF links resolve to a PDF in the same directory (HTTP 200 after publish).
- `@media print` hides both controls (grep or manual print preview).
- PDF page size is A4 landscape; spot-check one `.reveal` slide and one counter match final on-screen values after export.
- No REIN dollar amounts or confidential content in repo copies.
