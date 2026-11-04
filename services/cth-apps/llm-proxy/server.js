#!/usr/bin/env node
/**
 * CleantechHUB LLM proxy — Anthropic Messages API shape in, OpenRouter chat out.
 * No dependencies. Node 22+.
 */
'use strict';

const http = require('node:http');
const { URL } = require('node:url');
const fs = require('node:fs');
const path = require('node:path');

const HOST = process.env.CTH_LLM_HOST || '127.0.0.1';
const PORT = Number(process.env.CTH_LLM_PORT || 8796);
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY || '';
const OPENROUTER_MODEL =
  process.env.OPENROUTER_MODEL || 'google/gemini-2.0-flash-001';
const OPENROUTER_BASE =
  process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';
const MAX_TOKENS_CAP = Number(process.env.CTH_LLM_MAX_TOKENS || 8192);
const DAILY_CAP = Number(process.env.CTH_LLM_DAILY_CAP || 200);
const STATE_FILE =
  process.env.CTH_LLM_STATE_FILE ||
  '/var/lib/cleantechhub/cth-apps-llm-proxy/daily-usage.json';

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function json(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

function loadState() {
  try {
    const raw = fs.readFileSync(STATE_FILE, 'utf8');
    return JSON.parse(raw);
  } catch {
    return { day: '', counts: {} };
  }
}

function saveState(state) {
  const dir = path.dirname(STATE_FILE);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state));
}

function todayUtc() {
  return new Date().toISOString().slice(0, 10);
}

function clientKey(req) {
  const email =
    req.headers['x-forwarded-email'] ||
    req.headers['x-forwarded-user'] ||
    'anonymous';
  return String(email).toLowerCase().slice(0, 320);
}

function checkDailyLimit(req) {
  const state = loadState();
  const day = todayUtc();
  if (state.day !== day) {
    state.day = day;
    state.counts = {};
  }
  const key = clientKey(req);
  const count = state.counts[key] || 0;
  if (count >= DAILY_CAP) {
    return { ok: false, message: `Daily request cap (${DAILY_CAP}) reached.` };
  }
  state.counts[key] = count + 1;
  saveState(state);
  return { ok: true };
}

function anthropicToOpenRouter(body) {
  const messages = [];
  if (body.system) {
    const sys =
      typeof body.system === 'string'
        ? body.system
        : body.system.map((b) => b.text || '').join('\n');
    messages.push({ role: 'system', content: sys });
  }
  for (const m of body.messages || []) {
    let content = m.content;
    if (Array.isArray(content)) {
      content = content.map((b) => b.text || '').join('\n');
    }
    messages.push({ role: m.role, content: content || '' });
  }
  const max_tokens = Math.min(
    Number(body.max_tokens) || 1024,
    MAX_TOKENS_CAP,
  );
  return {
    model: OPENROUTER_MODEL,
    messages,
    max_tokens,
    temperature: body.temperature,
  };
}

function openRouterToAnthropic(orJson) {
  const text =
    orJson.choices?.[0]?.message?.content ??
    orJson.choices?.[0]?.text ??
    '';
  return {
    id: orJson.id || 'msg_cth_proxy',
    type: 'message',
    role: 'assistant',
    model: OPENROUTER_MODEL,
    content: [{ type: 'text', text: String(text) }],
    stop_reason: orJson.choices?.[0]?.finish_reason || 'end_turn',
    usage: orJson.usage,
  };
}

async function forwardOpenRouter(payload) {
  const url = `${OPENROUTER_BASE.replace(/\/$/, '')}/chat/completions`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${OPENROUTER_API_KEY}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://apps.cleantechhub.net',
      'X-Title': 'CleantechHUB AI Apps',
    },
    body: JSON.stringify(payload),
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`OpenRouter non-JSON (${res.status}): ${text.slice(0, 200)}`);
  }
  if (!res.ok) {
    const msg = data.error?.message || text.slice(0, 300);
    const err = new Error(msg);
    err.status = res.status;
    throw err;
  }
  return data;
}

async function handleAnthropicPost(req, res) {
  if (!OPENROUTER_API_KEY) {
    return json(res, 503, {
      type: 'error',
      error: { type: 'configuration_error', message: 'LLM proxy not configured' },
    });
  }
  const limit = checkDailyLimit(req);
  if (!limit.ok) {
    return json(res, 429, {
      type: 'error',
      error: { type: 'rate_limit_error', message: limit.message },
    });
  }
  let body;
  try {
    body = JSON.parse(await readBody(req));
  } catch {
    return json(res, 400, {
      type: 'error',
      error: { type: 'invalid_request', message: 'Invalid JSON body' },
    });
  }
  try {
    const orPayload = anthropicToOpenRouter(body);
    const orRes = await forwardOpenRouter(orPayload);
    return json(res, 200, openRouterToAnthropic(orRes));
  } catch (e) {
    const status = e.status && e.status >= 400 && e.status < 600 ? e.status : 502;
    return json(res, status, {
      type: 'error',
      error: { type: 'api_error', message: e.message || 'Upstream error' },
    });
  }
}

function handlePerplexityDisabled(res) {
  json(res, 503, {
    error: {
      message:
        'Perplexity / real-world example search is disabled on this CleantechHUB host.',
    },
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);

  if (req.method === 'GET' && url.pathname === '/health') {
    return json(res, 200, { ok: true, model: OPENROUTER_MODEL });
  }

  if (req.method === 'POST') {
    if (
      url.pathname === '/api/llm' ||
      url.pathname === '/api/llm/' ||
      url.pathname === '/'
    ) {
      return handleAnthropicPost(req, res);
    }
    if (url.pathname.includes('perplexity')) {
      return handlePerplexityDisabled(res);
    }
  }

  json(res, 404, { error: { message: 'Not found' } });
});

server.listen(PORT, HOST, () => {
  console.error(
    `[cth-apps-llm-proxy] listening on http://${HOST}:${PORT} model=${OPENROUTER_MODEL}`,
  );
});
