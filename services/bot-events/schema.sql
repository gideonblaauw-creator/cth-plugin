-- bot-events SQLite schema (applied at startup from server.js)

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bot_id TEXT NOT NULL,
  bot_name TEXT NOT NULL,
  layer TEXT NOT NULL CHECK (
    layer IN ('orchestrator', 'desk', 'workbench', 'hands')
  ),
  type TEXT NOT NULL CHECK (
    type IN ('start', 'finish', 'blocked', 'needs_gideon', 'heartbeat')
  ),
  task TEXT NOT NULL,
  link TEXT NOT NULL,
  cause_tag TEXT CHECK (
    cause_tag IS NULL
    OR cause_tag IN (
      'unclear_ticket',
      'missing_map',
      'wrong_model',
      'waiting_on_gideon',
      'broken_connector',
      'other'
    )
  ),
  ts TEXT NOT NULL,
  ingested_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_events_ts ON events (ts);
CREATE INDEX IF NOT EXISTS idx_events_bot_id ON events (bot_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events (type);
