/**
 * CleantechHUB — Google Calendar auto-color rules (Jess's Calendar Colorizer pattern).
 * Gideon installs via script.google.com (HITL). See README.md in this folder.
 *
 * Calendar color IDs: https://developers.google.com/apps-script/reference/calendar/event#setColor(String)
 * 1 Lavender, 2 Sage, 3 Grape, 4 Flamingo, 5 Banana, 6 Tangerine, 7 Peacock, 8 Graphite, 9 Blueberry, 10 Basil, 11 Tomato
 */

/** Set to your calendar ID (usually your Google email). Must match sidebar exactly. */
var CALENDAR_ID = 'gideon@cleantechhub.net';

/** true = log only, do not change events. Set false after reviewing Executions log. */
var DRY_RUN = true;

/** How far ahead to scan (days). Matches Jess's Colorizer default. */
var LOOKAHEAD_DAYS = 90;

/**
 * Keyword rules — first match wins (case-insensitive). Order: clients/partners, grants, internal, focus, personal.
 */
var COLOR_RULES = [
  // Client / partner meetings
  { keywords: ['teclogi'], colorId: '7' },
  { keywords: ['sunco'], colorId: '7' },
  { keywords: ['mubon', 'mub on'], colorId: '7' },
  { keywords: ['promigas'], colorId: '7' },
  { keywords: ['energy coop', 'energy-coop', 'energycoop'], colorId: '7' },
  { keywords: ['afe '], colorId: '7' },
  { keywords: ['ccf'], colorId: '7' },
  { keywords: ['climate-kic', 'climate kic', 'climatelab'], colorId: '7' },
  { keywords: ['paso'], colorId: '7' },
  { keywords: ['atenea'], colorId: '7' },
  { keywords: ['aura'], colorId: '7' },
  { keywords: ['rein', 'pvblic', 'pvblic fund'], colorId: '7' },
  // Grants / funders
  { keywords: ['grant', 'funder', 'donor', 'rfp', 'proposal deadline', 'giz', 'undp', 'bid', 'idb', 'p4g'], colorId: '9' },
  // Internal / CTH
  { keywords: ['cleantechhub', 'cth ', 'cth-', 'harness', 'desk', 'cloud hands', 'nexus', 'bookstack', 'datalab', 'standup', 'orchestrator'], colorId: '2' },
  // Focus / deep work
  { keywords: ['focus', 'deep work', 'no meetings', 'heads down', 'writing block'], colorId: '8' },
  // Personal
  { keywords: ['doctor', 'dentist', 'personal', 'gym', 'family', 'vacation', 'ooo', 'out of office'], colorId: '4' }
];

function colorCodeCalendar() {
  var calendar = CalendarApp.getCalendarById(CALENDAR_ID);
  if (!calendar) {
    throw new Error('Calendar not found: ' + CALENDAR_ID);
  }
  var start = new Date();
  var end = new Date();
  end.setDate(end.getDate() + LOOKAHEAD_DAYS);
  var events = calendar.getEvents(start, end);
  var changed = 0;
  var logged = 0;

  events.forEach(function (event) {
    var blob = (event.getTitle() + ' ' + (event.getDescription() || '')).toLowerCase();
    var match = findRule(blob);
    if (!match) {
      return;
    }
    if (DRY_RUN) {
      Logger.log('[DRY RUN] would set color ' + match.colorId + ' on: ' + event.getTitle());
      logged++;
      return;
    }
    if (event.getColor() !== match.colorId) {
      event.setColor(match.colorId);
      changed++;
    }
  });

  Logger.log('Done. DRY_RUN=' + DRY_RUN + ' scanned=' + events.length + ' logged=' + logged + ' changed=' + changed);
}

function findRule(text) {
  for (var i = 0; i < COLOR_RULES.length; i++) {
    var rule = COLOR_RULES[i];
    for (var j = 0; j < rule.keywords.length; j++) {
      if (text.indexOf(rule.keywords[j].toLowerCase()) !== -1) {
        return rule;
      }
    }
  }
  return null;
}
