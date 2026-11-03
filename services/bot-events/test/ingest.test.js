import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import {
  createBotEventsServer,
  openDatabase,
  validateEventBody,
} from '../server.js';

const TEST_TOKEN = 'test-bearer-token-secret';

function baseEvent(overrides = {}) {
  return {
    bot_id: 'bot-1',
    bot_name: 'Smoke Bot',
    layer: 'hands',
    type: 'start',
    task: 'Run harness ticket',
    link: 'https://cursor.com/agents/example',
    ...overrides,
  };
}

async function postEvent(port, body, token = TEST_TOKEN) {
  const res = await fetch(`http://127.0.0.1:${port}/event`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  return { res, json };
}

describe('validateEventBody', () => {
  it('accepts a minimal valid payload', () => {
    const result = validateEventBody(baseEvent());
    assert.equal(result.ok, true);
    if (result.ok) {
      assert.equal(result.value.cause_tag, null);
      assert.match(result.value.ts, /^\d{4}-\d{2}-\d{2}T/);
    }
  });

  it('rejects invalid layer', () => {
    const result = validateEventBody(baseEvent({ layer: 'invalid' }));
    assert.equal(result.ok, false);
  });

  it('rejects invalid cause_tag', () => {
    const result = validateEventBody(baseEvent({ cause_tag: 'nope' }));
    assert.equal(result.ok, false);
  });
});

describe('HTTP ingest + reads', () => {
  /** @type {ReturnType<typeof createBotEventsServer>} */
  let app;
  /** @type {import('node:sqlite').DatabaseSync} */
  let db;
  let tmpDir;
  let port;

  before(async () => {
    tmpDir = mkdtempSync(join(tmpdir(), 'bot-events-test-'));
    const dbPath = join(tmpDir, 'events.db');
    db = openDatabase(dbPath);
    app = createBotEventsServer({ db, token: TEST_TOKEN, port: 0, host: '127.0.0.1' });
    await app.listen();
    const addr = app.server.address();
    assert.ok(addr && typeof addr === 'object');
    port = addr.port;
  });

  after(async () => {
    await app.close();
    db.close();
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns 401 without bearer token', async () => {
    const res = await fetch(`http://127.0.0.1:${port}/event`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(baseEvent()),
    });
    assert.equal(res.status, 401);
  });

  it('returns 403 with wrong bearer token', async () => {
    const { res } = await postEvent(port, baseEvent(), 'wrong');
    assert.equal(res.status, 403);
  });

  it('returns 400 for invalid payload', async () => {
    const { res, json } = await postEvent(port, baseEvent({ type: 'explode' }));
    assert.equal(res.status, 400);
    assert.ok(json.error);
  });

  it('ingests and lists events', async () => {
    const { res, json } = await postEvent(
      port,
      baseEvent({ type: 'finish', cause_tag: 'other', ts: '2026-11-03T00:00:00.000Z' }),
    );
    assert.equal(res.status, 201);
    assert.equal(json.event.bot_id, 'bot-1');

    const listRes = await fetch(`http://127.0.0.1:${port}/events?bot_id=bot-1&limit=10`);
    const listJson = await listRes.json();
    assert.equal(listRes.status, 200);
    assert.ok(listJson.events.length >= 1);
  });

  it('reports bot status with silent_over_2h', async () => {
    const botsRes = await fetch(`http://127.0.0.1:${port}/bots`);
    const botsJson = await botsRes.json();
    assert.equal(botsRes.status, 200);
    const bot = botsJson.bots.find((b) => b.bot_id === 'bot-1');
    assert.ok(bot);
    assert.equal(typeof bot.silent_over_2h, 'boolean');
  });

  it('serves the live board at GET /board', async () => {
    const res = await fetch(`http://127.0.0.1:${port}/board`);
    assert.equal(res.status, 200);
    assert.match(res.headers.get('content-type') ?? '', /text\/html/);
    const html = await res.text();
    assert.match(html, /CleantechHUB Bot board/);
  });
});

describe('SSE /stream', () => {
  /** @type {ReturnType<typeof createBotEventsServer>} */
  let app;
  /** @type {import('node:sqlite').DatabaseSync} */
  let db;
  let tmpDir;
  let port;

  before(async () => {
    tmpDir = mkdtempSync(join(tmpdir(), 'bot-events-sse-'));
    db = openDatabase(join(tmpDir, 'events.db'));
    app = createBotEventsServer({ db, token: TEST_TOKEN, port: 0, host: '127.0.0.1' });
    await app.listen();
    const addr = app.server.address();
    assert.ok(addr && typeof addr === 'object');
    port = addr.port;
  });

  after(async () => {
    await app.close();
    db.close();
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it('delivers new events over SSE', async () => {
    const ac = new AbortController();
    const ssePromise = fetch(`http://127.0.0.1:${port}/stream`, { signal: ac.signal }).then(
      async (res) => {
        assert.equal(res.status, 200);
        assert.match(res.headers.get('content-type') ?? '', /text\/event-stream/);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const match = buffer.match(/data: (\{.*\})/);
          if (match) {
            return JSON.parse(match[1]);
          }
        }
        throw new Error('no SSE data received');
      },
    );

    await new Promise((r) => setTimeout(r, 50));

    const { res } = await postEvent(port, baseEvent({ bot_id: 'sse-bot', type: 'heartbeat' }));
    assert.equal(res.status, 201);

    const event = await Promise.race([
      ssePromise,
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('SSE timeout')), 5000),
      ),
    ]);

    ac.abort();
    assert.equal(event.bot_id, 'sse-bot');
    assert.equal(event.type, 'heartbeat');
  });
});
