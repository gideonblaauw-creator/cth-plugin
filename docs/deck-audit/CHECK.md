# CHECK — HTML deck skill

**Verdict: FAIL**

Independent check of draft PR #61. This checker did not write `skills/cth-html-deck/SKILL.md` or `skills/aic-brand/SKILL.md`. Sources read: `docs/deck-audit/A1-decks-cleantechhub.md`, `A1.json`, `A2-vercel-decks.md`, `A2.json`, `README.md`, `skills/cleantechhub-brand/SKILL.md`, and `skills/cleantechhub-brand/brand_dna.yaml`. Commit `0c39db1` is `0c39db16276685534e45ee21f14c4d838a019004` (19 Oct 2026, 21:13 UTC). Commit `16f5251` is `16f525180384a7d4b68838ea8370fe316e5092a3` (19 Oct 2026, 21:09 UTC). The 21:02 UTC stamp in A2 is the curl pass, and it matches `A2.json` `audited_at`.

The B4B shell was read at `origin/meetings-2026-10-13-b4b` @ `7cb3f08`. The live AIC stylesheet was fetched only to test numbers that A1 does not list.

## FAILs

### 1. EN/ES count — FAIL

`skills/cth-html-deck/SKILL.md` says EN/ES exists on three live decks, then names both ClimateLaunchpad pages, the CPI backbone, and AIC. `README.md` repeats "3 decks" and then "the other nine."

A1's own rows mark `en_es` true on four slugs: `cth-clp26`, `cth-clp26-rein`, `cpi-lab-backbone-cth`, and `aic-q1-2027-packages`. The other nine are one language. Four plus nine is thirteen. The summary word "three" in A1 contradicts that table.

**Fix:** In the skill and in `README.md`, write: "EN/ES exists on four live slugs (A1 rows): `cth-clp26`, `cth-clp26-rein`, `cpi-lab-backbone-cth`, and `aic-q1-2027-packages`. The other nine are one language." Keep the next sentence, which already requires a switch on a new paged deck.

### 2. "Every Vercel host A2 requested" — FAIL

The skill, the audit section, and `README.md` say every Vercel host A2 requested returned HTTP 402 `DEPLOYMENT_DISABLED`.

A2's known-host table is 402 for the nine named hosts plus `teclogi-financial-model.vercel.app`, at 21:02 UTC on 19 Oct 2026. The same file lists guessed hosts that returned 404 `DEPLOYMENT_NOT_FOUND`, including `cee-datathon-2026-10-14.vercel.app`, `matamala-cth-2026-10-13.vercel.app`, `epic-angels.vercel.app`, `grp-ic.vercel.app`, and `teclogi.vercel.app`. `energy-sprint-cohort-cth.vercel.app` also returned 402 and is outside that known list.

**Fix:** Replace the sentence in the skill (hosting step 4 and the Audit section) and in `README.md` with: "On 19 Oct 2026 at 21:02 UTC, A2's nine known hosts plus `teclogi-financial-model.vercel.app` returned HTTP 402 `DEPLOYMENT_DISABLED`. Guessed names in that audit returned 404 `DEPLOYMENT_NOT_FOUND`."

### 3. Hosting facts past A1 — FAIL

A1 records Appwrite project `cth-decks`, Caddy stripping `/<slug>/` and proxying, root HTTP 401 with an empty body, public slug pages, one wiki sample 301, and `index.html` fallback. A1 says the audit did not open the VPS. It does not state a team name, site framework, adapter, empty install and build, output directory, `_APP_DOMAIN_SITES`, basic auth, SSO, or a tar cap.

The skill states all of those as fact, says Caddy "serves" `/<slug>/`, and adds "Keep the published tar under 12 MB. A tar between 12.3 MB and 14 MB has been rejected by the proxy." Those megabyte figures are not in A1, A2, or `README.md`.

**Fix:** Replace the hosting paragraph and step 6 with: "A1 records Appwrite project `cth-decks`. Caddy strips `/<slug>/` and proxies to the site. The root returned HTTP 401 with an empty body. Slug pages stayed public. One wiki sample, `/decks/apc-cth-2026-10-07/`, returned 301 to this host. A missing asset that returns `text/html` is the `index.html` fallback. A1 did not open the VPS. Team, framework, adapter, install, build, output directory, `_APP_DOMAIN_SITES`, the root auth scheme, and any tar-size cap stay `[PENDIENTE]`. Do not write a megabyte number. Epic Angels left unreferenced `png/` renders and a local PDF out of the upload (A1). Do the same when the tree is large."

