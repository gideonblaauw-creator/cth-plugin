import { mkdir, readFile, writeFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  BufferJSON,
  decryptPollVote,
  getAggregateVotesInPollMessage,
  getKeyAuthor,
  jidNormalizedUser,
} from '@whiskeysockets/baileys';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const POLLS_DIR = path.join(ROOT, 'store', 'polls');

/** @type {Map<string, Promise<void>>} */
const writeQueues = new Map();

function queueWrite(key, fn) {
  const prev = writeQueues.get(key) ?? Promise.resolve();
  const next = prev.then(fn, fn);
  writeQueues.set(
    key,
    next.finally(() => {
      if (writeQueues.get(key) === next) writeQueues.delete(key);
    }),
  );
  return next;
}

async function writeJsonAtomic(file, data) {
  const tmp = `${file}.tmp`;
  const body = JSON.stringify(data, BufferJSON.replacer);
  await writeFile(tmp, body, { mode: 0o600 });
  await writeFile(file, body, { mode: 0o600 });
}

async function readJson(file) {
  try {
    const raw = await readFile(file, 'utf8');
    return JSON.parse(raw, BufferJSON.reviver);
  } catch {
    return null;
  }
}

function pollFile(msgId) {
  const safe = String(msgId).replace(/[^a-zA-Z0-9._-]/g, '_');
  return path.join(POLLS_DIR, `${safe}.json`);
}

function unwrapPollContent(message) {
  if (!message) return null;
  return (
    message.pollCreationMessage
    ?? message.pollCreationMessageV2
    ?? message.pollCreationMessageV3
    ?? message.ephemeralMessage?.message?.pollCreationMessage
    ?? message.ephemeralMessage?.message?.pollCreationMessageV2
    ?? message.ephemeralMessage?.message?.pollCreationMessageV3
    ?? null
  );
}

function pollMetaFromWaMessage(waMsg) {
  const poll = unwrapPollContent(waMsg?.message);
  if (!poll) return null;
  const name = poll.name ?? '';
  const options = (poll.options ?? []).map((o) => o.optionName).filter(Boolean);
  const selectableCount = poll.selectableOptionsCount ?? poll.selectableCount ?? 1;
  return { name, options, selectableCount };
}

function isPollCreation(waMsg) {
  return pollMetaFromWaMessage(waMsg) != null;
}

function votesFromAggregation(aggregated, pollUpdates, meId) {
  /** @type {Record<string, { voter: string, selected: string[], timestamp: number | null }>} */
  const byVoter = {};
  for (const update of pollUpdates ?? []) {
    const voter = getKeyAuthor(update.pollUpdateMessageKey, meId);
    if (!voter) continue;
    const ts = update.senderTimestampMs ?? null;
    const prev = byVoter[voter]?.timestamp ?? -1;
    if (ts != null && ts < prev) continue;
    const selected = [];
    for (const bucket of aggregated) {
      if (bucket.voters?.includes(voter)) selected.push(bucket.name);
    }
    byVoter[voter] = { voter, selected, timestamp: ts };
  }
  if (Object.keys(byVoter).length === 0) {
    for (const bucket of aggregated) {
      for (const voter of bucket.voters ?? []) {
        byVoter[voter] = { voter, selected: [bucket.name], timestamp: null };
      }
    }
  }
  return Object.values(byVoter);
}

function publicPollView(record, meId) {
  const aggregated = getAggregateVotesInPollMessage({
    message: record.creation?.message,
    pollUpdates: record.pollUpdates ?? [],
  }, meId);
  return {
    messageId: record.messageId,
    jid: record.remoteJid,
    name: record.name,
    options: record.options,
    selectableCount: record.selectableCount,
    votes: votesFromAggregation(aggregated, record.pollUpdates, meId),
  };
}

export async function initPollsStore() {
  await mkdir(POLLS_DIR, { recursive: true, mode: 0o700 });
}

