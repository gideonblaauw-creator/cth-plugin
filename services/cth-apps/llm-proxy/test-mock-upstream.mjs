#!/usr/bin/env node
/**
 * Integration test: mock OpenRouter + real proxy. No API key needed.
 * Usage: node test-mock-upstream.mjs
 */
import http from 'node:http';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const dir = path.dirname(fileURLToPath(import.meta.url));

const mock = http.createServer(async (req, res) => {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const body = JSON.parse(Buffer.concat(chunks).toString());
  const reply = {
    id: 'mock-or',
    choices: [
      {
        message: {
          content: JSON.stringify({
            gaps: [
              {
                key: 'fu_1',
                theme: 'TEST',
                question: 'Mock follow-up?',
                why: 'Mock reason',
              },
            ],
          }),
        },
        finish_reason: 'stop',
      },
    ],
  };
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(reply));
});

await new Promise((r) => mock.listen(0, '127.0.0.1', r));
const mockPort = mock.address().port;

const proxy = spawn(
  'node',
  [path.join(dir, 'server.js')],
  {
    env: {
      ...process.env,
      CTH_LLM_PORT: '8796',
      CTH_LLM_HOST: '127.0.0.1',
      CTH_LLM_STATE_FILE: '/tmp/cth-llm-test-usage.json',
      CTH_LLM_DAILY_CAP: '9999',
      OPENROUTER_API_KEY: 'test-key',
      OPENROUTER_BASE_URL: `http://127.0.0.1:${mockPort}/api/v1`,
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  },
);

await new Promise((r) => setTimeout(r, 400));

const anthropicReq = {
  model: 'claude-sonnet-4-6',
  max_tokens: 100,
  system: 'Return JSON only',
  messages: [{ role: 'user', content: 'hello' }],
};

const res = await fetch('http://127.0.0.1:8796/api/llm', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'anthropic-version': '2023-06-01',
    'X-Forwarded-Email': 'test@cleantechhub.net',
  },
  body: JSON.stringify(anthropicReq),
});

const data = await res.json();
proxy.kill('SIGTERM');
mock.close();

if (!res.ok || !data.content?.[0]?.text) {
  console.error('FAIL', res.status, data);
  process.exit(1);
}
console.log('OK proxy translation', data.content[0].text.slice(0, 80));
