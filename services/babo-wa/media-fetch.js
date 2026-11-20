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
        obj.viewOnceMessage?.message?.imageImage ||
        obj.viewOnceMessageV2?.message?.imageMessage ||
        null
      );
    }
    return null;
  };
  return pick(m);
}

/** Fetch audio/image via LIVE babo socket (no second auth session). */
export async function fetchChatAudio(sock, opts) {
  return fetchChatMedia(sock, { ...opts, kind: opts.kind || "audio" });
}

export async function fetchChatMedia(sock, opts) {
  if (!sock) throw new Error("socket required");
  return { ok: false, collected: 0, summary: [], downloads: [], source: "history" };
}
