# AI Apps for Good — CleantechHUB workflow evaluation (2026-11-04)

Read-only research on every app listed at [AI Apps for Good](https://aiappsforgood.org/) for fit with CleantechHUB (CTH) operating workflows.

## Executive summary

The directory currently advertises **23 apps** on a **single landing page** (no separate pagination or category index pages). Tools cluster into: **grant/org capacity** (Pitch Builder, MEL Builder, Compass, salary grids), **team rituals** (standup, icebreakers), **security/phishing**, **personality/coaching assessments**, and **scenario games** for advocacy learning.

For CTH, the highest leverage is **grant and deck drafting**, **MEL design**, **meeting/calendar hygiene**, **hard-conversation prep**, and **phishing/security awareness** that supports Gmail and VPS operations—not the HR/salary or attachment-style wellness tools.

Site-wide (project-built apps): **free, open access**, **CC BY 4.0**, **no accounts/analytics**; AI-powered apps send user input to **Claude (Anthropic)** for processing and do not retain it on AI Apps for Good servers. Community-contributed apps use their own hosting, terms, and pricing.

## Top 6 for CTH workflows

| Rank | App | Why (one line) |
| --- | --- | --- |
| 1 | **Pitch Builder** | Fast structured first draft of **10-slide funder/investor decks** from voice or text—maps directly to grant watch and Presentations. |
| 2 | **MEL Builder** | Chooses MEL approaches and generates a **implementation guide** (plus optional live NGO examples)—supports grant reporting and Nexus/Datalab evaluation design. |
| 3 | **Compass** | Surfaces **capacity-building priorities** across 80 projects—useful when scoping grantee support, internal roadmap, or automation backlogs. |
| 4 | **Tough Conversations** | **Evidence-based prep** for board, donor, partner, or team hard talks—pairs with Meetings/Granola and sensitive Inbox threads. |
| 5 | **Jess's Calendar Colorizer** | **Auto-colors Google Calendar** from keyword rules via Apps Script—cheap visual triage for meeting-heavy weeks without manual tagging. |
| 6 | **SecureCheck** (Impaque) | **No-login NGO security assessment** with prioritized fixes—complements Inbox risk awareness and n8n/VPS hardening conversations. |

**Runners-up:** FreshPhish and Spotting the Bait (phishing training); Morning Standup / This or That (meeting rituals); regenerative/circular **games** as templates for climate advocacy social content.

## Method

| Step | Detail |
| --- | --- |
| Discovery | Fetched `https://aiappsforgood.org/` (WebFetch); confirmed **23 Apps** counter and full card list on one page. |
| Pagination / categories | **None found**—no `/apps`, sitemap, or paginated category URLs (404). All listings are on the homepage. |
| App pages | Resolved each app URL via homepage intent, site search, and pattern probes (`*.html` on `aiappsforgood.org` plus linked community domains). |
| Per-app fields | Name, URL, one-line function, CTH workflow mapping, fit 1–5, cost/licence from site or app site only, combined risk note. |
| File size cap | No local file reads over 200 KB. |
| Reachability | WebFetch used where Cloudflare blocks raw `curl` (403 on VM). |

### Counts

| Metric | Value |
| --- | --- |
| Apps listed on site | **23** |
| Apps evaluated (rows in CSV) | **23** |
| Match | **Yes — row count equals site count** |

### Apps not on `aiappsforgood.org` host (linked community / partner URLs)

These appear on the directory but run on contributor domains—still evaluated and counted:

- **FounderMatch** → `https://foundermatch.us/`
- **SecureCheck** → `https://securecheck.impaque.com/`
- **AlignUP · Four Pulses** → `https://www.alignup.ca/` (pulse apps on `alignup-pulse.netlify.app/*`)
- **Jess's Calendar Colorizer** → `https://jessicaeastmanstewart.com/calendar-colorizer`
- **Spotting the Bait** → `https://spottingthebait.com/`
- **HR Essential Standards** → `https://claudieapp.netlify.app/`

### Gaps / caveats

- **FounderMatch** has no `aiappsforgood.org/*.html` mirror (404); only the external assessment URL works.
- **`https://alignup-pulse.netlify.app/`** root returns 404; individual pulse URLs (e.g. `/pulse-foundation/`) work—hub documented as `alignup.ca`.
- **SecureCheck.tools** is a **different** commercial CISO Marketplace product; the directory entry points to **Impaque SecureCheck** (`securecheck.impaque.com`), not the paid checklist SaaS.
- **Spotting the Bait** free quizzes vs **paid per-seat** weekly program—cost differs by tier.
- Homepage **filter/bookmark UI** could not be crawled separately (SPA/Cloudflare); app inventory taken from the static listing text and cross-checks.

### URL spot-check (3 apps)

| URL | Result |
| --- | --- |
| `https://aiappsforgood.org/pitchbuilder.html` | **OK** via WebFetch (full page content); VM `curl` **403** (Cloudflare). |
| `https://aiappsforgood.org/melbuilder.html` | **OK** via WebFetch; VM `curl` **403**. |
| `https://foundermatch.us/` | **HTTP 200** via VM HEAD request and WebFetch. |

## CTH workflow legend

- **Inbox/Gmail triage** — email volume, phishing, prioritization  
- **Grant watch** — proposals, donor requirements, MEL, capacity  
- **Socials/LinkedIn** — campaigns, advocacy storytelling  
- **Meetings/Granola** — rituals, prep, calendar  
- **Datalab/Nexus research** — portfolio, impact, research framing  
- **decks/Presentations** — slide artifacts  
- **Teclogi IR/Mail Finder** — investor/research mail workflows  
- **n8n automations** — ops automation on VPS  
- **none** — no material CTH workflow fit  

## Full evaluation table

See companion CSV: [`aiappsforgood-eval-2026-11-04.csv`](./aiappsforgood-eval-2026-11-04.csv).

| name | url | what_it_does | cth_workflows | fit | cost/licence |
| --- | --- | --- | --- | --- | --- |
| Archetype360 | https://aiappsforgood.org/archetype360.html | Professional personality assessment (8 dimensions, AI report) | Meetings/Granola; none | 2 | Free; CC BY 4.0 |
| CommStyle | https://aiappsforgood.org/commstyle.html | Communication-style assessment (6 archetypes, AI guide) | Meetings/Granola; Socials/LinkedIn | 2 | Free; CC BY-SA 4.0 |
| FounderMatch | https://foundermatch.us/ | Founder DNA and co-founder fit assessment | none | 2 | Free |
| Your Attachment Style | https://aiappsforgood.org/yourattachmentstyle.html | Attachment-style game + optional AI guidance | none | 1 | Free |
| Tough Conversations | https://aiappsforgood.org/toughconversations.html | AI prep for difficult conversations (15 techniques) | Meetings/Granola; Inbox/Gmail triage | 4 | Free |
| Compass | https://aiappsforgood.org/compass.html | Org capacity diagnostic → priorities / roadmap | Grant watch; Datalab/Nexus research; n8n automations | 4 | Free; CC BY 4.0 |
| Salary Grid Generator | https://aiappsforgood.org/salary-grid.html | Salary grid from anchors (deterministic + AI text) | none | 1 | Free |
| MEL Builder | https://aiappsforgood.org/melbuilder.html | MEL approach matcher + design guide | Grant watch; Datalab/Nexus research | 5 | Free |
| Pitch Builder | https://aiappsforgood.org/pitchbuilder.html | 10-question → AI sharpen → 10-slide pitch | Grant watch; decks/Presentations | 5 | Free; EN/FR |
| Business as Usual or Regenerative? | https://aiappsforgood.org/regenerative-game.html | Regenerative leadership scenario game | Socials/LinkedIn; decks/Presentations | 3 | Free |
| Play The Grand Bargain | https://aiappsforgood.org/grand-bargain-game.html | Humanitarian localization simulation | Socials/LinkedIn; Datalab/Nexus research | 2 | Free |
| Conventional or Circular? | https://aiappsforgood.org/circular-game.html | Circular vs conventional investor game | Socials/LinkedIn; Datalab/Nexus research | 3 | Free |
| This or That | https://aiappsforgood.org/this-or-that.html | Meeting icebreaker (100 either/or questions) | Meetings/Granola | 3 | Free |
| Morning Standup | https://aiappsforgood.org/morning-standup.html | Timed random-order standup | Meetings/Granola | 3 | Free |
| Morning Spotlight | https://aiappsforgood.org/morning-spotlight.html | Random spotlight warm-up | Meetings/Granola | 3 | Free |
| FreshPhish | https://aiappsforgood.org/freshphish.html | Phishing scenario training game | Inbox/Gmail triage; n8n automations | 4 | Free |
| Holistic Security | https://aiappsforgood.org/holistic-security.html | Holistic security literacy quiz | none | 2 | Free |
| Salary Grid PPP | https://aiappsforgood.org/salary-grid-ppp.html | PPP-adjusted salary grid | none | 1 | Free |
| SecureCheck | https://securecheck.impaque.com/ | NGO digital security self-assessment | Inbox/Gmail triage; n8n automations | 4 | Free; browser-only |
| AlignUP · Four Pulses | https://www.alignup.ca/ | Four alignment pulse checks | Meetings/Granola; Grant watch | 3 | Free pulses |
| Jess's Calendar Colorizer | https://jessicaeastmanstewart.com/calendar-colorizer | Google Calendar auto-color rules script | Meetings/Granola; Inbox/Gmail triage | 4 | Free generator |
| Spotting the Bait | https://spottingthebait.com/ | NGO phishing quizzes + optional weekly program | Inbox/Gmail triage; n8n automations | 4 | Free quizzes; paid per-seat program |
| HR Essential Standards | https://claudieapp.netlify.app/ | 16-dimension HR self-assessment | none | 2 | Free; EN/FR |

Risk detail for each row is in the CSV **risk** column.

---

*Research date: 2026-11-04. CleantechHUB internal use; public-voice adoption of third-party AI tools remains subject to CTH approval and secrets policy.*
