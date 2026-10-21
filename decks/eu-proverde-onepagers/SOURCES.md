# Sources for the EU-ProVerde one-pagers

Read on 21 October 2026 from the live sites. Every figure on `nexus-onepager.pdf` and `datalab-onepager.pdf` is listed here. Counts taken from a page’s own data file are the numbers that page renders.

No currency was added. The CleantechHUB homepage does not name a currency for the capital figure.

## Left off on purpose

- The brief’s “45” Dominican SMEs and “6 months” are not on these sites, so they are not on the pages.
- No public jury list or jury count was found on Nexus. The mentor directory is what the Nexus page uses.
- No startup in the public portfolio has country code `DO`. República Dominicana appears only as the search the pages offer to support.
- `https://nexus.cleantechhub.net/investors/data/investors.json` returned HTTP 401. No investor or funder count is used.
- The portfolio subtitle string says “102 startups con sitio web”. The same page fills the website stat from the data array, which has 126 websites. The pages use 126.
- The mentor header prints 36, 8 programmes, 6 countries, and 7 expertise areas as static text. The page script then sets the total from `MENTORS.length` (87). The records have 6 expertise labels and no country field. Those static 36 / 8 / 6 / 7 figures are not used.
- Nine portfolio records use the programme tags `Acceleration` (8) and `Accel.` (1). They sit in the 174. They are not one of the 8 programme filters.
- HubMap’s Costa Rica entry says the public profile is still being built and local representatives are pending. Its KPI values 91, 40, and 20 are not used.
- The Nexus home activity feed (names, “hace 2h”, “Vista interna”, the signed-in greeting) is not used.
- Demo company names on Datalab are not used. The app says startup datasets use an industry label, not a client name.
- No REIN dollar amount is cited.

## Nexus — `nexus.html`

| Fact on the page | Where it was read |
|---|---|
| Tagline “Inspira. Actúa. Transforma.” and the line “Tu ecosistema cleantech, en un lugar.” | https://nexus.cleantechhub.net/p/home |
| Portfolio of startups; mentors in impact, finance, sales, legal, and operations; angel investors, venture capital funds, and family offices active in Latin American cleantech; multilateral bodies, climate funds, and strategic alliances | https://nexus.cleantechhub.net/p/home |
| 174 startups in the public portfolio array | https://nexus.cleantechhub.net/p/startup-portfolio (`const S`, 174 `{n:"…"}` records) |
| Portfolio span 2018–2026 | https://nexus.cleantechhub.net/p/startup-portfolio (footer) |
| 8 programmes in the filters: CLAC 2021, CLAC 2022, CLAC 2023, CLAC 2024, CLAC 2025, CLP, CLP 2020, CLP 2025. The stat “8” is printed on the page. | https://nexus.cleantechhub.net/p/startup-portfolio |
| Themes: economía circular 75, bioeconomía 52, energía 47. Spanish labels come from the page’s `UI.ES` strings (`Circular`, `Bioeconomía`, `Energía`). The home card also says “economía circular, bioeconomía y transición energética”. | https://nexus.cleantechhub.net/p/startup-portfolio and https://nexus.cleantechhub.net/p/home |
| Stage counts: pre-seed 72, seed 77 | https://nexus.cleantechhub.net/p/startup-portfolio (`st` field) |
| 126 with a website (`w` is a non-empty string on 126 records; `w:null` on 48) | https://nexus.cleantechhub.net/p/startup-portfolio |
| 11 countries. Colombia 152. Also Mexico 5, Chile 4, Peru 3, Costa Rica 3, Guatemala 2, and 1 each in Spain, Panama, Argentina, Brazil, and Ecuador. | https://nexus.cleantechhub.net/p/startup-portfolio (`c` field) |
| 233 cleantech startup ideas from ClimateLaunchpad 2026 | https://nexus.cleantechhub.net/ideas (meta description) |
| 87 published mentors: 64 `Active`, 23 `Alumni` | https://nexus.cleantechhub.net/mentor-directory (`MENTORS`, and the script that writes `MENTORS.length` into the total) |
| Expertise labels: Impacto y Sostenibilidad, Negocios y Estrategia, Finanzas e Inversión, Operaciones y Tecnología, Ventas y Mercadeo, RRHH y Cultura | https://nexus.cleantechhub.net/mentor-directory |
| Investor and funder directory protects contact data. Only CleantechHUB staff can enter. The rest of Nexus stays public. | https://nexus.cleantechhub.net/investors and https://nexus.cleantechhub.net/p/funders |
| HubMap lists 5 university hubs | https://nexus.cleantechhub.net/hubs/hubs-data.json?v=20261021-hubmap-sv loaded by https://nexus.cleantechhub.net/hubs/ |
| ClimateLaunchpad 2026 startups: Externado de Colombia 22, Universidad Rafael Landívar (Guatemala) 7, Emprende UP (Peru) 11, UTEC (El Salvador) 8 | Same HubMap JSON, KPI `startups` / startup arrays |
| El Salvador hub publishes 77 ecosystem actors | Same HubMap JSON, UTEC KPI `actors` |
| Costa Rica public profile is under construction | Same HubMap JSON, Universidad LCI Veritas `about` |
| Ecosystem map: 381 actors. Peru 293, El Salvador 77, Colombia 6, United States 4, South Korea 1. | https://nexus.cleantechhub.net/ecosystem/data/actors.json loaded by https://nexus.cleantechhub.net/ecosystem . The page sets the actor stat to `actors.length`. The visible subtitle names Peru, El Salvador, and Colombia. |
| 14 verified relations with a source URL | https://nexus.cleantechhub.net/ecosystem/data/relations.json (85 rows). https://nexus.cleantechhub.net/ecosystem/story.mjs keeps a relation when `verified === true` and `source_url` is set. The map stat uses that filter. 14 rows pass. |
| Since 2019. Area served: Colombia, Peru, El Salvador, Guatemala, and Costa Rica. Email info@cleantechhub.net. | https://cleantechhub.net (schema.org block: `foundingDate`, `areaServed`, `email`) |
| “+10 Millons Capital Raised” on the homepage. The page quotes that string and does not add a currency. | https://cleantechhub.net |
| Logo | https://cleantechhub.net/wp-content/uploads/2025/04/LOGO-AZUL-OSCRURO-CON-TAG-LINE.png (header logo on https://cleantechhub.net) |
| Contact CTA cleantechhub.net | https://cleantechhub.net |

