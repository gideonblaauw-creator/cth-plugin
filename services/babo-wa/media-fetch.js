import { downloadContentFromMessage } from "@whiskeysockets/baileys";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import path from "node:path";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function b64ToBuf(v) {
  if (!v) return undefined;
  if (Buffer.isBuffer(v)) return v;
  return Buffer.from(String(v), "base64");
}

function mediaFrom(msg, kind) {
  const m = msg?.message;
  if (!m) return null;
  const pick = (obj) => {
    if (!obj) return null;
    if (kind === "audio") {
      return (
        obj.audioMessage ||
        obj.ephemeralMessage?.message?.audioMessage ||
        obj.viewOnceMessage?.message?.audioMessage ||
        obj.viewOnceMessageV2?.message?.audioMessage ||
        obj.viewOnceMessageV2Extension?.message?.audioMessage ||
        null
      );
    }
    if (kind === "image") {
      return (
        obj.imageMessage ||
        obj.ephemeralMessage?.message?.imageMessage ||
        obj.viewOnceMessage?.message?.imageMessage ||
        obj.viewOnceMessageV2?.message?.imageMessage ||
        null
      );
    }
    return null;
  };
  return pick(m);
}

function mediaFromStored(media, kind) {
  if (!media?.mediaKey || !media?.directPath) return null;
  const base = {
    mediaKey: b64ToBuf(media.mediaKey),
    fileEncSha256: b64ToBuf(media.fileEncSha256),
    fileSha256: b64ToBuf(media.fileSha256),
    directPath: media.directPath,
    url: media.url,
    fileLength: media.fileLength ?? undefined,
  };
  if (kind === "audio") {
    return {
      ...base,
      mimetype: media.mimetype || "audio/ogg; codecs=opus",
      seconds: media.seconds ?? undefined,
      ptt: media.ptt ?? true,
    };
  }
  return {
    ...base,
    mimetype: media.mimetype || "image/jpeg",
    caption: media.caption ?? undefined,
  };
}

async function saveMedia(media, kind, meta, outDir) {
  const stream = await downloadContentFromMessage(media, kind);
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  const buf = Buffer.concat(chunks);
  let ext = "bin";
  const mt = media.mimetype || "";
  if (kind === "audio") ext = mt.includes("mp4") ? "m4a" : "ogg";
  else if (mt.includes("png")) ext = "png";
  else if (mt.includes("webp")) ext = "webp";
  else ext = "jpg";
  const stamp = meta.ts || Math.floor(Date.now() / 1000);
  const id = meta.id || "unknown";
  const file = path.join(outDir, `${stamp}_${id}.${ext}`);
  await writeFile(file, buf);
  const out = {
    ...meta,
    seconds: media.seconds ?? meta.seconds ?? null,
    mimetype: media.mimetype ?? null,
    caption: media.caption ?? null,
    bytes: buf.length,
    file,
    kind,
  };
  await writeFile(path.join(outDir, `${stamp}_${id}.meta.json`), JSON.stringify(out, null, 2));
  return out;
}

function summarize(msg) {
  const m = msg?.message || {};
  return {
    id: msg?.key?.id,
    remoteJid: msg?.key?.remoteJid,
    participant: msg?.key?.participant || msg?.participant || null,
    fromMe: !!msg?.key?.fromMe,
    ts: Number(msg?.messageTimestamp || 0),
    pushName: msg?.pushName || null,
    types: Object.keys(m),
    hasAudio: Boolean(mediaFrom(msg, "audio")),
    hasImage: Boolean(mediaFrom(msg, "image")),
    text:
      m.conversation ||
      m.extendedTextMessage?.text ||
      m.imageMessage?.caption ||
      m.documentMessage?.caption ||
      null,
  };
}

/** Fetch audio/image via LIVE babo socket (no second auth session). */
export async function fetchChatAudio(sock, opts) {
  return fetchChatMedia(sock, { ...opts, kind: opts.kind || "audio" });
}

