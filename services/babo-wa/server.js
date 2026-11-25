import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import makeWASocket, {
  DisconnectReason,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} from '@whiskeysockets/baileys';
import QRCode from 'qrcode';
import pino from 'pino';
import {
  handleHistorySet,
  handleMessagesUpsert,
  initStore,
  setPollMeIdProvider,
  updateChats,
  updateContacts,
  upsertChats,
  upsertContacts,
} from './store.js';
import {
  getPollById,
  getPollCreationForGetMessage,
  handlePollMessagesUpdate,
  initPollsStore,
  listPolls,
  persistPollCreation,
} from './polls.js';
import { fetchChatAudio, fetchChatMedia } from './media-fetch.js';

const HOST = '127.0.0.1';
const PORT = 8790;
const ROOT = path.dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = path.join(ROOT, 'session');

/** @type {Buffer | null} */
let qrPng = null;
let qrGeneratedAt = 0;
/** @type {'starting' | 'qr_pending' | 'connected' | 'disconnected'} */
let connectionState = 'starting';
/** @type {string | null} */
let channelId = null;
/** @type {import('@whiskeysockets/baileys').WASocket | null} */
let activeSock = null;
let sendEnabled = false;

const logger = pino({ level: 'warn' });

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString('utf8');
}

function parseSendBody(raw) {
  if (!raw.trim()) return {};
  try {
    return JSON.parse(raw);
  } catch {
    return { text: raw };
  }
}

function normalizeJid(to) {
  if (!to) return null;
  if (to.includes('@')) return to;
  const digits = String(to).replace(/\D/g, '');
  return digits ? `${digits}@s.whatsapp.net` : null;
}

