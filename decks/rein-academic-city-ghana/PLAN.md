# Plan — REIN Hubs × Academic City deck

Date of this plan: 20 Oct 2026.
Meeting on the ticket: 21 Oct 2026.
Room name on the ticket: Pav.

## Goal

Build one English HTML deck for the Academic City meeting.
Keep the April 2026 proposal HTML text.
Keep the April 2026 proposal HTML order.
Add the 3-year investment scale.
Add the asset-to-stage map.
Add a SOURCES slide and `SOURCES.md`.

## Audience

Pav, in a REIN Hubs meeting on 21 Oct 2026.
Full name of Pav: not in the source files.
Role of Pav: not in the source files.

## Deliverable

Folder: `decks/rein-academic-city-ghana/`.
File: `index.html`.
Stage: 1920 × 1080.
Brand: REIN Hubs.
Branch: `rein-academic-city-ghana`.
Pull request: draft.
Do not deploy.
Do not merge.

## Done when

1. `index.html` opens with no server build step.
2. Paths inside the folder are relative.
3. Type inside the stage is 24px or more.
4. `?print` shows every slide.
5. The Year 1 check equals 103.
6. The three-year check equals 228.
7. Each asset-to-stage cell is `[PENDIENTE]`.
8. Preview PNGs exist for the cover, the investment slide, and the asset map.

## Sources in hand

1. `sources/academic-city-ghana-2026-04-23.html` — proposal page.
2. `sources/academic-city-ghana-2026-04-23.txt` — same words as the HTML page.
3. `sources/REIN_AcademicCityGhana_Deck_v1.pdf` — a different 18-page deck.
4. Gideon Blaauw via REIN Hubs desk, 20 Oct 2026 — the 3-year scale only.

The HTML page and the TXT file match.
The PDF does not match the HTML page.

## Constraints

- Invent no number, name, date, or link.
- Context is REIN Hubs. Use `#335D4F`, `#FF6633`, `#222A27`, `#5F6663`, `#C9D6D1`, `#F1F5F3`.
- Body face: Open Sans. Heading face: Poppins.
- Do not load a font from the network. Font files sit in `fonts/`.
- Credit line: `REIN Hubs · PVBLIC × CleantechHUB`.
- Footer: `Awaiting Gideon's approval`.
- Language of the proposal: English.
- Do not write Spanish sentences. The source has none.
- Shell behavior follows `skills/cth-html-deck` on branch `cursor/cth-html-deck-skill-3ac4`: menu, arrows, dots, expand cards, lightbox, questions, hash, `?print`.
- There is no `skills/rein-hubs-brand/SKILL.md` on `main`. Take the six colors from the deck skill.

## Out of scope

- Deploy to Vercel.
- Deploy to `decks.cleantechhub.net`.
- Merge of the pull request.
- A new action calendar.
- A Year 2 split.
- A Year 3 split.
- An asset-to-stage link.
- Copy of any figure from `cth-rein-funding-oct2026`.
- Spanish translation.

## Sum checks

Gideon scale:

- 75 + 8 + 20 = 103. Year 1 total is correct.
- 103 + 75 + 50 = 228. Three-year total is correct.

April 2026 HTML budget:

- 15000 + 30000 + 18000 + 12000 = 75000.
- 75000 matches programs US$75K.
- 8000 matches comms and hub maintenance US$8K.
- 20000 matches operations and integration US$20K.
- 15000 + 30000 + 18000 + 12000 + 8000 + 20000 = 103000.
- 103000 matches Year 1 US$103K.

The HTML page does not use the word "programs" for those four lines.
The HTML page does not state a Year 2 amount.
The HTML page does not state a Year 3 amount.

## Build order

1. Write this plan.
2. Copy the shell behavior. Set REIN colors.
3. Write the proposal slides in HTML order.
4. Write the investment slide.
5. Write the stage slide and the asset map.
6. Write `SOURCES.md`, the SOURCES slide, and `PENDIENTES.md`.
7. Run `build.sh`.
8. Open the deck. Fix clips.
9. Write `CHECK.md`.
10. Push the branch. Open a draft pull request.

## Push back

1. Do not merge the HTML page and the PDF.
   The PDF states other budget lines, other stage durations, and other counts.
   This deck keeps the HTML words on the proposal slides.
   The PDF stage list appears only on the stage slide, with a source label.
   PDF-only labs and ventures appear only on the asset map, with a source label.

2. Do not copy the PDF budget amounts into this deck.
   The deck skill says: do not cite REIN Hubs dollar amounts.
   The ticket orders two exceptions: the HTML proposal, kept intact, and the Gideon scale.
   The ticket does not order the PDF budget.
   `PENDIENTES.md` points to PDF page 7. It does not repeat those amounts.

3. Do not choose a stage model.
   The HTML cards say Activation, Incubation, Acceleration, and Cross-Continent Growth.
   The HTML fact row says Ideation, Incubation, Acceleration, and Growth.
   The PDF says Ideation, Incubation, Acceleration, and Growth, with other durations.
   The sources do not say that these names are the same stage.
   The map cell for every asset is `[PENDIENTE]`.

4. Do not invent Spanish.
   The deck skill asks for English and Spanish.
   The ticket says: use Spanish only when the original has Spanish.
   The original is English. One Spanish word in the HTML is "Convocatoria".
   Keep that word. Do not translate the deck.
   Spanish copy is `[PENDIENTE]`.

5. Do not launch more Cloud Hands from this run.
   The deck skill asks for one Hands job per slide group, each with a bc-id.
   This run is already one Cloud Hands.
   A second writer can change a figure.
   One writer keeps the figures stable.
   `CHECK.md` is a separate pass after the slides exist.

6. Do not invent a person record for Pav.
   The cover uses the ticket name Pav.
   Full name and role are `[PENDIENTE]`.

7. Do not update the April 2026 action list.
   Those dates are before 21 Oct 2026.
   The slides keep the dates.
   A new action list is `[PENDIENTE]`.

8. Do not send this deck to the room.
   REIN HOLD is active.
   The footer says Awaiting Gideon's approval.

9. The proposal footer contains `pvblic.org` links.
   The deck skill says: do not cite pvblic.org as a brand source.
   This deck keeps those links as proposal text.
   This deck does not take new facts from that site.

10. Granola has no note for a 21 Oct 2026 meeting.
    Do not add meeting decisions from memory.

## Update — REIN desk, 20 Oct 2026

The desk closed three items. The working stage label is Ideation (Activation). The asset map uses that desk list. English only is approved. Seat and team counts stay open. The count conflicts, the founding year, Pav, the action list, and the Year 2 and Year 3 splits stay open.

## Slide list

1. Cover
2. What is REIN Hubs
3. Key facts
4. FOSD and GHF
5. ALI and Pvblic One
6. Network
7. Support system
8. Six operational pillars
9. Annual budget
10. Four stages
11. 2026 milestones
12. Impact
13. Academic City
14. Organisation profile
15. Labs and initiatives
16. Alumni and ventures
17. Strategic fit
18. Quote and tailwind
19. Next steps
20. Contacts
21. 3-year sliding investment scale
22. Stage lists
23. Academic City assets → REIN stages
24. SOURCES
