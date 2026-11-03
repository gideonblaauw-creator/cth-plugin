import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';

const LAYERS = new Set(['orchestrator', 'desk', 'workbench', 'hands']);
const TYPES = new Set([
  'start',
  'finish',
  'blocked',
  'needs_gideon',
  'heartbeat',
]);
const CAUSE_TAGS = new Set([
  'unclear_ticket',
  'missing_map',
  'wrong_model',
  'waiting_on_gideon',
  'broken_connector',
  'other',
]);

const __dirname = dirname(fileURLToPath(import.meta.url));
const PUBLIC_DIR = join(__dirname, 'public');

/** @type {Record<string, { file: string; type: string }>} */
const BOARD_ROUTES = {
  '/board': { file: 'index.html', type: 'text/html; charset=utf-8' },
  '/board/': { file: 'index.html', type: 'text/html; charset=utf-8' },
  '/board/board.js': { file: 'board.js', type: 'application/javascript; charset=utf-8' },
  '/board/board.css': { file: 'board.css', type: 'text/css; charset=utf-8' },
};

/**
 * @param {string} pathname
 * @param {import('node:http').ServerResponse} res
 * @returns {boolean}
 */
function serveBoardAsset(pathname, res) {
  const route = BOARD_ROUTES[pathname];
  if (!route) return false;
  const body = readFileSync(join(PUBLIC_DIR, route.file), 'utf8');
  res.writeHead(200, { 'Content-Type': route.type });
  res.end(body);
  return true;
}

/** @type {Set<import('node:http').ServerResponse>} */
const sseClients = new Set();

/**
 * @param {string} dbPath
 */
export function openDatabase(dbPath) {
  const db = new DatabaseSync(dbPath);
  const schema = readFileSync(join(__dirname, 'schema.sql'), 'utf8');
  db.exec(schema);
  return db;
}

/**
 * @param {unknown} body
 * @returns {{ ok: true, value: Record<string, string | null> } | { ok: false, error: string }}
 */
export function validateEventBody(body) {
  if (body === null || typeof body !== 'object' || Array.isArray(body)) {
    return { ok: false, error: 'body must be a JSON object' };
  }
  const b = /** @type {Record<string, unknown>} */ (body);

  for (const field of ['bot_id', 'bot_name', 'layer', 'type', 'task', 'link']) {
    if (typeof b[field] !== 'string' || b[field].trim() === '') {
      return { ok: false, error: `${field} is required and must be a non-empty string` };
    }
  }

  if (!LAYERS.has(/** @type {string} */ (b.layer))) {
    return { ok: false, error: `layer must be one of: ${[...LAYERS].join(', ')}` };
  }
  if (!TYPES.has(/** @type {string} */ (b.type))) {
    return { ok: false, error: `type must be one of: ${[...TYPES].join(', ')}` };
  }

  let causeTag = null;
  if (b.cause_tag !== undefined && b.cause_tag !== null) {
    if (typeof b.cause_tag !== 'string' || !CAUSE_TAGS.has(b.cause_tag)) {
      return {
        ok: false,
        error: `cause_tag must be one of: ${[...CAUSE_TAGS].join(', ')}`,
      };
    }
    causeTag = b.cause_tag;
  }

  let ts;
  if (b.ts === undefined || b.ts === null) {
    ts = new Date().toISOString();
  } else if (typeof b.ts !== 'string') {
    return { ok: false, error: 'ts must be an ISO 8601 string' };
  } else {
    const parsed = Date.parse(b.ts);
    if (Number.isNaN(parsed)) {
      return { ok: false, error: 'ts must be a valid ISO 8601 datetime' };
    }
    ts = new Date(parsed).toISOString();
  }

  return {
    ok: true,
    value: {
      bot_id: /** @type {string} */ (b.bot_id).trim(),
      bot_name: /** @type {string} */ (b.bot_name).trim(),
      layer: /** @type {string} */ (b.layer),
      type: /** @type {string} */ (b.type),
      task: /** @type {string} */ (b.task).trim(),
      link: /** @type {string} */ (b.link).trim(),
      cause_tag: causeTag,
      ts,
    },
  };
}

