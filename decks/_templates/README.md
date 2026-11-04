# Deck templates

Shared pieces for CleantechHUB HTML decks on `decks.cleantechhub.net`.

## Download PDF (HARD — 4 Nov 2026)

Every deck folder that ships `index.html` must also ship a print-ready PDF and two **Download PDF** links. Full rules: `docs/html-deck-protocol.md`.

| File | Role |
|---|---|
| `pdf-download.css` | Footer + fixed pill styles; hides controls in `@media print`. |
| `pdf-download.html` | Copy-paste fragment — replace `DECK_BASENAME.pdf`. |
| `pdf-download.js` | Optional in-browser prep (reveals + counters); export script duplicates this. |
| `export-deck-pdf.py` | Generate the PDF beside the HTML. |

### Quick start

1. Copy `pdf-download.css` rules into the deck stylesheet (or link the file if the build allows).
2. Paste the fragment from `pdf-download.html` into `index.html` (footer + before `</body>`).
3. From the deck directory:

```bash
cp ../_templates/export-deck-pdf.py .
python3 export-deck-pdf.py --pdf YOUR-BASENAME.pdf
```

4. Commit `index.html` and `YOUR-BASENAME.pdf` in the same folder.
5. Verifier: both links return 200; print preview hides buttons; PDF is A4 landscape with backgrounds.

**Stage decks** (`.deck .slide`): script opens `index.html?print`, adds `print-all`, and exports. **Scroll decks** (REIN long-page): script finalizes `.reveal` and `[data-count]`, then exports the full document.

Playwright installs Chromium on first run (`pip install playwright && playwright install chromium`). Cloud Agent base image includes Python; install Playwright only when exporting.

### Brand tokens

Override before importing CSS:

```css
:root {
  --pdf-dl-bg: #2d6a4f;   /* CleantechHUB primary */
  --pdf-dl-focus: #1b4332;
}
```

REIN scroll decks typically use `--pdf-dl-bg: #ff6633` and `--pdf-dl-focus: #335d4f` (see `skills/rein-hubs-brand/SKILL.md`).

## `clp26-rein-shell/`

Sanitized one-page CLP26 / REIN report shell. When promoting a copy to a live deck, add the PDF snippet and run `export-deck-pdf.py` per the HARD rule above.