### 4. `teclogi-financial-model` called a Node app — FAIL

The skill says it is a Node app. `A1.json` says the migration report marks it BLOCKED (Next.js) and that no public slug was fetched. A2 says the host returned 402, no source was readable, and the 1920 shell must not be assumed.

**Fix:** Replace the sentence with: "`teclogi-financial-model` has no slug on this host. A1's migration note marks it BLOCKED (Next.js). A2 found HTTP 402 and no readable source. Leave it out of this static shell."

### 5. Glass fill — FAIL

The skill sets glass panels from `rgba(255,255,255,0.07)` to `rgba(255,255,255,0.12)` and attaches the blur and the 12px radius to that range.

B4B `shell/deck.css` sets `.glass` to fill `rgba(255,255,255,0.09)`, border `rgba(255,255,255,0.12)`, `backdrop-filter: blur(8px)`, radius 12px. Fill `0.07` is `.weight-box`, and that rule has no blur. The scrim stops in the skill match `.slide.has-photo::after` exactly.

**Fix:** Write: "`.glass` is fill `rgba(255,255,255,0.09)`, 1px border `rgba(255,255,255,0.12)`, `backdrop-filter: blur(8px)`, radius 12px. `.weight-box` is fill `rgba(255,255,255,0.07)` with the same border and no blur." Leave the scrim gradient as it is.

### 6. REIN source line — FAIL

The six hexes and the credit line match A1 `cth-clp26-rein`: `#335D4F`, `#FF6633`, `#222A27`, `#5F6663`, `#C9D6D1`, `#F1F5F3`, and "REIN Hubs · PVBLIC × CleantechHUB". The funding-table oranges `#F1562A` and `#FC987C`, Lora, and Poppins also match A1.

The skill cites `pvblic.org/rein-hubs` and an Oct 2026 factsheet. Neither source is in A1, A2, or this repo. The type stack adds Arial. A1's face list is Open Sans body, Poppins headings, and Source Sans 3 named and not loaded.

**Fix:** Write: "Take the six hexes and the credit line from A1 `cth-clp26-rein`. Body is Open Sans. Headings may be Poppins. Source Sans 3 may be named and is not loaded. Do not add Arial. Do not cite pvblic.org or a factsheet."

### 7. 24px floor and the 14px exceptions — FAIL

The floor and the exceptions can be read as one rule, and the B4B shell agrees with a careful reading: stage type is at least 24px, `.nav-hint` is `font-size: 14px` outside the stage and hidden under `body.print-all`, and `#slide-dots button` is a 14×14px circle with no `font-size`. `build.sh` closes `.deck-viewport` before it emits `.deck-chrome` and `.nav-hint`.

The skill never says the dots sit outside `.deck-stage`. The sentence "Nothing inside `.deck-stage` is set below 24px" therefore collides with "Dot buttons are 14px circles." The acceptance row only bans `font-size` under 24px, so a 14px dot inside the stage would pass the check.

**Fix:** After the nav-hint sentence, write: "`.nav-hint` and `#slide-dots` stay outside `.deck-stage`, as siblings after `.deck-viewport` in the B4B `build.sh`. `.nav-hint` may be `font-size: 14px` and is `display: none` under `body.print-all`. `#slide-dots button` may be 14×14px and must not set `font-size`. No painted size inside `.deck-stage` is below 24px."

In the Minimum type pass cell, write: "Fail any `font-size` under 24px that can match a node inside `.deck-stage`. Pass `.nav-hint` at 14px only when it is outside `.deck-stage` and hidden in `body.print-all`. Pass a 14×14px dot only when `#slide-dots` is outside `.deck-stage` and the rule sets no `font-size`."

### 8. AIC language storage — FAIL

`cth-html-deck` requires `localStorage` key `cth-deck-lang` and the room language on the ticket. `aic-brand` point 4 requires the live pattern: `data-i18n`, Spanish default, choice not stored. Point 5 says an AIC slide deck uses the deck shell and only the tokens change. Those three rules cannot be true of one AIC deck.