function qrPageHtml() {
  const qrBlock = qrPng
    ? `<img src="qr.png?t=${Date.now()}" alt="WhatsApp QR code" width="300" height="300">`
    : connectionState === 'connected'
      ? '<p>Connected. Waiting for channel assignment details.</p>'
      : '<p>Waiting for QR generation… page auto-refreshes.</p>';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Babo WhatsApp Pairing</title>
  <base href="/babo-wa-qr/">
  <meta http-equiv="refresh" content="15">
  <style>
    body { font-family: system-ui, sans-serif; max-width: 480px; margin: 2rem auto; text-align: center; color: #111; }
    img { border: 1px solid #ddd; border-radius: 8px; }
    .status { color: #555; margin: 1rem 0; }
    .hint { color: #777; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>Babo WhatsApp Pairing</h1>
  <p class="status">Status: <strong>${connectionState}</strong></p>
  ${qrBlock}
  <p class="hint">WhatsApp → Linked Devices → Link a Device</p>
  <p class="hint">QR auto-refreshes every 15 seconds (codes expire quickly).</p>
</body>
</html>`;
}

function bindStoreEvents(sock) {
  sock.ev.on('messaging-history.set', (payload) => {
    handleHistorySet(payload).catch((err) => {
      logger.warn({ err: err.message }, 'history store write failed');
    });
  });

  sock.ev.on('messages.upsert', (event) => {
    handleMessagesUpsert(event).catch((err) => {
      logger.warn({ err: err.message }, 'message store write failed');
    });
  });

  sock.ev.on('chats.upsert', (chats) => {
    upsertChats(chats).catch((err) => {
      logger.warn({ err: err.message }, 'chat store write failed');
    });
  });

  sock.ev.on('chats.update', (updates) => {
    updateChats(updates).catch((err) => {
      logger.warn({ err: err.message }, 'chat update store write failed');
    });
  });

  sock.ev.on('contacts.upsert', (contacts) => {
    upsertContacts(contacts).catch((err) => {
      logger.warn({ err: err.message }, 'contact store write failed');
    });
  });

  sock.ev.on('contacts.update', (updates) => {
    updateContacts(updates).catch((err) => {
      logger.warn({ err: err.message }, 'contact update store write failed');
    });
  });

  sock.ev.on('messages.update', (updates) => {
    const meId = sock.user?.id;
    handlePollMessagesUpdate(updates, meId).catch((err) => {
      logger.warn({ err: err.message }, 'poll update store write failed');
    });
  });
}

let connecting = false;

async function connectWhatsApp() {
  if (connecting) return;
  connecting = true;

  const { version } = await fetchLatestBaileysVersion();
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

  const sock = makeWASocket({
    auth: state,
    logger,
    version,
    printQRInTerminal: false,
    syncFullHistory: true,
    markOnlineOnConnect: false,
    generateHighQualityLinkPreview: false,
    getMessage: async (key) => getPollCreationForGetMessage(key),
  });
  activeSock = sock;

  sock.ev.on('creds.update', saveCreds);
  bindStoreEvents(sock);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      connectionState = 'qr_pending';
      qrGeneratedAt = Date.now();
      qrPng = await QRCode.toBuffer(qr, { type: 'png', margin: 2, width: 300 });
    }

    if (connection === 'open') {
      connectionState = 'connected';
      qrPng = null;
      const userId = sock.user?.id;
      channelId = userId ? userId.split(':')[0] : null;
      setPollMeIdProvider(() => sock.user?.id);
      logger.info({ channelId: channelId ?? 'unknown' }, 'whatsapp connected');
      return;
    }

    if (connection === 'close') {
      connectionState = 'disconnected';
      qrPng = null;
      channelId = null;
      connecting = false;
      const statusCode = lastDisconnect?.error?.output?.statusCode;
      if (statusCode !== DisconnectReason.loggedOut) {
        setTimeout(() => {
          connectWhatsApp().catch((err) => {
            console.error('whatsapp reconnect failed:', err.message);
          });
        }, 3000);
      }
    }
  });

  connecting = false;
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url ?? '/', `http://${HOST}:${PORT}`);
  const pathname = url.pathname;

  if (pathname === '/send-enable' && req.method === 'POST') {
    sendEnabled = true;
    return sendJson(res, 200, { sendEnabled });
  }

  if (pathname === '/send-disable' && req.method === 'POST') {
    sendEnabled = false;
    return sendJson(res, 200, { sendEnabled });
  }

  if (pathname === '/send' && req.method === 'POST') {
    if (!sendEnabled) {
      return sendJson(res, 403, { error: 'send disabled', sendEnabled });
    }

    if (connectionState !== 'connected' || !activeSock || !channelId) {
      return sendJson(res, 503, { error: 'not connected', sendEnabled });
    }

    const raw = await readBody(req);
    const body = parseSendBody(raw);
    const text = body.text ?? body.message;
    if (!text || typeof text !== 'string') {
      return sendJson(res, 400, { error: 'text required', sendEnabled });
    }

    const jid = normalizeJid(body.to ?? body.jid ?? channelId);
    if (!jid) {
      return sendJson(res, 400, { error: 'invalid recipient', sendEnabled });
    }

    try {
      const result = await activeSock.sendMessage(jid, { text });
      return sendJson(res, 200, {
        ok: true,
        messageId: result?.key?.id ?? null,
        to: jid,
        sendEnabled,
      });
    } catch (err) {
      return sendJson(res, 500, {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
        sendEnabled,
      });
    }
  }

  if (pathname === '/send-poll' && req.method === 'POST') {
    if (!sendEnabled) {
      return sendJson(res, 403, { error: 'send disabled', sendEnabled });
    }

    if (connectionState !== 'connected' || !activeSock || !channelId) {
      return sendJson(res, 503, { error: 'not connected', sendEnabled });
    }

    const raw = await readBody(req);
    let body = {};
    try {
      body = raw.trim() ? JSON.parse(raw) : {};
    } catch {
      return sendJson(res, 400, { error: 'invalid JSON body', sendEnabled });
    }

    const name = typeof body.name === 'string' ? body.name.trim() : '';
    const options = Array.isArray(body.options)
      ? body.options.filter((o) => typeof o === 'string' && o.trim()).map((o) => o.trim())
      : [];
    const selectableCount = Number.isFinite(body.selectableCount)
      ? Math.max(1, Math.floor(body.selectableCount))
      : 1;

    if (!name) {
      return sendJson(res, 400, { error: 'name required', sendEnabled });
    }
    if (options.length < 2 || options.length > 12) {
      return sendJson(res, 400, { error: 'options must be 2–12 strings', sendEnabled });
    }
    if (selectableCount > options.length) {
      return sendJson(res, 400, { error: 'selectableCount exceeds options', sendEnabled });
    }

    const jid = normalizeJid(body.to ?? body.jid ?? channelId);
    if (!jid) {
      return sendJson(res, 400, { error: 'invalid recipient', sendEnabled });
    }

    try {
      const result = await activeSock.sendMessage(jid, {
        poll: {
          name,
          values: options,
          selectableCount,
        },
      });
      if (result) {
        await persistPollCreation(result);
      }
      return sendJson(res, 200, {
        ok: true,
        messageId: result?.key?.id ?? null,
        to: jid,
        sendEnabled,
      });
    } catch (err) {
      return sendJson(res, 500, {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
        sendEnabled,
      });
    }
  }

  if ((pathname === '/polls' || pathname.startsWith('/polls/')) && req.method === 'GET') {
    const meId = activeSock?.user?.id;
    if (pathname === '/polls') {
      const jid = url.searchParams.get('jid');
      const polls = await listPolls(jid ? normalizeJid(jid) : null, meId);
      return sendJson(res, 200, { ok: true, polls });
    }
    const msgId = decodeURIComponent(pathname.slice('/polls/'.length));
    if (!msgId) return sendJson(res, 400, { error: 'message id required' });
    const poll = await getPollById(msgId, meId);
    if (!poll) return sendJson(res, 404, { error: 'poll not found' });
    return sendJson(res, 200, { ok: true, poll });
  }

  if (pathname === '/send-document' && req.method === 'POST') {
    if (!sendEnabled) {
      return sendJson(res, 403, { error: 'send disabled', sendEnabled });
    }

    if (connectionState !== 'connected' || !activeSock || !channelId) {
      return sendJson(res, 503, { error: 'not connected', sendEnabled });
    }

    const raw = await readBody(req);
    let body = {};
    try {
      body = raw.trim() ? JSON.parse(raw) : {};
    } catch {
      return sendJson(res, 400, { error: 'invalid JSON body', sendEnabled });
    }

    const { to, filePath, fileName, caption } = body;
    const mimetype =
      typeof body.mimetype === 'string' ? body.mimetype : 'application/pdf';

    if (!fileName || typeof fileName !== 'string') {
      return sendJson(res, 400, { error: 'fileName required', sendEnabled });
    }

    if (!filePath || typeof filePath !== 'string') {
      return sendJson(res, 400, { error: 'filePath required', sendEnabled });
    }

    const p = path.resolve(filePath);
    const outboxPrefix = '/opt/babo-wa/tmp/outbox/';
    if (!p.startsWith(outboxPrefix) || !fs.existsSync(p)) {
      return sendJson(res, 400, { error: 'invalid or missing file', sendEnabled });
    }

    const jid = normalizeJid(to ?? body.jid ?? channelId);
    if (!jid) {
      return sendJson(res, 400, { error: 'invalid recipient', sendEnabled });
    }

    try {
      const r = await activeSock.sendMessage(jid, {
        document: fs.readFileSync(p),
        fileName,
        mimetype,
        caption,
      });
      return sendJson(res, 200, {
        ok: true,
        messageId: r?.key?.id,
      });
    } catch (err) {
      return sendJson(res, 500, {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
        sendEnabled,
      });
    }
  }

  if (pathname === '/media/fetch' && req.method === 'POST') {
    if (connectionState !== 'connected' || !activeSock) {
      return sendJson(res, 503, { error: 'not connected' });
    }
    const raw = await readBody(req);
    let body = {};
    try {
      body = raw.trim() ? JSON.parse(raw) : {};
    } catch {
      return sendJson(res, 400, { error: 'invalid json' });
    }
    try {
      const kind = body.kind || 'audio';
      const result = await fetchChatMedia(activeSock, {
        jid: body.jid,
        cursorId: body.cursorId,
        cursorFromMe: body.cursorFromMe !== false,
        cursorTs: body.cursorTs,
        targetId: body.targetId || null,
        targetTs: body.targetTs ?? null,
        preferInbound: body.preferInbound !== false,
        outDir: body.outDir || (kind === 'image' ? '/opt/babo-wa/tmp/media-inbox' : '/opt/cth-voice/data/inbox'),
        waitMs: body.waitMs || 8000,
        historyCount: body.historyCount || 100,
        kind,
        maxDownloads: body.maxDownloads || (kind === 'image' ? 5 : 3),
      });
      return sendJson(res, result.ok ? 200 : 404, result);
    } catch (err) {
      return sendJson(res, 500, {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  // Read-only: check whether a phone number is registered on WhatsApp (no send, no presence).
  if (pathname.startsWith('/lookup/') && req.method === 'GET') {
    if (connectionState !== 'connected' || !activeSock) {
      return sendJson(res, 503, { error: 'not connected' });
    }
    const digits = decodeURIComponent(pathname.slice('/lookup/'.length)).replace(/\D/g, '');
    if (!digits) return sendJson(res, 400, { error: 'number required' });
    try {
      const results = (await activeSock.onWhatsApp(digits)) ?? [];
      const hit = results[0] ?? null;
      return sendJson(res, 200, {
        number: digits,
        exists: Boolean(hit?.exists),
        jid: hit?.jid ?? null,
        results,
      });
    } catch (err) {
      return sendJson(res, 500, { ok: false, error: err instanceof Error ? err.message : String(err) });
    }
  }

  // Save/edit a contact in the account's WhatsApp contact list (app-state sync only; no message, no presence).
  if (pathname === '/contact/add' && req.method === 'POST') {
    if (connectionState !== 'connected' || !activeSock) {
      return sendJson(res, 503, { error: 'not connected' });
    }
    const raw = await readBody(req);
    let body = {};
    try {
      body = raw.trim() ? JSON.parse(raw) : {};
    } catch {
      return sendJson(res, 400, { error: 'invalid json' });
    }
    const jid = normalizeJid(body.jid);
    const fullName = typeof body.fullName === 'string' ? body.fullName.trim() : '';
    const firstName = typeof body.firstName === 'string' ? body.firstName.trim() : '';
    if (!jid || !jid.endsWith('@s.whatsapp.net')) {
      return sendJson(res, 400, { error: 'jid must be a phone JID (@s.whatsapp.net)' });
    }
    if (!fullName) return sendJson(res, 400, { error: 'fullName required' });
    try {
      await activeSock.addOrEditContact(jid, {
        fullName,
        firstName: firstName || fullName.split(' ')[0],
        saveOnPrimaryAddressbook: true,
      });
      return sendJson(res, 200, { ok: true, jid, fullName, firstName: firstName || fullName.split(' ')[0] });
    } catch (err) {
      return sendJson(res, 500, { ok: false, error: err instanceof Error ? err.message : String(err) });
    }
  }

  // Read-only: query a contact profile picture URL via Baileys profilePictureUrl
  // (a server query, not a message and not a presence update).
  if ((pathname === '/profile-pic' || pathname.startsWith('/profile-pic/')) && req.method === 'GET') {
    if (connectionState !== 'connected' || !activeSock) {
      return sendJson(res, 503, { error: 'not connected' });
    }
    const raw = url.searchParams.get('jid')
      || (pathname.startsWith('/profile-pic/') ? decodeURIComponent(pathname.slice('/profile-pic/'.length)) : '');
    const jid = normalizeJid(raw);
    if (!jid) return sendJson(res, 400, { error: 'jid required' });
    if (!jid.endsWith('@s.whatsapp.net') && !jid.endsWith('@lid')) {
      return sendJson(res, 400, { error: 'jid must be a user JID' });
    }
    try {
      const pictureUrl = await activeSock.profilePictureUrl(jid, 'image');
      if (!pictureUrl) {
        return sendJson(res, 404, { ok: false, jid, error: 'no profile picture' });
      }
      return sendJson(res, 200, { ok: true, jid, url: pictureUrl });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      const notFound = /item-not-found|not found|404|no profile|exist/i.test(msg);
      return sendJson(res, notFound ? 404 : 500, { ok: false, jid, error: msg });
    }
  }

  if (pathname === '/status') {
    return sendJson(res, 200, {
      connection: connectionState,
      hasQr: Boolean(qrPng),
      qrAgeMs: qrPng ? Date.now() - qrGeneratedAt : null,
      channelId,
      sendEnabled,
    });
  }

  if (pathname === '/qr.png') {
    if (!qrPng) {
      res.writeHead(204);
      res.end();
      return;
    }
    res.writeHead(200, {
      'Content-Type': 'image/png',
      'Cache-Control': 'no-store, no-cache, must-revalidate',
    });
    res.end(qrPng);
    return;
  }

  if (pathname === '/' || pathname === '/babo-wa-qr' || pathname === '/babo-wa-qr/') {
    res.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store, no-cache, must-revalidate',
    });
    res.end(qrPageHtml());
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('not found');
});

await mkdir(AUTH_DIR, { recursive: true, mode: 0o700 });
await initStore();
await initPollsStore();

connectWhatsApp().catch((err) => {
  console.error('whatsapp start failed:', err.message);
});

server.listen(PORT, HOST, () => {
  console.log(`babo-wa listening on http://${HOST}:${PORT}`);
});
