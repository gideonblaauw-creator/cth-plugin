import { mkdir, readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { handlePollMessagesUpsert as persistPollsFromUpsert } from './polls.js';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const STORE_DIR = path.join(ROOT, 'store');
const CHATS_FILE = path.join(STORE_DIR, 'chats.json');
const MESSAGES_DIR = path.join(STORE_DIR, 'messages');

/** @type {Record<string, { id: string, name?: string | null, updatedAt: number }>} */
let chatsCache = {};
/** @type {Map<string, Promise<void>>} */
const writeQueues = new Map();

function jidToFile(jid) {
  return path.join(MESSAGES_DIR, `${jid.replace(/[^a-zA-Z0-9._-]/g, '_')}.json`);
}

async function readJson(file, fallback) {
  try {
    return JSON.parse(await readFile(file, 'utf8'));
  } catch {
    return fallback;
  }
}

async function writeJsonAtomic(file, data) {
  const tmp = `${file}.tmp`;
  await writeFile(tmp, JSON.stringify(data), { mode: 0o600 });
  await writeFile(file, JSON.stringify(data), { mode: 0o600 });
}

function queueWrite(key, fn) {
  const prev = writeQueues.get(key) ?? Promise.resolve();
  const next = prev.then(fn, fn);
  writeQueues.set(key, next.finally(() => {
    if (writeQueues.get(key) === next) writeQueues.delete(key);
  }));
  return next;
}

export async function initStore() {
  await mkdir(STORE_DIR, { recursive: true, mode: 0o700 });
  await mkdir(MESSAGES_DIR, { recursive: true, mode: 0o700 });
  chatsCache = await readJson(CHATS_FILE, {});
}

function chatName(chat) {
  return chat.name ?? chat.subject ?? chat.verifiedName ?? null;
}

function contactName(contact) {
  return contact.notify ?? contact.name ?? contact.verifiedName ?? null;
}

export async function upsertChats(chats) {
  if (!chats?.length) return;
  const now = Date.now();
  for (const chat of chats) {
    if (!chat?.id) continue;
    const name = chatName(chat);
    chatsCache[chat.id] = {
      id: chat.id,
      name: name ?? chatsCache[chat.id]?.name ?? null,
      updatedAt: now,
    };
  }
  await queueWrite('chats', () => writeJsonAtomic(CHATS_FILE, chatsCache));
}

export async function updateChats(updates) {
  if (!updates?.length) return;
  const now = Date.now();
  for (const update of updates) {
    if (!update?.id) continue;
    const prev = chatsCache[update.id] ?? { id: update.id, name: null, updatedAt: now };
    chatsCache[update.id] = {
      id: update.id,
      name: chatName(update) ?? prev.name,
      updatedAt: now,
    };
  }
  await queueWrite('chats', () => writeJsonAtomic(CHATS_FILE, chatsCache));
}

export async function upsertContacts(contacts) {
  if (!contacts?.length) return;
  const now = Date.now();
  for (const contact of contacts) {
    if (!contact?.id) continue;
    const name = contactName(contact);
    if (!name) continue;
    chatsCache[contact.id] = { id: contact.id, name, updatedAt: now };
  }
  await queueWrite('chats', () => writeJsonAtomic(CHATS_FILE, chatsCache));
}

export async function updateContacts(updates) {
  if (!updates?.length) return;
  const now = Date.now();
  for (const contact of updates) {
    if (!contact?.id) continue;
    const name = contactName(contact);
    if (!name) continue;
    chatsCache[contact.id] = { id: contact.id, name, updatedAt: now };
  }
  await queueWrite('chats', () => writeJsonAtomic(CHATS_FILE, chatsCache));
}

function messageRecord(msg) {
  const key = msg.key ?? {};
  const text =
    msg.message?.conversation ??
    msg.message?.extendedTextMessage?.text ??
    msg.message?.imageMessage?.caption ??
    msg.message?.videoMessage?.caption ??
    null;
  const audio =
    msg.message?.audioMessage ||
    msg.message?.ephemeralMessage?.message?.audioMessage ||
    msg.message?.viewOnceMessage?.message?.audioMessage ||
    msg.message?.viewOnceMessageV2?.message?.audioMessage ||
    msg.message?.viewOnceMessageV2Extension?.message?.audioMessage ||
    null;
  const rec = {
    id: key.id ?? null,
    remoteJid: key.remoteJid ?? null,
    fromMe: Boolean(key.fromMe),
    timestamp: Number(msg.messageTimestamp ?? 0),
    type: audio ? 'audioMessage' : text != null ? 'text' : Object.keys(msg.message ?? {})[0] ?? 'unknown',
    text,
  };
  // Persist enough audio fields for later /media/fetch without a second WA session.
  if (audio) {
    rec.media = {
      mimetype: audio.mimetype ?? null,
      seconds: audio.seconds ?? null,
      ptt: Boolean(audio.ptt),
      fileLength: audio.fileLength ? Number(audio.fileLength) : null,
      mediaKey: audio.mediaKey ? Buffer.from(audio.mediaKey).toString('base64') : null,
      fileEncSha256: audio.fileEncSha256 ? Buffer.from(audio.fileEncSha256).toString('base64') : null,
      fileSha256: audio.fileSha256 ? Buffer.from(audio.fileSha256).toString('base64') : null,
      directPath: audio.directPath ?? null,
      url: audio.url ?? null,
    };
  }
  return rec;
}

async function appendMessages(messages) {
  if (!messages?.length) return;
  const byJid = new Map();
  for (const msg of messages) {
    const jid = msg.key?.remoteJid;
    if (!jid) continue;
    if (!byJid.has(jid)) byJid.set(jid, []);
    byJid.get(jid).push(messageRecord(msg));
  }
  for (const [jid, records] of byJid) {
    const file = jidToFile(jid);
    await queueWrite(file, async () => {
      const existing = await readJson(file, []);
      const seen = new Set(existing.map((m) => m.id).filter(Boolean));
      const merged = [...existing];
      for (const rec of records) {
        if (rec.id && seen.has(rec.id)) continue;
        merged.push(rec);
      }
      merged.sort((a, b) => a.timestamp - b.timestamp);
      await writeJsonAtomic(file, merged);
    });
  }
}

export async function handleHistorySet({ chats, contacts, messages }) {
  await upsertChats(chats);
  await upsertContacts(contacts);
  await appendMessages(messages);
  await persistPollsFromUpsert(messages, pollMeIdProvider());
}

/** @type {() => string | undefined} */
let pollMeIdProvider = () => undefined;

export function setPollMeIdProvider(fn) {
  pollMeIdProvider = fn;
}

export async function handleMessagesUpsert({ messages }) {
  await appendMessages(messages);
  await persistPollsFromUpsert(messages, pollMeIdProvider());
}
