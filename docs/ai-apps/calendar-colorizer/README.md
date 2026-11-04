# Jess's Calendar Colorizer — CleantechHUB rules

Auto-colors **Gideon's Google Calendar** from keyword rules using Google Apps Script. Based on [Jess's Calendar Colorizer](https://jessicaeastmanstewart.com/calendar-colorizer); CTH rule set lives in `Code.gs`.

## Colour map

| Category | Google color | Keywords (sample) |
| --- | --- | --- |
| Client / partner | Peacock (`7`) | Teclogi, Sunco, MubOn, Promigas, Energy Coop, AFE, CCF, Climate-KIC, PASO, Atenea, AURA, REIN, Pvblic |
| Grants / funders | Blueberry (`9`) | grant, funder, donor, RFP, GIZ, UNDP, BID, P4G, … |
| Internal / CTH | Sage (`2`) | CleantechHUB, CTH, harness, desk, Nexus, BookStack, Datalab, standup |
| Focus blocks | Graphite (`8`) | focus, deep work, no meetings, writing block |
| Personal | Flamingo (`4`) | doctor, personal, gym, family, OOO |

First matching rule wins. Edit `COLOR_RULES` in `Code.gs` to tune.

## Install (Gideon — HITL only)

Cloud Hands do **not** have calendar access. Gideon installs locally.

1. Open `Code.gs`. Set `CALENDAR_ID` to the calendar name exactly as shown in Google Calendar's left sidebar (often your `@cleantechhub.net` address).
2. Leave **`DRY_RUN = true`** for the first run.
3. Go to [script.google.com](https://script.google.com) → **New project** → paste `Code.gs` → Save (e.g. `CTH Calendar Colorizer`).
4. Run **`colorCodeCalendar`** once. Approve permissions when prompted.
5. Open **Executions** (or View → Logs) and confirm `[DRY RUN]` lines look correct — no wrong colors on important events.
6. Set **`DRY_RUN = false`**, Save, Run again. Spot-check Calendar.
7. **Trigger:** Triggers → Add → `colorCodeCalendar`, time-driven, **Every 5 minutes** (same as Jess's guide).

## Troubleshooting

- **No colors:** Calendar ID must match exactly (case-sensitive).
- **Wrong bucket:** Re-order rules in `COLOR_RULES` (first match wins).
- **Pause:** Delete the time-driven trigger.

## AI Apps for Good adoption

Adopted **2026-11-04** per `docs/research/aiappsforgood-eval-2026-11-04.md`. Complements `skills/cth-meetings-comms/SKILL.md` calendar Workbench (manual moves still require HITL).