The forward rule for new paged decks is otherwise consistent with the audit: frame shells have no switch, and the skill still requires one. ClimateLaunchpad may keep `clp26lang`. The funding table stays a table with no switch.

**Fix:** In `aic-brand`, split the two products. "The live configurator keeps `data-i18n`, Spanish as the default, and does not store the choice. An AIC slide deck uses the `cth-html-deck` EN/ES contract (`cth-deck-lang`, room language from the ticket). Only the colour and type tokens change." In the deck skill's AIC section, add: "An AIC slide deck uses `cth-deck-lang`. It does not copy the configurator's in-memory toggle."

### 9. "Tokens there are `[PENDIENTE]`" — FAIL

The deck skill says the AIC tokens are `[PENDIENTE]`, then says to use the observed values. `aic-brand` already fills ink `#070c18`, gold `#c9a45c`, Cormorant Garamond, Inter, and the type-only mark. Those values match A1.

**Fix:** Replace the sentence with: "Observed ink `#070c18`, gold `#c9a45c`, Cormorant Garamond, Inter, and the type-only mark are filled in. Every other row in `skills/aic-brand/SKILL.md` stays `[PENDIENTE]` until Gideon adopts the proposal."

### 10. "A1 marks one block OBSERVED" — FAIL

A1 copies the live tokens and calls them a proposal. It does not use the word OBSERVED, and it does not split `:root` into a locked block and unlocked rows. That split is this proposal's label.

**Fix:** In `aic-brand`, write: "This proposal marks one block OBSERVED. A1 copied the values from the live page and did not use that label."

### 11. "Do not add a sixth hue" — FAIL

`brand_dna.yaml` has five CleantechHUB colours and forbids a sixth hue. The AIC table already lists ink, navy, navy2, ivory, muted, dim, gold, champ, gold-d, and platinum. "Sixth hue" does not name a rule for that table.

**Fix:** Delete "Do not add a sixth hue." Write: "Use only the custom properties listed in this file. Do not add a CleantechHUB green, a Manual de Marca blue, or a new hue."

### 12. AIC `--sans` rows disagree — FAIL

The observed paragraph includes Segoe UI. The token table sets `--sans` to `"Inter", system-ui, sans-serif`. The live `:root` value is `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif`. A1 names system-ui, Segoe UI, and sans-serif, and omits `-apple-system`.

**Fix:** Set both rows to `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif`.

### 13. AIC role column — FAIL

A1's roles that the skill rewrites: `--navy` is event cards (live CSS: `.ev` and `.tier`), not "Deep surface". `--navy2` is "Second navy". `--muted` includes the brand name. `--champ` is links, italic emphasis, and favicon letters. `--gold-d` is "Deep gold". `--plat` includes the premium tier. `--line` is a hairline on the gold hue. Focus outline is real on the live page (`:focus-visible` uses `--champ`) and is not in A1's role cell.

**Fix:** Copy A1's role phrases into the table. Add one clause on `--champ`: "The live page also uses it for the `:focus-visible` outline."

### 14. Acceptance checks — FAIL

