# Sources — Nexus CO₂ deck

## Fix decisions

### BIO NATURAL SOLUTIONS — 7,500 vs 4,500 t mitigated (website)

Both figures appear on [bionatsolutions.com](https://bionatsolutions.com/): a headline **+7,500 TM CO2 mitigadas** and a longer line on agrochemicals and food waste citing **+4,500 TM de CO2**. The 4,500 t line describes specific mechanisms that plausibly roll up into the broader 7,500 t headline; keeping both in the deck would double-count the same portfolio story. **Kept:** 7,500 t (`claim_status=achieved`, website). **Dropped:** 4,500 t row (overlapping sub-claim).

### CARBON BOX (KIMSA) vs CARBONBOX

**Same company.** The 2022 investor deck is titled *Pitch CarbonBox.pdf*, lists `www.carbonbox.app`, and uses contact email `@kimsa.co`. Nexus previously split KIMSA’s “CARBON BOX” website figure from the Carbonbox.app figure. **Merged** under slug `carbonbox`, display name **CARBONBOX**. **Distinct claims retained:** 13,000+ t GHG managed (KIMSA technology page, achieved); 112K+ tCO₂e managed (carbonbox.app, achieved); 436 ktonCO₂e/year Colombia (2022 deck, target — not summed with achieved managed totals).

## Website claims

| Fact | URL |
|------|-----|
| BIO NATURAL SOLUTIONS — +7500 TM CO2 mitigadas | https://bionatsolutions.com/ |
| BATX SAS — 520 tCO₂e avoided (baterías) | https://www.batx.co/impacto-1 |
| CICLORGÁNICOS — +25.000 t CO₂ eq evitadas (2019-2026) | https://ciclorganicos.com/ |
| CARBONBOX — 13000+ t GHG gestionadas (KIMSA) | https://www.kimsa.co/tecnologia-para-la-naturaleza |
| CARBONBOX — 112K+ tCO₂e gestionadas | https://carbonbox.app/ |
| O3 SMART CITIES — 1.500+ t CO₂ evitadas | https://o3smartcities.com.co |
| SEOS ENERGY — 645 t CO₂ evitadas | https://seosenergy.co/ |
| ZHANA SOLUTIONS — reducción CO2 (toneladas) | https://zhanasolutions.com/ |

## Investor deck claims

Canonical extract file: `research/nexus-co2/co2-decks.csv`. Public citations use **deck title + date** only (no Drive IDs or links).

| Startup | Figure | Deck title | Date |
|---------|--------|------------|------|
| BeCaps | 112.8 kT CO₂eq avoided (5 yr target) | Deck7eng.pdf | 2026-04-14 |
| BeCaps | 5.1 kt (2025 target) | BeCaps-OnePager4.pdf | 2026-04-14 |
| NOVATIO | 166,000 t CO₂eq/año (5 yr plan) | Deck_NOVATIO_Inversionista_2024.pdf | 2024-02-07 |
| NOVATIO | 640 t CO₂e/año (by 2025) | Presentación NOVATIO_Inversión_20220608.pdf | 2022-06-08 |
| NOVATIO | 50,000 t CO₂e/año (2024) | Presentación NOVATIO_Inversión_20220608.pdf | 2022-06-08 |
| CARBONBOX | 436 ktonCO₂e/año Colombia (target) | Pitch CarbonBox.pdf | 2022-06-11 |
| Calo Jabones | 3,200 t CO₂ evitados | Pitch CaloJabones ENE23.pdf | 2023-02-03 |
| BEFLY | 900,000 t CO₂/year (SDG forecast) | Pitch Deck BEFLY 2022.pdf | 2022-11-24 |
| Husk Ventures | 4,050 t CO₂ sequestered (year 10) | HUSK VENTURES - Investor Marketplace.pdf | 2020-02-28 |
| MO-BI | 9,919 kg CO₂ saved | MO-BI PITCH DECK Q4_2021 (ENGLISH).pptx.pdf | 2021-12-01 |
| EcoSea | 10.3 kton CO₂ prevented | EcoSea Deck .pdf | 2022-03-30 |
| EcoSea | 11 Mt CO₂/year potential (2050) | EcoSea Deck .pdf | 2022-03-30 |
| Natoure | 0.51 t CO₂/trip (2025 target) | Natoure Pitch Deck 2022.pdf | 2022-06-27 |

## Portfolio methodology

| Fact | URL |
|------|-----|
| Portfolio count (174) & coverage methodology | https://nexus.cleantechhub.net/p/startup-portfolio |
| Canonical merged data | `research/nexus-co2/co2.csv` |

## Deck shell

Layout, card grid (`imp-grid` / `growth-card`), topbar navigation, and explorer chrome from `decks/_templates/clp26-rein-shell/` (branch `cursor/clp26-rein-shell-template-668e`, PR #126), copied into this deck folder.