export async function persistPollCreation(waMsg) {
  const msgId = waMsg.key?.id;
  const remoteJid = waMsg.key?.remoteJid;
  if (!msgId || !remoteJid) return;
  const meta = pollMetaFromWaMessage(waMsg);
  if (!meta) return;
  const file = pollFile(msgId);
  await queueWrite(file, async () => {
    const existing = await readJson(file);
    const record = {
      messageId: msgId,
      remoteJid,
      participant: waMsg.key?.participant ?? null,
      name: meta.name,
      options: meta.options,
      selectableCount: meta.selectableCount,
      createdAt: Number(waMsg.messageTimestamp ?? Date.now()),
      creation: {
        key: waMsg.key,
        message: waMsg.message,
        messageTimestamp: waMsg.messageTimestamp,
        participant: waMsg.key?.participant,
      },
      pollUpdates: existing?.pollUpdates ?? [],
    };
    await writeJsonAtomic(file, record);
  });
}

export async function getPollCreationForGetMessage(key) {
  if (!key?.id) return undefined;
  const record = await readJson(pollFile(key.id));
  if (!record?.creation) return undefined;
  return {
    key: record.creation.key,
    message: record.creation.message,
    messageTimestamp: record.creation.messageTimestamp,
  };
}

async function appendPollUpdates(msgId, updates) {
  if (!updates?.length) return;
  const file = pollFile(msgId);
  await queueWrite(file, async () => {
    const record = await readJson(file);
    if (!record?.creation?.message) return;
    const merged = [...(record.pollUpdates ?? [])];
    const seen = new Set(merged.map((u) => u.pollUpdateMessageKey?.id).filter(Boolean));
    for (const u of updates) {
      const uid = u.pollUpdateMessageKey?.id;
      if (uid && seen.has(uid)) continue;
      if (uid) seen.add(uid);
      merged.push(u);
    }
    record.pollUpdates = merged;
    await writeJsonAtomic(file, record);
  });
}

export async function handlePollUpdateMessage(waMsg, meId) {
  const content = waMsg.message?.pollUpdateMessage;
  const creationKey = content?.pollCreationMessageKey;
  if (!creationKey?.id || !content?.vote || !meId) return;
  const record = await readJson(pollFile(creationKey.id));
  if (!record?.creation?.message) return;
  const meNorm = jidNormalizedUser(meId);
  const pollEncKey = record.creation.message?.messageContextInfo?.messageSecret;
  if (!pollEncKey) return;
  const pollCreatorJid = getKeyAuthor(creationKey, meNorm);
  const voterJid = getKeyAuthor(waMsg.key, meNorm);
  try {
    const voteMsg = decryptPollVote(content.vote, {
      pollEncKey,
      pollCreatorJid,
      pollMsgId: creationKey.id,
      voterJid,
    });
    const tsRaw = content.senderTimestampMs;
    const senderTimestampMs = typeof tsRaw === 'object' && tsRaw !== null && 'toNumber' in tsRaw
      ? tsRaw.toNumber()
      : Number(tsRaw ?? Date.now());
    await appendPollUpdates(creationKey.id, [{
      pollUpdateMessageKey: waMsg.key,
      vote: voteMsg,
      senderTimestampMs,
    }]);
  } catch {}
}

export async function handlePollMessagesUpsert(messages, meId) {
  if (!messages?.length) return;
  for (const msg of messages) {
    if (isPollCreation(msg)) await persistPollCreation(msg);
    if (msg.message?.pollUpdateMessage) await handlePollUpdateMessage(msg, meId);
  }
}

export async function handlePollMessagesUpdate(updates, meId) {
  if (!updates?.length) return;
  for (const { key, update } of updates) {
    const pollUpdates = update.pollUpdates;
    if (!pollUpdates?.length || !key?.id) continue;
    await appendPollUpdates(key.id, pollUpdates);
  }
}

export async function listPolls(jid, meId) {
  let files;
  try { files = await readdir(POLLS_DIR); } catch { return []; }
  const out = [];
  for (const f of files) {
    if (!f.endsWith('.json')) continue;
    const record = await readJson(path.join(POLLS_DIR, f));
    if (!record) continue;
    if (jid && record.remoteJid !== jid) continue;
    out.push(publicPollView(record, meId));
  }
  out.sort((a, b) => (a.messageId > b.messageId ? -1 : 1));
  return out;
}

export async function getPollById(msgId, meId) {
  const record = await readJson(pollFile(msgId));
  if (!record) return null;
  return publicPollView(record, meId);
}
