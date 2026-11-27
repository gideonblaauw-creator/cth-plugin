# Print QA notes — Part 3 questionnaire

- **Letterhead source:** `/opt/claude-files/Projects/CTH-Brand/letterhead/` (copied to `print/letterhead/`).
- **Header:** `CTH_header.png` — full bleed width; wave flush top on each page.
- **Footer bar:** `CTH_footer.png` fixed at bottom; address Open Sans 8 pt `#0C498A` above the bar.
- **Body:** Open Sans 9.5 pt; fields use write-in lines (hand fill).
- **Regenerate:** `print/render-questionnaire-pdf.sh` (Chromium + `build-questionnaire-html.py`).
- **Forms sync:** `print/compare-questions.py` (pdftotext vs `part3-google-forms-question-list.md`).

Checker crops: compare `letterhead/CTH_header.png` and rendered page 1 in a viewer.