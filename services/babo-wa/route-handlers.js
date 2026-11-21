import {
  filterOnWhatsApp,
  groupCreateResponse,
  parseGroupCreateBody,
  parseGroupDescriptionBody,
  parseGroupJidFromPath,
  publicGroupMeta,
} from './groups.js';

/**
 * @param {{
 *   sendEnabled: boolean;
 *   connectionState: string;
 *   activeSock: import('@whiskeysockets/baileys').WASocket | null;
 *   channelId: string | null;
 *   logger: import('pino').Logger;
 *   relockSend?: () => void;
 * }} deps
 */
export function createGroupRouteHandlers(deps) {
  const { logger, relockSend = () => {} } = deps;

  function guardSend(res, sendJson) {
    if (!deps.sendEnabled) {
      sendJson(res, 403, { error: 'send disabled', sendEnabled: deps.sendEnabled });
      return false;
    }
    if (deps.connectionState !== 'connected' || !deps.activeSock || !deps.channelId) {
      sendJson(res, 503, { error: 'not connected', sendEnabled: deps.sendEnabled });
      return false;
    }
    return true;
  }

  async function handleGroupCreate(body, res, sendJson) {
    if (!guardSend(res, sendJson)) return;
    try {
      const parsed = parseGroupCreateBody(body);
      if (parsed.error) {
        return sendJson(res, 400, { error: parsed.error, sendEnabled: deps.sendEnabled });
      }
      const { name, participants } = parsed;
      logger.info({ route: 'group-create', name, participantCount: participants.length });
      const { onWa, notOnWa } = await filterOnWhatsApp(deps.activeSock, participants);
      if (notOnWa.length) {
        return sendJson(res, 400, {
          error: 'numbers not on WhatsApp',
          notOnWhatsApp: notOnWa,
          sendEnabled: deps.sendEnabled,
        });
      }
      try {
        const created = await deps.activeSock.groupCreate(name, onWa);
        return sendJson(res, 200, {
          ok: true,
          ...groupCreateResponse(created),
          sendEnabled: deps.sendEnabled,
        });
      } catch (err) {
        return sendJson(res, 500, {
          ok: false,
          error: err instanceof Error ? err.message : String(err),
          sendEnabled: deps.sendEnabled,
        });
      }
    } finally {
      relockSend();
    }
  }

  async function handleGroupDescription(body, res, sendJson) {
    if (!guardSend(res, sendJson)) return;
    try {
      const parsed = parseGroupDescriptionBody(body);
      if (parsed.error) {
        return sendJson(res, 400, { error: parsed.error, sendEnabled: deps.sendEnabled });
      }
      logger.info({ route: 'group-description', jid: parsed.jid });
      try {
        await deps.activeSock.groupUpdateDescription(parsed.jid, parsed.description);
        return sendJson(res, 200, { ok: true, jid: parsed.jid, sendEnabled: deps.sendEnabled });
      } catch (err) {
        return sendJson(res, 500, {
          ok: false,
          error: err instanceof Error ? err.message : String(err),
          sendEnabled: deps.sendEnabled,
        });
      }
    } finally {
      relockSend();
    }
  }

  async function handleGroupInvite(jid, res, sendJson) {
    if (!guardSend(res, sendJson)) return;
    try {
      logger.info({ route: 'group-invite', jid });
      try {
        const code = await deps.activeSock.groupInviteCode(jid);
        return sendJson(res, 200, {
          ok: true,
          jid,
          code,
          link: `https://chat.whatsapp.com/${code}`,
          sendEnabled: deps.sendEnabled,
        });
      } catch (err) {
        return sendJson(res, 500, {
          ok: false,
          error: err instanceof Error ? err.message : String(err),
          sendEnabled: deps.sendEnabled,
        });
      }
    } finally {
      relockSend();
    }
  }

  async function handleGroupMeta(jid, res, sendJson) {
    if (deps.connectionState !== 'connected' || !deps.activeSock) {
      return sendJson(res, 503, { error: 'not connected' });
    }
    logger.info({ route: 'group-meta', jid });
    try {
      const meta = await deps.activeSock.groupMetadata(jid);
      return sendJson(res, 200, { ok: true, ...publicGroupMeta(meta, jid) });
    } catch (err) {
      return sendJson(res, 500, {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  return {
    handleGroupCreate,
    handleGroupDescription,
    handleGroupInvite,
    handleGroupMeta,
    parseGroupJidFromPath,
  };
}