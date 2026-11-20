import makeWASocket, {
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} from "@whiskeysockets/baileys";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import pino from "pino";

const AUTH = "/opt/babo-wa/session";
const OUT = "/opt/babo-wa/tmp/majo-audio";
await mkdir(OUT, { recursive: true });
const { state, saveCreds } = await useMultiFileAuthState(AUTH);
const { version } = await fetchLatestBaileysVersion();
const all = [];
let resolve;
const done = new Promise((r) => (resolve = r));
setTimeout(() => resolve("timeout"), 90000);

const sock = makeWASocket({
  auth: state,
  version,
  logger: pino({ level: "silent" }),
  printQRInTerminal: false,
  syncFullHistory: false,
  markOnlineOnConnect: false,
});
sock.ev.on("creds.update", saveCreds);
sock.ev.on("messaging-history.set", async (ev) => {
  const rows = (ev.messages || []).map((m) => ({
    id: m.key?.id,
    ts: Number(m.messageTimestamp || 0),
    fromMe: m.key?.fromMe,
    jid: m.key?.remoteJid,
    types: Object.keys(m.message || {}),
  }));
  all.push(...rows);
  console.log("batch", rows.length, "firstTs", rows[0]?.ts, "lastTs", rows.at(-1)?.ts);
  await writeFile(path.join(OUT, "hist-dump.json"), JSON.stringify(all, null, 2));
  // look for near-target window
  const near = rows.filter((r) => r.ts >= 1790130000 && r.ts <= 1790170000);
  console.log("near window", near.length, JSON.stringify(near));
  if (all.length >= 5) {
    // after first useful batch, if we have near-window or enough, can finish early after second page
  }
});
sock.ev.on("connection.update", async (u) => {
  console.log("conn", u.connection);
  if (u.connection !== "open") return;
  // page 1: 10 msgs before Gracias
  try {
    const r = await sock.fetchMessageHistory(
      10,
      { remoteJid: "170248292552852@lid", id: "AC3991E82DB3CE47A393F5471ABB17B4", fromMe: false },
      1790162207
    );
    console.log("fetch10", r);
  } catch (e) {
    console.error("fetch10 fail", e?.message || e);
  }
  await new Promise((r) => setTimeout(r, 15000));
  // page 2: if we got fromMe text as oldest in batch, continue from there
  const sorted = [...all].sort((a, b) => b.ts - a.ts);
  console.log("top10 by ts", JSON.stringify(sorted.slice(0, 10), null, 0));
  resolve("ok");
});
await done;
console.log("TOTAL", all.length);
const targets = new Set(["AC33860462A4B736BCC3D908E5665F3E", "ACE319408E8E85BEC5BA240E1CB8204D"]);
console.log("targets in dump", all.filter((r) => targets.has(r.id)));
try { sock.end?.(); } catch {}
process.exit(0);
