
import makeWASocket, {
  downloadContentFromMessage,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} from "@whiskeysockets/baileys";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import pino from "pino";

const AUTH = "/opt/babo-wa/session";
const OUT = "/opt/babo-wa/tmp/farfan-voice2";
const LID = "112936769048804@lid";
const TARGET_ID = "3AF59BA14985D1A41D55";
const TARGET_TS = 1790255068;
const MAX_ROUNDS = 8;

await mkdir(OUT, { recursive: true });

const { state, saveCreds } = await useMultiFileAuthState(AUTH);
const { version } = await fetchLatestBaileysVersion();

let cursor = {
  remoteJid: LID,
  id: "3B081B3F29CD30B90BB5",
  fromMe: true,
  timestamp: 1790271150,
};

const found = [];
const allSeen = [];
let pending = [];
let histResolve = null;

function audioFrom(msg) {
  const m = msg?.message;
  if (!m) return null;
  return (
    m.audioMessage ||
    m.ephemeralMessage?.message?.audioMessage ||
    m.viewOnceMessage?.message?.audioMessage ||
    m.viewOnceMessageV2?.message?.audioMessage ||
    m.viewOnceMessageV2Extension?.message?.audioMessage ||
    null
  );
}

async function trySave(msg, src) {
  const id = msg?.key?.id;
  if (!id) return;
  if (!allSeen.includes(id)) allSeen.push(id);
  const audio = audioFrom(msg);
  const ts = Number(msg.messageTimestamp || 0);
  const remote = msg.key?.remoteJid;
  const fromMe = !!msg.key?.fromMe;
  if (audio) {
    console.log("AUDIO", src, id, "fromMe", fromMe, "ts", ts, "remote", remote, "sec", audio.seconds);
  }
  const idMatch = id === TARGET_ID;
  const tsMatch = !fromMe && audio && Math.abs(ts - TARGET_TS) <= 120;
  if (!audio || (!idMatch && !tsMatch && !( !fromMe && audio && ts >= TARGET_TS - 3600 && ts <= TARGET_TS + 3600))) {
    // still allow any inbound audio in ±1h of target as candidate collect
    if (!fromMe && audio && Math.abs(ts - TARGET_TS) <= 3600) {
      // fall through
    } else if (!idMatch) {
      return;
    } else if (!audio) {
      await writeFile(path.join(OUT, id + ".noaudio.json"), JSON.stringify(msg, null, 2));
      return;
    }
  }
  if (!audio) return;
  if (!fromMe && Math.abs(ts - TARGET_TS) > 3600 && !idMatch) return;

  const key = id;
  if (found.find((f) => f.id === key)) return;
  console.log("DOWNLOADING", key, audio.mimetype, audio.seconds);
  await writeFile(path.join(OUT, key + ".meta.json"), JSON.stringify({ key: msg.key, messageTimestamp: ts, audioMessage: audio, src }, null, 2));
  const stream = await downloadContentFromMessage(audio, "audio");
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  const buf = Buffer.concat(chunks);
  const ext = (audio.mimetype || "").includes("mp4") ? "m4a" : "ogg";
  const file = path.join(OUT, `${key}.${ext}`);
  await writeFile(file, buf);
  const rec = { id: key, file, bytes: buf.length, seconds: audio.seconds, mimetype: audio.mimetype, fromMe, ts, remote, src };
  found.push(rec);
  console.log("SAVED", file, buf.length);
}

function onMessages(messages, src) {
  for (const msg of messages || []) {
    pending.push({ msg, src });
  }
  if (histResolve) {
    const r = histResolve;
    histResolve = null;
    r(messages || []);
  }
}

const sock = makeWASocket({
  version,
  auth: state,
  logger: pino({ level: "warn" }),
  printQRInTerminal: false,
  syncFullHistory: false,
});
sock.ev.on("creds.update", saveCreds);
sock.ev.on("messages.upsert", ({ messages, type }) => onMessages(messages, "upsert:" + type));
sock.ev.on("messaging-history.set", (ev) => {
  console.log("history.set", ev?.messages?.length || 0, "isLatest", ev?.isLatest);
  onMessages(ev?.messages || [], "history");
});

await new Promise((resolve, reject) => {
  const t = setTimeout(() => reject(new Error("connect timeout")), 30000);
  sock.ev.on("connection.update", (u) => {
    console.log("conn", u.connection);
    if (u.connection === "open") {
      clearTimeout(t);
      resolve();
    }
    if (u.connection === "close") {
      clearTimeout(t);
      reject(new Error("closed before open"));
    }
  });
});

async function drainPending() {
  const batch = pending.splice(0, pending.length);
  for (const { msg, src } of batch) {
    try { await trySave(msg, src); } catch (e) { console.error("saveerr", e.message); }
  }
}

for (let round = 1; round <= MAX_ROUNDS; round++) {
  console.log("ROUND", round, "cursor", cursor);
  const waitHist = new Promise((r) => {
    histResolve = r;
    setTimeout(() => { if (histResolve === r) { histResolve = null; r([]); } }, 6000);
  });
  try {
    const fr = await sock.fetchMessageHistory(
      80,
      { remoteJid: cursor.remoteJid, id: cursor.id, fromMe: cursor.fromMe },
      cursor.timestamp
    );
    console.log("fetch ok", fr);
  } catch (e) {
    console.error("fetch fail", e.message);
  }
  const histMsgs = await waitHist;
  await new Promise((r) => setTimeout(r, 1500));
  await drainPending();

  // Prefer exact target; else newest inbound audio near target
  if (found.some((f) => f.id === TARGET_ID) || found.some((f) => !f.fromMe)) {
    console.log("HIT_DONE", found.map((f) => f.id));
    break;
  }

  // advance cursor to oldest seen message this round (from histMsgs or pending trail)
  const pool = histMsgs.length ? histMsgs : [];
  // also scan allSeen via last history dump file
  if (!pool.length) {
    console.log("no hist msgs round", round);
    break;
  }
  let oldest = null;
  for (const m of pool) {
    const ts = Number(m.messageTimestamp || 0);
    if (!oldest || ts < Number(oldest.messageTimestamp || 0)) oldest = m;
  }
  if (!oldest?.key?.id) break;
  const newTs = Number(oldest.messageTimestamp || 0);
  if (newTs >= cursor.timestamp) {
    console.log("cursor not moving", newTs);
    break;
  }
  cursor = {
    remoteJid: oldest.key.remoteJid || LID,
    id: oldest.key.id,
    fromMe: !!oldest.key.fromMe,
    timestamp: newTs,
  };
  // stop if we've walked past target window
  if (newTs < TARGET_TS - 86400) {
    console.log("walked past target day");
    break;
  }
}

await drainPending();
found.sort((a, b) => Math.abs(a.ts - TARGET_TS) - Math.abs(b.ts - TARGET_TS));
const result = {
  found,
  preferred: found.find((f) => f.id === TARGET_ID) || found.find((f) => !f.fromMe) || found[0] || null,
  seenCount: allSeen.length,
  seen: allSeen.slice(0, 120),
};
await writeFile(path.join(OUT, "result.json"), JSON.stringify(result, null, 2));
console.log("RESULT", JSON.stringify(result.preferred));
console.log("FOUND_N", found.length, "SEEN", allSeen.length);
try { sock.end(undefined); } catch {}
process.exit(result.preferred ? 0 : 2);