## Datalab — `datalab.html`

| Fact on the page | Where it was read |
|---|---|
| “Laboratorio de datos: estrategia, flujos, living lab y enlaces a plataformas abiertas.” | https://datalab.cleantechhub.net |
| Climate Intel, portal de datos climáticos | https://datalab.cleantechhub.net linking to https://data.cleantechhub.net/ |
| Four environments: Datalab (strategy), Datathon (ephemeral), living lab (persistent), client product (read only) | https://datalab.cleantechhub.net/app/ (meta description and `ENVTO` / environment copy in `js/datalab.js?v=20261013b`) |
| Tagline “Inspira. Actúa. Transforma.” | https://datalab.cleantechhub.net |
| We read the public sustainability report, mark gaps, and match startup solutions with industry-anonymised datasets. Startup datasets use the industry label, not a client name. | https://datalab.cleantechhub.net/app/js/datalab-showcase-home.js?v=20261013b |
| Company map: sites, processes, assets, topics. Schema links company, site, process, asset, topic, gap, and financing. | https://datalab.cleantechhub.net/app/js/datalab.js?v=20261013b (overview and ontology labels) |
| Dashboard: click a gap, views by role (management, finance, sustainability, operations), and “qué cerrar primero”. | Same `datalab.js` overview |
| Path: informe → materialidad → brecha → solución | https://datalab.cleantechhub.net/app/js/datalab-showcase-home.js?v=20261013b and https://datalab.cleantechhub.net/app/js/showcase-v2.js?v=20261013b |
| Rule: strategy only, no operational data stored. Missing report facts stay «Pendiente de dato real». Return amounts stay empty until there is a source. An own materiality ranking is shown with its page when the report publishes one. | https://datalab.cleantechhub.net/app/js/datalab.js?v=20261013b |
| Living lab: Bogotá air quality, map, delta, and ROI gate in one view. Measure on site, before and after. | https://datalab.cleantechhub.net/living-lab/ and the living-lab handoff text in `datalab.js` |
| 19 of 19 live stations cross-checked against the Secretaría Distrital de Ambiente GIS layer | https://datalab.cleantechhub.net/app/js/lab-data.js?v=20261013b |
| Index dated 8 October 2026, version 4.1.0: 93 corporate profiles and 3 innovation datasets. Maturity: L1 4, L2 4, L3 24, L4 50, L5 11. | https://datalab.cleantechhub.net/data/showcase-index.json (`count` 96, `version.counts`, badge “Datos v4.1.0 · 8 oct 2026”), loaded by the app |
| Filters: name, sector, and CIIU code | https://datalab.cleantechhub.net/app/js/showcase-v2.js?v=20261013b (`filterCorps`) |
| Public levels L1 to L5 | https://datalab.cleantechhub.net/app/js/maturity-rules.js?v=20261013b and the showcase home |
| Logo and contact CTA | Same logo and https://cleantechhub.net contact as the Nexus page |

The area landing pages at `datalab.cleantechhub.net` carry the banner “Contenido de ejemplo”. The sentences above are taken from the app and from those page titles, not from invented product claims.