These rows are concrete and can stay: clipped sides (the 1366×768 and 1512×982 widths match A2's `smoke-layout.py`), SOURCES slide title, PDF page count, and the curl 200 split before and after HITL.

These rows do not enforce the rules above them:

- No EN/ES row. A deck with no toggle passes the table.
- "Every other numeral" does not restate the exemptions in section 2 (slide index, footer meeting date, copyright year).
- Citation "visible" does not reject a link inside an HTML comment or a chip hidden until `?review`. Those are the APC and CEE patterns A2 records.
- Keyboard omits Space, Page Up, Page Down, click halves, and the `#1` hash, all of which section 1 requires.
- Brand greps use alternation, so one hex makes the CTH or REIN command pass. The AIC grep allows `#B2EEFA`, `#9DC384`, `#669348`, `#69B5FA`, and `#1B4332`. The REIN grep allows `#69B5FA`, `#9DC384`, `#669348`, `#F1562A`, and `#FC987C`. The CTH grep does not reject `font-family: Inter`.

**Fix:** Add this row: "EN/ES. Pass when every sentence has `.lang-en` and `.lang-es`, the toggle sets `document.documentElement.lang` and `localStorage` key `cth-deck-lang`, the same numerals appear in both languages, and missing copy is the text `[PENDIENTE]`. ClimateLaunchpad may keep `clp26lang`. The funding table is out of scope."

Replace the numeral pass cell with: "Every numeral other than the slide index (`n / total`), the meeting date in the footer, and the copyright year is in `SOURCES.md`, inside `.hypo-badge`, or is the literal `[PENDIENTE]`."

Add to the citation pass cell: "The link is in the DOM, not in an HTML comment, and it is shown in screen mode without `?review`."

Extend the keyboard pass cell with Space, Page Up, Page Down, click halves (ignored on a link, button, card, tab, or lightbox control), hash `#1` for the first slide, and Escape closing the menu and the lightbox.

Replace the brand commands with one `grep -F` per required hex, each of which must match. Extend the absent-hex commands:

- CTH absent: `#2D6A4F`, `#1B4332`, `#95D5B2`, and `font-family` containing `Inter`.
- REIN absent: `#0C498A`, `#B2EEFA`, `#69B5FA`, `#9DC384`, `#669348`, `#2D6A4F`, `#95D5B2`, `#1B4332`, `#F1562A`, `#FC987C`.
- AIC absent: `#0C498A`, `#B2EEFA`, `#69B5FA`, `#9DC384`, `#669348`, `#2D6A4F`, `#1B4332`, `#95D5B2`, `#335D4F`, `#FF6633`, `#F1562A`.

Skip the cross-brand absent grep only when the ticket names a co-brand, and record that exception in `CHECK.md`.

## PASSes

### Coverage of the six requirements — PASS

The skill states each required rule: interactive stage and controls; a citation, a SOURCES slide, and `SOURCES.md`; one brand context among CleantechHUB, REIN Hubs, and AIC, with AIC marked a proposal; host `https://decks.cleantechhub.net/<slug>/` on the existing Appwrite project, HITL, and no new Vercel project; micro-parallel Hands with exclusive paths and a verifier who writes only `CHECK.md`; an acceptance table. The FAILs above are accuracy and testability, not missing sections.

### Interactive shell facts that match the audits — PASS

1920×1080, scale `min(viewport / 1920, viewport / 1080) * 0.96` on `.deck-stage`, and the frame sized to the scaled box match A2. `?print` / `#print`, `body.print-all`, and `@page` size `1920px 1080px` match A2. img2pdf at 508 mm × 285.75 mm, and the warning not to hardcode 9, match A2. The photo scrim stops match B4B `.slide.has-photo::after`. APC is the only live sources slide (`Fuentes públicas`). Bridge for Billions and Matamala stop at per-slide `.src` / `.cite` plus `SOURCES.md`. CEE hides `.pendiente` until `?review`. APC wrapped chips in HTML comments. Energy Coops is A4 landscape with no `.deck-frame`. The Matamala `brief.html` is a scrolling page. Chart.js 4.5.1, D3 7.9.0, topojson-client 3.1.0, and the absence of `#00A651` and `#FFC425` match A1. Frame shells have no chart library and no EN/ES switch.

### Brand hexes — PASS

CleantechHUB stage tokens match `brand_dna.yaml` and A2: `#0C498A`, `#B2EEFA`, `#9DC384`, `#669348`, `#69B5FA`, white `#FFFFFF`, letterbox `#051a33`, stack `'Open Sans', 'PT Sans', sans-serif`. Foundation tokens match `skills/cleantechhub-brand/SKILL.md`: `#2D6A4F`, `#1B4332`, `#95D5B2`, Inter. A1 found those foundation tokens absent as deck paint, and Inter only on the AIC page. REIN and funding-table hexes match A1, as cited in FAIL 6. AIC `#070c18`, `#c9a45c`, `#e6cf9f`, the rest of the `:root` table, favicon 64×64 radius 14, Georgia 24px weight 600, and the seven sections match A1. `--r: 18px` is in the live `:root` and was omitted by A1; it is not an invented number. Live labels at 11px and 12px are real. The ten probed AIC slugs returned 404 on 19 Oct 2026 in this check, and `aic-q1-2027-packages` returned 200.

### Micro-parallel Hands — PASS

Shell, slide-group, assembler, and verifier paths are exclusive. The verifier is a different bc-id and writes `CHECK.md` only. Models match the harness lock: `composer-2.5` with `fast=true` for the build, `gemini-3.7-flash` for mechanical checks, and HOLD when review, eval, or brand has no model. Jobs launch together, and the cap near eight matches the harness.

### Public repo — PASS

Neither skill contains a dollar amount, a credential, an API key, or a mailbox address. The REIN dollar-amount ban matches `skills/rein-hubs-comms/SKILL.md` and A1's note that funding amounts were not copied. Counterpart names in the skill are the public slug titles already printed in A1 and A2. The AIC founder line matches the public page. The skill does not copy speaker names or prices from that page.

### Commit pins — PASS

`deck-skill-audit-a1` @ `0c39db1` and `deck-skill-audit-a2` @ `16f5251` are the branch tips named in the skill and in `README.md`.

## Re-check

**Re-check verdict: FAIL**

Re-read after `b192b76` ("Apply the 14 checker fixes to the deck and AIC skills") on `cursor/cth-html-deck-skill-3ac4`. Sources re-read: both skills, `docs/deck-audit/README.md`, the A1 and A2 files, and the diff from `d0366d9` to `b192b76`. This pass did not edit the skills. Nothing was deployed.

Items 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, and 13 match the prescribed fixes and the audits. Items 6, 9, and 14 stay FAIL. Three new issues are open.

### 1. EN/ES count — PASS

`skills/cth-html-deck/SKILL.md` and `README.md` now say EN/ES exists on four live slugs and name `cth-clp26`, `cth-clp26-rein`, `cpi-lab-backbone-cth`, and `aic-q1-2027-packages`. The other nine are one language.

### 2. Vercel 402 scope — PASS

Hosting step 4, the Audit section, and `README.md` now limit HTTP 402 `DEPLOYMENT_DISABLED` to A2's nine known hosts plus `teclogi-financial-model.vercel.app` at 21:02 UTC on 19 Oct 2026. Guessed names are 404 `DEPLOYMENT_NOT_FOUND`.

### 3. Hosting facts past A1 — PASS

The hosting paragraph matches the A1 record: project `cth-decks`, Caddy strips `/<slug>/`, root HTTP 401 with an empty body, public slug pages, one wiki sample 301, and `index.html` fallback. Team, framework, adapter, install, build, output directory, `_APP_DOMAIN_SITES`, the root auth scheme, and any tar-size cap are `[PENDIENTE]`. The 12 MB, 12.3 MB, and 14 MB figures are gone. See new issue B for the prohibition that step 4 dropped.

### 4. `teclogi-financial-model` — PASS

The sentence now says no slug, BLOCKED (Next.js), HTTP 402, and no readable source. "Node app" is gone.

### 5. Glass fill — PASS

`.glass` is fill `rgba(255,255,255,0.09)`, border `rgba(255,255,255,0.12)`, blur 8px, radius 12px. `.weight-box` is fill `0.07` with the same border and no blur. The scrim stops are unchanged.

### 6. REIN source line — FAIL

Section 3 now takes the six hexes and the credit line from A1 `cth-clp26-rein`, names Open Sans, Poppins, and Source Sans 3, and says not to add Arial or cite pvblic.org or a factsheet.

The outliers paragraph still says: "Its orange is `#F1562A` and `#FC987C`, not the factsheet orange `#FF6633`." That cites a factsheet. A1 and A2 do not. The hex `#FF6633` is the `cth-clp26-rein` orange.

**Fix:** Replace that clause with: "Its orange is `#F1562A` and `#FC987C`, not the `cth-clp26-rein` orange `#FF6633`."

### 7. 24px floor and the 14px exceptions — PASS

`.nav-hint` and `#slide-dots` are outside `.deck-stage`, as siblings after `.deck-viewport`. The 14px hint and the 14×14px dots are stated with those conditions. The Minimum type pass cell matches.

### 8. AIC language storage — PASS

`aic-brand` point 4 keeps `data-i18n` and an unstored choice on the configurator, and sends an AIC slide deck to `cth-deck-lang` plus the room language. The deck skill says the same and says not to copy the in-memory toggle. Point 5 sends a slide deck to the shell.

### 9. "Every other row stays `[PENDIENTE]`" — FAIL

The prescribed sentence was applied. It is still false against `skills/aic-brand/SKILL.md`.

Observed rows beyond ink, gold, Cormorant Garamond, Inter, and the type-only mark: the favicon row, the seven-section product row, the footer links and the unstored EN/ES pill, and the second table's `--ink`, `--gold`, `--serif`, and `--sans` rows. `aic-brand` line 19 says "Everything else stays **[PENDIENTE]**," which is the same overclaim.

**Fix:** In the deck skill, replace "Every other row…" with: "Rows that stay `[PENDIENTE]` are `--navy`, `--navy2`, `--ivory`, `--muted`, `--dim`, `--champ`, `--gold-d`, `--plat`, `--line`, and `--r`. Ink, gold, both faces, the type-only mark, the favicon, and the seven-section shape are OBSERVED. The proposal is still not adopted." In `aic-brand`, replace "Everything else stays **[PENDIENTE]**" with that same split.

### 10. "A1 marks one block OBSERVED" — PASS

`aic-brand` now says this proposal marks one block OBSERVED, and that A1 copied the values and did not use that label.

### 11. "Do not add a sixth hue" — PASS

Point 2 now says: "Use only the custom properties listed in this file. Do not add a CleantechHUB green, a Manual de Marca blue, or a new hue."

### 12. AIC `--sans` rows — PASS

Both `--sans` rows are `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif`.

### 13. AIC role column — PASS

`--navy` is event cards. `--navy2` is second navy. `--muted` includes the brand name. `--champ` is links, italic emphasis, and favicon letters, plus the live `:focus-visible` clause. `--gold-d` is deep gold. `--plat` includes the premium tier. `--line` is a hairline on the gold hue.

### 14. Acceptance checks — FAIL

The EN/ES row, the numeral exemptions, the citation visibility sentence, and the per-hex `grep -F` lists landed. CTH absent hexes include the foundation greens and an Inter `font-family` pipe. REIN absent hexes include `#F1562A` and `#FC987C`.

The keyboard pass cell says: "Space, Page Up, and Page Down move the same way." Section 1 says Space and PageDown go forward and PageUp goes back. "The same way" names no direction, so the row cannot be scored.

**Fix:** Replace that clause with: "Space and PageDown go forward. PageUp goes back." Keep the click-half, hash `#1`, Escape, and index sentences.

### New issue A — README, stub, and changelog still say every AIC token is `[PENDIENTE]`

`docs/deck-audit/README.md` still says AIC is "PROPOSAL, tokens `[PENDIENTE]`." `.cursor/skills/aic-brand/SKILL.md` still says "Tokens stay [PENDIENTE] until Gideon adopts them." `CHANGELOG.md` still says the observed tokens were marked `[PENDIENTE]`.

**Fix:** Use the same split as item 9. Unlocked rows stay `[PENDIENTE]`. Ink, gold, both faces, the mark, the favicon, and the seven-section shape are OBSERVED. The proposal is not adopted.

### New issue B — hosting step 4 dropped the host and DNS ban

The old step 4 said: "Do not create a Vercel project, a new host, a DNS record, or an Appwrite reload." The rewrite keeps the Vercel ban and drops the host ban and the DNS ban. The checker did not ask for that drop. Leave `_APP_DOMAIN_SITES` and any Appwrite reload as `[PENDIENTE]`, as the hosting paragraph already does.

**Fix:** After "Do not create a Vercel project," add: "Do not create a new host or a DNS record."

### New issue C — AIC absent greps omit `#FC987C`

The REIN absent list rejects both funding oranges, `#F1562A` and `#FC987C`. The AIC absent list rejects `#F1562A` and omits `#FC987C`. An AIC deck can paint the second funding orange and still pass.

**Fix:** Add `grep -F '#FC987C' shell/deck.css` to the AIC absent list. It must print nothing.

### Public repo, re-scan — PASS

Neither skill contains a dollar amount, a credential, an API key, or a mailbox address. The leftover "factsheet" word is an accuracy miss, recorded under item 6. Counterpart names remain the public slug titles already in A1 and A2.
