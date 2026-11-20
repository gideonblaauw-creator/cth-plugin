import makeWASocket, {
  downloadContentFromMessage,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} from "@whiskeysockets/baileys";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import pino from "pino";

const AUTH = "/opt/babo-wa/session";
const OUT = "/opt/babo-wa/tmp/farfan-voice";
const TARGET_IDS = new Set([
  "3AF59BA14985D1A41D55",
  "AC46F93AEE324CCA35200806D14966AC",
]);
const PREFERRED = "3AF59BA14985D1A41D55";
const LID = "112936769048804@lid";
const ALT_JIDS = [LID, "18495813474@s.whatsapp.net", "573143807350@s.whatsapp.net"];
const CURSOR = {
  remoteJid: LID,
  id: "3B081B3F29CD30B90BB5",
  fromMe: true,
  timestamp: 1790271150,
};

await mkdir(OUT, { recursive: true });
const found = new Map();
const seen = [];
const { state, saveCreds } = await useMultiFileAuthState(AUTH);
const { version } = await fetchLatestBaileysVersion();

let doneResolve;
const done = new Promise((r) => { doneResolve = r; });
const timeout = setTimeout(() => doneResolve("timeout"), 100000);

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

async function tryDownload(msg, src) {
  const id = msg?.key?.id;
  if (!id) return;
  if (!seen.includes(id)) seen.push(id);
  const audio = audioFrom(msg);
  if (TARGET_IDS.has(id) || audio) {
    console.log("cand", src, id, "fromMe", msg.key?.fromMe, "keys", Object.keys(msg.message || {}), "audio?", !!audio);
  }
  if (!TARGET_IDS.has(id)) return;
  await writeFile(path.join(OUT, id + ".full.json"), JSON.stringify(msg, null, 2));
  if (found.has(id) || !audio) {
    if (!audio) console.log("HIT_NO_AUDIO", id);
    return;
  }
  console.log("DOWNLOADING", id, audio.mimetype, audio.seconds);
  await writeFile(path.join(OUT, id + ".meta.json"), JSON.stringify({ key: msg.key, messageTimestamp: msg.messageTimestamp, audioMessage: audio }, null, 2));
  const stream = await downloadContentFromMessage(audio, "audio");
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  const buf = Buffer.concat(chunks);
  const ext = (audio.mimetype || "").includes("mp4") ? "m4a" : "ogg";
  const file = path.join(OUT, `${id}.${ext}`);
  await writeFile(file, buf);
  found.set(id, { file, bytes: buf.length, seconds: audio.seconds, mimetype: audio.mimetype, fromMe: msg.key?.fromMe, ts: Number(msg.messageTimestamp) });
  console.log("SAVED", file, buf.length);
  if (found.has(PREFERRED)) doneResolve("ok");
}

function scan(messages, src) {
  for (const msg of messages || []) {
    tryDownload(msg, src).catch((e) => console.error("dlerr", e.message));
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
    for (const id of TARGET_IDS) {
      try {
        if (typeof sock.loadMessage === "function") {
          const m = await sock.loadMessage(LID, id);
          console.log("loadMessage", id, !!m);
          if (m) await tryDownload(m, "loadMessage");
        }
      } catch (e) {
        console.log("loadMessage fail", id, e.message);
      }
    }
  }
  if (u.connection === "close" && !found.size) doneResolve("closed");
});

const result = await done;
clearTimeout(timeout);
console.log("RESULT", result, "files", Object.fromEntries(found), "seen", seen.length);
await writeFile(path.join(OUT, "result.json"), JSON.stringify({ result, found: Object.fromEntries(found), seenCount: seen.length, seen: seen.slice(0, 100) }, null, 2));
try { sock.end(undefined); } catch {}
process.exit(found.size ? 0 : 2);
