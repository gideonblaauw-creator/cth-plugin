/** @typedef {import('@whiskeysockets/baileys').WASocket} WASocket */

const MAX_GROUP_PARTICIPANTS = 50;

const STATUS_REASON = {
  403: 'privacy',
  408: 'left recently',
  409: 'already in',
};

export function normalizeUserJid(input) {
  if (!input) return null;
  const raw = String(input).trim();
  if (raw.includes('@')) return raw;
  const digits = raw.replace(/\D/g, '');
  return digits ? `${digits}@s.whatsapp.net` : null;
}

export function isGroupJid(jid) {
  return typeof jid === 'string' && jid.endsWith('@g.us');
}

export function parseGroupCreateBody(body) {
  const name = typeof body?.name === 'string' ? body.name.trim() : '';
  const rawParticipants = Array.isArray(body?.participants) ? body.participants : null;
  if (!rawParticipants) {
    return { error: 'participants must be an array' };
  }
  const participants = rawParticipants
    .map((p) => normalizeUserJid(p))
    .filter(Boolean);
  if (!name) return { error: 'name required' };
  if (participants.length === 0) return { error: 'participants required' };
  if (participants.length > MAX_GROUP_PARTICIPANTS) {
    return { error: 'at most 50 participants' };
  }
  return { name, participants };
}

export function parseGroupDescriptionBody(body) {
  const jid = typeof body?.jid === 'string' ? body.jid.trim() : '';
  const description = typeof body?.description === 'string' ? body.description : '';
  if (!isGroupJid(jid)) return { error: 'jid must be a group JID (@g.us)' };
  return { jid, description };
}

export function parseGroupJidFromPath(encoded) {
  const jid = decodeURIComponent(encoded || '').trim();
  if (!isGroupJid(jid)) return { error: 'jid must be a group JID (@g.us)' };
  return { jid };
}

/**
 * @param {unknown} participantsResult
 */
export function splitGroupCreateParticipants(participantsResult) {
  const added = [];
  const failed = [];
  const list = Array.isArray(participantsResult) ? participantsResult : [];
  for (const entry of list) {
    const jid = entry?.jid ?? entry?.id ?? null;
    const status = entry?.status ?? entry?.error ?? null;
    const statusNum = Number(status);
    if (statusNum === 200 || status === '200') {
      if (jid) added.push(jid);
      continue;
    }
    if (!jid) continue;
    const reason = STATUS_REASON[statusNum] ?? String(status ?? 'unknown');
    failed.push({ jid, status: statusNum || status, reason });
  }
  return { added, failed };
}

/**
 * @param {Record<string, unknown>} groupResponse
 */
export function groupCreateResponse(groupResponse) {
  const gid = groupResponse?.gid ?? groupResponse?.id ?? null;
  const jid = typeof gid === 'string' ? gid : gid?.toString?.() ?? null;
  const subject = groupResponse?.subject ?? groupResponse?.name ?? null;
  const { added, failed } = splitGroupCreateParticipants(groupResponse?.participants);
  return { jid, subject, added, failed };
}

/**
 * @param {Awaited<ReturnType<WASocket['groupMetadata']>>} meta
 */
export function publicGroupMeta(meta, jid) {
  const participants = (meta?.participants ?? []).map((p) => ({
    id: p.id,
    admin: p.admin === 'admin' || p.admin === 'superadmin',
  }));
  return {
    jid,
    subject: meta?.subject ?? null,
    desc: meta?.desc ?? meta?.description ?? null,
    owner: meta?.owner ?? null,
    creation: meta?.creation ?? null,
    participants,
  };
}

export async function filterOnWhatsApp(sock, participants) {
  const results = (await sock.onWhatsApp(...participants)) ?? [];
  const existing = new Set(
    results.filter((r) => r?.exists && r.jid).map((r) => r.jid),
  );
  const onWa = participants.filter((jid) => existing.has(jid));
  const notOnWa = participants.filter((jid) => !existing.has(jid));
  return { onWa, notOnWa };
}