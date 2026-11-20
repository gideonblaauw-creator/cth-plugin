import makeWASocket, {
  downloadContentFromMessage,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
  DisconnectReason,
} from "@whiskeysockets/baileys";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import pino from "pino";

const AUTH = "/opt/babo-wa/session";
const OUT = "/opt/babo-wa/tmp/majo-audio";
const TARGET_IDS = new Set([
  "AC33860462A4B736BCC3D908E5665F3E",
  "ACE319408E8E85BEC5BA240E1CB8204D",
]);
// Cursor must be NEWER than targets so history sync walks back over them
const CURSOR = {
  remoteJid: "170248292552852@lid",
  id: "AC3991E82DB3CE47A393F5471ABB17B4",
  fromMe: false,
  timestamp: 1790162207,
};
const ALT_JIDS = [
  "170248292552852@lid",
  "5215544483488@s.whatsapp.net",
  "34637379826@s.whatsapp.net",
];

await mkdir(OUT, { recursive: true });
const found = new Map();
const seenIds = [];
const { state, saveCreds } = await useMultiFileAuthState(AUTH);
const { version } = await fetchLatestBaileysVersion();
const logger = pino({ level: "warn" });

let sock;
let doneResolve;
const done = new Promise((r) => { doneResolve = r; });
const timeout = setTimeout(() => doneResolve("timeout"), 150000);

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

async function tryDownload(msg) {
  const id = msg?.key?.id;
  if (!id) return;
  if (!seenIds.includes(id)) seenIds.push(id);
  if (!TARGET_IDS.has(id) || found.has(id)) return;
  const audio = audioFrom(msg);
  if (!audio) {
    console.log("HIT_NO_AUDIO", id, "keys", Object.keys(msg.message || {}), "hasMsg", !!msg.message);
    await writeFile(path.join(OUT, id + ".full.json"), JSON.stringify(msg, null, 2));
    return;
  }
  console.log("DOWNLOADING", id, audio.mimetype, audio.seconds, "url?", !!audio.url, "mediaKey?", !!audio.mediaKey);
  await writeFile(
    path.join(OUT, id + ".meta.json"),
    JSON.stringify({ key: msg.key, audioMessage: audio }, null, 2)
  );
  const stream = await downloadContentFromMessage(audio, "audio");
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  const buf = Buffer.concat(chunks);
  const ext = (audio.mimetype || "").includes("mp4") ? "m4a" : "ogg";
  const file = path.join(OUT, id + "." + ext);
  await writeFile(file, buf);
  found.set(id, file);
  console.log("SAVED", file, buf.length);
  if (found.size === TARGET_IDS.size) doneResolve("ok");
}

function scan(messages, src) {
  console.log("scan", src, "n", (messages || []).length);
  for (const m of messages || []) {
    const id = m?.key?.id;
    const types = Object.keys(m?.message || {});
    if (TARGET_IDS.has(id) || types.includes("audioMessage")) {
      console.log("cand", src, id, types, m?.messageTimestamp);
    }
    tryDownload(m).catch((e) => console.error("dl err", id, e?.message || e));
  }
}

sock = makeWASocket({
  auth: state,
  version,
  logger,
  printQRInTerminal: false,
  syncFullHistory: false,
  markOnlineOnConnect: false,
  getMessage: async () => undefined,
});
sock.ev.on("creds.update", saveCreds);
sock.ev.on("messages.upsert", ({ messages, type }) => scan(messages, "upsert:" + type));
sock.ev.on("messaging-history.set", (ev) => {
  console.log("history.set count", ev?.messages?.length || 0, "isLatest", ev?.isLatest);
  scan(ev?.messages || [], "history");
});

sock.ev.on("connection.update", async (u) => {
  console.log("conn", u.connection);
  if (u.connection === "open") {
    for (const jid of ALT_JIDS) {
      try {
        const r = await sock.fetchMessageHistory(
          80,
          { remoteJid: jid, id: CURSOR.id, fromMe: CURSOR.fromMe },
          CURSOR.timestamp
        );
        console.log("fetchMessageHistory", jid, "ok", r);
      } catch (e) {
        console.error("fetchMessageHistory", jid, "fail", e?.message || e);
      }
    }
    // also try loadMessage if available
    for (const id of TARGET_IDS) {
      try {
        if (typeof sock.loadMessage === "function") {
          const m = await sock.loadMessage(CURSOR.remoteJid, id);
          console.log("loadMessage", id, !!m);
          if (m) await tryDownload(m);
        }
      } catch (e) {
        console.error("loadMessage", id, e?.message || e);
      }
    }
  }
  if (u.connection === "close") {
    const code = u.lastDisconnect?.error?.output?.statusCode;
    console.error("closed", code, DisconnectReason[code] || "");
    if (found.size < TARGET_IDS.size) doneResolve("closed");
  }
});

const result = await done;
clearTimeout(timeout);
await writeFile(path.join(OUT, "seen-ids.json"), JSON.stringify(seenIds, null, 2));
console.log("RESULT", result, "files", Object.fromEntries(found), "seen", seenIds.length);
try { sock.end?.(undefined); } catch {}
process.exit(found.size === TARGET_IDS.size ? 0 : 2);
