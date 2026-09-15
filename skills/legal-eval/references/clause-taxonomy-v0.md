# Legal eval — clause taxonomy v0

Extend via ticket + Gideon lock. v0 minimum families for commercial consulting and governance packs.

| ID | Family | Extract focus | Playbook notes |
|---|---|---|---|
| `parties-entity` | Parties / entity | Legal names, roles, signatures | **CLEANTECHHUB INTERNATIONAL S.L.** lock; no invented labels |
| `scope-sow` | Scope / SOW | Deliverables, exclusions, change control | Preferred/fallback/forbidden vs playbook |
| `fees-payment` | Fees / payment | Amount, currency, invoicing, taxes | Align with commercial consulting library |
| `term-termination` | Term / termination | Duration, renewal, notice, exit | Hard stop: silent auto-renew >12m without notice |
| `ip-confidentiality` | IP / confidentiality | Background IP, work product, NDA carve-outs | Hard stop: preexisting IP assignment to counterparty |
| `liability-indemnity` | Liability / indemnity | Caps, exclusions, indemnities | Hard stop: uncapped liability |
| `governing-law-dispute` | Governing law / dispute | Law, forum, arbitration | Hard stop: unknown governing law |
| `data-privacy` | Data / privacy | Processing, DPA references, cross-border | Flag ES/CO multi-jurisdiction |
| `non-solicit-compete` | Non-solicit / non-compete | Scope, duration, geography | Moderate+ scrutiny |
| `force-majeure` | Force majeure | Events, notice, suspension | Boilerplate compare |
| `boilerplate` | Boilerplate | Notices, assignment, severability, entire agreement | Fallback library |
| `compliance-aml-sanctions` | Compliance / AML / sanctions | Representations, screening, export | Governance + consulting packs |
| `employment-contractor` | Employment / contractor | Status, benefits, substitution | Flag misclassification risk → counsel |
| `sl-entity-naming` | S.L. entity naming (CO commercial consulting) | Sociedad Limitada form, Spanish/English pairing | Mismatch → negotiate/blocker by mode |

## Doc-type emphasis

| Doc type | Priority families |
|---|---|
| NDA | parties-entity, ip-confidentiality, term-termination, governing-law-dispute |
| LOI / MOU | parties-entity, scope-sow, binding effect, term-termination, governing-law-dispute |
| Consulting agreement | Full taxonomy |
| Governance | compliance-aml-sanctions, employment-contractor, liability-indemnity, governing-law-dispute |

## Binding vs non-binding (LOI / MOU)

Always extract and label binding vs non-binding effect. Flag ambiguity as `negotiate` minimum in `moderate`; `blocker` in `strict` if send candidate.
