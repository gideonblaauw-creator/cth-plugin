# Understanding Lab playground standard (Gideon lock t1268u)

**One-liner:** All Understanding Lab / HITL playgrounds (microworlds) use the **LexiScan house-tour HTML format**. LexiScan is the canonical reference. Do not invent a new layout per product.

**Ownership:**
- **Infrastructure** = shared format lock (repo path, file set, checklist, anti-patterns, Vercel host naming). Remediation PRs migrate legacy playgrounds toward this standard.
- **FabFloow** = LexiScan **product craft only** (content, scenarios, Notion lab pages for LexiScan builds). FabFloow does not own the cross-product format lock.

**Related locks:** `docs/understanding-lab-tiers.md` (Tier 0/1/2), `docs/view-understanding-lab-footer.md` (PR footer), `docs/software-factory.md` (factory step 5 = Understanding Lab; Tier 1–2 hard gate before merge), `skills/harness/SKILL.md` § View Understanding Lab, `skills/infrastructure-comms/SKILL.md` §7.

---

## Canonical template

Copy these refs verbatim when citing the template in skills, tickets, or PR footers:

| Field | Value |
|---|---|
| **Repo** | https://github.com/gideonblaauw-creator/fabfloow-lexiscan |
| **Path** | `understanding-lab/playground/` (PR #16 **MERGED**) |
| **Files** | `index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh` |
| **Notion Playground** | https://app.notion.com/p/3d9dfee50be981e08a7bfffe2cc2f33f |
| **Shared decisions (LexiScan example)** | https://app.notion.com/p/3d9dfee50be981a39107ef7854ec3ce8 |
| **Public host (when live)** | https://fabfloow-ul-playground.vercel.app — Vercel project `fabfloow-ul-playground` (Understanding Lab host only; **not** LexiScan product demo or prod apps) |
| **Brand note** | LexiScan skin = FabFloow cream/mustard/copper; other products use their own brand — **never CTH lime on non-CTH products** |
| **Ownership** | Infra = shared format lock; FabFloow = LexiScan product craft only |
| **Ticket field (Tier 1–2)** | `playground_standard: lexiscan-html-v2` (optional but recommended) |

Hands on Tier 1–2 product repos **must** place the repo artifact at `understanding-lab/playground/` (or the product’s agreed Lane A equivalent) using this file set. The Notion Playground page links to the hosted or local artifact; it does not replace the HTML house tour. Export paste target = this build’s Shared decisions URL (LexiScan example above).

---

## Required format checklist

Every Tier 1–2 playground **must** satisfy all nine items. Infra reviews against this list on Tier 1–2 PASS.

1. **Interactive HTML house tour** — floor-plan / corridor navigation between rooms. **Not** a flat FAQ, not a single scroll of prose, not a tab shell as the primary navigation pattern.
2. **Per room:** description + **quests** + **quiz** (right/wrong feedback) + **decision door** (choice + rationale capture).
3. **EN + ES labels** — at least `nameEn` / `nameEs` on rooms and key UI strings. Prefer a language toggle when LexiScan extends one; rooms must remain bilingual either way.
4. **Progress persistence** — `localStorage` for room/quest progress + welcome overlay on first visit + explicit reset control.
5. **Decision ledger sidebar** + **download/export** as JSON and Markdown formatted for paste into Shared decisions.
6. **Export schema** — version, `playground_id`, and `decisions[]` aligned to Shared decisions row shape (same fields reviewers paste into Notion).
7. **Product-neutral chrome, product-branded skin** — layout and interaction model match LexiScan; colors/typography follow **that desk’s brand**. LexiScan chrome = FabFloow cream / mustard / copper. **Never** apply CleantechHUB lime (`#95D5B2`) on non-CTH product playgrounds. **Never** invent a third layout shell.
8. **`smoke.sh`** — greps for schema keys, room definitions, and export paths so CI or Infra can sanity-check without a browser.
9. **`README.md`** — `python -m http.server` runbook + this build’s Notion Shared decisions URL (from the ticket’s `lab_shared_decisions_url`).

**Beat 3 bar (unchanged):** Playground still delivers `scenario → consequences → options → choose` before Shared decisions. The house tour **implements** that bar across rooms; it does not replace it.

---

## Anti-patterns (do not ship on new Tier 1–2 builds)

| Anti-pattern | Why it fails | Remediation |
|---|---|---|
| **Scanner tabbed microworld shell** (Context / Explainer / Decision Tree / Decisions DB / GH / Clarifications as top-level tabs) | Competing layout; not the house tour | Migrate toward LexiScan standard. Legacy tab **content** may live **inside** a room, not as the outer shell. |
| Flat FAQ or static Notion-only “playground” | No scenario exploration; fails beat 3 | Add `understanding-lab/playground/` LexiScan-format artifact; link from Notion. |
| One-off product layout (cards, wizard, dashboard) | Third layout; review drift | Re-skin LexiScan structure with product brand tokens only. |
| CTH palette on client/FabFloow products | Brand leak | Use desk brand skill; CTH lime only on CTH-owned surfaces. |
| Export without schema version / `playground_id` | Shared decisions paste breaks | Match LexiScan export shape in `data.js` / `app.js`. |
| Missing `smoke.sh` or README runbook | Infra cannot verify or run locally | Copy LexiScan file set; adapt `data.js` only. |

**Legacy note:** Scanner’s older tabbed microworld is a **legacy pattern**. Existing Scanner installs may keep it until a dedicated remediation ticket migrates them. **New** Tier 1–2 playgrounds on any product repo use LexiScan standard from day one.

---

## Tier mapping

| Tier | Playground artifact |
|---|---|
| **0** | No playground required. |
| **1** | LexiScan-format house tour; may scope to **one** primary scenario room (2–3 decision doors). Stable host optional. |
| **2** | Full LexiScan-format house tour; all rooms for the build; stable host when Infra has planted `HITL_HTML_STABLE_URL` or product Vercel (LexiScan reference: `fabfloow-ul-playground`). |

Notion Playground URL on the ticket (`lab_playground_url`) points to the **hub page** for that build. The repo path `understanding-lab/playground/` is the **artifact** Infra and reviewers run locally or via public host. **Public host is not the LexiScan product demo** — Understanding Lab playgrounds deploy to the UL host project (LexiScan: Vercel `fabfloow-ul-playground`).

---

## Review checklist (Infrastructure)

On Tier 1–2 draft PR review, confirm:

- [ ] Path and six files present (`index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh`)
- [ ] House tour navigation (not tab shell / flat FAQ)
- [ ] Each room: quests, quiz feedback, decision door
- [ ] Bilingual labels (`nameEn` / `nameEs` or toggle)
- [ ] `localStorage` progress + welcome + reset
- [ ] Decision ledger + JSON/Markdown export
- [ ] Export schema matches Shared decisions
- [ ] Product brand only (no CTH lime on non-CTH products)
- [ ] `./smoke.sh` passes
- [ ] README lists Shared decisions URL for **this** build

---

## References

- Repo: https://github.com/gideonblaauw-creator/fabfloow-lexiscan
- Path: `understanding-lab/playground/` (PR #16 MERGED)
- Files: `index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh`
- Notion Playground: https://app.notion.com/p/3d9dfee50be981e08a7bfffe2cc2f33f
- Shared decisions (LexiScan example): https://app.notion.com/p/3d9dfee50be981a39107ef7854ec3ce8
- Public host (when live): Vercel project `fabfloow-ul-playground` (separate from LexiScan product demo; FabFloow will publish URL)
- HITL loop beats: `skills/notion/references/hitl-understanding-loops.md`
- PR footer when lab URLs exist: `docs/view-understanding-lab-footer.md`
