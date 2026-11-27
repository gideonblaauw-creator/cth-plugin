# Hands ticket: Datatón 24 Nov · preguntas por espacio (PDF)
Datalab desk · Gideon ask 23 Nov 18:08 COT (his words: "build 1 pdf with questions for every space, 1 page per space in the agenda, make sure everything is an ongoing conversation, not only ask the question but already anticipate what a potential response would be leave that in brackets, follow the CTH brand style").
Route: Cloud Hands, composer-2.5, Fast OFF. New draft PR on gideonblaauw-creator/cth-plugin. Write only to decks/dataton-2026-preguntas-espacios/. No merge, deploy, send, Drive share. Deadline: PR by 21:00 COT tonight (event 08:00 tomorrow).

## Source (box -> repo, Orchestrator copies)
- /workspace/dataton-2026-11-24/questions/context-pack.md -> decks/dataton-2026-preguntas-espacios/source/context-pack.md (canonical: Canva DAHbwkewuyo text, agenda v7 grid, 4 Granola notes 23 Nov, EO white paper v3 summary, 14 teams, space map).
- /workspace/pr176-check/v7/Agenda-Dataton-24nov.pdf -> source/ (canonical times and names).
- Do NOT copy the EO white paper PDF or its full-text extracts into the repo. It is marked "No circula".

## Plan (STE)
Goal: Make one Spanish PDF of moderator questions for each content space of the Datatón agenda.
Audience: Gideon (host/moderator), mentors and jury. Internal prep document.
Deliverable: A4 portrait PDF, 17 pages, plus HTML source and one PNG per page.
- p1 Cover: "Datatón · Preguntas por espacio", 24 nov 2026, Universidad Externado. Tagline "Observa. Actúa. Transforma."
- p2 Hilo conductor: one diagram of the macro -> micro thread (paisaje/territorio -> programa Observatorio + Datalab -> régimen corporativo -> sector digital -> nicho Air4U + adoptante -> método -> equipos -> selección -> vuelta al Observatorio/Datalab 2027). Use the MLP terms nicho / régimen / paisaje. Show the 15 spaces on the thread.
- p3-p17 one page per space, in agenda order (v7 times):
  08:30 Palabras de apertura · 08:40 Panel ODS 13 · 09:10 Lanzamiento Observatorio + Datalab · 09:40 Conversatorio Externado × Constructora Bolívar · 09:55 Conversatorio Digitalización (Enrique Medina, Agrometers) · 10:05 Sandbox 1/3 presentación Air4U · 10:10 Sandbox 2/3 demo en vivo · 10:20 Sandbox 3/3 Air4U × Apix Pharma · 10:45 Instrucciones y arranque (fold in Canva's 10:55 Mentores) · 11:00 Bloque 1 con monitores · 12:30 Almuerzo y networking (helix guest table) · 13:30 Bloque 2 + preparación del pitch · 16:00 Pitches finales (6 equipos) · 16:40 Deliberación del jurado · 16:50 Cierre: 3 ganadores + certificados.
  Skip pure logistics: 08:00 Registro, 09:25 Café, 15:30 Refrigerio, 17:00 Fin.

Each space page has, in this order:
1. Header: time, space name (sentence case), who participates (roles; names only where the agenda v7 has them), who asks whom (e.g. "Gideon -> panel", "monitores -> equipos", "jurado -> equipos").
2. "Viene de" strip: the one output this space receives from the previous space. "Lleva a" strip: the one output it hands to the next space.
3. Conversation of 4-6 turns. Each turn: **Pregunta** (one sentence), then [respuesta anticipada] in brackets and muted style (1-2 sentences, realistic, in the speaker's likely voice, built from the context pack), then **Repregunta** that builds on that anticipated answer. Each next question must follow from the previous answer, so the page reads as one ongoing conversation, not a list.
4. "Puente" line at the bottom: one bridge question or sentence that hands over to the next space.
5. Small source line (e.g. "Fuente: agenda v7, reunión 23 nov").

Done when:
- 17 pages A4 portrait, one space per page, nothing overflows or is clipped.
- Every space page has 4-6 Pregunta + [respuesta] + Repregunta turns, Viene de / Lleva a, Puente.
- Order and times match agenda v7 exactly.
- pdffonts shows Open Sans only (Titillium allowed only if used in an EO accent; prefer Open Sans).
- PNG render of every page attached in the PR.

Constraints:
- Spanish, human tone, tú/usted consistent per space (usted for panel/officials; tú for teams). No disclaimers. No AI-sounding phrasing.
- CTH brand style: cleantechhub-brand + the approved FODESEP reveal look (navy/cyan cards, text always on a contrasting card, sentence-style titles, logo top right, green title rule, small source lines). Only CTH palette. No people/team photos. Optional full-bleed atmospheric image on the cover only, under a strong navy scrim.
- Never say the event is free. No signature.
- Invent no numbers. Anticipated answers stay qualitative unless the number is in the context pack (e.g. Air4U "reducción del 14% de partículas" is in the 08:00 Granola note; attribute it as their claim).
- Do not present Constructora Bolívar as a signed pilot. Do not name a pilot territory or pilot dates for the Observatorio.
- Bolívar speaker name is unconfirmed (Canva: Alejandro Henao; agenda PDF: "Sr. Cortés"). Use the role "Constructora Bolívar · Aceleradora de Transformación" with no personal name.
- Panel per agenda v7: APC-Colombia (Natalia Vargas), Rector Universidad Externado, RAP Pacífico, Óscar (Apix Pharma). Apix attendance is not confirmed: write the Apix turns so the page still works if Apix is absent (one line "si Apix no está: ..." at most).
- Use the real data ladder: Bronce -> Plata -> Oro = niveles de confianza, not prizes. Funnel 14 equipos -> 6 finalistas -> 3 ganadores who enter the CTH Datalab in 2027. Everyone gets a certificate. Jury: Enrique Medina, Alejandro Díaz, Gideon.
- Team-block questions use the pack: Paso 0 BMC, Hoja 1 mapa de calor (¿DÓNDE?), Hoja 2 flujo + Medallion (¿QUÉ?), Hoja 3 dato a valor, Hoja 4 tablero, Hoja 5 pitch (Problema / Datos / Tablero / Impacto / Próximo paso).
- Quote the EO white paper only in short phrases (max ~12 words each). Do not reproduce sections.
- No internal words in the PDF: PR, Hands, Orchestrator, Cursor, desk, GO, ticket, github.

Out of scope: speaker scripts, slides, sending or sharing the PDF, Drive upload, any change to the agenda or team pack.

Push back (recorded): "1 page per space" taken literally is 19 agenda rows; the 4 logistics rows get no page (15 space pages + cover + thread map). The anticipated answers are prep for Gideon and the jury; if Gideon later shares pages with speakers, the brackets read as scripting, so keep them clearly marked as "respuesta anticipada".

Deliverables back: PR URL, head SHA, sha256 of the PDF, page count, PNG paths, pdffonts output, and a text audit for the banned internal words and "gratis/gratuito". I run an independent check before Gideon sees anything.