/**
 * @param {DatabaseSync} db
 * @param {Record<string, string | null>} event
 */
export function insertEvent(db, event) {
  const stmt = db.prepare(`
    INSERT INTO events (bot_id, bot_name, layer, type, task, link, cause_tag, ts)
    VALUES (@bot_id, @bot_name, @layer, @type, @task, @link, @cause_tag, @ts)
  `);
  const result = stmt.run(event);
  const row = db
    .prepare('SELECT * FROM events WHERE id = ?')
    .get(Number(result.lastInsertRowid));
  return row;
}

/** @param {Record<string, unknown>} row */
function broadcastSse(row) {
  const payload = `data: ${JSON.stringify(row)}\n\n`;
  for (const res of sseClients) {
    try {
      res.write(payload);
    } catch {
      sseClients.delete(res);
    }
  }
}

/**
 * @param {import('node:http').IncomingMessage} req
 */
function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      try {
        const raw = Buffer.concat(chunks).toString('utf8');
        resolve(raw ? JSON.parse(raw) : null);
      } catch {
        reject(new Error('invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

/**
 * @param {import('node:http').IncomingMessage} req
 * @param {string | undefined} expectedToken
 */
function authorizeBearer(req, expectedToken) {
  if (!expectedToken) {
    return { ok: false, status: 503, error: 'ingest auth not configured' };
  }
  const header = req.headers.authorization;
  if (!header || !header.startsWith('Bearer ')) {
    return { ok: false, status: 401, error: 'missing or invalid Authorization header' };
  }
  const token = header.slice('Bearer '.length).trim();
  if (token !== expectedToken) {
    return { ok: false, status: 403, error: 'invalid token' };
  }
  return { ok: true };
}

/**
 * @param {DatabaseSync} db
 * @param {URL} url
 */
function queryEvents(db, url) {
  const since = url.searchParams.get('since');
  const botId = url.searchParams.get('bot_id');
  const type = url.searchParams.get('type');
  let limit = url.searchParams.get('limit') ?? '100';

  const conditions = [];
  const params = {};

  if (since) {
    if (Number.isNaN(Date.parse(since))) {
      return { ok: false, error: 'since must be a valid ISO datetime' };
    }
    conditions.push('ts >= @since');
    params.since = new Date(Date.parse(since)).toISOString();
  }
  if (botId) {
    conditions.push('bot_id = @bot_id');
    params.bot_id = botId;
  }
  if (type) {
    if (!TYPES.has(type)) {
      return { ok: false, error: `type must be one of: ${[...TYPES].join(', ')}` };
    }
    conditions.push('type = @type');
    params.type = type;
  }

  const limitNum = Number.parseInt(limit, 10);
  if (!Number.isFinite(limitNum) || limitNum < 1 || limitNum > 1000) {
    return { ok: false, error: 'limit must be an integer between 1 and 1000' };
  }

  const where = conditions.length ? `WHERE ${conditions.join(' AND ')}` : '';
  const sql = `SELECT * FROM events ${where} ORDER BY ts DESC, id DESC LIMIT @limit`;
  const rows = db.prepare(sql).all({ ...params, limit: limitNum });
  return { ok: true, events: rows };
}

/**
 * @param {DatabaseSync} db
 */
function latestBots(db) {
  const rows = db
    .prepare(
      `
    SELECT e.*
    FROM events e
    INNER JOIN (
      SELECT bot_id, MAX(ts) AS max_ts
      FROM events
      GROUP BY bot_id
    ) latest ON e.bot_id = latest.bot_id AND e.ts = latest.max_ts
    ORDER BY e.bot_id
  `,
    )
    .all();

  const now = Date.now();
  const twoHoursMs = 2 * 60 * 60 * 1000;

  return rows.map((row) => {
    const lastTs = Date.parse(String(row.ts));
    const silent_over_2h =
      Number.isNaN(lastTs) || now - lastTs > twoHoursMs;
    return { ...row, silent_over_2h };
  });
}

/**
 * @param {{ db: DatabaseSync, token?: string, port?: number, host?: string }} opts
 */
export function createBotEventsServer({ db, token, port = 8795, host = '127.0.0.1' }) {
  const server = createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', `http://${host}`);

    const sendJson = (status, body) => {
      res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(body));
    };

    try {
      if (req.method === 'GET' && url.pathname === '/health') {
        sendJson(200, { ok: true, service: 'bot-events' });
        return;
      }

      if (req.method === 'POST' && url.pathname === '/event') {
        const auth = authorizeBearer(req, token);
        if (!auth.ok) {
          sendJson(auth.status, { error: auth.error });
          return;
        }
        let body;
        try {
          body = await readJsonBody(req);
        } catch {
          sendJson(400, { error: 'invalid JSON' });
          return;
        }
        const validated = validateEventBody(body);
        if (!validated.ok) {
          sendJson(400, { error: validated.error });
          return;
        }
        const row = insertEvent(db, validated.value);
        broadcastSse(row);
        sendJson(201, { event: row });
        return;
      }

      if (req.method === 'GET' && url.pathname === '/events') {
        const result = queryEvents(db, url);
        if (!result.ok) {
          sendJson(400, { error: result.error });
          return;
        }
        sendJson(200, { events: result.events });
        return;
      }

      if (req.method === 'GET' && url.pathname === '/stream') {
        res.writeHead(200, {
          'Content-Type': 'text/event-stream; charset=utf-8',
          'Cache-Control': 'no-cache',
          Connection: 'keep-alive',
        });
        res.write(': connected\n\n');
        sseClients.add(res);
        req.on('close', () => {
          sseClients.delete(res);
        });
        return;
      }

      if (req.method === 'GET' && url.pathname === '/bots') {
        sendJson(200, { bots: latestBots(db) });
        return;
      }

      if (req.method === 'GET' && serveBoardAsset(url.pathname, res)) {
        return;
      }

      sendJson(404, { error: 'not found' });
    } catch (err) {
      console.error(err);
      sendJson(500, { error: 'internal error' });
    }
  });

  return {
    server,
    listen: () =>
      new Promise((resolve) => {
        server.listen(port, host, () => resolve({ host, port }));
      }),
    close: () =>
      new Promise((resolve, reject) => {
        for (const client of sseClients) {
          try {
            client.end();
          } catch {
            /* ignore */
          }
        }
        sseClients.clear();
        server.close((err) => (err ? reject(err) : resolve()));
      }),
  };
}

function loadConfigFromEnv() {
  const dbPath = process.env.BOT_EVENTS_DB;
  const token = process.env.BOT_EVENTS_TOKEN;
  const port = Number.parseInt(process.env.BOT_EVENTS_PORT ?? '8795', 10);
  const host = process.env.BOT_EVENTS_HOST ?? '127.0.0.1';

  if (!dbPath) {
    console.error('BOT_EVENTS_DB is required');
    process.exit(1);
  }
  if (!Number.isFinite(port) || port < 1 || port > 65535) {
    console.error('BOT_EVENTS_PORT must be a valid port');
    process.exit(1);
  }
  return { dbPath, token, port, host };
}

const isMain = process.argv[1] === fileURLToPath(import.meta.url);

if (isMain) {
  const { dbPath, token, port, host } = loadConfigFromEnv();
  const db = openDatabase(dbPath);
  const app = createBotEventsServer({ db, token, port, host });
  app.listen().then(({ host: h, port: p }) => {
    console.log(`bot-events listening on http://${h}:${p}`);
  });
}
