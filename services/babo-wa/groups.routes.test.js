import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { createGroupRouteHandlers } from './route-handlers.js';

const GROUP_JID = '120363000000000000@g.us';

function mockRes() {
  /** @type {{ status?: number; body?: unknown }} */
  const state = {};
  return {
    state,
    res: {
      writeHead(status) {
        state.status = status;
      },
      end(raw) {
        state.body = JSON.parse(String(raw));
      },
    },
  };
}

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
}

function makeHandlers(overrides = {}) {
  let sendEnabled = overrides.sendEnabled ?? true;
  const state = {
    connectionState: 'connected',
    channelId: '5730000000000',
    sendEnabled,
    relocked: false,
    ...overrides.state,
  };
  const sock = {
    onWhatsApp: async (...jids) => jids.map((jid) => ({ jid, exists: true })),
    groupCreate: overrides.groupCreate ?? (async () => ({
      id: GROUP_JID,
      subject: 'MentorXs',
      participants: [
        { jid: '5730000000001@s.whatsapp.net', status: 200 },
        { jid: '5730000000002@s.whatsapp.net', status: 403 },
      ],
    })),
    groupUpdateDescription: overrides.groupUpdateDescription ?? (async () => {}),
    groupInviteCode: overrides.groupInviteCode ?? (async () => 'AbCdEfGhIjK'),
    groupMetadata: overrides.groupMetadata ?? (async () => ({
      subject: 'MentorXs',
      desc: 'desc',
      owner: '5730000000000@s.whatsapp.net',
      creation: 123,
      participants: [{ id: '5730000000001@s.whatsapp.net', admin: 'admin' }],
    })),
    ...overrides.sock,
  };

  const handlers = createGroupRouteHandlers({
    get sendEnabled() {
      return state.sendEnabled;
    },
    get connectionState() {
      return state.connectionState;
    },
    get activeSock() {
      return sock;
    },
    get channelId() {
      return state.channelId;
    },
    logger: { info() {}, warn() {} },
    relockSend() {
      state.sendEnabled = false;
      state.relocked = true;
    },
  });

  return { handlers, state, sock };
}

describe('group routes (mocked socket)', () => {
  it('POST /group-create returns 403 when send lock closed', async () => {
    const { handlers } = makeHandlers({ sendEnabled: false });
    const { res, state } = mockRes();
    await handlers.handleGroupCreate(
      { name: 'x', participants: ['5730000000001'] },
      res,
      sendJson,
    );
    assert.equal(state.status, 403);
    assert.match(state.body.error, /disabled/);
  });

  it('POST /group-create returns 400 for bad input', async () => {
    const { handlers } = makeHandlers();
    const { res, state } = mockRes();
    await handlers.handleGroupCreate({ name: '', participants: [] }, res, sendJson);
    assert.equal(state.status, 400);
  });

  it('POST /group-create parses partial add failures and relocks', async () => {
    const { handlers, state } = makeHandlers();
    const { res, state: http } = mockRes();
    await handlers.handleGroupCreate(
      { name: 'MentorXs', participants: ['5730000000001', '5730000000002'] },
      res,
      sendJson,
    );
    assert.equal(http.status, 200);
    assert.equal(http.body.jid, GROUP_JID);
    assert.equal(http.body.added.length, 1);
    assert.equal(http.body.failed[0].reason, 'privacy');
    assert.equal(state.relocked, true);
    assert.equal(state.sendEnabled, false);
  });

  it('POST /group-description behind send lock', async () => {
    const { handlers, state } = makeHandlers();
    const { res, state: http } = mockRes();
    await handlers.handleGroupDescription(
      { jid: GROUP_JID, description: 'Dataton group' },
      res,
      sendJson,
    );
    assert.equal(http.status, 200);
    assert.equal(http.body.ok, true);
    assert.equal(state.relocked, true);
  });

  it('GET /group-invite behind send lock', async () => {
    const { handlers } = makeHandlers();
    const { res, state } = mockRes();
    await handlers.handleGroupInvite(GROUP_JID, res, sendJson);
    assert.equal(state.status, 200);
    assert.match(state.body.link, /^https:\/\/chat\.whatsapp\.com\//);
  });

  it('GET /group-meta is read-only without send lock', async () => {
    const { handlers } = makeHandlers({ sendEnabled: false });
    const { res, state } = mockRes();
    await handlers.handleGroupMeta(GROUP_JID, res, sendJson);
    assert.equal(state.status, 200);
    assert.equal(state.body.subject, 'MentorXs');
    assert.equal(state.body.participants[0].admin, true);
  });
});