export async function fetchChatMedia(sock, opts) {
  const {
    jid,
    cursorId,
    cursorFromMe = true,
    cursorTs,
    targetId = null,
    targetTs = null,
    preferInbound = true,
    outDir = "/opt/cth-voice/data/inbox",
    waitMs = 8000,
    historyCount = 100,
    storedMedia = null,
    storePath = null,
    kind = "audio",
    maxDownloads = 5,
  } = opts;

  if (!sock) throw new Error("socket required");
  await mkdir(outDir, { recursive: true });

  if (storedMedia && targetId) {
    const media = mediaFromStored(storedMedia, kind);
    if (media) {
      const dl = await saveMedia(media, kind, {
        id: targetId,
        remoteJid: jid,
        fromMe: false,
        ts: targetTs || 0,
        source: "storedMedia",
      }, outDir);
      return { ok: true, collected: 0, summary: [], downloads: [dl], source: "storedMedia" };
    }
  }

  if (storePath && targetId) {
    try {
      const rows = JSON.parse(await readFile(storePath, "utf8"));
      const hit = (rows || []).find((m) => m.id === targetId && m.media);
      if (hit?.media) {
        const media = mediaFromStored(hit.media, kind);
        if (media) {
          const dl = await saveMedia(media, kind, {
            id: hit.id,
            remoteJid: hit.remoteJid || jid,
            fromMe: !!hit.fromMe,
            ts: hit.timestamp || targetTs || 0,
            source: "storeFile",
          }, outDir);
          return { ok: true, collected: 0, summary: [], downloads: [dl], source: "storeFile" };
        }
      }
    } catch {
      // continue
    }
  }

  if (!jid || !cursorId || !cursorTs) throw new Error("jid, cursorId, cursorTs required when no storedMedia");

  const collected = [];
  const onHist = (ev) => {
    for (const m of ev?.messages || []) collected.push(m);
  };
  const onUpsert = ({ messages }) => {
    for (const m of messages || []) collected.push(m);
  };
  sock.ev.on("messaging-history.set", onHist);
  sock.ev.on("messages.upsert", onUpsert);

  let fetchResult = null;
  let fetchError = null;
  try {
    fetchResult = await sock.fetchMessageHistory(
      historyCount,
      { remoteJid: jid, id: cursorId, fromMe: !!cursorFromMe },
      Number(cursorTs)
    );
    await sleep(waitMs);
  } catch (err) {
    fetchError = err instanceof Error ? err.message : String(err);
  } finally {
    sock.ev.off("messaging-history.set", onHist);
    sock.ev.off("messages.upsert", onUpsert);
  }

  const summary = collected.map(summarize);

  let candidates = collected.filter((msg) => mediaFrom(msg, kind));
  if (preferInbound) candidates = candidates.filter((msg) => !msg?.key?.fromMe);
  if (targetId) {
    const hit = collected.find((msg) => msg?.key?.id === targetId && mediaFrom(msg, kind));
    if (hit) candidates = [hit, ...candidates.filter((m) => m !== hit)];
  }
  if (targetTs != null) {
    candidates.sort(
      (a, b) =>
        Math.abs(Number(a.messageTimestamp) - Number(targetTs)) -
        Math.abs(Number(b.messageTimestamp) - Number(targetTs))
    );
  } else {
    candidates.sort((a, b) => Number(b.messageTimestamp || 0) - Number(a.messageTimestamp || 0));
  }

  const downloads = [];
  for (const msg of candidates.slice(0, maxDownloads)) {
    const media = mediaFrom(msg, kind);
    try {
      downloads.push(
        await saveMedia(media, kind, {
          id: msg.key.id,
          remoteJid: msg.key.remoteJid,
          participant: msg.key.participant || msg.participant || null,
          pushName: msg.pushName || null,
          fromMe: !!msg.key.fromMe,
          ts: Number(msg.messageTimestamp || 0),
          source: "history",
        }, outDir)
      );
    } catch (err) {
      downloads.push({ id: msg.key.id, error: err instanceof Error ? err.message : String(err) });
    }
  }

  return {
    ok: downloads.some((d) => d.file) || summary.length > 0,
    fetchResult,
    fetchError,
    collected: collected.length,
    summary,
    downloads,
    source: "history",
  };
}
